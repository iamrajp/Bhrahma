"""
Agent Skills manager for loading, parsing, and executing SKILL.md files
"""
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
import re
from loguru import logger
from sqlalchemy.orm import Session
import sys
sys.path.append(str(Path(__file__).parent.parent))
from models.database import Skill, SkillResource
from config import settings


class SkillParser:
    """Parser for SKILL.md files"""

    @staticmethod
    def parse_skill_file(content: str) -> Dict[str, Any]:
        """
        Parse a SKILL.md file and extract frontmatter and instructions

        Expected format:
        ---
        name: skill-name
        description: Description of the skill
        ---

        # Instructions in markdown
        """
        # Extract YAML frontmatter
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(frontmatter_pattern, content, re.DOTALL)

        if not match:
            raise ValueError("Invalid SKILL.md format: Missing YAML frontmatter")

        frontmatter_str, instructions = match.groups()

        try:
            frontmatter = yaml.safe_load(frontmatter_str)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in frontmatter: {str(e)}")

        # Validate required fields
        if 'name' not in frontmatter:
            raise ValueError("Missing required field 'name' in frontmatter")
        if 'description' not in frontmatter:
            raise ValueError("Missing required field 'description' in frontmatter")

        return {
            "name": frontmatter['name'],
            "description": frontmatter['description'],
            "tags": frontmatter.get('tags', ''),
            "category": frontmatter.get('category', 'general'),
            "instructions": instructions.strip(),
            "full_content": content
        }

    @staticmethod
    def create_skill_md(
        name: str,
        description: str,
        instructions: str,
        tags: str = "",
        category: str = "general"
    ) -> str:
        """Create a SKILL.md formatted string"""
        tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

        frontmatter = {
            "name": name,
            "description": description
        }

        if tags_list:
            frontmatter["tags"] = tags_list
        if category != "general":
            frontmatter["category"] = category

        yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)

        return f"---\n{yaml_str}---\n\n{instructions}"


class SkillManager:
    """Manager for loading, storing, and retrieving skills"""

    def __init__(self, db_session: Session):
        self.db = db_session
        self.skills_cache: Dict[str, Dict[str, Any]] = {}

    def load_skill_from_file(self, file_path: Path) -> Dict[str, Any]:
        """Load a skill from a SKILL.md file"""
        if not file_path.exists():
            raise FileNotFoundError(f"Skill file not found: {file_path}")

        content = file_path.read_text()
        return SkillParser.parse_skill_file(content)

    def save_skill_to_db(
        self,
        name: str,
        description: str,
        content: str,
        tags: str = "",
        category: str = "general"
    ) -> Skill:
        """Save a skill to the database"""
        # Check if skill already exists
        existing_skill = self.db.query(Skill).filter(Skill.name == name).first()

        if existing_skill:
            # Update existing skill
            existing_skill.description = description
            existing_skill.content = content
            existing_skill.tags = tags
            existing_skill.category = category
            self.db.commit()
            self.db.refresh(existing_skill)
            logger.info(f"Updated existing skill: {name}")
            return existing_skill
        else:
            # Create new skill
            new_skill = Skill(
                name=name,
                description=description,
                content=content,
                tags=tags,
                category=category
            )
            self.db.add(new_skill)
            self.db.commit()
            self.db.refresh(new_skill)
            logger.info(f"Created new skill: {name}")
            return new_skill

    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill from the database by name"""
        return self.db.query(Skill).filter(Skill.name == name, Skill.is_active == True).first()

    def get_all_skills(self) -> List[Skill]:
        """Get all active skills from the database"""
        return self.db.query(Skill).filter(Skill.is_active == True).all()

    def search_skills(self, query: str) -> List[Skill]:
        """Search skills by name, description, or tags"""
        search_pattern = f"%{query}%"
        return self.db.query(Skill).filter(
            Skill.is_active == True,
            (
                Skill.name.like(search_pattern) |
                Skill.description.like(search_pattern) |
                Skill.tags.like(search_pattern)
            )
        ).all()

    def select_skills_for_task(self, task_description: str, max_skills: int = 5) -> List[Skill]:
        """
        Select relevant skills for a given task based on description matching
        This is a simple implementation - in production, you'd use embeddings/semantic search
        """
        all_skills = self.get_all_skills()

        # Simple keyword matching for now
        task_keywords = set(task_description.lower().split())
        skill_scores = []

        for skill in all_skills:
            skill_keywords = set(
                (skill.name + " " + skill.description + " " + skill.tags).lower().split()
            )
            # Calculate overlap score
            overlap = len(task_keywords & skill_keywords)
            if overlap > 0:
                skill_scores.append((skill, overlap))

        # Sort by score and return top skills
        skill_scores.sort(key=lambda x: x[1], reverse=True)
        return [skill for skill, _ in skill_scores[:max_skills]]

    def import_skill_from_directory(self, skill_dir: Path) -> Skill:
        """Import a skill from a directory containing SKILL.md"""
        skill_md_path = skill_dir / "SKILL.md"
        if not skill_md_path.exists():
            raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

        # Parse the SKILL.md file
        skill_data = self.load_skill_from_file(skill_md_path)

        # Save to database
        skill = self.save_skill_to_db(
            name=skill_data['name'],
            description=skill_data['description'],
            content=skill_data['full_content'],
            tags=skill_data.get('tags', ''),
            category=skill_data.get('category', 'general')
        )

        # Import bundled resources (scripts, references, assets)
        for resource_type in ['scripts', 'references', 'assets']:
            resource_dir = skill_dir / resource_type
            if resource_dir.exists() and resource_dir.is_dir():
                for file_path in resource_dir.glob('*'):
                    if file_path.is_file():
                        self._save_skill_resource(
                            skill.id,
                            resource_type,
                            file_path.name,
                            file_path.read_text()
                        )

        return skill

    def _save_skill_resource(
        self,
        skill_id: int,
        resource_type: str,
        filename: str,
        content: str
    ):
        """Save a skill resource to the database"""
        resource = SkillResource(
            skill_id=skill_id,
            resource_type=resource_type,
            filename=filename,
            content=content
        )
        self.db.add(resource)
        self.db.commit()

    def get_skill_instructions(self, skill_name: str) -> str:
        """Get the instructions for a skill to include in the agent prompt"""
        skill = self.get_skill(skill_name)
        if not skill:
            raise ValueError(f"Skill not found: {skill_name}")

        # Parse the skill content to extract instructions
        skill_data = SkillParser.parse_skill_file(skill.content)
        return skill_data['instructions']

    def format_skills_for_prompt(self, skills: List[Skill]) -> str:
        """Format multiple skills for inclusion in a prompt"""
        if not skills:
            return ""

        skills_text = "\n\n# Available Skills\n\n"
        skills_text += "You have access to the following specialized skills:\n\n"

        for skill in skills:
            skill_data = SkillParser.parse_skill_file(skill.content)
            skills_text += f"## Skill: {skill.name}\n"
            skills_text += f"**Description**: {skill.description}\n\n"
            skills_text += f"{skill_data['instructions']}\n\n"
            skills_text += "---\n\n"

        return skills_text
