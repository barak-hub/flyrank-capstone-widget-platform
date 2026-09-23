from fastapi import FastAPI

from app.api.widgets import router as widgets_router
from app.api.submissions import router as submissions_router

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter

app = FastAPI(
    title="Embeddable Widget Platform",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(widgets_router)
app.include_router(submissions_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
