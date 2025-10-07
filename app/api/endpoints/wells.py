from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List, Optional, Literal
from app.schemas.well import Well, WellCreate, WellUpdate
from app.repository.well import WellRepository
from app.api.deps import get_well_repository
import pandas as pd
import io

router = APIRouter(prefix="/wells", tags=["wells"])


@router.get("/", response_model=List[Well])
def get_wells(
        skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
        limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
        sort_by: Optional[Literal["id", "name", "depth", "drill_date"]] = Query(None,
                                                                                   description="Поле для сортировки"),
        order: Optional[Literal["asc", "desc"]] = Query("asc", description="Порядок сортировки"),
        repo: WellRepository = Depends(get_well_repository)
):
    return repo.get_all(skip, limit, sort_by, order)


@router.get("/by-license/{license_id}", response_model=List[Well])
def get_wells_by_license(
        license_id: int,
        skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
        limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
        sort_by: Optional[Literal["id", "name", "depth", "drill_date"]] = Query(None,
                                                                                   description="Поле для сортировки"),
        order: Optional[Literal["asc", "desc"]] = Query("asc", description="Порядок сортировки"),
        repo: WellRepository = Depends(get_well_repository)
):
    return repo.get_by_license_id(license_id, skip, limit, sort_by, order)


@router.get("/{well_id}", response_model=Well)
def get_well(well_id: int, repo: WellRepository = Depends(get_well_repository)):
    well = repo.get_by_id(well_id)
    if not well:
        raise HTTPException(status_code=404, detail="Скважина не найдена")
    return well


@router.post("/", response_model=Well)
def create_well(well: WellCreate, repo: WellRepository = Depends(get_well_repository)):
    return repo.create(well)


@router.put("/{well_id}", response_model=Well)
def update_well(well_id: int, well_update: WellUpdate, repo: WellRepository = Depends(get_well_repository)):
    well = repo.update(well_id, well_update)
    if not well:
        raise HTTPException(status_code=404, detail="Скважина не найдена")
    return well


@router.delete("/{well_id}")
def delete_well(well_id: int, repo: WellRepository = Depends(get_well_repository)):
    if not repo.delete(well_id):
        raise HTTPException(status_code=404, detail="Скважина не найдена")
    return {"message": "Скважина успешно удалена"}


@router.get("/export/csv")
def export_wells_csv(repo: WellRepository = Depends(get_well_repository)):
    wells = repo.get_all(skip=0, limit=10000)

    data = []
    for well in wells:
        data.append({
            'id': well.id,
            'name': well.name,
            'depth': well.depth,
            'drill_date': well.drill_date,
            'license_id': well.license_id,
            'status': well.status.name if well.status else ''
        })

    df = pd.DataFrame(data)

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(
        io.BytesIO(stream.getvalue().encode('utf-8')),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=wells.csv"
    return response
