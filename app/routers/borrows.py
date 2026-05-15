from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User
from app.schemas import BorrowCreate, BorrowResponse
from app.crud import borrows as borrows_crud
from app.auth import get_current_admin_user, get_current_user

router = APIRouter(prefix="/borrows", tags=["Выдача книг"])


@router.post("/", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
def create_borrow(
    borrow: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_borrow = borrows_crud.create_borrow(db, borrow)
    if db_borrow is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create borrow. Check if reader and book exist and book is available"
        )
    return db_borrow


@router.post("/return/{borrow_id}", response_model=BorrowResponse)
def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_borrow = borrows_crud.return_book(db, borrow_id)
    if db_borrow is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot return book. Borrow not found or already returned"
        )
    return db_borrow


@router.get("/history/{reader_id}", response_model=List[BorrowResponse])
def get_reader_borrows(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    borrows = borrows_crud.get_reader_borrows(db, reader_id)
    return borrows
