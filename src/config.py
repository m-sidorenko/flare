from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.v1 import Field

class FlareSettings(BaseSettings):
    """
    Flare application configuration
    """
    service_host: str = Field("localhost", env="SERVICE_HOST")
    service_port: int = Field(8080, env="SERVICE_PORT")
    public_url: str = Field(
        ...,
        description="Public URL of the server (for Telegram webhook)",
        env="PUBLIC_URL")

    project_root_path: Path = Field(
        ...,
        description="Absolute path to the project root directory.\
                     The logs will be stored in the 'logs' subdirectory.",
        env="PROJECT_ROOT_PATH")

    logfire_token: str = Field(..., env="LOGFIRE_TOKEN")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Log level for the application",
        env="LOG_LEVEL"
    )
    logfire_env: Literal["dev", "prod"] = Field(
        default="dev",
        description="Environment (dev/prod)",
        env="LOGFIRE_ENV"
    )

    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    chat_id: str = Field(..., env="CHAT_ID")

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

config = FlareSettings()
