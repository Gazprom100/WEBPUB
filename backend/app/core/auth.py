from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..models.user import User
from ..core.database import get_db
from ..core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Создаем тестового пользователя
    test_user = User(
        id="00000000-0000-0000-0000-000000000000",
        email="test@example.com",
        full_name="Test User",
        is_active=True,
        is_superuser=True
    )
    return test_user 