from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.reference import Org, OrgCreate, LicenseStatus, LicenseStatusCreate, WellStatus, WellStatusCreate
from app.repository.reference import OrgRepository, LicenseStatusRepository, WellStatusRepository
from app.api.deps import get_org_repository, get_license_status_repository, get_well_status_repository

router = APIRouter(prefix="/references", tags=["references"])

@router.get("/orgs", response_model=List[Org])
def get_orgs(repo: OrgRepository = Depends(get_org_repository)):
    return repo.get_all()

@router.post("/orgs", response_model=Org)
def create_org(org: OrgCreate, repo: OrgRepository = Depends(get_org_repository)):
    return repo.create(org)

@router.get("/license-statuses", response_model=List[LicenseStatus])
def get_license_statuses(repo: LicenseStatusRepository = Depends(get_license_status_repository)):
    return repo.get_all()

@router.post("/license-statuses", response_model=LicenseStatus)
def create_license_status(status: LicenseStatusCreate, repo: LicenseStatusRepository = Depends(get_license_status_repository)):
    return repo.create(status)

@router.get("/well-statuses", response_model=List[WellStatus])
def get_well_statuses(repo: WellStatusRepository = Depends(get_well_status_repository)):
    return repo.get_all()

@router.post("/well-statuses", response_model=WellStatus)
def create_well_status(status: WellStatusCreate, repo: WellStatusRepository = Depends(get_well_status_repository)):
    return repo.create(status)
