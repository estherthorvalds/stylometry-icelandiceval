#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
dim10_lix.py — VÍDD 10: Læsilegsskor (LIX readability)
==========================================================

TILGANGUR / PURPOSE:
    Þessi skrifta reiknar LIX-læsilegskori (Läsbarhetsindex) úr
    textaskrám. LIX er klassísk sænsk læsilegsmæling sem sameinar
    orðalengd og setningalengd í eina tölu.

    This script computes the LIX readability score (Läsbarhetsindex)
    from raw text files. LIX is a classic Swedish readability metric
    that combines word length and sentence length into a single number.

    FORMÚLA / FORMULA:
        LIX = (orð / setningar) + (löng_orð / orð × 100)
            = (words / sentences) + (long_words / words × 100)

    þar sem „löng orð“ = orð með FLEIRI EN 6 stafi (staðlaður LIX-þröskuldur).
    Note: the standard LIX threshold is > 6 characters (i.e., 7+).
    Ath. Steingrímur Steinþórsson breytti staðlinum í 8 fyrir íslenska texta
    en hér höldum við okkur við 6 stafi vegna dim6 sem notar ≥ 8 stafi.

FYRIRVARI — KVÖRÐUN / CALIBRATION CAVEAT:
    LIX var upphaflega kvörðuð fyrir SÆNSKU og staðlaðir þröskuldar
    (< 30 = mjög auðvelt, > 60 = mjög erfitt) endurspegla sænska texta.
    Íslenska hefur (a) virkara samsetningarkerfi (fleiri löng orð) og
    (b) oft lengri setningar, svo hrávirðin fyrir íslensku eru líklega
    HÆRRI en fyrir sænsku af aðferðafræðilegum ástæðum — ekki vegna
    þess að textinn sé „ólæsari“. Þröskuldarnir eru birtir hér til
    HLIÐSJÓNAR, ekki sem kvörðuð skilgreining.

    LIX was originally calibrated for Swedish; standard thresholds
    reflect Swedish prose. For Icelandic, expect systematically higher
    raw scores due to compounding and longer sentences. Thresholds are
    shown as rough guides only — Icelandic baselines need to be
    established empirically from benchmark data itself.

HLUTVERK DIM10 Í VERKEFNINU / ROLE IN BENCHMARK:
    Dim10 er birt SAMHLIÐA dim6 (meðalorðalengd) sem hliðstætt
    kandídatamerki. Tilgangurinn er tvíþættur:
        (a) klassísk læsilegsmæling í sjálfu sér,
        (b) samanburður við dim6: hvort sambandið orð×setningar gefi
            meira greinandi afl en orðalengd ein og sér.
    Niðurstöðurnar úr þessum samanburði munu ákvarða hvort dim10
    haldist áfram sem sér-vídd í framhaldsverkefni (MA-verkefni) eða
    hvort dim6 ein nægi. Annað hvort gæti dottið út — eða bæði.

    Dim10 is kept as a PARALLEL candidate to dim6. Whether to retain
    it in the MA-thesis dimension set depends on whether its
    correlation with dim6 is strong enough that one subsumes the other.

AÐFERÐ / METHOD:
    1. Lesa hráan texta úr .txt skrá
    2. Skipta í setningar með `tokenizer.split_into_sentences`
       (Miðeind-pakkinn sem kann íslenskar skammstafanir t.d., o.s.frv.)
    3. Telja orð með nákvæmlega sömu reglum og dim6:
         - split á hvítbili
         - strippa kantagreinarmerki (PUNCT_TO_STRIP)
         - sleppa tókum án bókstafs (HAS_LETTER)
    4. Telja „löng orð“ (lengd > 6 stafir)
    5. Reikna LIX-formúluna

AF HVERJU `tokenizer`-PAKKINN? / WHY THE `tokenizer` PACKAGE?
    Barefn regex á .!? brýtur á íslenskum skammstöfunum eins og
    „þ.e.“, „o.s.frv.“, „t.d.“, „m.a.“ og á tugabrotum („3,14“).
    Miðeind-pakkinn `tokenizer` kann þessar reglur og gefur áreiðanlegar
    setningaskil. Sama forsenda er notuð í öðrum verkefnum Miðeindar.

INNTAK / INPUT:
    Hreinar textaskrár (.txt) — t.d. úr:
        data/experiment/human_reference/
        data/experiment/llm_continuations_preprocessed/{model}/

ÚTTAK / OUTPUT:
    1. CSV-skrá: output/dim10_lix.csv
    2. Tafla á skipanalínu

KEYRSLA / USAGE:
    python scripts/dim10_lix.py --text-dir data/experiment/human_reference/
    python scripts/dim10_lix.py --files file1.txt file2.txt
    python scripts/dim10_lix.py --text-dir ... --dry-run
    python scripts/dim10_lix.py --text-dir ... --debug
