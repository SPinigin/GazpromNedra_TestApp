from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.api.deps import get_database
from app.schemas import license as license_schemas
from app.repository.license import license_repo

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=license_schemas.License, status_code=201)
def create_license(
        *,
        db: Session = Depends(get_database),
        license_in: license_schemas.LicenseCreate
) -> license_schemas.License:
    logger.info(f"Создание лицензии с номером: {license_in.number}")

    existing_license = license_repo.get_license_by_number(db, number=license_in.number)
    if existing_license:
        logger.warning(f"Лицензия с номером {license_in.number} уже существует")
        raise HTTPException(
            status_code=400,
            detail="Лицензия с таким номером уже существует"
        )

    license_obj = license_repo.create_license(db, obj_in = license_in)
    logger.info(f"Лицензия успешно добавлена в базу")
    return license_obj