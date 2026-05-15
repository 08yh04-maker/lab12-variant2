from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import User
from app.schemas import ReaderCreate, ReaderUpdate, ReaderResponse, ReaderList
from app.crud import readers as readers_crud
from app.auth import get_current_admin_user

router = APIRouter(prefix="/readers", tags=["Читатели"])


def create_reader(
    reader: ReaderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    existing_user = db.query(User).filter(User.username == reader.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import User
from app.schemas import ReaderCreate, ReaderUpdate, ReaderResponse, ReaderList
from app.crud import readers as readers_crud
from app.auth import get_current_admin_user

router = APIRouter(prefix="/readers", tags=["Читатели"])


@router.post("/", response_model=ReaderResponse, status_code=status.HTTP_201_CREATED)
def create_reader(
    reader: ReaderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    existing_user = db.query(User).filter(User.username == reader.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    existing_user = db.query(User).filter(User.email == reader.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    return readers_crud.create_reader(db, reader)


@router.get("/", response_model=ReaderList)
def get_readers(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    skip = (page - 1) * size
    readers, total = readers_crud.get_readers(
        db,
        skip=skip,
        limit=size,
        search=search
    )

    return {
        "readers": readers,
        "total": total,
        "page": page,
        "size": size
    }


@router.get("/{reader_id}", response_model=ReaderResponse)
def get_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    reader = readers_crud.get_reader(db, reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found"
        )
    return reader


@router.put("/{reader_id}", response_model=ReaderResponse)
def update_reader(
    reader_id: int,
    reader: ReaderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    updated_reader = readers_crud.update_reader(db, reader_id, reader)
    if not updated_reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found"
        )
    return updated_reader


@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    if not readers_crud.delete_reader(db, reader_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found"
        )