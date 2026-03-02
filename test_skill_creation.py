#!/usr/bin/env python3
"""
Test skill creation
"""
import sys
sys.path.insert(0, "backend")

from models.database import get_session_maker
from services.llm_client import LLMFactory
from services.skill_manager import SkillManager
from agents.skill_creator import SkillCreator

async def test_create_skill():
    print("Testing skill creation...")

    # Setup
    SessionLocal = get_session_maker()
    db = SessionLocal()

    llm_client = LLMFactory.create_client("anthropic")
    skill_manager = SkillManager(db)
    skill_creator = SkillCreator(llm_client, skill_manager)

    # Create a test skill
    print("\nCreating test skill...")
    result = await skill_creator.create_skill(
        topic="Python pytest basics",
        description="Generate simple pytest unit tests",
        search_web=False,  # Disable web search for faster testing
        auto_test=False
    )

    print(f"\n✅ Skill created: {result['skill'].name}")
    print(f"   Description: {result['skill'].description}")
    print(f"   Category: {result['skill'].category}")

    # List all skills
    print("\nAll skills in database:")
    skills = skill_manager.get_all_skills()
    for skill in skills:
        print(f"  - {skill.name} ({skill.category})")

    db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_create_skill())
