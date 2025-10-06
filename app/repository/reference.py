from sqlalchemy.orm import Session
from app.models.reference import Org, LicenseStatus, WellStatus
from app.schemas.reference import OrgCreate, LicenseStatusCreate, WellStatusCreate


class OrgRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Org).all()

    def get_by_id(self, org_id: int):
        return self.db.query(Org).filter(Org.id == org_id).first()

    def create(self, org: OrgCreate):
        db_org = Org(**org.dict())
        self.db.add(db_org)
        self.db.commit()
        self.db.refresh(db_org)
        return db_org


class LicenseStatusRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(LicenseStatus).all()

    def get_by_id(self, status_id: int):
        return self.db.query(LicenseStatus).filter(LicenseStatus.id == status_id).first()

    def create(self, status: LicenseStatusCreate):
        db_status = LicenseStatus(**status.dict())
        self.db.add(db_status)
        self.db.commit()
        self.db.refresh(db_status)
        return db_status


class WellStatusRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(WellStatus).all()

    def get_by_id(self, status_id: int):
        return self.db.query(WellStatus).filter(WellStatus.id == status_id).first()

    def create(self, status: WellStatusCreate):
        db_status = WellStatus(**status.dict())
        self.db.add(db_status)
        self.db.commit()
        self.db.refresh(db_status)
        return db_status