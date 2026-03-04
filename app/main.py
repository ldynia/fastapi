import asyncio

from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.sse import EventSourceResponse
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_async_session
from db import get_sync_session


app = FastAPI(title="Boilerplate", version="0.1.0")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/asyncdb")
async def read_root(session: AsyncSession = get_async_session):
    stmt = text("SELECT 'World';")
    result = await session.exec(stmt)
    world = result.scalar_one()

    return {"Hello": world}


@app.get("/syncdb")
def read_root(session: AsyncSession = get_sync_session):
    stmt = text("SELECT 'World';")
    result = session.exec(stmt)
    world = result.scalar_one()

    return {"Hello": world}


@app.get("/sse/stream", response_class=EventSourceResponse)
async def message_stream(request: Request, timeout: int = 3) -> EventSourceResponse:
    counter = 0
    while True:
        if await request.is_disconnected() or counter > timeout:
            break
        yield counter
        counter += 1
        await asyncio.sleep(1)


@app.websocket("/ws/echo")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
        except WebSocketDisconnect:
            break

        await websocket.send_text(data)
