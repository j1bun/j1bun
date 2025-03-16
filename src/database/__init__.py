import enum

import motor.motor_asyncio

from core import config


class DatabasesEnum(str, enum.Enum):
    BACKEND = "j1bun-backend"


class CollectionsEnum(str, enum.Enum):
    CLIENT = "CLIENT"
    ACCOUNTANT = "ACCOUNTANT"


class MongoDB:
    """Mongo Database

    Methods:
        collection - returns collection
    """

    __slots__ = ("client", "database")

    client: motor.motor_asyncio.AsyncIOMotorClient
    database: motor.motor_asyncio.AsyncIOMotorDatabase

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            config.mongodb.get_uri,
        )
        self.database = self.client[DatabasesEnum.BACKEND]

    def __getattr__(self, collection: CollectionsEnum):
        """Returns a database collection"""
        if collection not in CollectionsEnum:
            raise NameError(f"`{collection}` not in CollectionsEnum")
        return self.database[collection]
