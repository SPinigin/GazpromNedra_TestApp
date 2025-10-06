from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc
from app.models.license import License
from app.schemas.license import LicenseCreate, LicenseUpdate
from typing import Optional


class LicenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None, order: str = "asc"):
        query = (self.db.query(License)
                 .options(joinedload(License.company), joinedload(License.status)))

        if sort_by:
            if hasattr(License, sort_by):
                column = getattr(License, sort_by)
                if order == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, license_id: int):
        return (self.db.query(License)
                .options(joinedload(License.company),
                         joinedload(License.status),
                         joinedload(License.wells).joinedload("status"))
                .filter(License.id == license_id).first())

    def get_by_number(self, license_number: str):
        return (self.db.query(License)
                .options(joinedload(License.company), joinedload(License.status))
                .filter(License.license_number == license_number).first())

    def get_by_status(self, status_id: int, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None,
                      order: str = "asc"):
        query = (self.db.query(License)
                 .options(joinedload(License.company), joinedload(License.status))
                 .filter(License.status_id == status_id))

        if sort_by:
            if hasattr(License, sort_by):
                column = getattr(License, sort_by)
                if order == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))

        return query.offset(skip).limit(limit).all()

    def create(self, license: LicenseCreate):
        db_license = License(**license.dict())
        self.db.add(db_license)
        self.db.commit()
        self.db.refresh(db_license)
        return self.get_by_id(db_license.id)

    def update(self, license_id: int, license_update: LicenseUpdate):
        db_license = self.db.query(License).filter(License.id == license_id).first()
        if db_license:
            update_data = license_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_license, field, value)
            self.db.commit()
            self.db.refresh(db_license)
            return self.get_by_id(db_license.id)
        return None

    def delete(self, license_id: int):
        db_license = self.db.query(License).filter(License.id == license_id).first()
        if db_license:
            self.db.delete(db_license)
            self.db.commit()
            return True
        return False