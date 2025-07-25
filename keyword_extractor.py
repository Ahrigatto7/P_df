from konlpy.tag import Okt
from collections import Counter

okt = Okt()

def extract_keywords(text, top_n=10):
    """한국어 명사 기준 키워드 추출"""
    nouns = okt.nouns(text)
    filtered = [n for n in nouns if len(n) > 1]
    freq = Counter(filtered)
    return [kw for kw, _ in freq.most_common(top_n)]
