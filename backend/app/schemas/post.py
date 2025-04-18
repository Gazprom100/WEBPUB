from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class PostStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

class PostBase(BaseModel):
    channel_id: UUID
    content: str
    scheduled_time: datetime

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    status: Optional[PostStatus] = None

class PostResponse(PostBase):
    id: UUID
    image_url: Optional[str] = None
    status: PostStatus
    telegram_message_id: Optional[str] = None
    created_by: UUID
    approved_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PostMetrics(BaseModel):
    views_count: int = Field(default=0)
    likes_count: int = Field(default=0)
    shares_count: int = Field(default=0)
    comments_count: int = Field(default=0)
    ctr: int = Field(default=0)  # Click-through rate in percentage

    class Config:
        from_attributes = True 