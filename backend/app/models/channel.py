from datetime import datetime
from typing import Optional, List, Dict
from beanie import Document, Link
from .user import User

class Channel(Document):
    username: str
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_monetized: bool = False
    subscriber_count: int = 0
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    settings: Dict = {}
    meta_data: Dict = {}
    owner: Link[User]

    class Settings:
        name = "channels"
        
    class Config:
        json_schema_extra = {
            "example": {
                "username": "tech_channel",
                "title": "Technology News",
                "description": "Latest tech news and updates",
                "category": "Technology",
                "is_monetized": True
            }
        } 