"""

import argparse
import csv
from pathlib import Path

from tokenizer import split_into_sentences

# Samnýtum tokenization-reglur dim6 beint — enginn samhliða skilgreining.
# Reusing dim6 tokenization rules verbatim ensures clean dim6↔dim10
# comparisons (same word counts, same long-word denominator).
from dim6_word_length import PUNCT_TO_STRIP, HAS_LETTER, mean


# ============================================================
# LIX-ÞRÖSKULDUR FYRIR LÖNG ORÐ / LIX LONG-WORD THRESHOLD
# ============================================================
# Staðlað LIX notar „fleiri en 6 stafi“ (þ.e. 7+). Þetta er
# ÖÐRUVÍSI en dim6 (≥ 8 stafir) og er viljandi haldið svo
# LIX-formúlan hafi nákvæmlega sömu merkingu og í sænsku
# upprunalegri.
# ============================================================

LIX_LONG_WORD_THRESHOLD = 6  # „more than 6 characters“ → length > 6


# ============================================================
# SETNINGASKILMING / SENTENCE SPLITTING
# ============================================================

def split_sentences(text: str) -> list[str]:
    """Skipta texta í setningar með tokenizer-pakka Miðeindar.

    Notar `tokenizer.split_into_sentences` sem tekur tillit til
    íslenskra skammstafana (þ.e., o.s.frv., t.d., m.a., o.fl.) og
    tugabrota („3,14“, „1.000“). Barefn regex á .!? nær EKKI þessum
    mynstrum og myndi ofmæla setningar.

    Args:
        text: Hráður texti.

    Returns:
        Listi af setningum sem hver er strengur. Tómar setningar
        síaðar burt.
    """
    sentences = [s.strip() for s in split_into_sentences(text)]
    return [s for s in sentences if s]


# ============================================================
# ORÐATALNING — ENDURTEKUR DIM6-REGLUR / WORD COUNT (dim6 rules)
# ============================================================

def count_words(text: str) -> tuple[int, int, list[str]]:
    """Telja orð og „löng orð“ með nákvæmlega dim6-reglum.

    ÞREP / STEPS:
        1. Skipta á hvítbili → listi af tókum
        2. Fjarlægja kantagreinarmerki með PUNCT_TO_STRIP
        3. Sleppa tókum án bókstafs (HAS_LETTER)
        4. Telja orð og þau sem eru lengri en 6 stafir

    Args:
        text: Hráður texti.

    Returns:
        (total_words, long_words, words) þar sem:
            - total_words: Heildarfjöldi gildra orða.
            - long_words: Fjöldi orða með lengd > 6 stafi.
            - words: Listi af hreinsuðum orðum (fyrir debug-útprentun).
    """
    words: list[str] = []
    long_words = 0

    for tok in text.split():
        cleaned = tok.strip(PUNCT_TO_STRIP)
        if not cleaned:
            continue
        if not HAS_LETTER.search(cleaned):
            continue
        words.append(cleaned)
        if len(cleaned) > LIX_LONG_WORD_THRESHOLD:
            long_words += 1

    return len(words), long_words, words


# ============================================================
# AÐALMÆLING / MAIN MEASUREMENT
# ============================================================

def measure_lix(
    text_file: Path,
    debug: bool = False,
) -> dict:
    """Reikna LIX-læsilegskori úr einni textaskrá.

    MÆLINGAR:
        - total_words: Heildarfjöldi gildra orða (dim6-reglur)
        - total_sentences: Fjöldi setninga (tokenizer-pakki)
        - mean_sentence_length: Orð per setningu
        - pct_long_words: Hlutfall orða með > 6 stafi (LIX-skilgreining)
        - lix_score: Heildarskor (orð/setn + pct_long_words)

    FORMÚLA:
        LIX = (words / sentences) + (long_words / words × 100)

    AÐVÖRUN: Ef textinn hefur færri en 5 setningar er prentuð
    viðvörun — stutt textabrot gefa óáreiðanlegan LIX-skor.

    Args:
        text_file: Slóð á .txt skrá.
        debug: Ef True, prenta fyrstu 5 setningar og lengstu 5 orðin.

    Returns:
        Dict með mælingum (sjá ofan). Lykill `filename` er bætt við.
    """
    if not text_file.exists():
        raise FileNotFoundError(f"Textaskrá fannst ekki: {text_file}")

    text = text_file.read_text(encoding='utf-8')

    # Setningaskilming
    sentences = split_sentences(text)
    total_sentences = len(sentences)

    # Orðatalning (dim6-reglur)
    total_words, long_words, words = count_words(text)

    # Aðvörun fyrir stutta texta
    if total_sentences < 5:
        print(
            f"  AÐVÖRUN: {text_file.name} hefur aðeins "
            f"{total_sentences} setningu(r) — LIX-skor er óáreiðanlegt "
            f"fyrir svona stutta texta."
        )

    # Verjumst deilingu með núlli
    if total_sentences == 0 or total_words == 0:
        mean_sent_len = 0.0
        pct_long = 0.0
        lix_score = 0.0
    else:
        mean_sent_len = total_words / total_sentences
        pct_long = (long_words / total_words) * 100
        lix_score = mean_sent_len + pct_long

    if debug:
        print(f"\n  [DEBUG] Skrá: {text_file.name}")
        print(
            f"  [DEBUG] Orð: {total_words}, Setningar: {total_sentences}, "
            f"Löng orð (>{LIX_LONG_WORD_THRESHOLD}): {long_words}"
        )
        print(
            f"  [DEBUG] Meðalsetningalengd: {mean_sent_len:.2f} orð, "
            f"Hlutfall langra orða: {pct_long:.1f}%"
        )
        print(f"  [DEBUG] LIX = {lix_score:.2f}")

        # Fyrstu 5 setningar — til að athuga setningaskilming
        print(f"  [DEBUG] Fyrstu 5 setningar:")
        for i, s in enumerate(sentences[:5], 1):
            snippet = s if len(s) <= 100 else s[:100] + '…'
            print(f"    {i}. {snippet}")

        # 5 lengstu orðin — til að athuga tókunarvinnslu
        if words:
            longest = sorted(set(words), key=len, reverse=True)[:5]
            print(
                f"  [DEBUG] 5 lengstu orðin: "
                f"{[f'{w}({len(w)})' for w in longest]}"
            )

    return {
        'filename': text_file.name,
        'total_words': total_words,
        'total_sentences': total_sentences,
        'mean_sentence_length': mean_sent_len,
        'pct_long_words': pct_long,
        'lix_score': lix_score,
    }


# ============================================================
# VISTA NIÐURSTÖÐUR SEM CSV / SAVE RESULTS AS CSV
# ============================================================

def save_results_csv(
    results: list[dict],
    output_path: Path,
) -> None:
    """Vista niðurstöður sem CSV-skrá.

    Dálkar:
        filename, total_words, total_sentences,
        mean_sentence_length, pct_long_words, lix_score

    Args:
        results: Listi af dict frá measure_lix.
        output_path: Slóð á CSV-skrá.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'filename',
        'total_words',
        'total_sentences',
        'mean_sentence_length',
        'pct_long_words',
        'lix_score',
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            row_out = dict(row)
            row_out['mean_sentence_length'] = (
                f"{row['mean_sentence_length']:.2f}"
            )
            row_out['pct_long_words'] = f"{row['pct_long_words']:.1f}"
            row_out['lix_score'] = f"{row['lix_score']:.2f}"
            writer.writerow(row_out)


