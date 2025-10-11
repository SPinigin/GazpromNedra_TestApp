import uuid
from datetime import date
from sqlalchemy import String, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Well(Base):
    __tablename__ = "wells"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    depth: Mapped[float] = mapped_column(Float, nullable=False)
    drill_date: Mapped[date] = mapped_column(Date, nullable=False)
    license_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("licenses.id"), nullable=False)
    status_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("well_statuses.id"), nullable=False)

    status: Mapped["WellStatus"] = relationship()
