from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import sessions
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Deep Work Session Tracker API",
    description="Track your focused work sessions with interruption monitoring",
    version="1.0.0"
)

# ----------------------------
# CORS SETTINGS FOR RENDER
# ----------------------------
FRONTEND_URL = "https://work-session-tracker.onrender.com"  # Updated to actual URL

origins = [
    FRONTEND_URL,               # Production frontend
    "http://localhost:3000",    # Local React dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600
)

# Include API routes
app.include_router(sessions.router)

@app.get("/")
async def root():
    return {
        "message": "Deep Work Session Tracker API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
