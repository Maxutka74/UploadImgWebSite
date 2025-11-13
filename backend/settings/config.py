from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

class AppConfig(BaseSettings):
    username: str | None = None
    password: str | None = None

    Image_DIR: str
    LOG_DIR: str

    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    SUPPORTED_FORMATS: set[str] = {'.jpg', '.png', '.gif'}

    model_config = SettingsConfigDict(
        env_file= BASE_DIR / str(".env"),
        env_file_encoding="utf-8",
    )

config = AppConfig()