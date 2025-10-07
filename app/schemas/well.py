from pydantic import BaseModel
from datetime import date
from typing import Optional
from .reference import WellStatus


class WellBase(BaseModel):
    name: str
    depth: float
    drill_date: date
    license_id: int
    status_id: int

class WellCreate(WellBase):
    pass


class WellUpdate(BaseModel):
    name: Optional[str] = None
    depth: Optional[float] = None
    drill_date: Optional[date] = None
    license_id: Optional[int] = None
    status_id: Optional[int] = None


class Well(WellBase):
    id: int
    status: Optional[WellStatus] = None

    class Config:
        from_attributes = True
