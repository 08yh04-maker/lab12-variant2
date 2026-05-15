from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.models import Reader, User
from app.schemas import ReaderCreate, ReaderUpdate
from app.auth import get_password_hash


def get_reader(db: Session, reader_id: int) -> Optional[Reader]:
    return db.query(Reader).options(joinedload(Reader.user)).filter(Reader.id == reader_id).first()


def get_reader_by_user_id(db: Session, user_id: int) -> Optional[Reader]:
    return db.query(Reader).filter(Reader.user_id == user_id).first()


def get_readers(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> tuple[List[Reader], int]:
    query = db.query(Reader).options(joinedload(Reader.user))

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Reader.full_name.ilike(search_term),
                Reader.phone.ilike(search_term)
            )
        )

    total = query.count()
    readers = query.offset(skip).limit(limit).all()

    return readers, total


def create_reader(db: Session, reader: ReaderCreate) -> Reader:
    db_user = User(
        username=reader.username,
        email=reader.email,
        hashed_password=get_password_hash(reader.password),
        is_admin=False
    )
    db.add(db_user)
    db.flush()

    db_reader = Reader(
        user_id=db_user.id,
        full_name=reader.full_name,
        phone=reader.phone,
        address=reader.address
    )
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader


def update_reader(db: Session, reader_id: int, reader: ReaderUpdate) -> Optional[Reader]:
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        return None

    update_data = reader.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reader, field, value)

    db.commit()
    db.refresh(db_reader)
    return db_reader


def delete_reader(db: Session, reader_id: int) -> bool:
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        return False

    user = db.query(User).filter(User.id == db_reader.user_id).first()
    if user:
        db.delete(user)

    db.delete(db_reader)
    db.commit()
    return True
