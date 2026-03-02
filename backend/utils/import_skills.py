"""
Utility script to import skills from directories
"""
from pathlib import Path
import sys
from loguru import logger

sys.path.append(str(Path(__file__).parent.parent))
from models.database import get_session_maker, init_database
from services.skill_manager import SkillManager


def import_skills_from_directory(skills_dir: Path):
    """
    Import all skills from a directory

    Expected structure:
    skills_dir/
        skill-name-1/
            SKILL.md
        skill-name-2/
            SKILL.md
    """
    logger.info(f"Importing skills from {skills_dir}")

    # Initialize database
    init_database()
    SessionLocal = get_session_maker()
    db = SessionLocal()

    skill_manager = SkillManager(db)
    imported_count = 0
    failed_count = 0

    # Iterate through subdirectories
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            logger.warning(f"Skipping {skill_dir.name} - no SKILL.md found")
            continue

        try:
            skill = skill_manager.import_skill_from_directory(skill_dir)
            logger.info(f"✓ Imported: {skill.name}")
            imported_count += 1
        except Exception as e:
            logger.error(f"✗ Failed to import {skill_dir.name}: {str(e)}")
            failed_count += 1

    db.close()

    logger.info(f"\nImport complete:")
    logger.info(f"  Imported: {imported_count}")
    logger.info(f"  Failed: {failed_count}")

    return imported_count, failed_count


def import_default_skills():
    """Import the default skills that come with Bhrahma"""
    project_root = Path(__file__).parent.parent.parent
    skills_dir = project_root / "skills"

    if not skills_dir.exists():
        logger.warning(f"Skills directory not found: {skills_dir}")
        return

    import_skills_from_directory(skills_dir)


def download_anthropic_skills():
    """
    Download skills from Anthropic's repository
    Requires git to be installed
    """
    import subprocess
    import tempfile
    import shutil

    logger.info("Downloading Anthropic skills from GitHub...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Clone the repository
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", "https://github.com/anthropics/skills.git", str(temp_path / "anthropic-skills")],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone repository: {e}")
            return
        except FileNotFoundError:
            logger.error("Git not found. Please install git to download Anthropic skills.")
            return

        anthropic_skills_dir = temp_path / "anthropic-skills" / "skills"

        if not anthropic_skills_dir.exists():
            logger.error("Skills directory not found in cloned repository")
            return

        # Import skills
        logger.info("Importing skills from Anthropic repository...")
        imported, failed = import_skills_from_directory(anthropic_skills_dir)

        # Optionally copy skills to local directory
        project_root = Path(__file__).parent.parent.parent
        local_skills_dir = project_root / "skills" / "anthropic"
        local_skills_dir.mkdir(parents=True, exist_ok=True)

        # Copy skill directories
        for skill_dir in anthropic_skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                dest_dir = local_skills_dir / skill_dir.name
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(skill_dir, dest_dir)

        logger.info(f"Copied {imported} skills to {local_skills_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Import skills into Bhrahma")
    parser.add_argument(
        "--source",
        choices=["local", "anthropic"],
        default="local",
        help="Source of skills to import"
    )
    parser.add_argument(
        "--dir",
        type=str,
        help="Custom directory to import skills from"
    )

    args = parser.parse_args()

    if args.dir:
        import_skills_from_directory(Path(args.dir))
    elif args.source == "anthropic":
        download_anthropic_skills()
    else:
        import_default_skills()
