from fastapi import FastAPI
from app.routers import notes, users
from config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(users.router, prefix="/users", tags=["users"]) 

@app.get("/")
async def root():
    return {
        "message": "Welcome to eNotes.pro API",
        "docs": "/docs",
        "redoc": "/redoc"
    }