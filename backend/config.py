"""
Configuration management for Bhrahma system
"""
from pydantic_settings import BaseSettings
from typing import Literal
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # LLM API Keys
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    MIXTRAL_API_KEY: str = ""

    # Default LLM
    DEFAULT_LLM: Literal["anthropic", "openai", "mixtral"] = "anthropic"

    # Database
    DATABASE_PATH: str = "database/bhrahma.db"

    # Web Search API Keys
    GOOGLE_SEARCH_API_KEY: str = ""
    GOOGLE_SEARCH_ENGINE_ID: str = ""
    BRAVE_SEARCH_API_KEY: str = ""

    # Application Settings
    LOG_LEVEL: str = "INFO"
    MAX_PARALLEL_AGENTS: int = 5

    # Paths
    SKILLS_DIR: Path = Path("skills")
    LOGS_DIR: Path = Path("logs")

    class Config:
        env_file = str(Path(__file__).parent.parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True

# Global settings instance
settings = Settings()

# Ensure directories exist
settings.SKILLS_DIR.mkdir(exist_ok=True)
settings.LOGS_DIR.mkdir(exist_ok=True)
Path(settings.DATABASE_PATH).parent.mkdir(exist_ok=True)
