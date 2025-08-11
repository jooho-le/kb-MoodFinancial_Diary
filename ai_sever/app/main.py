from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.services.db_service import connect_to_mongo, close_mongo_connection

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.image_analysis import router as image_router
from app.api.v1.endpoints.receipt_analysis import router as receipt_router
from app.api.v1.endpoints.analysis_store import router as analysis_store_router
from app.api.v1.endpoints.insight import router as insight_router

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup / Shutdown (중복 제거)
@app.on_event("startup")
async def on_startup():
    try:
        await connect_to_mongo()
    except Exception as e:
        print(f"[WARN] MongoDB connect failed: {e}")

@app.on_event("shutdown")
async def on_shutdown():
    await close_mongo_connection()

# Routers
app.include_router(health_router,         prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(image_router,          prefix=settings.API_V1_STR, tags=["Image"])
app.include_router(receipt_router,        prefix=settings.API_V1_STR, tags=["Receipt"])
app.include_router(analysis_store_router, prefix=settings.API_V1_STR, tags=["분석 저장"])
app.include_router(insight_router,        prefix=settings.API_V1_STR, tags=["Insight"])
