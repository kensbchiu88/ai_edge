from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.api.api_v1.routers import router
from app.api.dependencies.database import SessionDep
from app.core.exception_middleware import ExceptionMiddleware
from app.services.streaming import StreamingService
from app.services.video import VideoService
import urllib.parse
import urllib

middleware = [Middleware(ExceptionMiddleware)]

app = FastAPI(middleware=middleware)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

app.include_router(router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse(url="/static/index.html")

@app.get("/image/", response_class=HTMLResponse)
async def get_image(session: SessionDep, request: Request, uri: str):
    video_service = VideoService()
    image_path = video_service.save_frame_as_image(uri)

    streaming_service = StreamingService(session)
    streaming_id = streaming_service.get_id_by_uri(uri)

    params = { 'uri' : "/" + image_path, 'streaming_id' : streaming_id}
    param_encoded = urllib.parse.urlencode(params)
    url_with_params = f"/static/image.html?{param_encoded}"
    
    return RedirectResponse(url=url_with_params)