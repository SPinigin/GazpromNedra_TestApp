import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import Org, LicenseStatus, WellStatus


def create_initial_data():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        orgs_data = [
            {"name": "ОАО Газпром"},
            {"name": "ОАО Роснефть"},
            {"name": "ПАО ЛУКОЙЛ"},
            {"name": "ОАО Сургутнефтегаз"},
            {"name": "ОАО Башнефть"}
        ]

        for org_data in orgs_data:
            existing = db.query(Org).filter(Org.name == org_data["name"]).first()
            if not existing:
                org = Org(**org_data)
                db.add(org)

        license_statuses_data = [
            {"name": "действующая"},
            {"name": "переоформленная"},
            {"name": "архивная"}
        ]

        for status_data in license_statuses_data:
            existing = db.query(LicenseStatus).filter(LicenseStatus.name == status_data["name"]).first()
            if not existing:
                status = LicenseStatus(**status_data)
                db.add(status)

        well_statuses_data = [
            {"name": "в бурении"},
            {"name": "в эксплуатации"},
            {"name": "в консервации"},
            {"name": "ликвидирована"},
            {"name": "в испытании"}
        ]

        for status_data in well_statuses_data:
            existing = db.query(WellStatus).filter(WellStatus.name == status_data["name"]).first()
            if not existing:
                status = WellStatus(**status_data)
                db.add(status)

        db.commit()
        print("Initial data успешно создана!")
        print("Orgs: 5")
        print("License statuses: 3 (действующая, переоформленная, архивная)")
        print("Well statuses: 5")

    except Exception as e:
        db.rollback()
        print(f"Ошибка при создании initial data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_data()
