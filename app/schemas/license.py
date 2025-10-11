import uuid
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional, Any, Annotated
from .reference import Org, LicenseStatus

class LicenseBase(BaseModel):
    license_number: Annotated[str, Field(
        min_length=11,
        max_length=11,
        pattern=r'^[A-ZА-Я]{2}\s\d{5}\s[A-ZА-Я]{2}$',
        description="Номер лицензии в формате ХХ 00000 УУ"
        )]
    issue_date: Annotated[date, Field(description="Дата выдачи лицензии")]
    expire_date: Annotated[date, Field(description="Дата окончания лицензии")]
    org_id: Annotated[uuid.UUID, Field(description="ID предприятия")]
    status_id: Annotated[uuid.UUID, Field(description="ID статуса лицензии")]

class LicenseCreate(LicenseBase):
    pass

class LicenseUpdate(BaseModel):
    license_number: Annotated[str, Field(
        min_length=11,
        max_length=11,
        pattern=r'^[A-ZА-Я]{2}\s\d{5}\s[A-ZА-Я]{2}$',
        description="Номер лицензии в формате ХХ 00000 УУ"
    )]
    issue_date: Annotated[Optional[date], Field(None, description="Дата выдачи лицензии")]
    expire_date: Annotated[Optional[date], Field(None, description="Дата окончания лицензии")]
    org_id: Annotated[Optional[uuid.UUID], Field(None, description="ID предприятия")]
    status_id: Annotated[Optional[uuid.UUID], Field(None, description="ID статуса лицензии")]

class License(LicenseBase):
    id: Annotated[uuid.UUID, Field(description="ID лицензии")]
    org: Optional[Org] = None
    status: Optional[LicenseStatus] = None

    class Config:
        from_attributes = True

class LicenseWithWells(License):
    wells: Annotated[List[Any], Field(default=[], description="Список скважин лицензии")] = []
