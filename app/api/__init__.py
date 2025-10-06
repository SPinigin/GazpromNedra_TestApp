from fastapi import APIRouter
from endpoints import licenses_router, wells_router, references_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(licenses_router)
api_router.include_router(wells_router)
api_router.include_router(references_router)
