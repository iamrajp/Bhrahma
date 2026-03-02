"""
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Skill Schemas
class SkillBase(BaseModel):
    name: str
    description: str
    content: str
    tags: str = ""
    category: str = "general"


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# Chat Message Schemas
class ChatMessageRequest(BaseModel):
    content: str
    session_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    timestamp: datetime
    meta_data: Dict[str, Any] = {}

    class Config:
        from_attributes = True


# Agent Session Schemas
class AgentSessionResponse(BaseModel):
    id: int
    session_id: str
    agent_type: str
    parent_session_id: Optional[str]
    status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    skills_used: str
    llm_provider: Optional[str]
    error_message: Optional[str]

    class Config:
        from_attributes = True


# Queue Status Schema
class QueueStatus(BaseModel):
    queue_size: int
    current_task: Optional[str]
    is_processing: bool


# Skill Learning Request
class SkillLearningRequest(BaseModel):
    topic: str
    description: str
    search_web: bool = True
    auto_test: bool = True
