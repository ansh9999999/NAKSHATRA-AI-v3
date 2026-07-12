from fastapi import FastAPI

app = FastAPI(
    title="NAKSHATRA AI v3",
    version="3.0"
)

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
