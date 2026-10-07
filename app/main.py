from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from app.api.widgets import router as widgets_router
from app.api.submissions import router as submissions_router
from app.api.dashboard import router as dashboard_router

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter


app = FastAPI(
    title="Embeddable Widget Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(widgets_router)
app.include_router(submissions_router)
app.include_router(dashboard_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/widget/v1/widget.js")
def serve_widget_js():
    widget_path = Path(__file__).resolve().parent.parent / "frontend" / "widget.js"
    return FileResponse(
        widget_path,
        media_type="application/javascript",
        headers={"Cache-Control": "public, max-age=300"},
    )
