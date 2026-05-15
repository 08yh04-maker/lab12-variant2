from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Book
from app.schemas import BookCreate, BookUpdate


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()


def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
    return db.query(Book).filter(Book.isbn == isbn).first()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    search: Optional[str] = None
) -> tuple[List[Book], int]:
    query = db.query(Book)

    if category:
        query = query.filter(Book.category == category)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Book.title.ilike(search_term),
                Book.author.ilike(search_term)
            )
        )

    total = query.count()
    books = query.offset(skip).limit(limit).all()

    return books, total


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        published_year=book.published_year,
        quantity_total=book.quantity_total,
        quantity_available=book.quantity_total,
        category=book.category,
        description=book.description
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate) -> Optional[Book]:
    db_book = get_book(db, book_id)
    if not db_book:
        return None

    update_data = book.model_dump(exclude_unset=True)

    if "quantity_total" in update_data:
        diff = update_data["quantity_total"] - db_book.quantity_total
        db_book.quantity_available += diff
        if db_book.quantity_available < 0:
            db_book.quantity_available = 0

    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True
