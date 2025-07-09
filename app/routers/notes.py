from fastapi import APIRouter, HTTPException
from app.schemas.notes import NoteCreate, NoteResponse

router = APIRouter()

notes_db = []

@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    new_note = {
        "id": len(notes_db) + 1,
        "title": note.title,
        "content": note.content
    }
    notes_db.append(new_note)
    return new_note

@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(note_id: int):
    if note_id > len(notes_db) or note_id < 1:
        raise HTTPException(status_code=404, detail="Note not found")
    return notes_db[note_id - 1]