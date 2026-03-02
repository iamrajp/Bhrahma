"""
Bhrahma Main Agent - Orchestrates skills and sub-agents
"""
from typing import List, Dict, Optional, Any
from pathlib import Path
import sys
import asyncio
from datetime import datetime
from loguru import logger
import uuid

sys.path.append(str(Path(__file__).parent.parent))
from services.llm_client import LLMFactory, LLMClient
from services.skill_manager import SkillManager
from services.web_search import WebSearchService
from models.database import ChatMessage, AgentSession, get_session_maker
from config import settings


class BhrahmaAgent:
    """
    Main Bhrahma agent that can:
    - Select and use appropriate skills
    - Learn new skills from the internet
    - Spawn sub-agents for parallel task execution
    - Interact with multiple LLM providers
    """

    def __init__(
        self,
        session_id: str,
        llm_provider: Optional[str] = None,
        db_session = None
    ):
        self.session_id = session_id
        self.llm_provider = llm_provider or settings.DEFAULT_LLM
        self.llm_client: LLMClient = LLMFactory.create_client(self.llm_provider)
        self.db = db_session or next(get_session_maker()())
        self.skill_manager = SkillManager(self.db)
        self.web_search = WebSearchService()
        self.conversation_history: List[Dict[str, str]] = []

    async def process_message(self, user_message: str) -> str:
        """
        Process a user message and generate a response

        Workflow:
        1. Analyze the message
        2. Select relevant skills
        3. Determine if sub-agents are needed
        4. Execute the task
        5. Return response
        """
        logger.info(f"Bhrahma processing message in session {self.session_id}")

        # Save user message to database
        self._save_message("user", user_message)

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Create agent session
        agent_session = self._create_agent_session()

        try:
            # Step 1: Analyze the task and select skills
            relevant_skills = self.skill_manager.select_skills_for_task(user_message)
            logger.info(f"Selected {len(relevant_skills)} skills for task")

            # Step 2: Check if skill-creator should be used
            needs_learning, skill_info = await self._needs_new_skill(user_message, relevant_skills)

            if needs_learning:
                logger.info(f"Triggering skill-creator to learn: {skill_info['topic']}")
                # Invoke the skill creator
                learned_skill = await self._learn_new_skill(skill_info)
                if learned_skill:
                    logger.info(f"Successfully learned skill: {learned_skill.name}")
                    # Add the newly learned skill to relevant skills for this task
                    relevant_skills.append(learned_skill)
                    response = f"✅ I've learned a new skill: **{learned_skill.name}**\n\n{learned_skill.description}\n\nNow I can help you with tasks related to this skill. What would you like me to do?"

                    # Update agent session
                    agent_session.status = "completed"
                    agent_session.completed_at = datetime.utcnow()
                    agent_session.skills_used = learned_skill.name
                    self.db.commit()

                    # Save assistant response
                    self._save_message("assistant", response, {"skill_learned": learned_skill.name})
                    self.conversation_history.append({"role": "assistant", "content": response})

                    return response

            # Step 3: Build system prompt with skills
            system_prompt = self._build_system_prompt(relevant_skills)

            # Step 4: Determine if parallel sub-agents are needed
            needs_parallel = await self._needs_parallel_execution(user_message)

            if needs_parallel:
                logger.info("Task requires parallel execution")
                response = await self._execute_with_subagents(
                    user_message,
                    system_prompt,
                    relevant_skills
                )
            else:
                # Single agent execution
                response = await self._execute_single(user_message, system_prompt)

            # Update agent session
            agent_session.status = "completed"
            agent_session.completed_at = datetime.utcnow()
            agent_session.skills_used = ",".join([s.name for s in relevant_skills])
            self.db.commit()

            # Save assistant response
            self._save_message("assistant", response, {
                "skills_used": [s.name for s in relevant_skills],
                "llm_provider": self.llm_provider
            })

            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

            return response

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            agent_session.status = "failed"
            agent_session.error_message = str(e)
            agent_session.completed_at = datetime.utcnow()
            self.db.commit()
            raise

    def _build_system_prompt(self, skills: List) -> str:
        """Build system prompt with skills"""
        base_prompt = """You are Bhrahma, an advanced AI agent capable of learning new skills and solving complex tasks.

You can:
1. Use specialized skills to solve problems
2. Learn new skills from the internet when needed
3. Coordinate multiple sub-agents for parallel task execution
4. Adapt to different types of tasks and domains

Always be helpful, accurate, and efficient in your responses."""

        if skills:
            skills_text = self.skill_manager.format_skills_for_prompt(skills)
            return base_prompt + "\n\n" + skills_text

        return base_prompt

    async def _execute_single(self, message: str, system_prompt: str) -> str:
        """Execute task with single agent"""
        response = await self.llm_client.generate(
            messages=self.conversation_history,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=4096
        )

        return response["content"]

    async def _execute_with_subagents(
        self,
        message: str,
        system_prompt: str,
        skills: List
    ) -> str:
        """Execute task with parallel sub-agents"""
        # First, use LLM to decompose the task
        decomposition_prompt = f"""Decompose the following task into 2-5 independent subtasks that can be executed in parallel:

Task: {message}

Return the subtasks as a numbered list."""

        decomposition_response = await self.llm_client.generate(
            messages=[{"role": "user", "content": decomposition_prompt}],
            system_prompt="You are a task decomposition specialist.",
            temperature=0.3,
            max_tokens=1024
        )

        subtasks = self._parse_subtasks(decomposition_response["content"])

        if not subtasks or len(subtasks) < 2:
            # If decomposition fails, fall back to single execution
            return await self._execute_single(message, system_prompt)

        logger.info(f"Decomposed into {len(subtasks)} subtasks")

        # Spawn sub-agents for each subtask (up to MAX_PARALLEL_AGENTS)
        subtasks = subtasks[:settings.MAX_PARALLEL_AGENTS]

        # Create tasks for parallel execution
        tasks = [
            self._execute_subagent(subtask, system_prompt, i)
            for i, subtask in enumerate(subtasks)
        ]

        # Execute in parallel
        subagent_results = await asyncio.gather(*tasks)

        # Synthesize results
        synthesis_prompt = f"""Original task: {message}

Subtask results:
{self._format_subagent_results(subtasks, subagent_results)}

Synthesize these results into a coherent, comprehensive response to the original task."""

        final_response = await self.llm_client.generate(
            messages=[{"role": "user", "content": synthesis_prompt}],
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=4096
        )

        return final_response["content"]

    async def _execute_subagent(
        self,
        subtask: str,
        system_prompt: str,
        agent_id: int
    ) -> str:
        """Execute a single sub-agent"""
        logger.info(f"Sub-agent {agent_id} processing: {subtask}")

        # Create sub-agent session
        sub_session_id = f"{self.session_id}_sub_{agent_id}"
        sub_agent_session = AgentSession(
            session_id=sub_session_id,
            agent_type="sub-agent",
            parent_session_id=self.session_id,
            status="running",
            started_at=datetime.utcnow(),
            llm_provider=self.llm_provider
        )
        self.db.add(sub_agent_session)
        self.db.commit()

        try:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": subtask}],
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=2048
            )

            sub_agent_session.status = "completed"
            sub_agent_session.completed_at = datetime.utcnow()
            self.db.commit()

            return response["content"]

        except Exception as e:
            logger.error(f"Sub-agent {agent_id} failed: {str(e)}")
            sub_agent_session.status = "failed"
            sub_agent_session.error_message = str(e)
            sub_agent_session.completed_at = datetime.utcnow()
            self.db.commit()
            return f"[Sub-agent {agent_id} failed: {str(e)}]"

    async def _needs_new_skill(self, message: str, existing_skills: List):
        """
        Determine if a new skill needs to be learned
        Returns: (bool, dict) - (needs_learning, skill_info)
        """
        import re

        learning_keywords = ["learn", "create skill", "new skill", "teach", "documentation"]
        message_lower = message.lower()

        # Check if user is asking to learn something
        if any(keyword in message_lower for keyword in learning_keywords):
            # Extract URLs from the message (for documentation)
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            urls = re.findall(url_pattern, message)

            # Use LLM to extract skill topic and description
            analysis_prompt = f"""Analyze this user message and extract the skill learning request:

User message: "{message}"

Extract:
1. Topic: What skill should be learned? (short phrase)
2. Description: What should this skill do? (1-2 sentences)
3. URLs: Any documentation URLs mentioned

Return in this format:
TOPIC: [topic here]
DESCRIPTION: [description here]
URLS: [comma-separated URLs or 'none']

If this is NOT a skill learning request, return: NOT_LEARNING"""

            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,
                max_tokens=256
            )

            content = response["content"].strip()

            if "NOT_LEARNING" in content:
                return False, {}

            # Parse the response
            topic_match = re.search(r'TOPIC:\s*(.+)', content)
            desc_match = re.search(r'DESCRIPTION:\s*(.+)', content)
            urls_match = re.search(r'URLS:\s*(.+)', content)

            if topic_match and desc_match:
                skill_info = {
                    "topic": topic_match.group(1).strip(),
                    "description": desc_match.group(1).strip(),
                    "urls": []
                }

                # Add URLs from regex or LLM extraction
                if urls:
                    skill_info["urls"] = urls
                elif urls_match and "none" not in urls_match.group(1).lower():
                    extracted_urls = [u.strip() for u in urls_match.group(1).split(',')]
                    skill_info["urls"] = extracted_urls

                logger.info(f"Detected skill learning request: {skill_info}")
                return True, skill_info

        return False, {}

    async def _learn_new_skill(self, skill_info: Dict):
        """
        Learn a new skill using the skill creator
        """
        from agents.skill_creator import SkillCreator

        try:
            skill_creator = SkillCreator(self.llm_client, self.skill_manager)

            # Crawl documentation if URLs provided
            search_web = True
            documentation_urls = skill_info.get("urls", [])

            if documentation_urls:
                logger.info(f"Crawling documentation: {documentation_urls}")
                # The skill creator will crawl these URLs

            # Create the skill
            result = await skill_creator.create_skill(
                topic=skill_info["topic"],
                description=skill_info["description"],
                search_web=search_web,
                auto_test=False,  # Skip testing for now
                urls=documentation_urls
            )

            if result and result.get("skill"):
                return result["skill"]

            return None

        except Exception as e:
            logger.error(f"Error learning skill: {str(e)}")
            return None

    async def _needs_parallel_execution(self, message: str) -> bool:
        """Determine if task needs parallel execution"""
        # Simple heuristic: check for keywords indicating complex/multi-part tasks
        parallel_keywords = [
            "multiple", "several", "compare", "analyze all",
            "various", "different", "each", "both"
        ]
        return any(keyword in message.lower() for keyword in parallel_keywords)

    def _parse_subtasks(self, decomposition: str) -> List[str]:
        """Parse subtasks from LLM decomposition response"""
        lines = decomposition.strip().split('\n')
        subtasks = []

        for line in lines:
            line = line.strip()
            # Look for numbered items (1., 2., 1), 2), etc.)
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering and clean up
                subtask = line.lstrip('0123456789.-) ').strip()
                if subtask:
                    subtasks.append(subtask)

        return subtasks

    def _format_subagent_results(self, subtasks: List[str], results: List[str]) -> str:
        """Format subagent results for synthesis"""
        formatted = ""
        for i, (subtask, result) in enumerate(zip(subtasks, results), 1):
            formatted += f"\n### Subtask {i}: {subtask}\n"
            formatted += f"Result: {result}\n"
        return formatted

    def _save_message(self, role: str, content: str, metadata: Dict = None):
        """Save message to database"""
        message = ChatMessage(
            session_id=self.session_id,
            role=role,
            content=content,
            meta_data=metadata or {}
        )
        self.db.add(message)
        self.db.commit()

    def _create_agent_session(self) -> AgentSession:
        """Create and return a new agent session"""
        # Create unique session ID for this execution
        execution_session_id = f"{self.session_id}_{uuid.uuid4().hex[:8]}"

        session = AgentSession(
            session_id=execution_session_id,
            agent_type="bhrahma",
            status="running",
            started_at=datetime.utcnow(),
            llm_provider=self.llm_provider
        )
        self.db.add(session)
        self.db.commit()
        return session
