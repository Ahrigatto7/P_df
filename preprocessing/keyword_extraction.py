"""Keyword extraction utilities for the Saju preprocessing pipeline."""
from collections import Counter
from typing import List


KEYWORDS = ["십신", "격국", "육친", "충형파해합"]


def extract_keywords(tokens: List[str]) -> List[str]:
    counter = Counter(tokens)
    found = [kw for kw in KEYWORDS if kw in counter]
    return found
