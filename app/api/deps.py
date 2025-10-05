from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Query
from app.core.database import get_db
from app.core.config import settings


def get_database() -> Generator[Session, None, None]:
    return get_db()

def get_pagination_params(
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Размер страницы")
) -> dict:
    skip = (page - 1) * size
    return {"skip": skip, "limit": size, "page": page, "size": size}