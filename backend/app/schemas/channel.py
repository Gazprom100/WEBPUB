from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class ChannelBase(BaseModel):
    channel_id: str
    bot_token: str

class ChannelCreate(ChannelBase):
    pass

class ChannelUpdate(BaseModel):
    is_active: Optional[bool] = None
    bot_token: Optional[str] = None

class ChannelResponse(ChannelBase):
    id: UUID
    channel_name: str
    channel_username: Optional[str] = None
    channel_description: Optional[str] = None
    channel_avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChannelStats(BaseModel):
    subscribers_count: int = Field(default=0)
    views_count: int = Field(default=0)
    average_engagement: int = Field(default=0)  # Percentage

    class Config:
        from_attributes = True 