from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import User
from app.schemas import BookCreate, BookUpdate, BookResponse, BookList
from app.crud import books as books_crud
from app.auth import get_current_admin_user

router = APIRouter(prefix="/books", tags=["Книги"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    existing_book = books_crud.get_book_by_isbn(db, book.isbn)
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ISBN already exists"
        )

    return books_crud.create_book(db, book)


@router.get("/", response_model=BookList)
def get_books(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size
    books, total = books_crud.get_books(
        db,
        skip=skip,
        limit=size,
        category=category,
        search=search
    )

    return {
        "books": books,
        "total": total,
        "page": page,
        "size": size
    }


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = books_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    if book.isbn:
        existing_book = books_crud.get_book_by_isbn(db, book.isbn)
        if existing_book and existing_book.id != book_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ISBN already exists"
            )

    updated_book = books_crud.update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    if not books_crud.delete_book(db, book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
