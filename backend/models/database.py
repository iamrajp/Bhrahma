"""
Database models for Bhrahma system
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import settings

Base = declarative_base()

class Skill(Base):
    """Model for storing Agent Skills"""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)  # Full SKILL.md content
    tags = Column(String, default="")  # Comma-separated tags
    category = Column(String, default="general")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    resources = relationship("SkillResource", back_populates="skill", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Skill(name='{self.name}', category='{self.category}')>"


class SkillResource(Base):
    """Model for storing bundled resources with skills (scripts, files, etc.)"""
    __tablename__ = "skill_resources"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    resource_type = Column(String, nullable=False)  # script, reference, asset
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    skill = relationship("Skill", back_populates="resources")

    def __repr__(self):
        return f"<SkillResource(filename='{self.filename}', type='{self.resource_type}')>"


class ChatMessage(Base):
    """Model for storing chat messages"""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    meta_data = Column(JSON, default={})  # Store additional info (skills used, agents spawned, etc.)

    def __repr__(self):
        return f"<ChatMessage(role='{self.role}', session_id='{self.session_id}')>"


class AgentSession(Base):
    """Model for tracking agent execution sessions"""
    __tablename__ = "agent_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, nullable=False, index=True)
    agent_type = Column(String, nullable=False)  # bhrahma, sub-agent
    parent_session_id = Column(String, nullable=True)  # For sub-agents
    status = Column(String, default="pending")  # pending, running, completed, failed
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    skills_used = Column(String, default="")  # Comma-separated skill names
    llm_provider = Column(String, nullable=True)  # anthropic, openai, mixtral
    error_message = Column(Text, nullable=True)
    meta_data = Column(JSON, default={})

    def __repr__(self):
        return f"<AgentSession(session_id='{self.session_id}', status='{self.status}')>"


# Database setup
def get_database_url():
    """Get SQLite database URL"""
    db_path = Path(settings.DATABASE_PATH)
    db_path.parent.mkdir(exist_ok=True, parents=True)
    return f"sqlite:///{db_path}"


def init_database():
    """Initialize database and create all tables"""
    engine = create_engine(
        get_database_url(),
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
    Base.metadata.create_all(bind=engine)
    return engine


def get_session_maker():
    """Get SQLAlchemy session maker"""
    engine = init_database()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


# Dependency for FastAPI
def get_db():
    """Database dependency for FastAPI routes"""
    SessionLocal = get_session_maker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
