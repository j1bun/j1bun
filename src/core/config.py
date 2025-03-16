from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWT(BaseModel):
    SECRET: str = "JWT_SECRET"


class MongoDB(BaseModel):
    HOST: str = "127.0.0.1"
    PORT: int = 27017
    USER: str = "mongo--production-root"
    PASSWORD: str = "mongo--production-root-password"

    @computed_field
    def get_uri(self) -> str:
        return f"mongodb://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}"


class Settings(BaseSettings):
    jwt: JWT = JWT()
    mdb: MongoDB = MongoDB()

    model_config = SettingsConfigDict(env_prefix="__")


settings = Settings()
