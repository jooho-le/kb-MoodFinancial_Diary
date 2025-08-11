from typing import List, Dict
from collections import defaultdict
import numpy as np

def analyze_patterns(data: List[Dict]) -> List[str]:
    # 감정별 소비 총합/횟수 계산
    emotion_spending = defaultdict(list)

    for record in data:
        emotion = record.get("emotion")
        amount = record.get("amount")
        if emotion and isinstance(amount, (int, float)):
            emotion_spending[emotion].append(amount)

    insights = []
    for emotion, amounts in emotion_spending.items():
        avg = np.mean(amounts)
        if avg > 10000:  # 기준: 평균 10,000원 이상이면 주목할 패턴
            insights.append(f"{emotion} 상태일 때 평균 소비가 {int(avg):,}원으로 높습니다.")

    if not insights:
        insights.append("뚜렷한 소비 패턴이 발견되지 않았습니다.")

    return insights
