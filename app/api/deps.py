from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repository.license import LicenseRepository
from app.repository.well import WellRepository
from app.repository.reference import OrgRepository, LicenseStatusRepository, WellStatusRepository

def get_license_repository(db: Session = Depends(get_db)) -> LicenseRepository:
    return LicenseRepository(db)

def get_well_repository(db: Session = Depends(get_db)) -> WellRepository:
    return WellRepository(db)

def get_org_repository(db: Session = Depends(get_db)) -> OrgRepository:
    return OrgRepository(db)

def get_license_status_repository(db: Session = Depends(get_db)) -> LicenseStatusRepository:
    return LicenseStatusRepository(db)

def get_well_status_repository(db: Session = Depends(get_db)) -> WellStatusRepository:
    return WellStatusRepository(db)
