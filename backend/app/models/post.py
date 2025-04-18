from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import BaseModel

class Post(BaseModel):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey('telegram_channels.id'), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(Enum('draft', 'approved', 'scheduled', 'published', 'failed', name='post_status'), default='draft')
    telegram_message_id = Column(String)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Relationships
    channel = relationship("TelegramChannel", back_populates="posts")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    metrics = relationship("PostMetrics", back_populates="post")

    def __repr__(self):
        return f"<Post {self.id}>" 