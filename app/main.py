from fastapi import FastAPI
from app.database.db import engine, Base
from app.routers import auth, users, notes

app = FastAPI(
    title="eNotes.pro API",
    description="API for eNotes.pro application",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(notes.router, prefix="/notes")

@app.get("/")
def read_root():
    return {"message": "Welcome to eNotes.pro API"}