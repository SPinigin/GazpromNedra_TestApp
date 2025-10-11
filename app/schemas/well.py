import uuid
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Annotated
from .reference import WellStatus

class WellBase(BaseModel):
    name: Annotated[str, Field(
        min_length=1,
        max_length=10,
        description="Скважина"
    )]
    depth: Annotated[float, Field(
        gt=0,
        le=15000,
        description="Глубина скважины в метрах"
    )]
    drill_date: Annotated[date, Field(description="Дата бурения скважины")]
    license_id: Annotated[uuid.UUID, Field(description="ID лицензии")]
    status_id: Annotated[uuid.UUID, Field(description="ID статуса скважины")]

class WellCreate(WellBase):
    pass

class WellUpdate(BaseModel):
    name: Annotated[str, Field(
        None,
        min_length=1,
        max_length=10,
        description="Скважина"
    )]
    depth: Annotated[Optional[float], Field(
        None,
        gt=0,
        le=15000,
        description="Глубина скважины в метрах"
    )]
    drill_date: Annotated[Optional[date], Field(None, description="Дата бурения скважины")]
    license_id: Annotated[Optional[uuid.UUID], Field(None, description="ID лицензии")]
    status_id: Annotated[Optional[uuid.UUID], Field(None, description="ID статуса скважины")]


class Well(WellBase):
    id: Annotated[uuid.UUID, Field(description="ID скважины")]
    status: Optional[WellStatus] = None

    class Config:
        from_attributes = True
