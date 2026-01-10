"""Application configuration."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # Data storage
    DATA_DIR: str = "./data"
    STORAGE_TYPE: str = "local"  # 'local' or 's3' (future)

    # Optional Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    USE_REDIS: bool = False

    # Security (POC: Default values for local development)
    SECRET_KEY: str = "poc-secret-key-not-used-in-production-change-in-prod"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # API Configuration
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    ENVIRONMENT: str = "development"  # 'development' or 'production'
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Event Buffering
    EVENT_BUFFER_SIZE: int = 100
    EVENT_FLUSH_INTERVAL: int = 60  # seconds

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
