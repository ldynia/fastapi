import socket

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from config.service import POSTGRES_PORT
from config.service import REDIS_PORT
from utilities.dependencies import red
from utilities.dependencies import async_session
from utilities.dependencies import sync_session

from utilities.dependencies import router


@router.get("/")
async def read_root():
    return {"Hello": "FastAPI"}


@router.get("/livez")
async def alive():
    return {"status": "ok"}


@router.get("/readyz")
async def ready(db: AsyncSession = async_session):
    try:
        socket.getaddrinfo("postgres", POSTGRES_PORT)
        postgres_ready = True
    except socket.gaierror:
        postgres_ready = False

    try:
        await db.exec(text("SELECT 1;"))
        postgres_ready = True
    except Exception:
        postgres_ready = False
    
    try:
        socket.getaddrinfo("redis", REDIS_PORT)
        redis_ready = True
    except socket.gaierror:
        redis_ready = False
    
    try:
        await red.ping()
        redis_ready = True
    except Exception:
        redis_ready = False

    payload = {
        "database": "ready" if postgres_ready else "not ready",
        "cache": "ready" if redis_ready else "not ready",
    }
    
    all_ready = all([postgres_ready, redis_ready])  
    status_code = status.HTTP_200_OK if all_ready else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(content=payload, status_code=status_code)


@router.get("/asyncdb")
async def read_root(db: AsyncSession = async_session):
    result = await db.exec(text("SELECT 'Async DB';"))
    world = result.scalar_one()

    return {"Hello": world}


@router.get("/syncdb")
def read_root(db: AsyncSession = sync_session):
    result = db.exec(text("SELECT 'Sync DB';"))
    world = result.scalar_one()

    return {"Hello": world}
