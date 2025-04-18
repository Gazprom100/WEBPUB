from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, JSON, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from .base import Base


class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled" 
    PUBLISHED = "published"


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    content = Column(String)
    status = Column(Enum(PostStatus), default=PostStatus.DRAFT)
    
    # Publishing
    publish_at = Column(DateTime)
    published_at = Column(DateTime)
    
    # Media
    media_urls = Column(JSON, default=[])
    thumbnail_url = Column(String)
    
    # Metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    
    # Settings and metadata
    settings = Column(JSON, default={})
    metadata = Column(JSON, default={})
    
    # Foreign keys
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id"), nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    channel = relationship("Channel", back_populates="posts")
    metrics = relationship("PostMetrics", back_populates="post")
    
    def __repr__(self):
        return f"<Post {self.title}>" 