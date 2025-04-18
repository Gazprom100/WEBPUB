from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from .base import Base

class PostMetrics(Base):
    """Historical metrics data for posts"""
    
    __tablename__ = "post_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)
    engagement_rate = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    demographics = Column(JSON, default={})
    referrers = Column(JSON, default={})
    
    post = relationship("Post", back_populates="metrics")
    
    def __repr__(self):
        return f"<PostMetrics for post {self.post_id} at {self.timestamp}>"


class ChannelMetrics(Base):
    """Historical metrics data for channels"""
    
    __tablename__ = "channel_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    subscriber_count = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    avg_views = Column(Float, default=0.0)
    avg_engagement = Column(Float, default=0.0)
    avg_ctr = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    demographics = Column(JSON, default={})
    traffic_sources = Column(JSON, default={})
    
    channel = relationship("Channel", back_populates="metrics")
    
    def __repr__(self):
        return f"<ChannelMetrics for channel {self.channel_id} at {self.timestamp}>" 