from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import date
from ref import WellStatus


class WellBase(BaseModel):
    name: str
    depth: float
    drill_date: date
    license_id: int
    status_id: int

    @validator('depth')
    def validate_depth(cls, v):
        if v <= 0:
            raise ValueError('Глубина скважины должна быть больше 0')
        return v

class WellCreate(WellBase):
    pass

class WellUpdate(BaseModel):
    name: Optional[str] = None
    depth: Optional[float] = None
    drill_date: Optional[date] = None
    license_id: Optional[int] = None
    status_id: Optional[int] = None

    @validator('depth')
    def validate_depth(cls, v):
        if v is not None and v <= 0:
            raise ValueError ('Глубина скважины должна быть больше 0')
        return v

class Well(WellBase):
    id: int
    status: WellStatus

    class Config:
        orm_mode = True

class WellListResponse(BaseModel):
    items: List[Well]
    total: int
    page: int
    size: int
    pages: int