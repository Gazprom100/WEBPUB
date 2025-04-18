from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import BaseModel

class ChannelMetrics(BaseModel):
    __tablename__ = "channel_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey('telegram_channels.id'), nullable=False)
    subscribers_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    average_engagement = Column(Integer, default=0)  # Percentage
    
    # Relationships
    channel = relationship("TelegramChannel", back_populates="metrics")

class PostMetrics(BaseModel):
    __tablename__ = "post_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey('posts.id'), nullable=False)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    ctr = Column(Integer, default=0)  # Click-through rate in percentage
    
    # Relationships
    post = relationship("Post", back_populates="metrics") 