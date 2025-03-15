import enum

import motor.motor_asyncio

from core import config


class CollectionsEnum(str, enum.Enum):
    CLIENT = "CLIENT"
    ACCOUNTANT = "ACCOUNTANT"


class MongoDB:
    """Mongo Database

    Methods:
        collection - returns collection
    """

    __slots__ = ("client",)

    client: motor.motor_asyncio.AsyncIOMotorClient

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            host=config.mongodb.HOST,
            port=config.mongodb.PORT,
        )

    def __getattr__(self, collection: CollectionsEnum):
        """Returns a database collection"""
        if collection not in CollectionsEnum:
            raise NameError(f"`{collection}` not in CollectionsEnum")
        return self.client[collection]
