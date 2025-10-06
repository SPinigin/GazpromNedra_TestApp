from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.app.api.deps import get_database
from backend.app.schemas import ref as reference_schemas
from backend.app.models.ref import Org, LicenseStatus, WellStatus
from backend.app.repository.base import BaseRepository

logger = logging.getLogger(__name__)
router = APIRouter()

org_repository = BaseRepository[Org, reference_schemas.OrgCreate, reference_schemas.OrgUpdate](Org)
license_status_repository = BaseRepository[LicenseStatus, reference_schemas.LicenseStatusCreate, reference_schemas.LicenseStatusUpdate](LicenseStatus)
well_status_repository = BaseRepository[WellStatus, reference_schemas.WellStatusCreate, reference_schemas.WellStatusUpdate](WellStatus)


@router.post("/orgs/", response_model=reference_schemas.Org, status_code=201)
def create_org(
    *,
    db: Session = Depends(get_database),
    org_in: reference_schemas.OrgCreate
) -> reference_schemas.Org:
    logger.info(f"Создание предприятия: {org_in.name}")
    return org_repository.create(db, obj_in=org_in)


@router.get("/orgs/", response_model=List[reference_schemas.Org])
def get_orgs(
    db: Session = Depends(get_database),
    skip: int = 0,
    limit: int = 100
) -> List[reference_schemas.Org]:
    return org_repository.get_multi(db, skip=skip, limit=limit)


@router.get("/orgs/{org_id}", response_model=reference_schemas.Org)
def get_org(
    org_id: int,
    db: Session = Depends(get_database)
) -> reference_schemas.Org:
    org = org_repository.get(db, id=org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Предприятие не найдено")
    return org


@router.put("/orgs/{org_id}", response_model=reference_schemas.Org)
def update_org(
    *,
    org_id: int,
    db: Session = Depends(get_database),
    org_in: reference_schemas.OrgUpdate
) -> reference_schemas.Org:
    org = org_repository.get(db, id=org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Предприятие не найдено")
    return org_repository.update(db, db_obj=org, obj_in=org_in)


@router.delete("/orgs/{org_id}", status_code=204)
def delete_org(
    org_id: int,
    db: Session = Depends(get_database)
):
    org = org_repository.get(db, id=org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Предприятие не найдено")
    org_repository.remove(db, id=org_id)


@router.post("/license-statuses/", response_model=reference_schemas.LicenseStatus, status_code=201)
def create_license_status(
    *,
    db: Session = Depends(get_database),
    status_in: reference_schemas.LicenseStatusCreate
):
    return license_status_repository.create(db, obj_in=status_in)


@router.get("/license-statuses/", response_model=List[reference_schemas.LicenseStatus])
def get_license_statuses(
    db: Session = Depends(get_database),
    skip: int = 0,
    limit: int = 100
):
    return license_status_repository.get_multi(db, skip=skip, limit=limit)


@router.post("/well-statuses/", response_model=reference_schemas.WellStatus, status_code=201)
def create_well_status(
    *,
    db: Session = Depends(get_database),
    status_in: reference_schemas.WellStatusCreate
):
    return well_status_repository.create(db, obj_in=status_in)


@router.get("/well-statuses/", response_model=List[reference_schemas.WellStatus])
def get_well_statuses(
    db: Session = Depends(get_database),
    skip: int = 0,
    limit: int = 100
):
    return well_status_repository.get_multi(db, skip=skip, limit=limit)