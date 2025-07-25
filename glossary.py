# 동의어 사전 (필요시 확장 가능)
SYNONYM_MAP = {
    "AI": "인공지능",
    "머신러닝": "기계학습",
    "딥러닝": "심층학습",
    "NLP": "자연어처리",
    "GPT": "생성형인공지능"
}

def normalize_terms(keywords):
    """동일 의미의 키워드를 하나로 통합"""
    return [SYNONYM_MAP.get(k, k) for k in keywords]
