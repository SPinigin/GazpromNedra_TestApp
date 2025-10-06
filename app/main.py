from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import logging
import time
from app.api import api_router
from app.core.config import settings
from app.core.database import engine, Base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Application starting up...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Application shutting down...")

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="REST API Gazprom-Nedra",
    version="1.0.0",
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.4f}s"
    )
    return response

app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "message": "Gazprom-Nedra TestApp",
        "description": "REST API Gazprom-Nedra",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)