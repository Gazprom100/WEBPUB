from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MetricsTimeRange(BaseModel):
    days: int = 30  # Default to last 30 days

class ChannelMetricsResponse(BaseModel):
    subscribers_count: int
    views_count: int
    average_engagement: float
    average_views: float = 0
    average_shares: float = 0
    average_comments: float = 0
    average_ctr: float = 0

class PostMetricsResponse(BaseModel):
    views_count: int
    likes_count: int
    shares_count: int
    comments_count: int
    ctr: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 