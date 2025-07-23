"""Basic text cleansing utilities for the Saju preprocessing pipeline."""
import re


def clean_text(text: str) -> str:
    """Remove unwanted characters and normalize whitespace."""
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


if __name__ == "__main__":
    import sys
    input_text = sys.stdin.read()
    print(clean_text(input_text))
