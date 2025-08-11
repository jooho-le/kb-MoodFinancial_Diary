from fastapi import UploadFile
from PIL import Image
import io
from datetime import datetime
from deepface import DeepFace
import cv2
import numpy as np
from app.models.image_model import ImageMeta
from app.services.db_service import db

# 감정값 변환
def convert_emotions_to_float(emotions: dict) -> dict:
    return {k: float(v) for k, v in emotions.items()}

# 얼굴 감정 분석
def analyze_emotion(image: Image.Image) -> dict:
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    try:
        result = DeepFace.analyze(img_bgr, actions=['emotion'], enforce_detection=False)
        emotions = result[0]['emotion'] if isinstance(result, list) else result['emotion']
        return convert_emotions_to_float(emotions)
    except Exception as e:
        return {"error": str(e)}

# 메인 처리 함수
async def process_and_store_image(file: UploadFile) -> ImageMeta:
    # 1) 이미지 로드
    content = await file.read()
    image = Image.open(io.BytesIO(content)).convert("RGB")
    width, height = image.size

    # 2) 얼굴 감정 분석
    emotions = analyze_emotion(image)

    # 3) 메타데이터 생성
    meta = ImageMeta(
        filename=file.filename,
        width=width,
        height=height,
        uploaded_at=datetime.utcnow()
    )

    # 4) MongoDB 저장
    await db.client["moodfinance"].images.insert_one({
        **meta.dict(),
        "emotions": emotions
    })

    return meta, emotions
