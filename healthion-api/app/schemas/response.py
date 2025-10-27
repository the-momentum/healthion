from pydantic import BaseModel


class UploadDataResponse(BaseModel):
    status_code: int | None = None
    response: str
