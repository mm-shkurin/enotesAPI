import httpx
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import Token, UserCreate, UserResponse
from app.models.users import User
from config import settings
from app.database import get_db

router = APIRouter(tags=["Authentication"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt

@router.get("/auth/vk")
async def auth_vk():
    auth_url = (
        f"https://oauth.vk.com/authorize?"
        f"client_id={settings.vk_client_id}&"
        f"redirect_uri={settings.vk_redirect_uri}&"
        f"display=page&"
        f"scope=email&" 
        f"response_type=code&"
        f"v=5.131"
    )
    return RedirectResponse(auth_url)

@router.get("/auth/vk/callback", response_model=Token)
async def auth_vk_callback(
    code: str, 
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Обмен кода на access token
    token_url = "https://oauth.vk.com/access_token"
    params = {
        "client_id": settings.vk_client_id,
        "client_secret": settings.vk_client_secret,
        "redirect_uri": settings.vk_redirect_uri,
        "code": code
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(token_url, params=params)
        data = response.json()

    if "error" in data:
        raise HTTPException(
            status_code=400,
            detail=f"VK error: {data['error_description']}"
        )

    access_token = data.get("access_token")
    vk_user_id = data.get("user_id")
    email = data.get("email", "")

    # Получение информации о пользователе
    user_info_url = "https://api.vk.com/method/users.get"
    params = {
        "user_ids": vk_user_id,
        "access_token": access_token,
        "v": "5.131",
        "fields": "first_name,last_name"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(user_info_url, params=params)
        user_data = response.json()

    if "error" in user_data:
        raise HTTPException(
            status_code=400,
            detail=f"VK API error: {user_data['error']['error_msg']}"
        )

    vk_user = user_data["response"][0]

    user = await User.get_by_vk_id(db, vk_user_id)
    
    user_data = {
        "vk_id": vk_user_id,
        "email": email,
        "first_name": vk_user["first_name"],
        "last_name": vk_user["last_name"],
        "access_token": access_token
    }
    
    if user:
        user = await User.update(db, user.id, user_data)
    else:
        user = await User.create(db, UserCreate(**user_data))
    
    jwt_token = create_access_token(
        data={"sub": str(user.id)}
    )
    
    return {"access_token": jwt_token, "token_type": "bearer"}