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
FRONTEND_URL = "https://worktracker-frontend.onrender.com"

origins = [
    FRONTEND_URL,        # Production frontend
    "http://localhost:3000",   # Local React dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allowed domains
    allow_credentials=False,      # You don't use cookies/sessions
    allow_methods=["*"],          # Allow all methods: GET, POST, PUT, DELETE
    allow_headers=["*"],          # Allow all request headers
    expose_headers=["*"],         # Expose headers if needed
    max_age=600                   # Preflight cache
)

# Include routers
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
