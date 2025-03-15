from typing import Any
# from uuid import uuid4

from litestar import Router, Request, post
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware.session.server_side import (
    ServerSideSessionBackend,
    ServerSideSessionConfig,
)

from litestar.security.session_auth import SessionAuth
from litestar.stores.memory import MemoryStore

from routes.user import schema


MOCK_DB: dict[str, schema.User] = {}
MOCK_USER_ID: str = "b686bb73-3b9c-4c91-83d8-acf3e46e4a8c"
memory_store = MemoryStore()


async def retrieve_user_handler(
    session: dict[str, Any],
    connection: "ASGIConnection[Any, Any, Any, Any]",
) -> schema.User | None:
    if user_id := session.get("user_id"):
        return MOCK_DB.get(user_id)


@post("/login")
async def login(
    data: schema.UserLoginPayload,
    request: "Request[Any, Any, Any]",
) -> schema.User:
    user_id = await memory_store.get(data.email)

    if not user_id:
        raise NotAuthorizedException
    user_id = user_id.decode("utf-8")

    request.set_session({"user_id": user_id})

    return MOCK_DB[user_id]


@post("/signup")
async def signup(
    data: schema.UserCreatePayload,
    request: Request[Any, Any, Any],
) -> schema.User:
    user = schema.User(name=data.name, email=data.email, id=MOCK_USER_ID)

    await memory_store.set(data.email, str(user.id))

    MOCK_DB[str(user.id)] = user
    request.set_session({"user_id": str(user.id)})

    return user


session_auth = SessionAuth[schema.User, ServerSideSessionBackend](
    retrieve_user_handler=retrieve_user_handler,
    session_backend_config=ServerSideSessionConfig(),
    exclude=["/login", "/signup", "/schema"],
)

router = Router(
    path="/auth",
    tags=["auth"],
    route_handlers=[login, signup],
)
