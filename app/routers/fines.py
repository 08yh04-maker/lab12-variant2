from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User
from app.schemas import FineResponse
from app.crud import fines as fines_crud
from app.auth import get_current_admin_user, get_current_user

router = APIRouter(prefix="/fines", tags=["Штрафы"])


@router.post("/pay/{fine_id}", response_model=FineResponse)
def pay_fine(
    fine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_fine = fines_crud.pay_fine(db, fine_id)
    if db_fine is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fine not found or already paid"
        )
    return db_fine


@router.get("/reader/{reader_id}", response_model=List[FineResponse])
def get_reader_fines(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fines = fines_crud.get_reader_fines(db, reader_id)
    return fines
