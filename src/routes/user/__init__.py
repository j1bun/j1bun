from typing import Any, Literal

from litestar import Router, Request, get

from . import schema


@get("/", sync_to_thread=False)
def get_user(
    request: Request[schema.User, dict[Literal["user_id"], str], Any],
) -> Any:
    return request.user


router = Router(
    path="/user",
    tags=["user"],
    route_handlers=[get_user],
)
