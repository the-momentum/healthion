import json

from fastapi import APIRouter, File, UploadFile, Depends

from app.services.import_service import ImportService
from app.schemas.response import UploadDataResponse

router = APIRouter()


@router.post("/import_data")
async def import_data(
    file: UploadFile = File(...),
    import_service: ImportService = Depends(ImportService),
) -> UploadDataResponse:
    content = await file.read()
    content_str = content.decode("utf-8")
    data = json.loads(content_str)
    print(data)

    import_service.load_data(data)

    return UploadDataResponse(response="Ok")
