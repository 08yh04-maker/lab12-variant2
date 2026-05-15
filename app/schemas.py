from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# ===== Auth Schemas =====
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ===== Book Schemas =====
class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    isbn: str = Field(min_length=10, max_length=20)
    published_year: int = Field(ge=1000, le=datetime.now().year)
    quantity_total: int = Field(ge=1)
    category: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=1000)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    published_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    quantity_total: Optional[int] = Field(None, ge=1)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=1000)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    published_year: int
    quantity_total: int
    quantity_available: int
    category: str
    description: Optional[str]

    class Config:
        from_attributes = True


class BookList(BaseModel):
    books: List[BookResponse]
    total: int
    page: int
    size: int


# ===== Reader Schemas =====
class ReaderCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=5, max_length=20)
    address: Optional[str] = Field(None, max_length=200)


class ReaderUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=5, max_length=20)
    address: Optional[str] = Field(None, max_length=200)


class ReaderResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone: str
    address: Optional[str]
    registered_at: datetime
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True


class ReaderList(BaseModel):
    readers: List[ReaderResponse]
    total: int
    page: int
    size: int


# ===== Borrow Schemas =====
class BorrowCreate(BaseModel):
    reader_id: int
    book_id: int


class BorrowResponse(BaseModel):
    id: int
    reader_id: int
    book_id: int
    borrow_date: date
    due_date: date
    return_date: Optional[date]
    status: str
    book: Optional[BookResponse] = None
    reader: Optional[ReaderResponse] = None

    class Config:
        from_attributes = True


# ===== Fine Schemas =====
class FineResponse(BaseModel):
    id: int
    borrow_id: int
    reader_id: int
    amount: float
    paid: bool
    issued_date: datetime
    paid_date: Optional[datetime]

    class Config:
        from_attributes = True


class FineList(BaseModel):
    fines: List[FineResponse]
    total: int


# ===== Report Schemas =====
class PopularBook(BaseModel):
    book_id: int
    title: str
    author: str
    borrow_count: int


class Debtor(BaseModel):
    reader_id: int
    full_name: str
    phone: str
    total_unpaid_fines: float


class OverdueBook(BaseModel):
    borrow_id: int
    reader_id: int
    reader_name: str
    book_id: int
    book_title: str
    due_date: date
    days_overdue: int


class AdminStats(BaseModel):
    total_books: int
    total_readers: int
    active_borrows: int
    total_unpaid_fines: float
    total_books_available: int
