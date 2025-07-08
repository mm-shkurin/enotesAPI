from pydantic import BaseModel
from typing import Dict, Any, Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str | None = None

class User(UserBase):
    id: int
    is_active: bool
    vk_data: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True