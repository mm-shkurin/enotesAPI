from sqlalchemy import Column, Integer, String
from .base import Base  

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    vk_id = Column(Integer, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    access_token = Column(String)