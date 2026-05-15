from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Fine


def get_fine(db: Session, fine_id: int) -> Optional[Fine]:
    return db.query(Fine).filter(Fine.id == fine_id).first()


def get_reader_fines(db: Session, reader_id: int) -> List[Fine]:
    return db.query(Fine).filter(Fine.reader_id == reader_id).all()


def pay_fine(db: Session, fine_id: int) -> Optional[Fine]:
    db_fine = get_fine(db, fine_id)
    if not db_fine or db_fine.paid:
        return None

    db_fine.paid = True
    db_fine.paid_date = datetime.utcnow()
    db.commit()
    db.refresh(db_fine)
    return db_fine
