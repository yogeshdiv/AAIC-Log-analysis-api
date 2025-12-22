from fastapi import FastAPI
from app.routes.log_routes import router as log_router

app = FastAPI(title="Log Access API", version="1.0.0")

app.include_router(log_router, prefix="/api", tags=["logs"])
