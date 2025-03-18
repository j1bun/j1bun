from litestar.openapi.config import OpenAPIConfig
from litestar import Litestar

from database import MongoDB
from routes import auth, user


async def init_db_connection(app: Litestar):
    mdb = getattr(app.state, "mdb", None)
    if mdb is None:
        app.state.mdb = MongoDB()


app = Litestar(
    path="/api",
    route_handlers=[
        auth.router,
        user.router,
    ],
    on_app_init=[auth.jwt_auth.on_app_init],
    on_startup=[init_db_connection],
    openapi_config=OpenAPIConfig(
        title="My API",
        version="1.0.0",
    ),
)
