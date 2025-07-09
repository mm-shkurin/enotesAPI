import aiohttp
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.db import get_db
from app.models.users import User
from app.schemas.token import Token
from app.services.security import create_access_token, get_current_user
from config import settings
from typing import Optional

router = APIRouter(tags=["auth"])

async def get_token_from_header(authorization: Optional[str] = Header(None)) -> Optional[str]:
    if authorization and authorization.startswith("Bearer "):
        return authorization.replace("Bearer ", "")
    return None

@router.get("/vk")
async def auth_vk():
    return RedirectResponse(
        f"https://oauth.vk.com/authorize?"
        f"client_id={settings.vk_client_id}&"
        f"redirect_uri={settings.vk_redirect_uri}&"
        f"display=page&"
        f"scope=email&"
        f"response_type=code&"
        f"v=5.131"
    )

@router.get("/test")
async def test_auth():
    """Тестовый эндпоинт для проверки авторизации без VK"""
    return {
        "message": "Тестовый эндпоинт авторизации работает",
        "vk_client_id": settings.vk_client_id,
        "redirect_uri": settings.vk_redirect_uri
    }

@router.get("/vk/callback", response_model=Token)
async def auth_vk_callback(
    code: str, 
    db: AsyncSession = Depends(get_db)
):
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code is required"
        )
    
    token_url = "https://oauth.vk.com/access_token"
    params = {
        "client_id": settings.vk_client_id,
        "client_secret": settings.vk_client_secret,
        "redirect_uri": settings.vk_redirect_uri,
        "code": code
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(token_url, params=params) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"VK token request failed with status {response.status}"
                    )
                token_data = await response.json()
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"VK token request failed: {str(e)}"
        )
    
    if "access_token" not in token_data:
        error = token_data.get("error", "Unknown error")
        error_description = token_data.get("error_description", "")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"VK error: {error}. {error_description}"
        )
    
    user_url = "https://api.vk.com/method/users.get"
    user_params = {
        "access_token": token_data["access_token"],
        "v": "5.131",
        "fields": "id,first_name,last_name,email,photo_200,screen_name"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(user_url, params=user_params) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"VK user data request failed with status {response.status}"
                    )
                user_data = await response.json()
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"VK user data request failed: {str(e)}"
        )
    
    if "error" in user_data or "response" not in user_data:
        error_msg = user_data.get("error", {}).get("error_msg", "Unknown VK error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"VK API error: {error_msg}"
        )
    
    vk_user = user_data["response"][0]
    
    if "id" not in vk_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="VK user ID is required"
        )
    
    vk_user["access_token"] = token_data["access_token"]  
    vk_user["email"] = token_data.get("email")  
    
    username = f"vk_{vk_user['id']}"
    
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalars().first()
    
    if not user:
        user = User(
            username=username,
            email=vk_user.get("email"),
            vk_data=vk_user
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        user.vk_data = vk_user
        if vk_user.get("email"):
            user.email = vk_user["email"]
        await db.commit()
        await db.refresh(user)
    
    access_token = create_access_token(
        data={"sub": user.username}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
async def get_current_user_info(
    token: str = Depends(get_token_from_header),
    db: AsyncSession = Depends(get_db)
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is required"
        )
    
    user = await get_current_user(token, db)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "vk_id": user.vk_id,
        "is_active": user.is_active
    }
    