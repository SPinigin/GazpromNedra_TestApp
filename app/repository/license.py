from typing import List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.license import License
from app.schemas.license import LicenseCreate, LicenseUpdate
from base import BaseRepository


class LicenseRepository(BaseRepository[License, LicenseCreate, LicenseUpdate]):
    
    def get_by_number(self, db:Session, *, number: str) -> Optional[License]:
        return db.query(License).filter(License.number == number).first()
    
    def search_by_number_or_status(
            self,
            db:Session,
            *,
            search_term: str,
            skip: int = 0,
            limit: int = 100
            # check that
    ) -> list[type[License]]:
        return (
            db.query(License)
            .join(License.status)
            .filter(
                or_(
                    License.number.ilike(f"%{search_term}%"),
                    License.status.has(name=search_term)
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
license_repo = LicenseRepository(License)