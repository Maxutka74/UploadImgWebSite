import os
import uuid
from datetime import datetime
from settings.config import config

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(title='Upload Server')

os.makedirs(config.Image_DIR, exist_ok=True)
app.mount('/images', StaticFiles(directory=config.Image_DIR), name='images')

@app.get("/")
async def root():
    return {"message": "Welcome to the Upload Server"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if not ext in config.SUPPORTED_FORMATS:
        raise HTTPException(status_code=400, detail=f"Unsupported format. Allowed: {config.SUPPORTED_FORMATS}")

    contents = await file.read()

    size = len(contents)
    if size > config.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File too large. Max size: {config.MAX_FILE_SIZE} bytes")


    base = os.path.splitext(filename)[0]
    safe_base = "".join(c if c.isalnum() or c in "._-" else "_" for c in base).lower()
    unique_name = f"{safe_base}_{uuid.uuid4()}{ext}"
    file_path = os.path.join(config.Image_DIR, unique_name)

    with open(file_path, 'wb') as f:
        f.write(contents)

    return {"filename": unique_name, "url": f"/image/{unique_name}"}

@app.get("/upload/")
async def list_files():
    try:
        filenames = os.listdir(config.Image_DIR)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Images directory not found.")

    files = []
    for filename in filenames:
        file_path = os.path.join(config.Image_DIR, filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext in config.SUPPORTED_FORMATS and os.path.isfile(file_path):
            created_at = datetime.fromtimestamp(os.path.getctime(file_path))
            size = os.path.getsize(file_path)
            files.append({
                "filename": filename,
                "created_at": created_at,
                "size": size,
                "url": f"/image/{filename}"
            })

    return files
