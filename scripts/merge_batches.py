#!/usr/bin/env python3
"""Merge headline batches into a single numbered list."""

import json
import sys
from pathlib import Path

batch_dir = Path("output/news_headlines/human_texts/batches")
start_batch = int(sys.argv[1]) if len(sys.argv) > 1 else 3
end_batch = int(sys.argv[2]) if len(sys.argv) > 2 else 15

num = 1
for b in range(start_batch, end_batch + 1):
    path = batch_dir / f"batch_{b:02d}.json"
    if not path.exists():
        print(f"# Missing: {path}", file=sys.stderr)
        continue
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for h in data["headlines"]:
        print(f"{num}. {h['text']}")
        num += 1