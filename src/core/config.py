from pydantic import BaseModel


class MongoDB(BaseModel):
    HOST: str = "127.0.0.1"
    PORT: int = 27017
