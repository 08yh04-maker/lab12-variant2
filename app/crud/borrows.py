from typing import List, Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session, joinedload

from app.models import Borrow, Book, Reader, BorrowStatus, Fine
from app.schemas import BorrowCreate


def get_borrow(db: Session, borrow_id: int) -> Optional[Borrow]:
    return db.query(Borrow).options(
        joinedload(Borrow.book),
        joinedload(Borrow.reader)
    ).filter(Borrow.id == borrow_id).first()


def get_reader_borrows(db: Session, reader_id: int) -> List[Borrow]:
    return db.query(Borrow).options(
        joinedload(Borrow.book),
        joinedload(Borrow.reader)
    ).filter(Borrow.reader_id == reader_id).order_by(Borrow.borrow_date.desc()).all()


def create_borrow(db: Session, borrow: BorrowCreate) -> Optional[Borrow]:
    reader = db.query(Reader).filter(Reader.id == borrow.reader_id).first()
    if not reader:
        return None

    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    if not book or book.quantity_available < 1:
        return None

    db_borrow = Borrow(
        reader_id=borrow.reader_id,
        book_id=borrow.book_id,
        borrow_date=date.today(),
        due_date=date.today() + timedelta(days=14),
        status=BorrowStatus.BORROWED
    )

    book.quantity_available -= 1

    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow


def return_book(db: Session, borrow_id: int) -> Optional[Borrow]:
    db_borrow = get_borrow(db, borrow_id)
    if not db_borrow or db_borrow.status != BorrowStatus.BORROWED:
        return None

    db_borrow.return_date = date.today()
    db_borrow.status = BorrowStatus.RETURNED

    book = db.query(Book).filter(Book.id == db_borrow.book_id).first()
    if book:
        book.quantity_available += 1

    if db_borrow.return_date > db_borrow.due_date:
        days_overdue = (db_borrow.return_date - db_borrow.due_date).days
        if days_overdue > 0:
            fine_amount = days_overdue * 10.0
            fine = Fine(
                borrow_id=db_borrow.id,
                reader_id=db_borrow.reader_id,
                amount=fine_amount,
                paid=False
            )
            db.add(fine)

    db.commit()
    db.refresh(db_borrow)
    return db_borrow
