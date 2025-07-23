"""Convert extracted rules to a GPT-friendly JSONL format."""
import json
from typing import List, Dict


def convert_to_jsonl(items: List[Dict[str, str]], out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
