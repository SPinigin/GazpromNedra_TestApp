from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc
from app.models.well import Well
from app.schemas.well import WellCreate, WellUpdate
from typing import Optional


class WellRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None, order: str = "asc"):
        query = (self.db.query(Well)
                 .options(joinedload(Well.status)))

        if sort_by:
            if hasattr(Well, sort_by):
                column = getattr(Well, sort_by)
                if order == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, well_id: int):
        return (self.db.query(Well)
                .options(joinedload(Well.status))
                .filter(Well.id == well_id).first())

    def get_by_license_id(self, license_id: int, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None,
                          order: str = "asc"):
        query = (self.db.query(Well)
                 .options(joinedload(Well.status))
                 .filter(Well.license_id == license_id))

        if sort_by:
            if hasattr(Well, sort_by):
                column = getattr(Well, sort_by)
                if order == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))

        return query.offset(skip).limit(limit).all()

    def create(self, well: WellCreate):
        db_well = Well(**well.dict())
        self.db.add(db_well)
        self.db.commit()
        self.db.refresh(db_well)
        return self.get_by_id(db_well.id)

    def update(self, well_id: int, well_update: WellUpdate):
        db_well = self.db.query(Well).filter(Well.id == well_id).first()
        if db_well:
            update_data = well_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_well, field, value)
            self.db.commit()
            self.db.refresh(db_well)
            return self.get_by_id(db_well.id)
        return None

    def delete(self, well_id: int):
        db_well = self.db.query(Well).filter(Well.id == well_id).first()
        if db_well:
            self.db.delete(db_well)
            self.db.commit()
            return True
        return False
