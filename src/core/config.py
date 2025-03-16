from pydantic import computed_field
from pydantic_settings import BaseSettings


class MongoDB(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 27017
    USER: str = "mongo--production-root"
    PASSWORD: str = "mongo--production-root-password"

    @computed_field
    @property
    def get_uri(self) -> str:
        return f"mongodb://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}"


mongodb = MongoDB()
