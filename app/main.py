import asyncio


from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.sse import EventSourceResponse


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


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
