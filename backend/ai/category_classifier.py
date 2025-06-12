# backend/ai/category_classifier.py
from transformers import pipeline

# ✅ 모델 로딩 (최초 1회, 느릴 수 있음)
classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

# ✅ 규칙 기반
def rule_based_category(text):
    text = text.lower()
    if any(keyword in text for keyword in ['유튜브', '멜론', '가사']):
        return '음악'
    elif any(keyword in text for keyword in ['롤', '배그', '게임', 'steam']):
        return '게임'
    elif any(keyword in text for keyword in ['코딩', '에러', 'git', '프로그래밍']):
        return 'IT'
    return None

# ✅ 최종 분류기
def hybrid_category_classifier(text):
    rule_result = rule_based_category(text)
    if rule_result:
        return {
            "category": rule_result,
            "source": "rule"
        }

    result = classifier(text, candidate_labels=["게임", "IT", "음악", "뉴스", "기타"])
    return {
        "category": result["labels"][0],
        "score": result["scores"][0],
        "source": "bert"
    }
