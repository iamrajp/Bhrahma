"""
In-memory message queue for handling chat requests
"""
import asyncio
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass
from loguru import logger
import uuid


@dataclass
class QueueTask:
    """Represents a task in the queue"""
    task_id: str
    message: str
    session_id: str
    timestamp: datetime
    metadata: Dict[str, Any]


class MessageQueue:
    """In-memory message queue with FIFO processing"""

    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.is_processing: bool = False
        self.current_task: Optional[QueueTask] = None
        self.processing_lock = asyncio.Lock()

    async def enqueue(
        self,
        message: str,
        session_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add a message to the queue"""
        task_id = str(uuid.uuid4())
        task = QueueTask(
            task_id=task_id,
            message=message,
            session_id=session_id,
            timestamp=datetime.utcnow(),
            metadata=metadata or {}
        )

        await self.queue.put(task)
        logger.info(f"Task {task_id} enqueued. Queue size: {self.queue.qsize()}")
        return task_id

    async def process_queue(self, processor: Callable):
        """Process tasks from the queue"""
        while True:
            try:
                # Get next task from queue
                task = await self.queue.get()

                async with self.processing_lock:
                    self.is_processing = True
                    self.current_task = task

                logger.info(f"Processing task {task.task_id}")

                try:
                    # Process the task using the provided processor function
                    await processor(task)
                except Exception as e:
                    logger.error(f"Error processing task {task.task_id}: {str(e)}")
                finally:
                    # Mark task as done
                    self.queue.task_done()
                    self.current_task = None
                    self.is_processing = False

            except asyncio.CancelledError:
                logger.info("Queue processing cancelled")
                break
            except Exception as e:
                logger.error(f"Unexpected error in queue processing: {str(e)}")

    def get_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            "queue_size": self.queue.qsize(),
            "is_processing": self.is_processing,
            "current_task": {
                "task_id": self.current_task.task_id,
                "message": self.current_task.message[:100] + "..." if len(self.current_task.message) > 100 else self.current_task.message,
                "session_id": self.current_task.session_id
            } if self.current_task else None
        }

    async def wait_until_complete(self):
        """Wait until all tasks in the queue are processed"""
        await self.queue.join()


# Global queue instance
message_queue = MessageQueue()
