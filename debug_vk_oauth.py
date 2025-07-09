#!/usr/bin/env python3
"""
Детальная диагностика проблем с VK OAuth
"""
import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

def test_vk_oauth():
    """Тестирует VK OAuth пошагово"""
    
    client_id = os.getenv('VK_CLIENT_ID')
    client_secret = os.getenv('VK_CLIENT_SECRET')
    redirect_uri = os.getenv('VK_REDIRECT_URI')
    
    print("🔍 Детальная диагностика VK OAuth")
    print("=" * 50)
    
    # Шаг 1: Проверка переменных окружения
    print("1️⃣ Проверка переменных окружения:")
    print(f"   Client ID: {client_id}")
    print(f"   Client Secret: {'*' * len(client_secret) if client_secret else 'НЕ УСТАНОВЛЕН'}")
    print(f"   Redirect URI: {redirect_uri}")
    print()
    
    # Шаг 2: Формирование URL авторизации
    auth_params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'display': 'page',
        'scope': 'email',
        'response_type': 'code',
        'v': '5.131'
    }
    
    auth_url = f"https://oauth.vk.com/authorize?{urlencode(auth_params)}"
    print("2️⃣ URL авторизации:")
    print(f"   {auth_url}")
    print()
    
    # Шаг 3: Тест запроса к VK
    print("3️⃣ Тест запроса к VK OAuth:")
    try:
        response = requests.get(auth_url, allow_redirects=False)
        print(f"   Статус: {response.status_code}")
        print(f"   Заголовки: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("   ✅ VK принимает запрос")
        elif response.status_code == 418:
            print("   ❌ VK блокирует запрос (418)")
            print("   Возможные причины:")
            print("   - Неправильный client_id")
            print("   - Приложение заблокировано")
            print("   - Неправильный redirect_uri")
        elif response.status_code == 302:
            print("   ✅ VK перенаправляет (ожидаемое поведение)")
        else:
            print(f"   ⚠️ Неожиданный статус: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка запроса: {e}")
    
    print()
    
    # Шаг 4: Рекомендации
    print("4️⃣ Рекомендации для исправления:")
    print("   📋 Проверьте в настройках VK-приложения:")
    print("      - Тип приложения: Standalone или Веб-сайт")
    print("      - Статус: Опубликовано или в тестировании")
    print("      - Адрес сайта: https://enotes.loca.lt")
    print("      - Базовый домен: enotes.loca.lt")
    print("      - Redirect URI: https://enotes.loca.lt/auth/vk/callback")
    print("      - Разрешена авторизация пользователя через VK ID")
    print()
    print("   🔗 Откройте в браузере:")
    print(f"      {auth_url}")
    print()
    print("   📱 Если приложение в тестировании:")
    print("      - Добавьте свой VK ID в список разрешенных пользователей")

if __name__ == "__main__":
    test_vk_oauth() 