from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import BaseModel

class TelegramChannel(BaseModel):
    __tablename__ = "telegram_channels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(String, unique=True, nullable=False)
    channel_name = Column(String, nullable=False)
    channel_username = Column(String)
    channel_description = Column(String)
    channel_avatar_url = Column(String)
    bot_token = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="channels")
    posts = relationship("Post", back_populates="channel")
    metrics = relationship("ChannelMetrics", back_populates="channel")

    def __repr__(self):
        return f"<TelegramChannel {self.channel_name}>" 