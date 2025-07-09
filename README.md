# eNotes.pro API

API для приложения eNotes.pro с авторизацией через VK OAuth.

## Особенности

- FastAPI backend
- VK OAuth авторизация
- PostgreSQL база данных
- JWT токены
- Асинхронная архитектура

## Установка и настройка

### 1. Клонирование и установка зависимостей

```bash
git clone <repository-url>
cd enotesAPI
python -m venv venv
source venv/bin/activate  # На Linux/Mac
# или
venv\Scripts\activate  # На Windows
pip install -r requirements.txt
```

### 2. Настройка базы данных

Создайте PostgreSQL базу данных и настройте переменные окружения.

### 3. Настройка VK OAuth

1. Перейдите на [VK Developers](https://vk.com/dev)
2. Создайте новое приложение
3. Получите `client_id` и `client_secret`
4. Настройте `redirect_uri` (например: `http://localhost:8000/auth/vk/callback`)

### 4. Настройка переменных окружения

Скопируйте `env.example` в `.env` и заполните необходимые значения:

```bash
cp env.example .env
```

Заполните следующие переменные:
- `POSTGRES_*` - настройки базы данных
- `VK_CLIENT_ID` - ID вашего VK приложения
- `VK_CLIENT_SECRET` - секретный ключ VK приложения
- `VK_REDIRECT_URI` - URI для перенаправления после авторизации
- `SECRET_KEY` - секретный ключ для JWT токенов

### 5. Запуск миграций

```bash
python run_alembic.py
```

### 6. Запуск приложения

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Авторизация

- `GET /auth/vk` - Перенаправление на VK OAuth
- `GET /auth/vk/callback` - Callback для получения токена
- `GET /auth/me` - Информация о текущем пользователе

### Пользователи

- `GET /users/` - Список пользователей
- `GET /users/{user_id}` - Информация о пользователе

### Заметки

- `GET /notes/` - Список заметок
- `POST /notes/` - Создание заметки
- `GET /notes/{note_id}` - Получение заметки
- `PUT /notes/{note_id}` - Обновление заметки
- `DELETE /notes/{note_id}` - Удаление заметки

## Тестирование

```bash
pytest tests/
```

## Исправленные проблемы

1. ✅ Исправлен неправильный импорт `get_db` в `security.py`
2. ✅ Убрано дублирование функции `create_access_token`
3. ✅ Добавлена проверка HTTP статусов при запросах к VK API
4. ✅ Добавлена валидация данных от VK API
5. ✅ Исправлен импорт `settings` в `vk_auth.py`
6. ✅ Добавлен эндпоинт `/auth/me` для получения информации о пользователе
7. ✅ Добавлены тесты для проверки авторизации
8. ✅ Создан файл с примером конфигурации

## Безопасность

- Все пароли хешируются
- JWT токены имеют ограниченное время жизни
- VK OAuth обеспечивает безопасную авторизацию
- Валидация всех входящих данных