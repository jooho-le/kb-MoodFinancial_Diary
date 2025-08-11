from fastapi import APIRouter, HTTPException
from app.models.analysis_model import AnalysisData
from app.core.database import get_database
from pymongo.errors import PyMongoError

router = APIRouter()

@router.post("/store-analysis")
async def store_analysis(data: AnalysisData):
    db = get_database()
    try:
        result = db.analysis.insert_one(data.dict())
        return {"message": "저장 성공", "id": str(result.inserted_id)}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"DB 저장 실패: {e}")
