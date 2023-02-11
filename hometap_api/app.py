import logging
import time
from typing import Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError

from hometap_api.v1.endpoints import home
from hometap_api.v1.settings import SETTINGS

logger = logging.getLogger(__name__)

app = FastAPI()

COMPONENT_ENDPOINTS = [home.endpoint]


def _configure_routers(component: FastAPI) -> None:
    for endpoint in COMPONENT_ENDPOINTS:
        component.include_router(endpoint.router, prefix=endpoint.prefix)
    return


def _configure_stats(component: FastAPI) -> None:
    # Default middleware configuration to add stats we would want to log
    @component.middleware("http")
    async def add_middleware(request: Request, call_next: Callable) -> Response:
        start = time.time()
        response = await call_next(request)
        process_time = time.time() - start
        response.headers["X-Process-Time"] = str(process_time)
        return response


def _configure_middleware(component: FastAPI) -> None:
    # Attaching middlwares defined in settings
    for m in SETTINGS.middlewares:
        logger.info(f"[!] Attaching {m[0].__name__}")
        component.add_middleware(m[0], **m[1])
        logger.info(f"[+] {m[0].__name__} attached")


def _configure_logging(component: FastAPI) -> None:
    pass


def _configure_validation_error_handler(component: FastAPI) -> None:
    # Adding custom exception handler to intercept pydantic validation errors
    # and return HTTP 422 code
    @component.exception_handler(ValidationError)
    async def handle_exception(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()}),
        )


_configure_stats(app)
_configure_middleware(app)
_configure_routers(app)
_configure_validation_error_handler(app)
_configure_logging(app)
