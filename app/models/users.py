from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.database.db import BaseModel
import uuid

class User(BaseModel):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    vk_id = Column(String, unique=True, index=True)
    tg_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    #isGuest bool must be here
    vk_data = Column(JSONB, nullable=True)  
    tg_data = Column(JSONB, nullable=True) 

    @property
    def vk_id(self):
        return self.vk_data.get('id') if self.vk_data else None
    
    @property
    def tg_id(self):
        return self.tg_data.get('id') if self.tg_data else None