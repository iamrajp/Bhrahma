"""
Skill Creator Agent - Learns new skills from the internet
"""
from typing import Dict, Any, List
from pathlib import Path
import sys
from loguru import logger

sys.path.append(str(Path(__file__).parent.parent))
from services.llm_client import LLMClient, LLMFactory
from services.web_search import WebSearchService
from services.skill_manager import SkillManager, SkillParser
from config import settings


class SkillCreator:
    """
    Agent that creates new skills by learning from the internet
    """

    def __init__(self, llm_client: LLMClient, skill_manager: SkillManager):
        self.llm_client = llm_client
        self.skill_manager = skill_manager
        self.web_search = WebSearchService()

    async def create_skill(
        self,
        topic: str,
        description: str,
        search_web: bool = True,
        auto_test: bool = True,
        urls: list = None
    ) -> Dict[str, Any]:
        """
        Create a new skill by researching the topic

        Args:
            topic: The skill topic (e.g., "Python testing with pytest")
            description: What the skill should do
            search_web: Whether to search the web for information
            auto_test: Whether to auto-test the generated skill

        Returns:
            Dict with skill data and metadata
        """
        logger.info(f"Creating skill for topic: {topic}")

        # Step 1: Gather information from the web
        research_data = ""
        if search_web:
            research_data = await self._research_topic(topic, urls)

        # Step 2: Generate the skill
        skill_content = await self._generate_skill(topic, description, research_data)

        # Step 3: Parse and validate the skill
        try:
            skill_data = SkillParser.parse_skill_file(skill_content)
        except Exception as e:
            logger.error(f"Failed to parse generated skill: {str(e)}")
            # Try to fix the skill
            skill_content = await self._fix_skill(skill_content, str(e))
            skill_data = SkillParser.parse_skill_file(skill_content)

        # Step 4: Test the skill (if applicable)
        test_results = None
        if auto_test:
            test_results = await self._test_skill(skill_data)

        # Step 5: Optimize the description
        optimized_description = await self._optimize_description(
            skill_data['name'],
            skill_data['description'],
            skill_data['instructions']
        )

        skill_data['description'] = optimized_description

        # Regenerate skill content with optimized description
        final_skill_content = SkillParser.create_skill_md(
            name=skill_data['name'],
            description=optimized_description,
            instructions=skill_data['instructions'],
            tags=skill_data.get('tags', ''),
            category=skill_data.get('category', 'general')
        )

        # Step 6: Save to database
        saved_skill = self.skill_manager.save_skill_to_db(
            name=skill_data['name'],
            description=optimized_description,
            content=final_skill_content,
            tags=skill_data.get('tags', ''),
            category=skill_data.get('category', 'general')
        )

        logger.info(f"Successfully created skill: {skill_data['name']}")

        return {
            "skill": saved_skill,
            "skill_data": skill_data,
            "test_results": test_results,
            "research_sources": research_data[:500] if research_data else None
        }

    async def _research_topic(self, topic: str, urls: list = None) -> str:
        """Research a topic from the web"""
        logger.info(f"Researching topic: {topic}")

        all_research = ""

        # If specific URLs provided, crawl them first
        if urls:
            logger.info(f"Crawling {len(urls)} provided documentation URLs")
            for url in urls:
                try:
                    page_data = await self.web_search.scrape_page(url)
                    if page_data.get("text"):
                        all_research += f"\n\n## Documentation: {url}\n\n"
                        all_research += f"# {page_data.get('title', 'Documentation')}\n\n"
                        all_research += page_data["text"][:15000]  # More content from direct URLs
                        all_research += "\n\n---\n"

                        # Also crawl linked pages from the same domain
                        domain = url.split('/')[2]
                        for link in page_data.get("links", [])[:10]:  # Top 10 links
                            link_url = link.get("url", "")
                            if link_url.startswith('/'):
                                link_url = f"https://{domain}{link_url}"
                            if domain in link_url and link_url != url:
                                try:
                                    sub_page = await self.web_search.scrape_page(link_url)
                                    if sub_page.get("text"):
                                        all_research += f"\n## {link.get('text', 'Page')}\n"
                                        all_research += sub_page["text"][:5000]
                                        all_research += "\n\n"
                                except:
                                    pass

                except Exception as e:
                    logger.error(f"Error scraping {url}: {str(e)}")

        # Also do web search for additional context
        search_queries = [
            f"{topic} official documentation",
            f"{topic} tutorial guide"
        ]

        for query in search_queries[:1]:  # Limit to 1 query when URLs provided
            try:
                scraped_pages = await self.web_search.search_and_scrape(
                    query=query,
                    num_results=2
                )

                documentation = self.web_search.extract_documentation(scraped_pages)
                all_research += f"\n\n## Search: {query}\n\n{documentation}"

            except Exception as e:
                logger.error(f"Error searching for {query}: {str(e)}")

        return all_research

    async def _generate_skill(
        self,
        topic: str,
        description: str,
        research_data: str
    ) -> str:
        """Generate a SKILL.md file using LLM"""
        prompt = f"""You are an expert at creating Agent Skills in the SKILL.md format.

Create a new skill for the following:

**Topic**: {topic}
**Description**: {description}

**Research Data**:
{research_data[:8000] if research_data else "No web research available. Use your training knowledge."}

Generate a complete SKILL.md file following this format:

```
---
name: skill-name-in-kebab-case
description: Clear, specific description of what the skill does and when to use it (be pushy about triggering!)
category: choose-appropriate-category
tags: relevant, tags
---

# Skill Name

Clear introduction to the skill.

## When to Use This Skill

- Specific trigger condition 1
- Specific trigger condition 2
- etc.

## Instructions

Step-by-step instructions with reasoning...

## Examples

Concrete examples of using the skill...

## Best Practices

Key points to remember...
```

**Requirements**:
1. Make the description very specific and "pushy" about when to trigger
2. Keep instructions under 500 lines
3. Explain the "why" behind each step
4. Include practical examples
5. Focus on one clear purpose

Generate the complete SKILL.md content now:"""

        response = await self.llm_client.generate(
            messages=[{"role": "user", "content": prompt}],
            system_prompt="You are a skill creation expert. Generate high-quality, focused skills.",
            temperature=0.7,
            max_tokens=4096
        )

        # Extract the skill content (remove markdown code blocks if present)
        content = response["content"]
        if "```" in content:
            # Extract content between code blocks
            parts = content.split("```")
            for part in parts:
                if part.strip().startswith("---"):
                    content = part.strip()
                    break

        return content

    async def _fix_skill(self, skill_content: str, error_message: str) -> str:
        """Attempt to fix a malformed skill"""
        prompt = f"""The following SKILL.md file has an error:

**Error**: {error_message}

**Skill Content**:
```
{skill_content}
```

Please fix the SKILL.md file and return the corrected version. Ensure:
1. YAML frontmatter is properly formatted
2. Required fields (name, description) are present
3. Content follows the SKILL.md format

Return only the fixed SKILL.md content:"""

        response = await self.llm_client.generate(
            messages=[{"role": "user", "content": prompt}],
            system_prompt="You are a SKILL.md format expert.",
            temperature=0.3,
            max_tokens=4096
        )

        return response["content"].strip()

    async def _test_skill(self, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test a skill with sample queries"""
        # For now, just validate that it can be parsed
        # In a full implementation, you'd create test cases and run them
        return {
            "validated": True,
            "name": skill_data['name'],
            "has_instructions": bool(skill_data['instructions'])
        }

    async def _optimize_description(
        self,
        name: str,
        description: str,
        instructions: str
    ) -> str:
        """Optimize the skill description for better triggering"""
        prompt = f"""You are optimizing a skill description to make it trigger more reliably.

**Skill Name**: {name}

**Current Description**: {description}

**Instructions Summary**: {instructions[:1000]}

Create an optimized description that:
1. Clearly states what the skill does
2. Explicitly lists when to use it
3. Is "pushy" about triggering conditions
4. Includes relevant keywords
5. Is 2-3 sentences maximum

Example good description:
"Generate Python unit tests using pytest. Use this skill whenever the user asks to test Python code, create tests, add test coverage, or verify functionality. Works with functions, classes, and modules."

Return only the optimized description (no explanation):"""

        response = await self.llm_client.generate(
            messages=[{"role": "user", "content": prompt}],
            system_prompt="You are an expert at writing skill descriptions.",
            temperature=0.5,
            max_tokens=256
        )

        return response["content"].strip().strip('"').strip("'")
