from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import BaseModel

class ChannelMetrics(BaseModel):
    __tablename__ = "channel_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey('telegram_channels.id'), nullable=False)
    subscribers_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    average_engagement = Column(Integer, default=0)  # Percentage
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Derived metrics
    avg_views = Column(Float, default=0.0)
    avg_engagement = Column(Float, default=0.0)
    
    # Additional data
    demographics = Column(JSON, default={})
    traffic_sources = Column(JSON, default={})
    
    # Relationships
    channel = relationship("TelegramChannel", back_populates="metrics")

    def __repr__(self):
        return f"<ChannelMetrics for channel {self.channel_id} at {self.timestamp}>"

class PostMetrics(BaseModel):
    __tablename__ = "post_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey('posts.id'), nullable=False)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    ctr = Column(Integer, default=0)  # Click-through rate in percentage
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Derived metrics
    ctr = Column(Float, default=0.0)
    engagement_rate = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    
    # Additional data
    demographics = Column(JSON, default={})
    referrers = Column(JSON, default={})
    
    # Relationships
    post = relationship("Post", back_populates="metrics")

    def __repr__(self):
        return f"<PostMetrics for post {self.post_id} at {self.timestamp}>" 