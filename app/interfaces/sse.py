import asyncio

from fastapi import Request
from fastapi.sse import EventSourceResponse

from utilities.dependencies import router


@router.get("/sse/stream", response_class=EventSourceResponse)
async def message_stream(request: Request, timeout: int = 3) -> EventSourceResponse:
    counter = 0
    while True:
        if await request.is_disconnected() or counter > timeout:
            break
        yield counter
        counter += 1
        await asyncio.sleep(1)
