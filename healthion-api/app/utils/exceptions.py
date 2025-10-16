import asyncio
from collections.abc import Callable
from functools import singledispatch, wraps
from typing import TYPE_CHECKING
from uuid import UUID

import httpx
from fastapi import status
from fastapi.exceptions import HTTPException, RequestValidationError
from jose import JWTError
from jose.exceptions import ExpiredSignatureError
from psycopg.errors import IntegrityError as PsycopgIntegrityError
from sqlalchemy.exc import IntegrityError as SQLAIntegrityError

if TYPE_CHECKING:
    from app.services import AppService


class ResourceNotFoundError(Exception):
    def __init__(self, entity_name: str, entity_id: int | UUID | None = None):
        self.entity_name = entity_name
        if entity_id:
            self.detail = f"{entity_name.capitalize()} with ID: {entity_id} not found."
        else:
            self.detail = f"{entity_name.capitalize()} not found."


@singledispatch
def handle_exception(exc: Exception, _: str) -> HTTPException:
    raise exc


@handle_exception.register
def _(exc: SQLAIntegrityError | PsycopgIntegrityError, entity: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{entity.capitalize()} entity already exists. Details: {exc.args[0]}",
    )


@handle_exception.register
def _(exc: ResourceNotFoundError, _: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.detail)


@handle_exception.register
def _(exc: AttributeError, entity: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{entity.capitalize()} doesn't support attribute or method. Details: {exc.args[0]} ",
    )


@handle_exception.register
def _(exc: RequestValidationError, _: str) -> HTTPException:
    err_args = exc.args[0][0]
    # Safely get ctx error if it exists
    ctx_error = ""
    if 'ctx' in err_args and 'error' in err_args['ctx']:
        ctx_error = f" - {err_args['ctx']['error']}"
    
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{err_args['msg']}{ctx_error}",
    )


@handle_exception.register
def _(exc: ExpiredSignatureError, _: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired. Please, log in again."
    )


@handle_exception.register
def _(exc: JWTError, _: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token: {str(exc)}"
    )


@handle_exception.register
def _(exc: httpx.HTTPError, _: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=f"Unable to verify token: {str(exc)}"
    )


def handle_exceptions[**P, T, Service: AppService](func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    async def async_wrapper(instance: Service, *args: P.args, **kwargs: P.kwargs) -> T:
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(instance, *args, **kwargs)
            else:
                return func(instance, *args, **kwargs)
        except Exception as exc:
            entity_name = getattr(instance, "name", "unknown")
            raise handle_exception(exc, entity_name) from exc

    return async_wrapper
