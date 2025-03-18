"""JWT -> MongoDB

login:
    user -> token-sub -> ...
auth:
    pass

"""

from typing import Any

from litestar import Router, Request, Response, get, post
from litestar.connection import ASGIConnection

from litestar.stores.memory import MemoryStore
from litestar.security.jwt import JWTAuth, Token

from core.config import settings
from routes.user import schema


memory_store = MemoryStore()


async def retrieve_user_handler(
    token: Token, connection: "ASGIConnection[Any, Any, Any, Any]"
) -> schema.User | None:
    print("uTOKEN:", token)
    return await connection.app.state.mdb.CLIENT.find_one(
        {
            "model": "User",
            "token-sub": token.sub,
        }
    )


jwt_auth = JWTAuth[schema.User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.jwt.SECRET,
    exclude=["/login", "/schema"],
)


@post("/login")
async def login(
    data: schema.User,
) -> Response[schema.User]:
    # TODO: check & set user.token-sub -> data.id ???
    return jwt_auth.login(
        identifier=str(data.id),
        token_extras={"email": data.email},
        response_body=data,
    )


@get("/some-path")
async def some_route_handler(
    request: "Request[schema.User, Token, Any]",
) -> Any:
    print("rUSER:", request.user)
    print("rAUTH:", request.auth)
    # request.user is set to the instance of user returned by the middleware
    assert isinstance(request.user, schema.User)
    # request.auth is the instance of 'litestar_jwt.Token' created from the data encoded in the auth header
    assert isinstance(request.auth, Token)


router = Router(
    path="/auth",
    tags=["auth"],
    route_handlers=[
        login,
        some_route_handler,
    ],
)
