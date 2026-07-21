from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    user: str = "postgres"
    password: str = ""
    host: str = "localhost"
    port: int = 5432
    database_name : str = "FinCore"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database_name}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
        env_nested_delimiter="__"
    )

    debug: bool = True

    jwt_secret_key: str
    webhook_secret_key: str
    access_token_expire_minutes: int = 30
    jwt_scheduler_task_interval_hours: int = 1

    db: DatabaseConfig

settings = Settings()


