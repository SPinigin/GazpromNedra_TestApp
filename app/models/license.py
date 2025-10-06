from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    license_number = Column(String, unique=True, nullable=False, index=True)
    issue_date = Column(Date, nullable=False)
    expire_date = Column(Date, nullable=False)
    org_id = Column(Integer, ForeignKey("orgs.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("license_statuses.id"), nullable=False)

    org = relationship("Org", back_populates="licenses")
    status = relationship("LicenseStatus")
    wells = relationship("Well", back_populates="license")


from app.models.reference import Org

Org.licenses = relationship("License", back_populates="org")