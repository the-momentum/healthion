from logging import INFO, basicConfig

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.utils.exceptions import handle_exception
from app.api import head_router
from app.middlewares import add_cors_middleware

basicConfig(level=INFO, format="[%(asctime)s - %(name)s] (%(levelname)s) %(message)s")

api = FastAPI(title=settings.api_name)

add_cors_middleware(api)


@api.get("/")
async def root() -> dict[str, str]:
    return {"message": "Server is running!"}


@api.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> None:
    raise handle_exception(exc, err_msg=exc.args[0][0]["msg"])


api.include_router(head_router, prefix=settings.api_latest)
