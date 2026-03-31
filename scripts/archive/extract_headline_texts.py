#!/usr/bin/env python3
"""
extract_headline_texts.py — Extract plain headline texts from IGC news XML,
split into batches for repeated experiments.

Usage:
    python3 scripts/extract_headline_texts.py \
        -i "data/raw/IGC-News1 22.10 (annotated version)/IGC-News1-22.10.ana" \
        -o output/batches \
        --batch-size 40 \
        --num-batches 15
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

URI = "http://www.tei-c.org/ns/1.0"
NS = {"tei": URI}


def extract_headline(filepath: Path) -> str | None:
    """Extract headline text from a single TEI-XML file."""
    try:
        tree = ET.parse(filepath)
    except ET.ParseError:
        return None

    root = tree.getroot()
    header = root.find(".//tei:teiHeader", NS)
    if header is None:
        return None

    title_elem = header.find(".//tei:biblStruct/tei:analytic/tei:title", NS)
    if title_elem is None or not title_elem.text:
        return None

    return title_elem.text.strip()


def find_article_xmls(input_path: Path) -> list:
    """Find all article XML files (those with _ in the name)."""
    xml_files = []
    for root_dir, dirs, files in os.walk(input_path):
        for fname in sorted(files):
            if fname.endswith(".xml") and "_" in fname:
                xml_files.append(Path(root_dir) / fname)
    return xml_files


def main():
    parser = argparse.ArgumentParser(
        description="Extract headline texts from IGC and split into batches."
    )
    parser.add_argument("--input", "-i", required=True, help="Path to IGC news XML directory")
    parser.add_argument("--output", "-o", default="output/batches", help="Output directory for batch files")
    parser.add_argument("--batch-size", "-b", type=int, default=40, help="Headlines per batch (default: 40)")
    parser.add_argument("--num-batches", "-n", type=int, default=15, help="Number of batches (default: 15)")

    args = parser.parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    total_needed = args.batch_size * args.num_batches
    print(f"Need {total_needed} headlines ({args.num_batches} batches × {args.batch_size})")

    # Find all article XMLs
    print(f"Scanning {input_path}...")
    xml_files = find_article_xmls(input_path)
    print(f"Found {len(xml_files)} XML files")

    # Extract headlines
    headlines = []
    for filepath in xml_files:
        h = extract_headline(filepath)
        if h:
            headlines.append(h)
        if len(headlines) >= total_needed:
            break

    print(f"Extracted {len(headlines)} headlines")

    if len(headlines) < total_needed:
        print(f"Warning: only {len(headlines)} available, need {total_needed}", file=sys.stderr)
        actual_batches = len(headlines) // args.batch_size
        print(f"Can produce {actual_batches} full batches")
    else:
        actual_batches = args.num_batches

    # Split into batches and save
    for batch_num in range(actual_batches):
        start = batch_num * args.batch_size
        end = start + args.batch_size
        batch = headlines[start:end]

        batch_data = {
            "batch": batch_num + 1,
            "headlines": [
                {"index": i, "text": h}
                for i, h in enumerate(batch)
            ]
        }

        batch_file = output_dir / f"batch_{batch_num + 1:02d}.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=2)

        print(f"  Batch {batch_num + 1:2d}: headlines {start+1}–{end} → {batch_file}")

    print(f"\n{actual_batches} batch files saved to {output_dir}/")


if __name__ == "__main__":
    main()