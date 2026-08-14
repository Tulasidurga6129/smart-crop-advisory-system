from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1 import auth, users, profile, farms
from app.api.v1.profile import router as profile_router
app = FastAPI(
    title="Smart Crop Advisory System API",
    description="Backend API for the Smart Crop Advisory System",
    version="1.0.0",
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)
app.include_router(farms.router)

app.include_router(
    users_router,
    prefix="/api/v1",
)

app.include_router(
    profile_router,
    prefix="/api/v1",
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