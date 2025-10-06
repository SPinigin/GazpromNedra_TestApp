from pydantic import BaseModel
from typing import Optional


class OrgBase(BaseModel):
    name: str
    inn: str
    description: Optional[str] = None

class OrgCreate(OrgBase):
    pass

class OrgUpdate(OrgBase):
    name: Optional[str] = None
    inn: Optional[str] = None
    description: Optional[str] = None

class Org(OrgBase):
    id: int

    class Config:
        orm_mode = True

class LicenseStatusBase(BaseModel):
    name: str
    description: Optional[str] = None

class LicenseStatusCreate(LicenseStatusBase):
    pass

class LicenseStatusUpdate(LicenseStatusBase):
    name: Optional[str] = None
    description: Optional[str] = None

class LicenseStatus(LicenseStatusBase):
    id: int

    class Config:
        orm_mode = True

class WellStatusBase(BaseModel):
    name: str
    description: Optional[str] = None

class WellStatusCreate(WellStatusBase):
    pass

class WellStatusUpdate(WellStatusBase):
    name: Optional[str] = None
    description: Optional[str] = None

class WellStatus(WellStatusBase):
    id: int

    class Config:
        orm_mode = True