import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    status,
    BackgroundTasks,
    Request,
    Depends,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
)

from .views.redis import redis_tokens
from core.config import USERS_DB, REDIS_TOKENS_SET_NAME
from .crud import storage
from schemas.movie import Movie

logger = logging.getLogger(__name__)

static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from the developer portal. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic auth",
    description="Basic **username** + **password** auth. [Read more](#)",
    auto_error=False,
)

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def prefetch_movie(slug: str) -> Movie | None:
    movie = storage.get_by_slug(slug)

    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug '{slug}' not found.",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    # Code BEFORE enter inside the view function
    yield
    # Code AFTER exiting the view function
    if request.method in UNSAFE_METHODS:
        logger.info("Add background task to save storage.")
        background_tasks.add_task(storage.save_state)


def valid_basic_auth(credentials: HTTPBasicCredentials) -> None:
    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials are required. Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ],
):
    if request.method not in UNSAFE_METHODS:
        return

    valid_basic_auth(credentials=credentials)


def valid_api_token(api_token: HTTPAuthorizationCredentials) -> None:
    if redis_tokens.sismember(REDIS_TOKENS_SET_NAME, api_token.credentials):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token.",
    )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ],
):
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )

    valid_api_token(api_token=api_token)


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return None

    if credentials:
        return valid_basic_auth(credentials=credentials)
    if api_token:
        return valid_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth is required.",
    )
