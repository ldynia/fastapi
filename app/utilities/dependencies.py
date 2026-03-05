import redis.asyncio as redis

from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI

from config.service import APP_TITLE
from config.service import APP_VERSION
from config.service import REDIS_HOST
from config.service import REDIS_PORT
from utilities.db import get_async_session
from utilities.db import get_sync_session


app = FastAPI(title=APP_TITLE, version=APP_VERSION)
red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
router = APIRouter()

async_session = Depends(get_async_session)
sync_session = Depends(get_sync_session)
