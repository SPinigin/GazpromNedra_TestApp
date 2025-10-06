from sqlalchemy import Column, Integer, String
from backend.app.core.database import Base


class Org(Base):
    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    inn = Column(String, nullable=False, unique=True)
    description = Column(String)

class LicenseStatus(Base):
    __tablename__ = "license_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

class WellStatus(Base):
    __tablename__ = "well_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)