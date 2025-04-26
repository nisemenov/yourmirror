from litestar import Litestar, get
# from litestar.config.cors import CORSConfig
# from litestar.logging import LoggingConfig
# from litestar.openapi import OpenAPIConfig
# from litestar.config.response_cache import ResponseCacheConfig
# from litestar.stores.redis import RedisStore
#
# from server.auth import jwt_auth
# from server.config import settings
# from server.instances import AppLitestar
# from server.database import database_contextmanager
# from server.deps import session_transaction
# from .routing import api_router
# from server.crud import init_base_manager
# from server.admin import admin
#
# openapi_config = OpenAPIConfig(
#     title='Portal ANS',
#     version='1',
# )
#
# cors_config = CORSConfig(allow_origins=['*'], allow_methods=['*'])
#
# logging_config = LoggingConfig(
#     root={"level": "INFO", "handlers": ["queue_listener"]},
#     formatters={
#         "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
#     },
#     log_exceptions="always",
# )

# redis_store = RedisStore.with_client(url=settings.redis_url, db=0)
# cache_config = ResponseCacheConfig(store="redis_backed_store")


@get("/")
async def hello_world() -> str:
    return "Hello, world!"


app = Litestar(
    [hello_world]
    # route_handlers=[api_router],
    # on_app_init=[jwt_auth.on_app_init],
    # on_startup=[init_base_manager],
    # lifespan=[database_contextmanager],
    # dependencies={'transaction': session_transaction},
    # debug=settings.DEBUG,
    # cors_config=cors_config,
    # logging_config=logging_config,
    # openapi_config=openapi_config,
    # plugins=[admin],
    # stores={"redis_backed_store": redis_store},
    # response_cache_config=cache_config,
)
