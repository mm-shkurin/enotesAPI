from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Основные настройки приложения
    app_name: str = "eNotes.pro"
    debug: bool = True
    
    # Настройки PostgreSQL
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    
    # Формирование URL для базы данных
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    # Настройки VK OAuth
    vk_client_id: str
    vk_client_secret: str
    vk_redirect_uri: str  # Исправлено с vk_secret_url
    
    # Настройки JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30  # Исправлено с access_timeout

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Разрешает дополнительные поля без ошибок

settings = Settings()