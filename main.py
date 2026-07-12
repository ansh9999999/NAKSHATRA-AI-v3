from fastapi import FastAPI
from scheduler import start_scheduler

app = FastAPI(
    title="NAKSHATRA AI v3",
    version="3.0"
)
@app.on_event("startup")
def startup():
    start_scheduler()

@app.get("/")
def home():
    return {
        "project": "NAKSHATRA AI v3",
        "status": "Running",
        "version": "3.0"
    }

@app.get("/health")
def health():
    return {
        "status": "OK"
    }
