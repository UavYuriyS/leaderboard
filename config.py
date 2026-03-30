from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file first (lower priority)
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variables having priority over .env file"""

    app_version: str = "0.1.0"
    api_key: str = "your-secret-api-key-change-this"
    admin_api_key: str = "your-admin-api-key-change-this"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "leaderboard"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    backend_port: int = 8888

    class Config:
        env_file = ".env"
        case_sensitive = False
        # Environment variables override .env file values
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


# Global settings instance
settings = Settings()
