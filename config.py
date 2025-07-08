from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "eNotes.pro"
    debug: bool = True
    
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    # Настройки VK OAuth
    vk_client_id: str
    vk_client_secret: str
    vk_redirect_uri: str
    
    # Настройки JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  

settings = Settings()