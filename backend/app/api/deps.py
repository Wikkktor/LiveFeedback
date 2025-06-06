import os
from typing import Any, Generator
from core.auth import oauth2_bearer
from db.session import SessionLocal
from dotenv import load_dotenv
from fastapi import Depends, Response
from jose import jwt, JWTError
from models.user import User
from sqlalchemy.orm import Session

from core.exceptions import get_user_exception

load_dotenv()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    response: Response,
    token: str = Depends(oauth2_bearer),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload: dict[str, Any] = jwt.decode(
            token, os.getenv("TOKEN"), algorithms=[os.getenv("ALGORYTM")]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise get_user_exception()
    except JWTError:
        raise get_user_exception()

    if user := db.query(User).filter(User.id == user_id).first():
        return user
    raise get_user_exception()
