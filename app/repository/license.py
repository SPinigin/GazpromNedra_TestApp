from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.license import License
from app.schemas.license import LicenseCreate, LicenseUpdate
from typing import Optional


class LicenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None, order: str = "asc"):
        query = self.db.query(License)

        # Применяем сортировку
        if sort_by:
            if hasattr(License, sort_by):
                column = getattr(License, sort_by)
                if order == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, license_id: int):
        license_obj = self.db.query(License).filter(License.id == license_id).first()
        if license_obj:
            from app.models.well import Well
            wells = self.db.query(Well).filter(Well.license_id == license_id).all()
            setattr(license_obj, 'wells', wells)
        return license_obj

    def get_by_number(self, license_number: str):
        return self.db.query(License).filter(License.license_number == license_number).first()

    def get_by_status(self, status_id: int, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None,
                      order: str = "asc"):
        query = self.db.query(License).filter(License.status_id == status_id)

        if sort_by:
            if hasattr(License, sort_by):
                column = getattr(License, sort_by)
                if order == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))

        return query.offset(skip).limit(limit).all()

    def create(self, license: LicenseCreate):
        db_license = License(**license.model_dump())
        self.db.add(db_license)
        self.db.commit()
        self.db.refresh(db_license)
        return db_license

    def update(self, license_id: int, license_update: LicenseUpdate):
        db_license = self.db.query(License).filter(License.id == license_id).first()
        if db_license:
            update_data = license_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_license, field, value)
            self.db.commit()
            self.db.refresh(db_license)
            return db_license
        return None

    def delete(self, license_id: int):
        db_license = self.db.query(License).filter(License.id == license_id).first()
        if db_license:
            self.db.delete(db_license)
            self.db.commit()
            return True
        return False
