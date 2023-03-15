import os
from dataclasses import dataclass, field
from logging import getLogger
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

from fast_api.v1.exceptions import EnvironmentNotFoundException

logger = getLogger(__name__)


@dataclass
class Settings:
    env: str
    middlewares: Optional[list]
    house_canary_key: str
    house_canary_url: str
    secrets_dir: Optional[str]


def ProductionSettings() -> Settings:
    return Settings(
        env="prod",
        middlewares=[],
        secrets_dir=os.environ.get("SECRETS_DIR") or "/app/secrets",
        house_canary_url="https://house-canary-api.com/api",
        house_canary_key=os.environ.get("SECRET_NAME"),
    )


def DevelopmentSettings() -> Settings:
    return Settings(
        env="dev",
        middlewares=[],
        secrets_dir=os.environ.get("SECRETS_DIR") or "/app/secrets",
        house_canary_url="https://house-canary-api-dev/api",
        house_canary_key=os.environ.get("SECRET_NAME"),
    )


def DockerSettings() -> Settings:
    origins = []  # specify web app origins if making cross-origin requests

    return Settings(
        env="docker",
        middlewares=[
            (
                CORSMiddleware,
                {
                    "allow_origins": f"{origins}",
                    "allow_credentials": True,
                    "allow_methods": "['*']",
                    "allow_headers": "['*']",
                },
            )
        ],
        secrets_dir=os.environ.get("SECRETS_DIR") or "/app/secrets",
        house_canary_url="https://40a2af34-f05f-4ca4-aa6b-c6eb444ff269.mock.pstmn.io",
        house_canary_key=os.environ.get("SECRET_NAME"),
    )


@dataclass
class Environments:
    prod: Settings = field(default_factory=ProductionSettings())
    dev: Settings = field(default_factory=DevelopmentSettings())
    docker: Settings = field(default_factory=DockerSettings())


def _get_environments() -> Environments:
    return Environments(
        prod=ProductionSettings(),
        dev=DevelopmentSettings(),
        docker=DockerSettings(),
    )


def get_settings(env: str = None) -> Settings:
    environments = _get_environments()
    if env:
        try:
            return getattr(environments, env)
        except AttributeError:
            raise EnvironmentNotFoundException("Requested environment does not exist.")
    try:
        e = os.environ["ENV"]
        return getattr(environments, e)
    except KeyError:
        logger.warning("[!] Environment is not defined, defaulting to docker")
        return DockerSettings()


SETTINGS = get_settings()
