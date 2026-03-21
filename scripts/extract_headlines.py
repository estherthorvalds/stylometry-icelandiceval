#!/usr/bin/env python3
"""
extract_headlines.py — Extract headline + body pairs from IGC/RMH news TEI-XML
and measure subject drop rate.

Part of: stylometry-icelandiceval benchmark (proof of concept)
Course: TÖL025M – Introduction to Language Technology

TWO-PHASE WORKFLOW:

  Phase 1 — Extract raw headlines and tagged body text from IGC:
    python3 scripts/extract_headlines.py extract \
        -i "data/raw/IGC-News1 22.10 (annotated version)/IGC-News1-22.10.ana" \
        -o output/extracted_pairs.json -n 40

  Phase 2 — Merge LLM-tagged headlines and compute subject drop analysis:
    python3 scripts/extract_headlines.py analyze \
        -i output/extracted_pairs.json \
        -t output/tagged_headlines.json \
        -o output/headline_analysis.json

Between phases, the headline texts are tagged by an LLM (Sonnet 4.6)
using the IFD tagset. The tagged output is saved as tagged_headlines.json.
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List


# ─── TEI namespace ───────────────────────────────────────────────────────────

URI = "http://www.tei-c.org/ns/1.0"
TEI = "{" + URI + "}"
NS = {"tei": URI}


# ─── Data structures ────────────────────────────────────────────────────────

def is_nominative_nominal(pos: str) -> bool:
    """Check if a POS tag represents a nominative-case noun, pronoun, or adjective.

    IFD tag positions for case (0-indexed):
      - Nouns (n...):      position 3 = case
      - Adjectives (l...): position 3 = case
      - Pronouns (f...):   position 4 = case
      - Articles (g...):   position 3 = case

    Nominative case is encoded as 'n' at the case position.
    """
    if not pos or len(pos) < 4:
        return False

    word_class = pos[0]

    if word_class == 'n' and len(pos) >= 4:
        return pos[3] == 'n'
    if word_class == 'l' and len(pos) >= 4:
        return pos[3] == 'n'
    if word_class == 'f' and len(pos) >= 5:
        return pos[4] == 'n'
    if word_class == 'g' and len(pos) >= 4:
        return pos[3] == 'n'

    return False


def count_nominative_nominals(tokens: list) -> int:
    """Count nominative nominals in a list of {text, lemma, pos} dicts."""
    return sum(1 for t in tokens if is_nominative_nominal(t.get("pos", "")))


def has_any_nominative(tokens: list) -> bool:
    """Check if any token is a nominative nominal."""
    return count_nominative_nominals(tokens) > 0


# ─── Phase 1: Extract ───────────────────────────────────────────────────────

def extract_tokens_from_sentences(parent_element) -> list:
    """Extract token dicts from <w> and <pc> elements inside <s> sentences."""
    tokens = []
    for s_elem in parent_element.iter(f"{TEI}s"):
        for child in s_elem:
            tag_name = child.tag.replace(TEI, "")
            if tag_name == "w":
                text = child.text or ""
                lemma = child.attrib.get("lemma", text)
                pos = child.attrib.get("pos", "")
                tokens.append({"text": text.strip(), "lemma": lemma, "pos": pos})
            elif tag_name == "pc":
                text = child.text or ""
                pos = child.attrib.get("pos", "p")
                tokens.append({"text": text.strip(), "lemma": text.strip(), "pos": pos})
    return tokens


def parse_tei_file(filepath: Path) -> Optional[dict]:
    """Parse a single TEI-XML file and extract headline text + body tokens."""
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        print(f"  XML parse error in {filepath.name}: {e}", file=sys.stderr)
        return None

    root = tree.getroot()
    file_id = root.attrib.get("{http://www.w3.org/XML/1998/namespace}id", filepath.stem)

    header = root.find(".//tei:teiHeader", NS)
    if header is None:
        return None

    title_elem = header.find(".//tei:biblStruct/tei:analytic/tei:title", NS)
    if title_elem is None or not title_elem.text:
        return None

    headline_text = title_elem.text.strip()

    date_elem = header.find(".//tei:biblStruct/tei:analytic/tei:date", NS)
    date = date_elem.attrib.get("when", date_elem.text) if date_elem is not None else None

    author_elem = header.find(".//tei:biblStruct/tei:analytic/tei:author", NS)
    author = author_elem.text if author_elem is not None and author_elem.text else None

    first_para = root.find(".//tei:body//tei:div/tei:p", NS)
    if first_para is None:
        first_para = root.find(".//tei:body//tei:p", NS)
    if first_para is None:
        return None

    body_tokens = extract_tokens_from_sentences(first_para)
    if not body_tokens:
        return None

    return {
        "file_id": file_id,
        "source_file": str(filepath),
        "date": date,
        "author": author,
        "headline_text": headline_text,
        "body_first_para": {
            "tokens": body_tokens,
            "token_count": len(body_tokens),
            "has_nominative_nominal": has_any_nominative(body_tokens),
            "nominative_count": count_nominative_nominals(body_tokens),
        },
    }


def find_xml_files(input_path: Path, limit: int = 50) -> list:
    """Find TEI-XML article files, skipping corpus/source index files."""
    xml_files = []
    for root_dir, dirs, files in os.walk(input_path):
        for fname in sorted(files):
            if not fname.endswith(".xml"):
                continue
            if fname.count("_") == 0:
                continue
            xml_files.append(Path(root_dir) / fname)
            if len(xml_files) >= limit:
                return xml_files
    return xml_files


def run_extract(args):
    """Phase 1: Extract headline text and tagged body from IGC XML files."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Scanning for XML files in {input_path}...")
    xml_files = find_xml_files(input_path, limit=args.limit)
    print(f"Found {len(xml_files)} XML files")

    pairs = []
    skipped = 0
    for i, filepath in enumerate(xml_files):
        if args.verbose:
            print(f"  [{i+1}/{len(xml_files)}] Parsing {filepath.name}...")

        pair = parse_tei_file(filepath)
        if pair is not None:
            pairs.append(pair)
            if args.verbose:
                b_nom = "✓" if pair["body_first_para"]["has_nominative_nominal"] else "✗"
                print(f"    → body nom: {b_nom}  headline: {pair['headline_text'][:60]}...")
        else:
            skipped += 1

    print(f"\nExtracted {len(pairs)} pairs (skipped {skipped} files)")

    if not pairs:
        print("No pairs found.", file=sys.stderr)
        sys.exit(1)

    # Build output
    output = {
        "metadata": {
            "description": "Extracted headline text + POS-tagged body from IGC news corpus",
            "corpus_version": "IGC-News1 22.10 (annotated)",
            "project": "stylometry-icelandiceval",
            "phase": "extract",
            "note": "Headlines are plain text — need LLM tagging before analysis.",
        },
        "headlines_for_tagging": [
            {"index": i, "file_id": p["file_id"], "text": p["headline_text"]}
            for i, p in enumerate(pairs)
        ],
        "pairs": pairs,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Results saved to {output_path}")

    # Also print headlines in a format ready for LLM tagging
    print("\n" + "=" * 65)
    print("HEADLINES FOR LLM TAGGING")
    print("=" * 65)
    for i, p in enumerate(pairs):
        print(f"  {i+1:3d}. {p['headline_text']}")
    print("=" * 65)
    print(f"\n{len(pairs)} headlines need IFD POS tagging.")
    print("Copy the headlines_for_tagging array from the JSON output")
    print("and use it with the LLM tagging prompt.")


# ─── Phase 2: Analyze ───────────────────────────────────────────────────────

def run_analyze(args):
    """Phase 2: Merge LLM-tagged headlines with body data and compute stats."""
    pairs_path = Path(args.input)
    tagged_path = Path(args.tagged)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load extracted pairs
    with open(pairs_path, encoding="utf-8") as f:
        extracted = json.load(f)
    pairs = extracted["pairs"]

    # Load LLM-tagged headlines
    with open(tagged_path, encoding="utf-8") as f:
        tagged_data = json.load(f)

    # The tagged file should be a list of objects with index + tokens
    tagged_headlines = tagged_data if isinstance(tagged_data, list) else tagged_data.get("tagged_headlines", [])

    # Build index lookup
    tagged_by_index = {}
    for th in tagged_headlines:
        tagged_by_index[th["index"]] = th["tokens"]

    # Merge and analyze
    results = []
    matched = 0
    for i, pair in enumerate(pairs):
        headline_tokens = tagged_by_index.get(i, [])
        if headline_tokens:
            matched += 1

        h_nom_count = count_nominative_nominals(headline_tokens)
        h_has_nom = h_nom_count > 0

        result = {
            "file_id": pair["file_id"],
            "date": pair["date"],
            "author": pair["author"],
            "headline": {
                "text": pair["headline_text"],
                "tokens": headline_tokens,
                "token_count": len(headline_tokens),
                "has_nominative_nominal": h_has_nom,
                "nominative_count": h_nom_count,
            },
            "body_first_para": pair["body_first_para"],
        }
        results.append(result)

    # Compute statistics
    total = len(results)
    tagged_results = [r for r in results if r["headline"]["token_count"] > 0]
    tagged_count = len(tagged_results)

    headline_has_nom = sum(1 for r in tagged_results if r["headline"]["has_nominative_nominal"])
    body_has_nom = sum(1 for r in results if r["body_first_para"]["has_nominative_nominal"])

    headline_drop = 1 - (headline_has_nom / tagged_count) if tagged_count > 0 else None
    body_drop = 1 - (body_has_nom / total)

    avg_h_nom = sum(r["headline"]["nominative_count"] for r in tagged_results) / tagged_count if tagged_count else 0
    avg_b_nom = sum(r["body_first_para"]["nominative_count"] for r in results) / total

    avg_h_len = sum(r["headline"]["token_count"] for r in tagged_results) / tagged_count if tagged_count else 0
    avg_b_len = sum(r["body_first_para"]["token_count"] for r in results) / total

    h_tok_total = sum(r["headline"]["token_count"] for r in tagged_results)
    b_tok_total = sum(r["body_first_para"]["token_count"] for r in results)

    nom_per_tok_h = sum(r["headline"]["nominative_count"] for r in tagged_results) / h_tok_total if h_tok_total else 0
    nom_per_tok_b = sum(r["body_first_para"]["nominative_count"] for r in results) / b_tok_total if b_tok_total else 0

    stats = {
        "total_pairs": total,
        "headlines_tagged": tagged_count,
        "headline_subject_drop_rate": round(headline_drop, 4) if headline_drop is not None else None,
        "body_subject_drop_rate": round(body_drop, 4),
        "headline_has_nominative_nominal": headline_has_nom,
        "body_has_nominative_nominal": body_has_nom,
        "avg_nominative_per_headline": round(avg_h_nom, 2),
        "avg_nominative_per_body_para": round(avg_b_nom, 2),
        "avg_headline_tokens": round(avg_h_len, 1),
        "avg_body_para_tokens": round(avg_b_len, 1),
        "nom_per_token_headline": round(nom_per_tok_h, 4),
        "nom_per_token_body": round(nom_per_tok_b, 4),
    }

    # Print summary
    print("\n" + "=" * 65)
    print("SUBJECT DROP ANALYSIS — HEADLINE vs BODY")
    print("=" * 65)
    print(f"Total pairs:                    {stats['total_pairs']}")
    print(f"Headlines tagged:               {stats['headlines_tagged']}")
    print()
    if stats["headline_subject_drop_rate"] is not None:
        print(f"Headline subject drop rate:     {stats['headline_subject_drop_rate']:.1%}")
        print(f"  (no nominative nominal in     "
              f"{tagged_count - headline_has_nom} / {tagged_count} headlines)")
    print(f"Body subject drop rate:         {stats['body_subject_drop_rate']:.1%}")
    print(f"  (no nominative nominal in     "
          f"{total - body_has_nom} / {total} first paragraphs)")
    print()
    print(f"Avg nominative nominals:")
    print(f"  per headline:                 {stats['avg_nominative_per_headline']}")
    print(f"  per body paragraph:           {stats['avg_nominative_per_body_para']}")
    print()
    print(f"Avg tokens:")
    print(f"  per headline:                 {stats['avg_headline_tokens']}")
    print(f"  per body paragraph:           {stats['avg_body_para_tokens']}")
    print()
    print(f"Nominative nominals per token:")
    print(f"  headline:                     {stats['nom_per_token_headline']:.4f}")
    print(f"  body:                         {stats['nom_per_token_body']:.4f}")
    print("=" * 65)

    # Save output
    output = {
        "metadata": {
            "description": "Subject drop analysis: headline vs body text",
            "corpus_version": "IGC-News1 22.10 (annotated)",
            "project": "stylometry-icelandiceval",
            "phase": "analyze",
            "headline_tagging": "Sonnet 4.6 (IFD tagset)",
            "body_tagging": "ABLTagger (from IGC corpus)",
            "methodology": (
                "Subject presence approximated by nominative-case nominals "
                "(nouns, pronouns, adjectives, articles) using IFD POS tags."
            ),
        },
        "statistics": stats,
        "pairs": results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to {output_path}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Extract and analyze headline subject drop from IGC news."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Phase 1: extract
    p_extract = subparsers.add_parser("extract", help="Extract headlines + body from IGC XML")
    p_extract.add_argument("--input", "-i", required=True, help="Path to IGC news XML directory")
    p_extract.add_argument("--output", "-o", default="output/extracted_pairs.json", help="Output JSON path")
    p_extract.add_argument("--limit", "-n", type=int, default=50, help="Max files to process")
    p_extract.add_argument("--verbose", "-v", action="store_true")

    # Phase 2: analyze
    p_analyze = subparsers.add_parser("analyze", help="Merge tagged headlines and compute stats")
    p_analyze.add_argument("--input", "-i", required=True, help="Path to extracted_pairs.json")
    p_analyze.add_argument("--tagged", "-t", required=True, help="Path to tagged_headlines.json")
    p_analyze.add_argument("--output", "-o", default="output/headline_analysis.json", help="Output JSON path")

    args = parser.parse_args()

    if args.command == "extract":
        run_extract(args)
    elif args.command == "analyze":
        run_analyze(args)


if __name__ == "__main__":
    main()