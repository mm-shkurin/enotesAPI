from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.database.db import BaseModel
import uuid

class Note(Base):
    __tablename__ = 'notes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    stt = Column(Text, nullable=True)
    summary = Column(Text, nullable=True) 
    prufer_sequence = Column(Text, nullable=True)
    s3link = Column(Text, nullable=True)