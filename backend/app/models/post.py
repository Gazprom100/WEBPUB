from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, Float, JSON, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.models.base import Base


class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled" 
    PUBLISHED = "published"


class Post(Base):
    title = Column(String, nullable=False)
    description = Column(String)
    content = Column(String, nullable=False)
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
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    channel = relationship("Channel", back_populates="posts")
    
    def __repr__(self):
        return f"<Post {self.title}>" 