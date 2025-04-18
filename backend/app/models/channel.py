from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .base import Base

class Channel(Base):
    __tablename__ = "channels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    title = Column(String)
    description = Column(String)
    category = Column(String)
    is_monetized = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # Stats
    subscriber_count = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    avg_engagement = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    
    # Settings and metadata
    settings = Column(JSON, default={})
    metadata = Column(JSON, default={})
    
    # Foreign keys
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="channels")
    posts = relationship("Post", back_populates="channel")
    metrics = relationship("ChannelMetrics", back_populates="channel")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Channel {self.username}>" 