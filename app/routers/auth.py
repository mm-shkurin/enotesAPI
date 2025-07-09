import aiohttp
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.db import get_db
from app.models.users import User
from app.schemas.token import Token
from app.services.security import create_access_token
from config import settings
import json

router = APIRouter(tags=["auth"])

@router.get("/vk", response_class=HTMLResponse)
async def auth_vk():
    html="""
    <body><center>
	<div>
  <script src="https://unpkg.com/@vkid/sdk@<3.0.0/dist-sdk/umd/index.js"></script>
  <script type="text/javascript">
    if ('VKIDSDK' in window) {
      const VKID = window.VKIDSDK;

      VKID.Config.init({
        app: 53860682,
        redirectUrl: 'https://gavyt.ooguy.com/auth/vk/callback',
        responseMode: VKID.ConfigResponseMode.Callback,
        source: VKID.ConfigSource.LOWCODE,
        scope: '', // Заполните нужными доступами по необходимости
      });

      const oneTap = new VKID.OneTap();

      oneTap.render({
        container: document.currentScript.parentElement,
        showAlternativeLogin: true
      })
      .on(VKID.WidgetEvents.ERROR, vkidOnError)
      .on(VKID.OneTapInternalEvents.LOGIN_SUCCESS, function (payload) {
        const code = payload.code;
        const deviceId = payload.device_id;

        VKID.Auth.exchangeCode(code, deviceId)
          .then(vkidOnSuccess)
          .catch(vkidOnError);
      });
    
      function vkidOnSuccess(data) {
        // Обработка полученного результата
      }
    
      function vkidOnError(error) {
        // Обработка ошибки
      }
    }
  </script>
</div>
    </center></body>
    """
    return HTMLResponse(content=html, status_code=200)

# @router.get("/vk")
# async def auth_vk():
    # return RedirectResponse(
        # f"https://oauth.vk.com/authorize?"
        # f"client_id={settings.vk_client_id}&"
        # f"redirect_uri={settings.vk_redirect_uri}&"
        # f"display=page&"
        # f"scope=email&"
        # f"response_type=code&"
        # f"v=5.131"
    # )

@router.get("/vk/callback", response_model=Token)
async def auth_vk_callback(
    code: str, 
    db: AsyncSession = Depends(get_db)
):
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
                token_data = await response.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"VK token request failed: {str(e)}"
        )
    
    if "access_token" not in token_data:
        error = token_data.get("error", "Unknown error")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"VK error: {error}"
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
                user_data = await response.json()
    except Exception as e:
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
    vk_user["access_token"] = token_data["access_token"]  
    vk_user["email"] = token_data.get("email")  
    
    vk_id = f"vk_{vk_user['id']}"
    
    result = await db.execute(
        select(User).where(User.vk_id == vk_id)
    )
    user = result.scalar()
    
    if not user:
        user = User(
            vk_id=vk_id,
            email=vk_user.get("email"),
            vk_data=vk_user
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else: #?
        user.vk_data = vk_user
        if vk_user.get("email"):
            user.email = vk_user["email"]
        await db.commit()
        await db.refresh(user)
    
    access_token = create_access_token(
        data={"sub": user.vk_id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
 
@router.get("/tg", response_class=HTMLResponse)
async def auth_tg():
    html="""
    <body><center>
	<script async 
	src="https://telegram.org/js/telegram-widget.js?2" 
	data-telegram-login="oauth_test987_bot" data-size="large" 
	data-auth-url="tg/callback"></script>
    </center></body>
    """
    return HTMLResponse(content=html, status_code=200)

@router.get("/tg/callback",status_code=status.HTTP_201_CREATED)
async def auth_tg_callback(id:str, first_name:str, last_name:str, username:str, photo_url:str,
 auth_date:str, hash:str,db: AsyncSession = Depends(get_db)):
    oauth_json = json.dumps({
    "id": id,
    "first_name": first_name,
    "last_name": last_name,
    "username": username,
    "photo_url": photo_url,
    "auth_date": auth_date,
    "hash": hash
    })
    
    exists = await db.execute(
        select(User).where(User.tg_id == id)
    )
    exists = exists.scalar()
    # exists = db.query(User).filter(models.User.tg_id==id).scalar()
    if not exists:
        user_record=User(tg_id=id,tg_data=oauth_json)
        await db.add(user_record)
        await db.commit()
        # await db.refresh(user)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User alredy exist")