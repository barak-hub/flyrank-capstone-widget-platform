from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models
from app.api.widgets import router as widgets_router
from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Widget Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(widgets_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Widget Platform",
    }
