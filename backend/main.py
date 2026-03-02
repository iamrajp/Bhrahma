"""
FastAPI backend for Bhrahma agentic system
"""
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio
from loguru import logger
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from models import (
    init_database,
    get_db,
    ChatMessageRequest,
    ChatMessageResponse,
    SkillResponse,
    SkillLearningRequest,
    QueueStatus,
    ChatMessage,
    Skill
)
from services.message_queue import message_queue, QueueTask
from services.skill_manager import SkillManager
from services.llm_client import LLMFactory
from agents.bhrahma_agent import BhrahmaAgent
from agents.skill_creator import SkillCreator
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Bhrahma Agentic System",
    description="AI agent system with skill learning capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and start queue processor"""
    logger.info("Initializing Bhrahma system...")
    init_database()
    logger.info("Database initialized")

    # Start queue processor in background
    asyncio.create_task(message_queue.process_queue(process_message_task))
    logger.info("Message queue processor started")


async def process_message_task(task: QueueTask):
    """Process a message task from the queue"""
    logger.info(f"Processing task {task.task_id}")

    # Get database session
    from models.database import get_session_maker
    SessionLocal = get_session_maker()
    db = SessionLocal()

    try:
        # Create Bhrahma agent
        llm_provider = task.metadata.get("llm_provider", settings.DEFAULT_LLM)
        agent = BhrahmaAgent(
            session_id=task.session_id,
            llm_provider=llm_provider,
            db_session=db
        )

        # Process the message
        response = await agent.process_message(task.message)

        logger.info(f"Task {task.task_id} completed successfully")

    except Exception as e:
        logger.error(f"Error processing task {task.task_id}: {str(e)}")
        # Save error message
        error_msg = ChatMessage(
            session_id=task.session_id,
            role="system",
            content=f"Error: {str(e)}",
            meta_data={"error": True}
        )
        db.add(error_msg)
        db.commit()

    finally:
        db.close()


# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Bhrahma Agentic System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        available_llms = LLMFactory.get_available_providers()
    except Exception as e:
        logger.warning(f"LLM check failed in health endpoint: {str(e)}")
        available_llms = []

    return {
        "status": "healthy",
        "database": "connected",
        "queue": "running",
        "available_llms": available_llms
    }


@app.post("/chat", response_model=dict)
async def send_message(
    message_request: ChatMessageRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Send a message to Bhrahma agent
    Message will be queued and processed asynchronously
    """
    import uuid

    session_id = message_request.session_id or str(uuid.uuid4())

    # Enqueue the message
    task_id = await message_queue.enqueue(
        message=message_request.content,
        session_id=session_id,
        metadata={}
    )

    return {
        "task_id": task_id,
        "session_id": session_id,
        "status": "queued",
        "message": "Message queued for processing"
    }


@app.get("/chat/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_messages(
    session_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat messages for a session"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()

    return list(reversed(messages))


@app.get("/queue/status", response_model=QueueStatus)
async def get_queue_status():
    """Get current queue status"""
    status = message_queue.get_status()
    return QueueStatus(
        queue_size=status["queue_size"],
        current_task=status["current_task"]["message"] if status["current_task"] else None,
        is_processing=status["is_processing"]
    )


@app.get("/skills", response_model=List[SkillResponse])
async def list_skills(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all available skills"""
    skill_manager = SkillManager(db)

    if category:
        skills = db.query(Skill).filter(
            Skill.is_active == True,
            Skill.category == category
        ).all()
    else:
        skills = skill_manager.get_all_skills()

    return skills


@app.get("/skills/{skill_name}", response_model=SkillResponse)
async def get_skill(
    skill_name: str,
    db: Session = Depends(get_db)
):
    """Get a specific skill"""
    skill_manager = SkillManager(db)
    skill = skill_manager.get_skill(skill_name)

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    return skill


@app.post("/skills/learn", response_model=dict)
async def learn_skill(
    request: SkillLearningRequest,
    db: Session = Depends(get_db)
):
    """
    Learn a new skill from the internet
    """
    try:
        llm_client = LLMFactory.create_client()
        skill_manager = SkillManager(db)
        skill_creator = SkillCreator(llm_client, skill_manager)

        result = await skill_creator.create_skill(
            topic=request.topic,
            description=request.description,
            search_web=request.search_web,
            auto_test=request.auto_test
        )

        return {
            "success": True,
            "skill_name": result["skill"].name,
            "skill_id": result["skill"].id,
            "message": f"Successfully created skill: {result['skill'].name}"
        }

    except Exception as e:
        logger.error(f"Error learning skill: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/llm/providers")
async def list_llm_providers():
    """List available LLM providers"""
    return {
        "providers": LLMFactory.get_available_providers(),
        "default": settings.DEFAULT_LLM
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
