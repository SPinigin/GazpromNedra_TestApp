import uuid
from typing import Annotated
from pydantic import BaseModel, Field


class OrgBase(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=255, description="Предприятие")]

class OrgCreate(OrgBase):
    pass

class Org(OrgBase):
    id: Annotated[uuid.UUID, Field(description="ID предприятия")]

    class Config:
        from_attributes = True

class LicenseStatusBase(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=255, description="Статус лицензии")]

class LicenseStatusCreate(LicenseStatusBase):
    pass

class LicenseStatus(LicenseStatusBase):
    id: Annotated[uuid.UUID, Field(description="ID статуса лицензии")]

    class Config:
        from_attributes = True

class WellStatusBase(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=255, description="Статус скважины")]

class WellStatusCreate(WellStatusBase):
    pass

class WellStatus(WellStatusBase):
    id: Annotated[uuid.UUID, Field(description="ID статуса скважины")]

    class Config:
        from_attributes = True
