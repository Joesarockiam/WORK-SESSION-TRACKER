from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import sessions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Deep Work Session Tracker API",
    description="Track your focused work sessions with interruption monitoring",
    version="1.0.0"
)

# ============================
# UPDATED CORS SETTINGS
# ============================
origins = [
    "https://work-session-tracker.onrender.com",  # Correct frontend URL
    "http://localhost:3000",                      # Local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(sessions.router)

@app.get("/")
async def root():
    return {"message": "Deep Work Session Tracker API"}
