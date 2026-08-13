from fastapi import FastAPI

app = FastAPI(
    title="Smart Crop Advisory System API",
    description="Backend API for the Smart Crop Advisory System",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Smart Crop Advisory System API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }