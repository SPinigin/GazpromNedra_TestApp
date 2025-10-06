from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List, Optional, Literal
from app.schemas.license import License, LicenseCreate, LicenseUpdate, LicenseWithWells
from app.repository.license import LicenseRepository
from app.api.deps import get_license_repository
import pandas as pd
import io

router = APIRouter(prefix="/licenses", tags=["licenses"])


@router.get("/", response_model=List[License])
def get_licenses(
        skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
        limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
        status_id: Optional[int] = Query(None, description="Фильтр по статусу"),
        sort_by: Optional[Literal["id", "license_number", "issue_date", "expiry_date"]] = Query(None,
                                                                                                description="Поле для сортировки"),
        order: Optional[Literal["asc", "desc"]] = Query("asc", description="Порядок сортировки"),
        repo: LicenseRepository = Depends(get_license_repository)
):
    if status_id:
        return repo.get_by_status(status_id, skip, limit, sort_by, order)
    return repo.get_all(skip, limit, sort_by, order)


@router.get("/search")
def search_licenses(
        license_number: Optional[str] = Query(None, description="Номер лицензии"),
        status_id: Optional[int] = Query(None, description="ID статуса"),
        skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
        limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
        sort_by: Optional[Literal["id", "license_number", "issue_date", "expiry_date"]] = Query(None,
                                                                                                description="Поле для сортировки"),
        order: Optional[Literal["asc", "desc"]] = Query("asc", description="Порядок сортировки"),
        repo: LicenseRepository = Depends(get_license_repository)
):
    if license_number:
        license_obj = repo.get_by_number(license_number)
        if not license_obj:
            raise HTTPException(status_code=404, detail="License not found")
        return license_obj
    elif status_id:
        return repo.get_by_status(status_id, skip, limit, sort_by, order)
    else:
        return repo.get_all(skip, limit, sort_by, order)


@router.get("/{license_id}", response_model=LicenseWithWells)
def get_license(license_id: int, repo: LicenseRepository = Depends(get_license_repository)):
    license_obj = repo.get_by_id(license_id)
    if not license_obj:
        raise HTTPException(status_code=404, detail="License not found")
    return license_obj


@router.post("/", response_model=License)
def create_license(license: LicenseCreate, repo: LicenseRepository = Depends(get_license_repository)):
    return repo.create(license)


@router.put("/{license_id}", response_model=License)
def update_license(
        license_id: int,
        license_update: LicenseUpdate,
        repo: LicenseRepository = Depends(get_license_repository)
):
    license_obj = repo.update(license_id, license_update)
    if not license_obj:
        raise HTTPException(status_code=404, detail="License not found")
    return license_obj


@router.delete("/{license_id}")
def delete_license(license_id: int, repo: LicenseRepository = Depends(get_license_repository)):
    if not repo.delete(license_id):
        raise HTTPException(status_code=404, detail="License not found")
    return {"message": "License deleted successfully"}


@router.get("/export/csv")
def export_licenses_csv(repo: LicenseRepository = Depends(get_license_repository)):
    licenses = repo.get_all(skip=0, limit=10000)

    data = []
    for license_obj in licenses:
        data.append({
            'id': license_obj.id,
            'license_number': license_obj.license_number,
            'issue_date': license_obj.issue_date,
            'expire_date': license_obj.expiry_date,
            'org': license_obj.org.name if license_obj.org else '',
            'status': license_obj.status.name if license_obj.status else ''
        })

    df = pd.DataFrame(data)

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(
        io.BytesIO(stream.getvalue().encode('utf-8')),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=licenses.csv"
    return response


@router.get("/export/xlsx")
def export_licenses_xlsx(repo: LicenseRepository = Depends(get_license_repository)):
    licenses = repo.get_all(skip=0, limit=10000)

    data = []
    for license_obj in licenses:
        data.append({
            'ID': license_obj.id,
            'License Number': license_obj.license_number,
            'Issue Date': license_obj.issue_date,
            'Expire Date': license_obj.expiry_date,
            'Org': license_obj.org.name if license_obj.org else '',
            'Status': license_obj.status.name if license_obj.status else ''
        })

    df = pd.DataFrame(data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Licenses', index=False)
    output.seek(0)

    response = StreamingResponse(
        io.BytesIO(output.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response.headers["Content-Disposition"] = "attachment; filename=licenses.xlsx"
    return response