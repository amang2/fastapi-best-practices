from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"


class DatabaseSettings(BaseSettings):
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    database: str = Field(default="devdatabase")
    driver: str = Field(default="asyncpg")

    model_config = ConfigDict(
        env_prefix="DB_",
        env_file=ENV_PATH,
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def url(self) -> str:
        return (
            f"postgresql+{self.driver}://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


class AppSettings(BaseSettings):
    app_name: str = Field(default="FastAPI App")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

    model_config = ConfigDict(
        env_file=ENV_PATH,
        env_prefix="APP_",
        case_sensitive=False,
        extra="ignore"
    )


settings = AppSettings()
DATABASE_URL = settings.database.url
APP_NAME = settings.app_name
APP_VERSION = settings.app_version
DEBUG = settings.debug
LOG_LEVEL = settings.log_level

