#!/usr/bin/env python3
"""
Test script for Bhrahma system
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    try:
        from models.database import init_database, get_session_maker
        from services.llm_client import LLMFactory
        from services.skill_manager import SkillManager
        from config import settings
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\nTesting database...")
    try:
        from models.database import init_database
        init_database()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_env_vars():
    """Test environment variables"""
    print("\nTesting environment variables...")
    try:
        from config import settings

        if settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY != "your_anthropic_api_key_here":
            print(f"✅ ANTHROPIC_API_KEY: Set (length: {len(settings.ANTHROPIC_API_KEY)})")
            has_key = True
        else:
            print("⚠️  ANTHROPIC_API_KEY: Not set or using placeholder")
            has_key = False

        print(f"✅ DEFAULT_LLM: {settings.DEFAULT_LLM}")
        print(f"✅ DATABASE_PATH: {settings.DATABASE_PATH}")

        return has_key
    except Exception as e:
        print(f"❌ Environment check failed: {e}")
        return False

def test_llm_client():
    """Test LLM client"""
    print("\nTesting LLM client...")
    try:
        from services.llm_client import LLMFactory

        available = LLMFactory.get_available_providers()
        print(f"✅ Available LLM providers: {available}")

        if not available:
            print("❌ No LLM providers available. Please add API key to .env")
            return False

        client = LLMFactory.create_client()
        print(f"✅ Created LLM client successfully")
        return True
    except Exception as e:
        print(f"❌ LLM client test failed: {e}")
        return False

def test_skills():
    """Test skill system"""
    print("\nTesting skill system...")
    try:
        from models.database import get_session_maker
        from services.skill_manager import SkillManager

        SessionLocal = get_session_maker()
        db = SessionLocal()
        skill_manager = SkillManager(db)

        skills = skill_manager.get_all_skills()
        print(f"✅ Found {len(skills)} skills in database")

        for skill in skills:
            print(f"   - {skill.name} ({skill.category})")

        db.close()
        return True
    except Exception as e:
        print(f"❌ Skill system test failed: {e}")
        return False

def run_quick_test():
    """Run a quick LLM test"""
    print("\n" + "="*50)
    print("QUICK LLM TEST")
    print("="*50)

    try:
        from services.llm_client import LLMFactory

        client = LLMFactory.create_client()
        print("Sending test message to LLM...")

        response = client.generate_sync(
            messages=[{"role": "user", "content": "Say 'Hello from Bhrahma!' and nothing else."}],
            temperature=0.3,
            max_tokens=50
        )

        print(f"\n✅ LLM Response: {response['content']}")
        print(f"✅ Tokens used: {response['usage']['input_tokens']} input, {response['usage']['output_tokens']} output")
        return True
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False

def main():
    print("="*50)
    print("BHRAHMA SYSTEM TEST")
    print("="*50)

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Environment", test_env_vars()))
    results.append(("Database", test_database()))
    results.append(("LLM Client", test_llm_client()))
    results.append(("Skills", test_skills()))

    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(result[1] for result in results)

    if all_passed:
        print("\n✅ All tests passed! System is ready.")

        # Offer to run quick LLM test
        print("\nWould you like to run a quick LLM test? (y/n)")
        try:
            response = input().strip().lower()
            if response == 'y':
                run_quick_test()
        except:
            pass
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Make sure .env file exists with your API key")
        print("2. Run: cp .env.example .env")
        print("3. Edit .env and add your ANTHROPIC_API_KEY")
        print("4. Run: python backend/utils/import_skills.py --source local")

if __name__ == "__main__":
    main()
