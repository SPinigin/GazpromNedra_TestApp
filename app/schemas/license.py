from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import date
import re
from reference import Org, LicenseStatus
from well import Well


class LicenseBase(BaseModel):
    number: str
    issue_date: date
    expire_date: date
    org_id: int
    staus_id: int

    @validator('number')
    def validate_license_number(cls, v):
        pattern = r'^[A-Z]{2} \d{5} [A-Z]{2}$'
        if not re.match(pattern, v):
            raise ValueError('Номер лицензии должен быть в формате XX 00000 YY')
        return v
    
    @validator('expire_date')
    def validate_expire_date(cls, v, values):
        if 'issue_date' in values and v<= values['issue_date']:
            raise ValueError('Дата окончания лицензии должна быть позже даты выдачи')
        return v

class LicenseCreate(LicenseBase):
    pass

class LicenseUpdate(BaseModel):
    number: Optional[str] = None
    issue_date: Optional[date] = None
    expire_date: Optional[date] = None
    org_id: Optional[int] = None
    staus_id: Optional[int] = None

    @validator('number')
    def validate_license_number(cls, v):
        if v is not None:
            pattern = r'^[A-Z]{2} \d{5} [A-Z]{2}$'
            if not re.match(pattern, v):
                raise ValueError ('Номер лицензии должен быть в формате XX 00000 YY')
            return v

class License(LicenseBase):
    id: int
    org: Org
    status: LicenseStatus
    wells: Optional[List[Well]]

    class Config:
        orm_mode = True

class LicenseListResponse(BaseModel):
    items: List[License]
    total: int
    page: int
    size: int
    pages: int