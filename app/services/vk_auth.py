import aiohttp
from config import settings

async def get_vk_user_data(access_token: str):
    url = "https://api.vk.com/method/users.get"
    params = {
        "access_token": access_token,
        "v": "5.131",
        "fields": "id,first_name,last_name,email,photo_200,screen_name"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise ValueError(f"VK API returned status {response.status}")
            data = await response.json()
    
    if "error" in data or "response" not in data:
        error_msg = data.get("error", {}).get("error_msg", "Unknown VK error")
        raise ValueError(f"VK API error: {error_msg}")
    
    user_data = data["response"][0]
    user_data["username"] = f"vk_{user_data['id']}"
    return user_data