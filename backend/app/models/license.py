from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False, unique=True, index=True)
    issue_date = Column(Date, nullable=False)
    expire_date = Column(Date, nullable=False)

    org_id = Column(Integer, ForeignKey("orgs.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("license_statuses.id"), nullable=False)

    org = relationship("Org", lazy="joined")
    status = relationship("LicenseStatus", lazy="joined")
    wells = relationship("Well", back_populates="licenses", cascade="all, delete-orphan")