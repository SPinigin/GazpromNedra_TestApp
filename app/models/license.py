import uuid
from datetime import date
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import LicenseStatus


class License(Base):
    __tablename__ = "licenses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    license_number: Mapped[str] = mapped_column(String(11), unique=True, nullable=False, index=True)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    expire_date: Mapped[date] = mapped_column(Date, nullable=False)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orgs.id"), nullable=False)
    status_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("license_statuses.id"), nullable=False)

    org: Mapped["Org"] = relationship()
    status: Mapped["LicenseStatus"] = relationship()
