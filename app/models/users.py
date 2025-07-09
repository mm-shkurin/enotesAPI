from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.db import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    vk_data = Column(JSONB, nullable=True)  

    # Relationship
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")

    @property
    def vk_id(self):
        if self.vk_data is not None:
            return self.vk_data.get('id')
        return None