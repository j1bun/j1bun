"""Accountant router

=> monthly spending -> daily spending
"""

from litestar import Router, post


@post()
async def index():
    pass


router = Router(
    path="/accountant",
    tags=["accountant"],
    route_handlers=[],
)
