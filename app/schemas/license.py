from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from reference import Org, LicenseStatus


class LicenseBase(BaseModel):
    license_number: str
    issue_date: date
    expire_date: date
    org_id: int
    status_id: int


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    license_number: Optional[str] = None
    issue_date: Optional[date] = None
    expire_date: Optional[date] = None
    org_id: Optional[int] = None
    status_id: Optional[int] = None


class License(LicenseBase):
    id: int
    org: Optional[Org] = None
    status: Optional[LicenseStatus] = None

    class Config:
        from_attributes = True


class LicenseWithWells(License):
    wells: List["Well"] = []


from app.schemas.well import Well

LicenseWithWells.model_rebuild()