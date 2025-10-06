from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import math
import logging
import io

from backend.app.api.deps import get_database, get_pagination_params
from backend.app.schemas import well as well_schemas
from backend.app.repository.well import well_repository
from backend.app.repository.license import license_repository
from backend.app.services.export import export_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=well_schemas.Well, status_code=201)
def create_well(
        *,
        db: Session = Depends(get_database),
        well_in: well_schemas.WellCreate
) -> well_schemas.Well:

    logger.info(f"Создание скважины: {well_in.name}")

    license_obj = license_repository.get(db, id=well_in.license_id)
    if not license_obj:
        logger.warning(f"Лицензия с ID: {well_in.license_id} не найдена")
        raise HTTPException(status_code=404, detail="Лицензия не найдена")

    well_obj = well_repository.create(db, obj_in=well_in)
    logger.info(f"Скважина с ID: {well_obj.id} успешно создана")
    return well_obj


@router.get("/", response_model=well_schemas.WellListResponse)
def get_wells(
        db: Session = Depends(get_database),
        pagination: dict = Depends(get_pagination_params),
        license_id: Optional[int] = Query(None, description="Фильтр по лицензии"),
        order_by: Optional[str] = Query("id", description="Поле для сортировки"),
        order_desc: bool = Query(False, description="Сортировка по убыванию")
) -> well_schemas.WellListResponse:

    logger.info(f"Скважины: {pagination}, ID лицензии: {license_id}")

    if license_id:
        wells = well_repository.get_by_license(db, license_id=license_id, **pagination)
        total = well_repository.count_by_license(db, license_id=license_id)
    else:
        wells = well_repository.get_multi(
            db, order_by=order_by, order_desc=order_desc, **pagination
        )
        total = well_repository.count(db)

    pages = math.ceil(total / pagination["size"])

    return well_schemas.WellListResponse(
        items=wells,
        total=total,
        page=pagination["page"],
        size=pagination["size"],
        pages=pages
    )


@router.get("/{well_id}", response_model=well_schemas.Well)
def get_well(
        well_id: int,
        db: Session = Depends(get_database)
) -> well_schemas.Well:
    logger.info(f"Скважина с ID: {well_id}")

    well_obj = well_repository.get(db, id=well_id)
    if not well_obj:
        logger.warning(f"Скважина с ID: {well_id} не найдена")
        raise HTTPException(status_code=404, detail="Скважина не найдена")

    return well_obj


@router.put("/{well_id}", response_model=well_schemas.Well)
def update_well(
        *,
        well_id: int,
        db: Session = Depends(get_database),
        well_in: well_schemas.WellUpdate
) -> well_schemas.Well:
    logger.info(f"Обновление скважины с ID: {well_id}")

    well_obj = well_repository.get(db, id=well_id)
    if not well_obj:
        raise HTTPException(status_code=404, detail="Скважина не найдена")

    if well_in.license_id and well_in.license_id != well_obj.license_id:
        license_obj = license_repository.get(db, id=well_in.license_id)
        if not license_obj:
            raise HTTPException(status_code=404, detail="Лицензия не найдена")

    well_obj = well_repository.update(db, db_obj=well_obj, obj_in=well_in)
    logger.info(f"Скважина с ID: {well_id} успешно обновлена")
    return well_obj


@router.delete("/{well_id}", status_code=204)
def delete_well(
        well_id: int,
        db: Session = Depends(get_database)
):
    logger.info(f"Удаление скважины с ID: {well_id}")

    well_obj = well_repository.get(db, id=well_id)
    if not well_obj:
        raise HTTPException(status_code=404, detail="Скважина не найдена")

    well_repository.remove(db, id=well_id)
    logger.info(f"Скважина с ID: {well_id} успешна удалена")
    return Response(status_code=204)


@router.get("/license/{license_id}/wells", response_model=well_schemas.WellListResponse)
def get_wells_by_license(
        license_id: int,
        db: Session = Depends(get_database),
        pagination: dict = Depends(get_pagination_params)
) -> well_schemas.WellListResponse:
    logger.info(f"Скважины лицензии с ID: {license_id}")

    license_obj = license_repository.get(db, id=license_id)
    if not license_obj:
        raise HTTPException(status_code=404, detail="Лицензия не найдена")

    wells = well_repository.get_by_license(db, license_id=license_id, **pagination)
    total = well_repository.count_by_license(db, license_id=license_id)
    pages = math.ceil(total / pagination["size"])

    return well_schemas.WellListResponse(
        items=wells,
        total=total,
        page=pagination["page"],
        size=pagination["size"],
        pages=pages
    )


@router.get("/export/excel", response_class=StreamingResponse)
def export_wells_excel(
        db: Session = Depends(get_database),
        license_id: Optional[int] = Query(None)
):
    logger.info("Экспорт скважин в Excel")

    if license_id:
        wells = well_repository.get_by_license(db, license_id=license_id, skip=0, limit=10000)
    else:
        wells = well_repository.get_multi(db, skip=0, limit=10000)

    excel_data = export_service.export_wells_to_excel(wells)

    return StreamingResponse(
        io.BytesIO(excel_data.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=wells.xlsx"}
    )


@router.get("/export/csv", response_class=Response)
def export_wells_csv(
        db: Session = Depends(get_database),
        license_id: Optional[int] = Query(None)
):
    logger.info("Экспорт скважин в CSV")

    if license_id:
        wells = well_repository.get_by_license(db, license_id=license_id, skip=0, limit=10000)
    else:
        wells = well_repository.get_multi(db, skip=0, limit=10000)

    csv_data = export_service.export_wells_to_csv(wells)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=wells.csv"}
    )