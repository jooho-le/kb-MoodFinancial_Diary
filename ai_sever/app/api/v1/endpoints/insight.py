# app/api/v1/endpoints/insight.py
from fastapi import APIRouter, HTTPException
from app.core.database import get_database
from app.core.pattern_analysis import analyze_patterns

router = APIRouter()

@router.get("/insight")
async def get_insight():
    try:
        db = get_database()
        docs = list(db.analysis.find({}, {"_id": 0}))
        insights = analyze_patterns(docs)
        return {"count": len(docs), "insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
