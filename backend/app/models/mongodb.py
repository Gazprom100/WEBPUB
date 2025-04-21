from datetime import datetime
from typing import Optional, List
from enum import Enum
from beanie import Document, Link
from pydantic import EmailStr, Field

class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"

class PostMetrics(BaseModel):
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    ctr: float = 0.0
    revenue: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(Document):
    email: EmailStr
    hashed_password: str
    full_name: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True,
            }
        }

class Channel(Document):
    username: str
    category: str
    description: Optional[str]
    is_monetized: bool = False
    owner: Link[User]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "channels"

class Post(Document):
    title: str
    description: Optional[str]
    content: str
    status: PostStatus = PostStatus.DRAFT
    media_urls: List[str] = []
    
    # Metrics
    views_count: int = 0
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    ctr: float = 0.0
    revenue: float = 0.0
    
    # Relations
    author: Link[User]
    channel: Link[Channel]
    
    # Dates
    scheduled_for: Optional[datetime]
    published_at: Optional[datetime]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "posts"

class ChannelMetrics(Document):
    channel: Link[Channel]
    subscribers_count: int = 0
    total_views: int = 0
    avg_engagement: float = 0.0
    total_revenue: float = 0.0
    metric_date: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "channel_metrics" 