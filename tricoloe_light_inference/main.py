from fastapi import FastAPI
from fastapi.middleware import Middleware
from app.api.api_v1.routers import router
from app.core.exception_middleware import ExceptionMiddleware

middleware = [Middleware(ExceptionMiddleware)]

app = FastAPI(middleware=middleware)

app.include_router(router, prefix="/api/v1")
