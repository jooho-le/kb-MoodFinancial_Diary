import io
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re

# Tesseract 경로 (수정 금지)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 이미지 전처리
def preprocess_image(content: bytes) -> Image.Image:
    # Bytes → OpenCV 이미지
    image = np.array(Image.open(io.BytesIO(content)))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 흑백화
    gray = cv2.fastNlMeansDenoising(gray, h=30)  # 노이즈 제거
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # 이진화
    return Image.fromarray(thresh)

# OCR 처리
async def extract_text_from_receipt(content: bytes) -> str:
    processed_image = preprocess_image(content)
    text = pytesseract.image_to_string(processed_image, lang="kor+eng")
    return text

# 간단한 파싱: 품목 & 금액 추출
def parse_receipt_text(text: str):
    items = []
    prices = []
    total_price = None

    lines = text.splitlines()
    for line in lines:
        # 금액 패턴: 1,000 / 1000 / 10,000원
        price_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*원?', line)
        if price_match:
            price = price_match.group(1).replace(",", "")
            prices.append(int(price))
            # 품목명은 금액 앞부분으로 추정
            item_name = line.split(price_match.group(0))[0].strip()
            if item_name:
                items.append({"item": item_name, "price": int(price)})
        # 총액 탐지
        if "합계" in line or "총액" in line:
            total_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)', line)
            if total_match:
                total_price = int(total_match.group(1).replace(",", ""))

    return {
        "items": items,
        "prices": prices,
        "total": total_price
    }

# 메인 함수: 텍스트 추출 + 파싱
async def process_receipt(content: bytes):
    text = await extract_text_from_receipt(content)
    parsed_data = parse_receipt_text(text)
    return {
        "extracted_text": text,
        "parsed_data": parsed_data
    }
