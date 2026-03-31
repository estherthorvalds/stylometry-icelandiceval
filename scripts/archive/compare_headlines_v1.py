#!/usr/bin/env python3
"""
compare_headlines.py — Compare subject drop rates between human-written
and LLM-generated headlines.

Usage:
    python3 scripts/compare_headlines.py \
        --human output/tagged_headlines.json \
        --llm output/LLM_generated/*.json \
        -o output/comparison.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List


def is_nominative_nominal(pos: str) -> bool:
    """Check if a POS tag represents a nominative-case nominal."""
    if not pos or len(pos) < 4:
        return False
    wc = pos[0]
    if wc == 'n' and len(pos) >= 4:
        return pos[3] == 'n'
    if wc == 'l' and len(pos) >= 4:
        return pos[3] == 'n'
    if wc == 'f' and len(pos) >= 5:
        return pos[4] == 'n'
    if wc == 'g' and len(pos) >= 4:
        return pos[3] == 'n'
    return False


def analyze_headline_set(tagged_headlines: list) -> dict:
    """Compute subject drop statistics for a set of tagged headlines."""
    total = len(tagged_headlines)
    if total == 0:
        return {"error": "No headlines"}

    stats_per_headline = []
    for h in tagged_headlines:
        tokens = h.get("tokens", [])
        nom_count = sum(1 for t in tokens if is_nominative_nominal(t.get("pos", "")))
        has_nom = nom_count > 0
        token_count = len(tokens)
        stats_per_headline.append({
            "token_count": token_count,
            "nominative_count": nom_count,
            "has_nominative_nominal": has_nom,
        })

    has_nom_count = sum(1 for s in stats_per_headline if s["has_nominative_nominal"])
    drop_rate = 1 - (has_nom_count / total)

    total_tokens = sum(s["token_count"] for s in stats_per_headline)
    total_nom = sum(s["nominative_count"] for s in stats_per_headline)

    return {
        "total_headlines": total,
        "headlines_with_nominative": has_nom_count,
        "headlines_without_nominative": total - has_nom_count,
        "subject_drop_rate": round(drop_rate, 4),
        "avg_tokens_per_headline": round(total_tokens / total, 1),
        "avg_nominative_per_headline": round(total_nom / total, 2),
        "nom_per_token": round(total_nom / total_tokens, 4) if total_tokens > 0 else 0,
    }


def load_tagged(path: Path) -> list:
    """Load a tagged headlines JSON file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return data.get("tagged_headlines", [])


def main():
    parser = argparse.ArgumentParser(
        description="Compare subject drop rates: human vs LLM headlines."
    )
    parser.add_argument(
        "--human", required=True,
        help="Path to human tagged_headlines.json"
    )
    parser.add_argument(
        "--llm", nargs="+", required=True,
        help="Paths to LLM tagged headline JSON files"
    )
    parser.add_argument(
        "--output", "-o", default="output/comparison.json",
        help="Output JSON path"
    )

    args = parser.parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Analyze human headlines
    human_data = load_tagged(Path(args.human))
    human_stats = analyze_headline_set(human_data)

    # Analyze each LLM
    llm_results = {}
    for llm_path_str in args.llm:
        llm_path = Path(llm_path_str)
        name = llm_path.stem.replace("_tagged_headlines", "")
        llm_data = load_tagged(llm_path)
        llm_results[name] = analyze_headline_set(llm_data)

    # Print comparison table
    print()
    print("=" * 78)
    print("SUBJECT DROP COMPARISON — HUMAN vs LLM-GENERATED HEADLINES")
    print("=" * 78)
    print()
    print(f"{'Source':<30s} {'Drop rate':>10s} {'No nom':>8s} {'Total':>7s} "
          f"{'Avg tok':>8s} {'Avg nom':>8s} {'Nom/tok':>8s}")
    print("-" * 78)

    print(f"{'Human':<30s} {human_stats['subject_drop_rate']:>9.1%} "
          f"{human_stats['headlines_without_nominative']:>8d} "
          f"{human_stats['total_headlines']:>7d} "
          f"{human_stats['avg_tokens_per_headline']:>8.1f} "
          f"{human_stats['avg_nominative_per_headline']:>8.2f} "
          f"{human_stats['nom_per_token']:>8.4f}")

    for name, stats in sorted(llm_results.items()):
        print(f"{name:<30s} {stats['subject_drop_rate']:>9.1%} "
              f"{stats['headlines_without_nominative']:>8d} "
              f"{stats['total_headlines']:>7d} "
              f"{stats['avg_tokens_per_headline']:>8.1f} "
              f"{stats['avg_nominative_per_headline']:>8.2f} "
              f"{stats['nom_per_token']:>8.4f}")

    print("-" * 78)
    print()
    print("Drop rate = proportion of headlines with NO nominative nominal (subject drop)")
    print("Nom/tok   = nominative nominals per token (subject density)")
    print("=" * 78)

    # Compute deltas from human baseline
    print()
    print("DELTA FROM HUMAN BASELINE:")
    print("-" * 50)
    for name, stats in sorted(llm_results.items()):
        drop_delta = stats["subject_drop_rate"] - human_stats["subject_drop_rate"]
        nom_delta = stats["nom_per_token"] - human_stats["nom_per_token"]
        direction = "more" if drop_delta > 0 else "less"
        print(f"  {name:<28s} drop: {drop_delta:>+.1%}  ({direction} subject drop)")

    print("=" * 78)

    # Save output
    output = {
        "metadata": {
            "description": "Subject drop comparison: human vs LLM-generated headlines",
            "project": "stylometry-icelandiceval",
            "headline_tagging": "Sonnet 4.6 (IFD tagset)",
            "feature": "Subject drop (absence of nominative-case nominals)",
        },
        "human": human_stats,
        "llm": llm_results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()