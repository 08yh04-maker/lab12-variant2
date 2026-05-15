from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user, get_current_admin_user
from app.models import User


def get_db_dependency():
    return Depends(get_db)


def get_current_user_dependency():
    return Depends(get_current_user)


def get_admin_user_dependency():
    return Depends(get_current_admin_user)