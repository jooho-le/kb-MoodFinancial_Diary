from fastapi import APIRouter, UploadFile, File
from app.services.receipt_service import process_receipt

router = APIRouter()

@router.post("/receipt")
async def upload_and_analyze_receipt(file: UploadFile = File(...)):
    content = await file.read()
    result = await process_receipt(content)
    return result
