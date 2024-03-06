import json
from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.api_v1.routers import router
from app.api.dependencies.database import SessionDep
from app.core.exception_middleware import ExceptionMiddleware
from app.services.label import LabelService
from app.services.streaming import StreamingService
from app.services.video import VideoService

middleware = [Middleware(ExceptionMiddleware)]

app = FastAPI(middleware=middleware)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

templates = Jinja2Templates(directory="templates")

app.include_router(router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/image/", response_class=HTMLResponse)
async def get_image(session: SessionDep, request: Request, uri: str):
    video_service = VideoService()
    image_path = video_service.save_frame_as_image(uri)

    streaming_service = StreamingService(session)
    streaming_id = streaming_service.get_id_by_uri(uri)
    print("----")

    label_service = LabelService(session)
    labels = label_service.get_labels(streaming_id)

    print(labels)

    for label in labels:        
        print(label)
    
    label_data_json = json.dumps([label.dict() for label in labels])

    print(label_data_json)

    return templates.TemplateResponse("image.html", {"request": request,"temp_img_path": "/" + image_path, "streaming_id": streaming_id, "label_data": label_data_json})

    
#@app.get("/")
#async def root():
#    return {"message": "Hello World"}


# Run the FastAPI app
#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="127.0.0.1", port=8000)