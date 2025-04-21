from datetime import datetime
from typing import Optional, List, Dict
from beanie import Document, Link
from enum import Enum
from .user import User
from .channel import Channel

class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"

class Post(Document):
    title: str
    description: Optional[str] = None
    content: str
    status: PostStatus = PostStatus.DRAFT
    publish_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    media_urls: List[str] = []
    thumbnail_url: Optional[str] = None
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    ctr: float = 0.0
    revenue: float = 0.0
    settings: Dict = {}
    meta_data: Dict = {}
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    author: Link[User]
    channel: Link[Channel]

    class Settings:
        name = "posts"
        
    class Config:
        json_schema_extra = {
            "example": {
                "title": "New Post",
                "description": "Post description",
                "content": "Post content",
                "status": "draft"
            }
        } 