from pydantic_settings import BaseSettings


class MongoDB(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 27017


mongodb = MongoDB()
