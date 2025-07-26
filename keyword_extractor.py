"""Keyword extraction utilities."""

from collections import Counter
import re

try:
    from konlpy.tag import Okt  # type: ignore
    _Okt = Okt()
except Exception:  # pragma: no cover - fallback when konlpy is unavailable
    _Okt = None


def _simple_nouns(text: str) -> list[str]:
    """Fallback noun extractor for environments without ``konlpy``.

    This implementation is heuristic based and simply extracts Korean words and
    strips common particle suffixes so that tests can run without the external
    dependency.
    """

    words = re.findall(r"[가-힣]+", text)
    suffixes = [
        "은",
        "는",
        "이",
        "가",
        "와",
        "과",
        "도",
        "을",
        "를",
        "에",
        "에서",
        "으로",
        "로",
        "에게",
        "의",
        "이다",
        "입니다",
        "합니다",
        "것입니다",
    ]

    nouns = []
    for w in words:
        for suf in suffixes:
            if w.endswith(suf) and len(w) > len(suf):
                w = w[: -len(suf)]
                break
        if len(w) > 1:
            nouns.append(w)
    return nouns


def extract_keywords(text: str, top_n: int = 10) -> list[str]:
    """Extract top N Korean nouns from ``text``.

    When ``konlpy`` is installed, ``Okt`` is used for accurate noun extraction.
    Otherwise a simple regex-based fallback is used so that the function works
    without external dependencies.
    """

    if _Okt is not None:
        nouns = _Okt.nouns(text)
    else:  # fallback for environments without konlpy
        nouns = _simple_nouns(text)

    filtered = [n for n in nouns if len(n) > 1]
    freq = Counter(filtered)
    return [kw for kw, _ in freq.most_common(top_n)]

