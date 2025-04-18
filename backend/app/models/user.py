from sqlalchemy import Column, String, Boolean, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum('admin', 'operator', name='user_roles'), nullable=False)
    reset_password_token = Column(String, unique=True)
    reset_password_token_expires = Column(DateTime)

    def __repr__(self):
        return f"<User {self.email}>" 