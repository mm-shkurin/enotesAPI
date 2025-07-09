#!/usr/bin/env python3
"""
Скрипт для проверки конфигурации VK OAuth
"""
import os
from urllib.parse import urlencode

# Загружаем переменные окружения
from dotenv import load_dotenv

# Принудительно перезагружаем .env файл
load_dotenv(override=True)

def check_vk_config():
    """Проверяет конфигурацию VK OAuth"""
    
    # Получаем переменные окружения
    client_id = os.getenv('VK_CLIENT_ID')
    client_secret = os.getenv('VK_CLIENT_SECRET')
    redirect_uri = os.getenv('VK_REDIRECT_URI')
    
    print("🔍 Проверка конфигурации VK OAuth:")
    print(f"Client ID: {'✅ Установлен' if client_id else '❌ Отсутствует'}")
    print(f"Client Secret: {'✅ Установлен' if client_secret else '❌ Отсутствует'}")
    print(f"Redirect URI: {redirect_uri or '❌ Отсутствует'}")
    
    if not all([client_id, client_secret, redirect_uri]):
        print("\n❌ Не все переменные окружения установлены!")
        return False
    
    # Формируем URL авторизации
    auth_params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'display': 'page',
        'scope': 'email',
        'response_type': 'code',
        'v': '5.131'
    }
    
    auth_url = f"https://oauth.vk.com/authorize?{urlencode(auth_params)}"
    
    print(f"\n🔗 URL авторизации:")
    print(auth_url)
    
    print(f"\n📋 Что проверить в настройках VK:")
    print(f"1. Client ID: {client_id}")
    print(f"2. Redirect URI: {redirect_uri}")
    print(f"3. Тип приложения: Standalone или Веб-сайт")
    print(f"4. Статус приложения: Опубликовано или в тестировании")
    
    return True

if __name__ == "__main__":
    check_vk_config() 