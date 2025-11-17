import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from settings.config import config
from settings.logging_config import get_logger
from handlers.files import list_uploaded_images
from handlers.upload import handle_uploaded_file
from expections.api_errors import APIError, MultipleFilesError

logger = get_logger(__name__)

app = FastAPI(title='Upload Image Website')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
    )

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    logger.error(f"{request.method} {request.url.path} -> {exc.status_code}: {exc.message}")
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


@app.get("/")
async def root():
    logger.info("Healthcheck endpoint hit: /")
    return {"message": "Welcome to Upload Image Website"}

@app.get("/upload/")
async def get_upload():
    try:
        files = list_uploaded_images()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Image not found")
    except PermissionError:
        raise HTTPException(status_code=500, detail="Permission denied")

    if not files:
        raise HTTPException(status_code=404, detail="No images uploaded")

    return files


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        saved_info = handle_uploaded_file(
            {
                "filename": file.filename,
                "file": file.file.read()
            }
        )
    except MultipleFilesError:
        raise HTTPException(status_code=400, detail="Only one file allowed")
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    logger.info(f"File '{saved_info['filename']}' uploaded successfully")
    return saved_info



@app.delete("/upload/{filename}")
async def delete_file(filename: str):
    ext = os.path.splitext(filename)[1].lower()

    if ext not in config.SUPPORTED_FORMATS:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    filepath = os.path.join(config.IMAGE_DIR, filename)

    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        os.remove(filepath)
    except PermissionError:
        raise HTTPException(status_code=500, detail="Permission denied")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    return {"message": f"File '{filename}' deleted successfully"}