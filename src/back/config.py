from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Postgres variables
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    # API variables
    API_EXT_PORT: int

    @property
    def db_url(self):
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}"
                f":{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    @property
    def api_external_port(self):
        return self.API_EXT_PORT

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
