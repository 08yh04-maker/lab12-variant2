from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.models import Borrow, Book, Reader, Fine, BorrowStatus


def get_popular_books(db: Session, limit: int = 10) -> List[dict]:
    results = (
        db.query(
            Book.id.label("book_id"),
            Book.title.label("title"),
            Book.author.label("author"),
            func.count(Borrow.id).label("borrow_count")
        )
        .join(Borrow, Book.id == Borrow.book_id)
        .group_by(Book.id)
        .order_by(func.count(Borrow.id).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "book_id": row.book_id,
            "title": row.title,
            "author": row.author,
            "borrow_count": row.borrow_count
        }
        for row in results
    ]


def get_debtors(db: Session) -> List[dict]:
    results = (
        db.query(
            Reader.id.label("reader_id"),
            Reader.full_name.label("full_name"),
            Reader.phone.label("phone"),
            func.coalesce(func.sum(Fine.amount), 0).label("total_unpaid_fines")
        )
        .join(Fine, Reader.id == Fine.reader_id)
        .filter(Fine.paid == False)
        .group_by(Reader.id)
        .having(func.sum(Fine.amount) > 0)
        .all()
    )

    return [
        {
            "reader_id": row.reader_id,
            "full_name": row.full_name,
            "phone": row.phone,
            "total_unpaid_fines": row.total_unpaid_fines
        }
        for row in results
    ]


def get_overdue_books(db: Session) -> List[dict]:
    today = date.today()

    results = (
        db.query(
            Borrow.id.label("borrow_id"),
            Reader.id.label("reader_id"),
            Reader.full_name.label("reader_name"),
            Book.id.label("book_id"),
            Book.title.label("book_title"),
            Borrow.due_date.label("due_date")
        )
        .join(Reader, Borrow.reader_id == Reader.id)
        .join(Book, Borrow.book_id == Book.id)
        .filter(Borrow.status == BorrowStatus.BORROWED)
        .filter(Borrow.due_date < today)
        .all()
    )

    return [
        {
            "borrow_id": row.borrow_id,
            "reader_id": row.reader_id,
            "reader_name": row.reader_name,
            "book_id": row.book_id,
            "book_title": row.book_title,
            "due_date": row.due_date,
            "days_overdue": (today - row.due_date).days
        }
        for row in results
    ]


def get_admin_stats(db: Session) -> dict:
    total_books = db.query(func.count(Book.id)).scalar()
    total_readers = db.query(func.count(Reader.id)).scalar()
    active_borrows = db.query(func.count(Borrow.id)).filter(
        Borrow.status == BorrowStatus.BORROWED
    ).scalar()
    total_unpaid_fines = db.query(func.coalesce(func.sum(Fine.amount), 0)).filter(
        Fine.paid == False
    ).scalar()
    total_books_available = db.query(func.coalesce(func.sum(Book.quantity_available), 0)).scalar()

    return {
        "total_books": total_books,
        "total_readers": total_readers,
        "active_borrows": active_borrows,
        "total_unpaid_fines": float(total_unpaid_fines),
        "total_books_available": total_books_available
    }
