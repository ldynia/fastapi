from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from utilities.dependencies import router


@router.websocket("/ws/echo")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
        except WebSocketDisconnect:
            break

        await websocket.send_text(data)
