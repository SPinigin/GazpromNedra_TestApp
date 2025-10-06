from fastapi import APIRouter
from backend.app.api.v1.endpoints import licenses, wells, refs

api_router = APIRouter()

api_router.include_router(licenses.router, prefix="/licenses", tags=["licenses"])
api_router.include_router(wells.router, prefix="/wells", tags=["wells"])
api_router.include_router(refs.router, prefix="/refs", tags=["refs"])