# ============================================================
# PRENTA TÖFLU / PRINT TABLE
# ============================================================

def print_results_table(results: list[dict]) -> None:
    """Prenta niðurstöður á skipanalínu sem töflu.

    Args:
        results: Listi af dict frá measure_lix.
    """
    print(f"\nVÍDD 10: LIX-læsilegskor (Läsbarhetsindex)")
    print("=" * 90)

    # Hauslína / Header
    print(
        f"  {'Skrá':<35} {'Orð':<7} {'Setn.':<6} "
        f"{'Mlengd':<8} {'>6staf%':<8} {'LIX':<7}"
    )
    print(
        f"  {'-'*35} {'-'*7} {'-'*6} {'-'*8} {'-'*8} {'-'*7}"
    )

    for r in results:
        print(
            f"  {r['filename']:<35} "
            f"{r['total_words']:<7} "
            f"{r['total_sentences']:<6} "
            f"{r['mean_sentence_length']:<8.2f} "
            f"{r['pct_long_words']:<8.1f} "
            f"{r['lix_score']:<7.2f}"
        )

    # --- MEÐALTÖL / AVERAGES ---
    if results:
        avg_sent = mean([r['mean_sentence_length'] for r in results])
        avg_pct = mean([r['pct_long_words'] for r in results])
        avg_lix = mean([r['lix_score'] for r in results])
        print(
            f"  {'-'*35} {'-'*7} {'-'*6} {'-'*8} {'-'*8} {'-'*7}"
        )
        print(
            f"  {'MEÐALTAL':<35} "
            f"{'':7} "
            f"{'':6} "
            f"{avg_sent:<8.2f} "
            f"{avg_pct:<8.1f} "
            f"{avg_lix:<7.2f}"
        )

    print("=" * 90)
    print()
    print("  SKÝRING DÁLKA / COLUMN KEY:")
    print("    Orð     = Fjöldi gildra orða (dim6-reglur)")
    print("    Setn.   = Fjöldi setninga (tokenizer-pakki Miðeindar)")
    print("    Mlengd  = Meðalsetningalengd (orð / setningar)")
    print("    >6staf% = Hlutfall orða með FLEIRI EN 6 stafi "
          "(LIX-skilgreining)")
    print("    LIX     = Mlengd + >6staf% (Läsbarhetsindex)")
    print()
    print("  TÚLKUN (LIX-ÞRÖSKULDAR — KVÖRÐAÐIR FYRIR SÆNSKU):")
    print("    LIX < 30    → mjög auðvelt (barnabækur, samræður)")
    print("    LIX 30–40   → auðvelt (skáldskapur, blogg)")
    print("    LIX 40–50   → miðlungs (fréttir, almennir textar)")
    print("    LIX 50–60   → erfitt (formlegt, fræðilegt)")
    print("    LIX > 60    → mjög erfitt (lagatextar, tæknitextar)")
    print()
    print("  ATHUGIÐ / NOTE:")
    print("    Þessir þröskuldar eru kvörðaðir fyrir SÆNSKU. Íslenskir")
    print("    textar ná kerfisbundið hærri LIX-gildum vegna (a) virkara")
    print("    samsetningarkerfis (fleiri löng orð) og (b) oft lengri")
    print("    setninga. Þröskuldarnir hér eru GRÓFIR vísar — íslenskir")
    print("    kvörðunarþröskuldar þurfa að byggjast á reynslugögnum úr")
    print("    mæliprófinu sjálfu.")
    print()
    print("    LIX thresholds are Swedish-calibrated. Icelandic baselines")
    print("    must be established empirically from the benchmark itself.")


