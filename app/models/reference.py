import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Org(Base):
    __tablename__ = "orgs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)


class LicenseStatus(Base):
    __tablename__ = "license_statuses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)


class WellStatus(Base):
    __tablename__ = "well_statuses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
