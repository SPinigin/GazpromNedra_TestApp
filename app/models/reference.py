from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Org(Base):
    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)


class LicenseStatus(Base):
    __tablename__ = "license_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)


class WellStatus(Base):
    __tablename__ = "well_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)