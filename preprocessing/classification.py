"""Content classification utilities for the Saju preprocessing pipeline."""
from typing import List, Dict


def classify_sections(lines: List[str]) -> Dict[str, List[str]]:
    """Simple rule-based classification of lines into sections."""
    sections = {"interpretation": [], "terminology": [], "cases": []}
    for line in lines:
        if line.startswith("해석"):
            sections["interpretation"].append(line)
        elif line.startswith("용어"):
            sections["terminology"].append(line)
        else:
            sections["cases"].append(line)
    return sections
