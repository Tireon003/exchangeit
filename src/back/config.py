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
    # SECRET KEY for hashing
    HASH_SECRET: str
    # REDIS variables
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def db_url(self):
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}"
                f":{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    @property
    def api_external_port(self):
        return self.API_EXT_PORT

    @property
    def hash_secret(self):
        return self.HASH_SECRET

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
