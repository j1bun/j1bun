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
            host=config.MongoDB.HOST,
            port=config.MongoDB.PORT,
        )

    def collection(self, collection: CollectionsEnum):
        """Returns the collection"""
        return self.client[collection]
