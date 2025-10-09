from pydantic import BaseModel


class UploadDataResponse(BaseModel):
    response: str
