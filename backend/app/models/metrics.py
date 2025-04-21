from datetime import datetime
from typing import Optional, Dict
from beanie import Document, Link
from .post import Post
from .channel import Channel

class PostMetrics(Document):
    post: Link[Post]
    timestamp: datetime = datetime.utcnow()
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    ctr: float = 0.0
    engagement_rate: float = 0.0
    revenue: float = 0.0
    demographics: Dict = {}
    referrers: Dict = {}

    class Settings:
        name = "post_metrics"

class ChannelMetrics(Document):
    channel: Link[Channel]
    timestamp: datetime = datetime.utcnow()
    subscriber_count: int = 0
    total_views: int = 0
    total_likes: int = 0
    total_comments: int = 0
    total_shares: int = 0
    avg_views: float = 0.0
    avg_engagement: float = 0.0
    avg_ctr: float = 0.0
    revenue: float = 0.0
    demographics: Dict = {}
    traffic_sources: Dict = {}

    class Settings:
        name = "channel_metrics" 