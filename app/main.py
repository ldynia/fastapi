import uvicorn

from config.service import APP_HOST
from config.service import APP_PORT
from interfaces.rest import router as rest_routes
from interfaces.sse import router as sse_routes
from interfaces.websockets import router as websocket_routes
from utilities.dependencies import app


app.include_router(rest_routes)
app.include_router(sse_routes)
app.include_router(websocket_routes)


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
