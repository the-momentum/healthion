from fastapi import APIRouter, Depends, Request, Response

from app.services import import_service, json_import_service
from app.schemas import UploadDataResponse
from app.utils.auth_dependencies import get_current_user_id
from app.database import DbSession

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

router = APIRouter()

DATABASE_URL = "postgresql://healthion:healthion@db:5432/healthion"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# @router.post("/apple/import/auto-health-export")
# async def import_data(
#     request: Request,
#     db: DbSession = SessionLocal(),
#     user_id: str = Depends(get_current_user_id)
# ) -> UploadDataResponse:
#     """Import health data from file upload or JSON."""
#     content_type = request.headers.get("content-type", "")
    
#     if "multipart/form-data" in content_type:
#         form = await request.form()
#         file = form.get("file")
#         if not file:
#             return UploadDataResponse(response="No file found")
        
#         content_str = await file.read()
#         content_str = content_str.decode("utf-8")
#     else:
#         body = await request.body()
#         content_str = body.decode("utf-8")
    
#     return await import_service.import_data_from_request(db, content_str, content_type, user_id)


# @router.post("/apple/import/healthion")
# async def import_data_healthion(
#         request: Request,
#         db: DbSession = SessionLocal(),
#         user_id: str = Depends(get_current_user_id)
# ) -> UploadDataResponse:
#     """Import health data from file upload or JSON."""
#     content_type = request.headers.get("content-type", "")

#     if "multipart/form-data" in content_type:
#         form = await request.form()
#         file = form.get("file")
#         if not file:
#             return UploadDataResponse(response="No file found")

#         content_str = await file.read()
#         content_str = content_str.decode("utf-8")
#     else:
#         body = await request.body()
#         content_str = body.decode("utf-8")

#     return await json_import_service.import_data_from_request(db, content_str, content_type, user_id)

@router.post("/apple/import/auto-health-export")
async def import_data(
        request: Request,
        user_id: str = None
) -> Response:
    """Import health data from file upload or JSON."""
    db = SessionLocal()
    try:
        content_type = request.headers.get("content-type", "")
        if "multipart/form-data" in content_type:
            form = await request.form()
            file = form.get("file")
            if not file:
                return UploadDataResponse(status_code=400, response="No file found")
            content_str = await file.read()
            content_str = content_str.decode("utf-8")
        else:
            body = await request.body()
            content_str = body.decode("utf-8")
        result = await import_service.import_data_from_request(db, content_str, content_type,
                                                                    user_id=user_id)
        return Response(
            content=result.model_dump_json(),
            status_code=result.status_code or 200,
            media_type="application/json"
        )
    except Exception as e:
        db.rollback()
        # Return error response with proper status code
        error_response = UploadDataResponse(status_code=400, response=f"Import failed: {str(e)}")
        return Response(
            content=error_response.model_dump_json(),
            status_code=400,
            media_type="application/json"
        )
    finally:
        db.close()


@router.post("/apple/import/healthion")
async def import_data_healthion(
        request: Request
) -> Response:
    """Import health data from file upload or JSON."""
    db = SessionLocal()
    try:
        content_type = request.headers.get("content-type", "")
        if "multipart/form-data" in content_type:
            form = await request.form()
            file = form.get("file")
            if not file:
                return UploadDataResponse(status_code=400, response="No file found")
            content_str = await file.read()
            content_str = content_str.decode("utf-8")
        else:
            body = await request.body()
            content_str = body.decode("utf-8")
        result = await json_import_service.import_data_from_request(db, content_str, content_type,
                                                                    user_id=None)
        return Response(
            content=result.model_dump_json(),
            status_code=result.status_code or 200,
            media_type="application/json"
        )
    except Exception as e:
        db.rollback()
        # Return error response with proper status code
        error_response = UploadDataResponse(status_code=400, response=f"Import failed: {str(e)}")
        return Response(
            content=error_response.model_dump_json(),
            status_code=400,
            media_type="application/json"
        )
    finally:
        db.close()



