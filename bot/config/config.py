from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl

load_dotenv()


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env')

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        return str(MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))


settings = Settings()

