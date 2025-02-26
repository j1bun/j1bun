from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig

from routes import auth, user


app = Litestar(
    route_handlers=[
        auth.router,
        user.router,
    ],
    on_app_init=[auth.session_auth.on_app_init],
    openapi_config=OpenAPIConfig(
        title="My API",
        version="1.0.0",
    ),
)