# ============================================================
# FINNA ALLAR TEXTASKRÁR / FIND ALL TEXT FILES
# ============================================================

def find_text_files(text_dir: Path) -> list[Path]:
    """Finna allar .txt skrár í möppu (endurkvæmt).

    Args:
        text_dir: Mappa með textaskrám.

    Returns:
        Raðaður listi af Path-hlutum.
    """
    txt_files = sorted(text_dir.rglob('*.txt'))

    if not txt_files:
        print(f"  AÐVÖRUN: Engar .txt skrár fundust í {text_dir}")

    return txt_files


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra LIX-mælingu á textaskrám."""
    parser = argparse.ArgumentParser(
        description=(
            "Vídd 10: Reikna LIX-læsilegskor "
            "(Läsbarhetsindex, Swedish-calibrated)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Á möppu:
  python scripts/dim10_lix.py \\
      --text-dir data/experiment/human_reference/

  # Á tilgreindum skrám:
  python scripts/dim10_lix.py \\
      --files data/experiment/human_reference/news_ref_001.txt

  # Með villuleit (sýnir setningaskilming og lengstu orð):
  python scripts/dim10_lix.py \\
      --text-dir data/experiment/human_reference/ --debug

  # Dry-run (reikna, prenta, ekki vista CSV):
  python scripts/dim10_lix.py \\
      --text-dir data/experiment/human_reference/ --dry-run
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--text-dir',
        type=Path,
        help="Mappa með textaskrám (.txt). Leit er endurkvæm."
    )
    group.add_argument(
        '--files',
        type=Path,
        nargs='+',
        help="Ein eða fleiri textaskrár til að greina."
    )

    parser.add_argument(
        '--output-csv',
        type=Path,
        default=Path('output/dim10_lix.csv'),
        help="Slóð á CSV-úttaksskrá (sjálfgefið: output/dim10_lix.csv)"
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Prenta fyrstu 5 setningar og lengstu 5 orðin per skrá."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Reikna og prenta — ekki vista CSV."
    )

    args = parser.parse_args()

    # --- FINNA SKRÁR ---
    if args.text_dir:
        if not args.text_dir.is_dir():
            print(f"VILLA: Mappa finnst ekki: {args.text_dir}")
            return
        text_files = find_text_files(args.text_dir)
    else:
        text_files = args.files
        for f in text_files:
            if not f.exists():
                print(f"VILLA: Skrá finnst ekki: {f}")
                return

    if not text_files:
        print("VILLA: Engar skrár til að greina.")
        return

    print(f"\n  Greini {len(text_files)} skrá(r)...")
    if args.debug:
        print("  [DEBUG] Villuleitarhamur virkur")

    # --- KEYRA MÆLINGU ---
    results = []
    for tf in text_files:
        result = measure_lix(tf, debug=args.debug)
        results.append(result)

    # --- PRENTA TÖFLU ---
    print_results_table(results)

    # --- VISTA CSV (NEMA DRY-RUN) ---
    if args.dry_run:
        print("\n  [dry-run] CSV ekki vistað.")
    else:
        save_results_csv(results, args.output_csv)
        print(f"\n  CSV vistað: {args.output_csv}")


if __name__ == "__main__":
    main()
