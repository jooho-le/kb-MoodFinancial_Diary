from fastapi import APIRouter, UploadFile, File
from app.services.image_service import process_and_store_image

router = APIRouter()

@router.post("/image")
async def upload_and_analyze_image(file: UploadFile = File(...)):
    meta, emotions = await process_and_store_image(file)
    return {
        "filename": meta.filename,
        "width": meta.width,
        "height": meta.height,
        "uploaded_at": meta.uploaded_at,
        "emotions": emotions
    }
