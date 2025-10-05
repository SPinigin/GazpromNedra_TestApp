from typing import List
from sqlalchemy.orm import Session
from app.models.well import Well
from app.schemas.well import WellCreate, WellUpdate
from base import BaseRepository

class WellRepository(BaseRepository[Well, WellCreate, WellUpdate]):

    def get_by_license(
            self,
            db: Session,
            *,
            license_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[Well]:
        return(
            db.query(Well)
            .filter(Well.license_id == license_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_license(self, db: Session, *, license_id: int) -> int:
        return db.query(Well).filter(Well.license_id == license_id).count()

well_repo = WellRepository(Well)