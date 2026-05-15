from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Date,
    ForeignKey, Float, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from datetime import datetime, date
import enum

from app.database import Base


class BorrowStatus(str, enum.Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reader = relationship("Reader", back_populates="user", uselist=False)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    author = Column(String(100), index=True, nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    published_year = Column(Integer, nullable=False)
    quantity_total = Column(Integer, nullable=False, default=1)
    quantity_available = Column(Integer, nullable=False, default=1)
    category = Column(String(50), index=True, nullable=False)
    description = Column(String(1000), nullable=True)

    borrows = relationship("Borrow", back_populates="book")


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(200), nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reader")
    borrows = relationship("Borrow", back_populates="reader")
    fines = relationship("Fine", back_populates="reader")


class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    borrow_date = Column(Date, default=date.today)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(SQLEnum(BorrowStatus), default=BorrowStatus.BORROWED)

    reader = relationship("Reader", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")


class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True, index=True)
    borrow_id = Column(Integer, ForeignKey("borrows.id", ondelete="CASCADE"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    paid = Column(Boolean, default=False)
    issued_date = Column(DateTime, default=datetime.utcnow)
    paid_date = Column(DateTime, nullable=True)

    reader = relationship("Reader", back_populates="fines")
    borrow = relationship("Borrow")
