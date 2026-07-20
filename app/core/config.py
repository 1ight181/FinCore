from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
    )

    user: str
    password: str
    host: str
    port: int
    database_name : str

    def get_postgres_dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
        env_nested_delimiter="__",
    )

    debug: bool = True

    db_settings: DatabaseConfig = DatabaseConfig()


settings = Settings()


