from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
