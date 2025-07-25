from konlpy.tag import Okt
from collections import Counter

okt = Okt()

def extract_keywords(text, top_n=10):
    """한국어 텍스트에서 명사 추출 후 상위 빈도 키워드 반환"""
    nouns = okt.nouns(text)
    filtered = [n for n in nouns if len(n) > 1]  # 한 글자 제외
    freq = Counter(filtered)
    return [kw for kw, _ in freq.most_common(top_n)]
