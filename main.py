from fastapi import FastAPI
from contextlib import asynccontextmanager

from scheduler import start_scheduler

PROJECT_NAME = "NAKSHATRA AI v3"
VERSION = "3.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting NAKSHATRA AI v3...")
    start_scheduler()
    yield
    print("🛑 Stopping NAKSHATRA AI v3...")


app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    lifespan=lifespan
)


@app.get("/")
def home():
    return {
        "project": PROJECT_NAME,
        "version": VERSION,
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }
    from notify import send_notification

send_notification(
    "🚀 NAKSHATRA AI TEST",
    "Render deployment successful.\n\nNotifications are working."
)
