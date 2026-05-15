from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User
from app.schemas import PopularBook, Debtor, OverdueBook, AdminStats
from app.crud import reports as reports_crud
from app.auth import get_current_admin_user

router = APIRouter(prefix="/reports", tags=["Отчёты"])


@router.get("/popular-books", response_model=List[PopularBook])
def get_popular_books(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return reports_crud.get_popular_books(db, limit)


@router.get("/debtors", response_model=List[Debtor])
def get_debtors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return reports_crud.get_debtors(db)


@router.get("/overdue-books", response_model=List[OverdueBook])
def get_overdue_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return reports_crud.get_overdue_books(db)


@router.get("/admin/stats", response_model=AdminStats)
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return reports_crud.get_admin_stats(db)
