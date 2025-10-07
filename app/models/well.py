from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Well(Base):
    __tablename__ = "wells"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    depth = Column(Float, nullable=False)
    drill_date = Column(Date, nullable=False)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("well_statuses.id"), nullable=False)

    status = relationship("WellStatus")
