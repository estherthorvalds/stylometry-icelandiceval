#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
dim6_word_length.py — VÍDD 6: Meðalorðalengd (mean word length)
=================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta mælir meðalorðalengd (í stöfum) í hráum textaskrám.
    Þetta er einföld en áhrifarík yfirborðsmæling (surface-level feature)
    sem greinir á milli textategunda án þáttara.

    This script measures average word length in characters from raw text
    files. Unlike dim1–dim5, this does NOT use parsed output — it works
    directly on plain text.

MÁLVÍSINDI / LINGUISTICS:
    Orðalengd er klassískur mælikvarði í stílfræði (stylometry) og
    textaflokkunarverkefnum. Lengri orð eru algengari í formlegum,
    fræðilegum og tæknilegum textum. Styttri orð eru algengari í
    hversdagslegu máli, bloggum og samræðum.

    HVERS VEGNA ÞETTA VIRKAR SÉRSTAKLEGA VEL Í ÍSLENSKU:
        Íslenska hefur mjög virkt samsetningarkerfi (productive compounding).
        Fræðilegur texti notar oft mjög löng samsett orð sem hlaða mörgum
        merkingum í eitt orð:

            „heilbrigðisþjónustukerfi" = 25 stafir
            (heilbrigðis + þjónustu + kerfi = health service system)

            „loftslagsbreytingastefna" = 24 stafir
            (loftsags + breytinga + stefna = climate change policy)

            „félagsvísindastofnun" = 21 stafir
            (félags + vísinda + stofnun = social science institute)

        Í hversdagslegu máli og bloggum eru þessi samsett orð mun sjaldgæfari.
        Þess vegna er munurinn á meðalorðalengd milli textategunda yfirleitt
        MEIRI í íslensku en í ensku.

    VÆNTAR NIÐURSTÖÐUR:
    - Fræðitextar (Læknablaðið): LENGST — tæknileg samsett orð, formlegt mál
    - Fréttir (RÚV): Á MILLI — formlegt en aðgengilegt
    - Blogg (Jonas.is): STYST — hversdagslegt, óformlegt mál

    TENGSL VIÐ BIBER-RAMMA / CONNECTION TO BIBER'S MDA:
        Biber (1988) notaði „mean word length" sem einn af vísunum á
        „Informational Production" víddinni. Lengri orð = meiri
        upplýsingaþéttleiki. Stutt, algeng orð = meira „involvement"
        (persónulegur, samræðutengdur texti).

AÐFERÐ / METHOD:
    1. Lesa hráan texta úr .txt skrám
    2. Skipta í tóka (tokens) á hvítbili
    3. Fjarlægja greinarmerki frá köntum hvers tóka
    4. Sleppa tókum sem eru ALGJÖRLEGA greinarmerki eða tölur
    5. Mæla lengd hvers orðs og reikna meðaltal, miðgildi, staðalfrávik

    GREINARMERKI SEM FJARLÆGÐ ERU / PUNCTUATION STRIPPED:
        . , ; : ! ? „ " " « » ( ) [ ] { } – — - / ... ,,
        AÐEINS frá köntum (leading/trailing), EKKI inni í orði.
        „Nýju-Delí" heldur bandstrikinu → 9 stafir.

INNTAK / INPUT:
    Hreinir textaskrár (.txt) — t.d. úr:
        data/human_texts/
        data/experiment/human_reference/
        data/experiment/llm_continuations_clean/

ÚTTAK / OUTPUT:
    1. CSV-skrá: output/dim6_word_length.csv
    2. Tafla á skipanalínu

KEYRSLA / USAGE:
    python scripts/dim6_word_length.py --text-dir data/experiment/human_reference/
    python scripts/dim6_word_length.py --text-dir data/experiment/llm_continuations_clean/gpt_5/
    python scripts/dim6_word_length.py --files data/human_texts/news/news_001.txt

    # Sem innflutt eining:
    from dim6_word_length import measure_word_length
    result = measure_word_length(Path("data/experiment/human_reference/news_ref_001.txt"))
"""

import argparse
import csv
import math
import re
from pathlib import Path


# ============================================================
# GREINARMERKI SEM FJARLÆGÐ ERU / PUNCTUATION TO STRIP
# ============================================================
# Við fjarlægjum greinarmerki frá KÖNTUM tóka (leading/trailing)
# en HÖLDUM í greinarmerki sem eru INNI Í orðum.
#
# Dæmi:
#   „Gunnarsdóttir,"  →  Gunnarsdóttir   (komma og gæsalappir fjarlægð)
#   "sagði."           →  sagði            (punktur og gæsalappir fjarlægð)
#   Nýju-Delí          →  Nýju-Delí       (bandstrik haldið — inni í orði)
#   50%                →  (sleppt — tölustafur)
#   ...                →  (sleppt — aðeins greinarmerki)
#
# Python str.strip() tekur streng af stöfum og fjarlægir alla
# þá stafi sem koma FRAMAN og AFTAN við strenginn. Þetta er
# nákvæmlega rétta hegðunin hér: fjarlægja alla kantamerki.
#
# Við notum stórt mengi greinarmerki til að ná yfir:
# - Íslenskar gæsalappir: „ " „ " (alveg öðruvísi en enskar)
# - Tvöföld komma sem hefst á gæsalöppum: ,,
# - Langt strik (em-dash): —
# - Stutt strik (en-dash): –
# - Venjuleg greinarmerki: . , ; : ! ?
# - Svigar: ( ) [ ] { }
# - Tilvitnunarmerki: « » " ' " " ' '
# - Skástrik og punktar: / ...
# ============================================================

PUNCT_TO_STRIP = (
    '.,;:!?'           # Algeng greinarmerki
    '„"""\'''«»'       # Gæsalappir / tilvitnunarmerki (íslensku og enskar)
    '()[]{}'            # Svigar
    '–—-'              # Strik (en-dash, em-dash, venjulegt bandstrik)
    '/'                 # Skástrik
    '…'                # Úrfellingarpunktar (Unicode)
    '\u200b'           # Zero-width space (getur slæðst inn úr XML)
)

# Regex til að athuga hvort tóki sé ALGJÖRLEGA greinarmerki eða bil.
# Ef allir stafir eru í þessu mengi, þá er tókinn ekki orð.
# \d nær yfir tölustafi, \W nær yfir allt sem er ekki orð-stafur,
# en þar sem við viljum einnig sleppa hreinum tölum, notum við
# sérsniðna nálgun.
#
# Nálgun: Eftir að kantamerki hafa verið fjarlægð, athugum við:
#   1. Er tókinn tómur? → sleppa
#   2. Inniheldur tókinn ENGAN bókstaf? → sleppa (tölur, tákn)
#
# Þetta heldur í orð eins og „1,2" (ef þau berast) en sleppir
# hreinum tölustöfum eins og „2015" eða „3.000".
HAS_LETTER = re.compile(r'[a-záéíóúýþæöðA-ZÁÉÍÓÚÝÞÆÖÐ]')


# ============================================================
# ÞÁTTA TEXTA Í ORÐ / TOKENIZE TEXT INTO WORDS
# ============================================================

def tokenize_and_measure(text: str, debug: bool = False) -> list[int]:
    """Skipta texta í orð og mæla lengd hvers orðs.

    ÞREP / STEPS:
        1. Skipta á hvítbili → listi af tókum
        2. Fjarlægja kantamerki (leading/trailing punctuation)
        3. Sleppa tókum sem eru tómir, algjörlega greinarmerki, eða tölur
        4. Mæla lengd hvers orðs (í stöfum)

    GREINARMERKI-REGLUR / PUNCTUATION RULES:
        - Kantamerki fjarlægð: . , ; : ! ? „ " o.s.frv.
        - Bandstrik INNI Í orðum haldið: „Nýju-Delí" → 9 stafir
        - Úrfellingarpunktar fjarlægðir: „..." → tómt → sleppt

    Args:
        text: Hráður texti.
        debug: Ef True, prenta nokkur dæmi um tóka til villuleitar.

    Returns:
        Listi af heiltölum — lengd hvers gilds orðs í stöfum.
    """
    # Skipta á hvítbili. split() án viðfangs skiptir á öllum
    # hvítbilstegundum (bil, ný lína, flipa) og sleppir tómum strengjum.
    raw_tokens = text.split()

    if debug:
        print(f"  [DEBUG tokenize] Fjöldi hráa tóka: {len(raw_tokens)}")
        print(f"  [DEBUG tokenize] Fyrstu 10 tókar: {raw_tokens[:10]}")

    lengths = []
    skipped_punct = 0
    skipped_number = 0
    skipped_empty = 0

    for i, tok in enumerate(raw_tokens):
        # Skref 2: Fjarlægja kantamerki
        cleaned = tok.strip(PUNCT_TO_STRIP)

        # Skref 3a: Sleppa tómum strengjum (tókinn var aðeins greinarmerki)
        if not cleaned:
            skipped_punct += 1
            continue

        # Skref 3b: Sleppa tókum sem innihalda ENGAN bókstaf.
        # Þetta nær yfir hreinar tölur (2015, 3.000) og flóknar
        # tölustafasamsetningar (1,2%, 100-120).
        if not HAS_LETTER.search(cleaned):
            skipped_number += 1
            continue

        # Skref 4: Mæla lengd
        word_len = len(cleaned)
        lengths.append(word_len)

        # Debug: Sýna fyrstu 5 orðin sem voru mæld
        if debug and len(lengths) <= 5:
            print(f"  [DEBUG tokenize] Orð #{len(lengths)}: "
                  f"'{tok}' → '{cleaned}' → {word_len} stafir")

    if debug:
        print(f"  [DEBUG tokenize] Gild orð: {len(lengths)}, "
              f"sleppt greinarmerki: {skipped_punct}, "
              f"sleppt tölur: {skipped_number}")

    return lengths


# ============================================================
# TÖLFRÆÐIFÖLL / STATISTICAL FUNCTIONS
# ============================================================
# Við notum ENGIN ytri söfn (numpy, scipy) — aðeins stöðluð
# Python-söfn. Þetta heldur háðni (dependencies) í lágmarki.
# ============================================================

def mean(values: list[int | float]) -> float:
    """Reikna meðaltal (arithmetic mean).

    Args:
        values: Listi af tölum.

    Returns:
        Meðaltal. 0.0 ef listinn er tómur.
    """
    if not values:
        return 0.0
    return sum(values) / len(values)


def median(values: list[int | float]) -> float:
    """Reikna miðgildi (median).

    Ef jafnmörg gildi eru á báðar hliðar, skila meðaltali tveggja
    miðjugilda. Þetta er hefðbundin skilgreining á miðgildi.

    Args:
        values: Listi af tölum.

    Returns:
        Miðgildi. 0.0 ef listinn er tómur.
    """
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    else:
        return float(sorted_vals[mid])


def stdev(values: list[int | float]) -> float:
    """Reikna staðalfrávik (population standard deviation).

    Notar N-deilingu (population), ekki N-1 (sample), þar sem
    við mælum ALLAN textann, ekki úrtak úr honum.

    Args:
        values: Listi af tölum.

    Returns:
        Staðalfrávik. 0.0 ef listinn hefur færri en 2 gildi.
    """
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


# ============================================================
# AÐALMÆLING / MAIN MEASUREMENT
# ============================================================

def measure_word_length(
    text_file: Path,
    debug: bool = False,
) -> dict:
    """Mæla orðalengd í einni textaskrá.

    MÆLINGAR:
        - total_words: Heildarfjöldi gildra orða (eftir síun)
        - mean_length: Meðalorðalengd í stöfum
        - median_length: Miðgildi orðalengdar
        - std_length: Staðalfrávik orðalengdar
        - pct_long_words: Hlutfall „langra orða" (8+ stafir)

    HVAÐ ER „LANGT ORÐ" (8+ STAFIR)?
        Þröskuldurinn 8 stafir er hefðbundinn í stílfræði (stylometry).
        Hann kemur úr rannsóknum á ensku og evrópskum tungumálum þar sem
        orð með 8+ stafi eru tiltölulega sjaldgæf í talmáli en algeng í
        fræðitextum. Á íslensku gæti þessi þröskuldur verið örlítið of
        lágur (vegna hins framleiðandi samsetningarkerfis), en við notum
        hann til samanburðar við alþjóðlegar rannsóknir.

    Args:
        text_file: Slóð á .txt skrá með hráum texta.
        debug: Ef True, prenta villuleitarupplýsingar.

    Returns:
        Dict með mælingum (sjá dálkalýsingu ofan).
    """
    if not text_file.exists():
        raise FileNotFoundError(f"Textaskrá fannst ekki: {text_file}")

    text = text_file.read_text(encoding='utf-8')

    if debug:
        print(f"\n  [DEBUG measure] Skrá: {text_file.name}")
        print(f"  [DEBUG measure] Stærð: {len(text)} stafir, "
              f"~{len(text.split())} tókar fyrir síun")

    # Mæla orðalengdir
    lengths = tokenize_and_measure(text, debug=debug)

    # --- REIKNA TÖLFRÆÐI / COMPUTE STATISTICS ---
    total_words = len(lengths)
    mean_len = mean(lengths)
    median_len = median(lengths)
    std_len = stdev(lengths)

    # Hlutfall langra orða (8+ stafir)
    # ÞRÖSKULDUR 8 STAFIR / 8-CHARACTER THRESHOLD:
    # Þetta er algengur þröskuldur í stílfræði frá Biber (1988),
    # Stamatatos (2009) og öðrum. Á íslensku þýðir þetta t.d.
    # orð eins og „forsætisráðherra" (18), „niðurstöður" (12),
    # „rannsóknir" (11), „sjúkdómum" (10) eru „löng".
    # Styttri orð eins og „sagði" (5), „var" (3), „það" (3)
    # eru „stutt".
    n_long = sum(1 for l in lengths if l >= 8)
    pct_long = (n_long / total_words * 100) if total_words > 0 else 0.0

    if debug:
        print(f"  [DEBUG measure] Meðaltal: {mean_len:.2f}, "
              f"Miðgildi: {median_len:.1f}, Staðalfr.: {std_len:.2f}")
        print(f"  [DEBUG measure] Löng orð (8+): {n_long} af "
              f"{total_words} ({pct_long:.1f}%)")
        # Sýna 5 lengstu orðin til skoðunar
        if lengths:
            # Finna raunverulegu orðin til birtingar
            word_len_pairs = []
            for tok in text.split():
                cleaned = tok.strip(PUNCT_TO_STRIP)
                if cleaned and HAS_LETTER.search(cleaned):
                    word_len_pairs.append((len(cleaned), cleaned))
            word_len_pairs.sort(reverse=True)
            top5 = word_len_pairs[:5]
            print(f"  [DEBUG measure] 5 lengstu orðin: "
                  f"{[f'{w}({l})' for l, w in top5]}")

    return {
        'filename': text_file.name,
        'total_words': total_words,
        'mean_length': mean_len,
        'median_length': median_len,
        'std_length': std_len,
        'pct_long_words': pct_long,
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
        filename, total_words, mean_length, median_length,
        std_length, pct_long_words

    Args:
        results: Listi af dict frá measure_word_length.
        output_path: Slóð á CSV-skrá til að vista.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'filename',
        'total_words',
        'mean_length',
        'median_length',
        'std_length',
        'pct_long_words',
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            row_out = dict(row)
            row_out['mean_length'] = f"{row['mean_length']:.2f}"
            row_out['median_length'] = f"{row['median_length']:.1f}"
            row_out['std_length'] = f"{row['std_length']:.2f}"
            row_out['pct_long_words'] = f"{row['pct_long_words']:.1f}"
            writer.writerow(row_out)


# ============================================================
# PRENTA TÖFLU / PRINT TABLE
# ============================================================

def print_results_table(results: list[dict]) -> None:
    """Prenta niðurstöður á skipanalínu sem töflu.

    Args:
        results: Listi af dict frá measure_word_length.
    """
    print(f"\nVÍDD 6: Meðalorðalengd (mean word length in characters)")
    print("=" * 90)

    # Hauslína / Header
    print(f"  {'Skrá':<35} {'Orð':<7} {'Meðal':<7} {'Miðg.':<7} "
          f"{'Staðfr.':<8} {'8+staf%':<8}")
    print(f"  {'-'*35} {'-'*7} {'-'*7} {'-'*7} {'-'*8} {'-'*8}")

    for r in results:
        print(
            f"  {r['filename']:<35} "
            f"{r['total_words']:<7} "
            f"{r['mean_length']:<7.2f} "
            f"{r['median_length']:<7.1f} "
            f"{r['std_length']:<8.2f} "
            f"{r['pct_long_words']:<8.1f}"
        )

    # --- MEÐALTÖL / AVERAGES ---
    if results:
        avg_mean = mean([r['mean_length'] for r in results])
        avg_pct = mean([r['pct_long_words'] for r in results])
        print(f"  {'-'*35} {'-'*7} {'-'*7} {'-'*7} {'-'*8} {'-'*8}")
        print(
            f"  {'MEÐALTAL':<35} "
            f"{'':7} "
            f"{avg_mean:<7.2f} "
            f"{'':7} "
            f"{'':8} "
            f"{avg_pct:<8.1f}"
        )

    print("=" * 90)
    print()
    print("  SKÝRING DÁLKA / COLUMN KEY:")
    print("    Orð     = Fjöldi gildra orða (eftir síun greinarmerka/talna)")
    print("    Meðal   = Meðalorðalengd í stöfum")
    print("    Miðg.   = Miðgildi orðalengdar")
    print("    Staðfr. = Staðalfrávik orðalengdar")
    print("    8+staf% = Hlutfall orða með 8 eða fleiri stafi")
    print()
    print("  TÚLKUN:")
    print("    Meðal ~ 5.5+  → langt (fræðitextar, tæknitextar)")
    print("    Meðal ~ 4.5-5.5 → miðlungs (fréttir)")
    print("    Meðal ~ 4.0-4.5 → stutt (blogg, óformlegt)")
    print("    8+staf% > 30%  → mikil tækniorð/samsett orð")
    print("    8+staf% < 20%  → hversdagslegt orðaforði")


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
    """Keyra mælingu á textaskrám og prenta/vista niðurstöður."""
    parser = argparse.ArgumentParser(
        description="Vídd 6: Mæla meðalorðalengd (mean word length).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Á möppu:
  python scripts/dim6_word_length.py \\
      --text-dir data/experiment/human_reference/

  # Á tilgreindum skrám:
  python scripts/dim6_word_length.py \\
      --files data/human_texts/news/news_001.txt data/human_texts/blog/blog_001.txt

  # Með villuleit (debug mode):
  python scripts/dim6_word_length.py \\
      --text-dir data/experiment/human_reference/ --debug
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
        default=Path('output/dim6_word_length.csv'),
        help="Slóð á CSV-úttaksskrá (sjálfgefið: output/dim6_word_length.csv)"
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Prenta villuleitarupplýsingar per skrá (debug mode). "
             "Sýnir tókanisering, lengstu orð, o.fl."
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
        print("  [DEBUG] Villuleitarhamur virkur — sýni ítarlegar upplýsingar")

    # --- KEYRA MÆLINGU ---
    results = []
    for tf in text_files:
        result = measure_word_length(tf, debug=args.debug)
        results.append(result)

    # --- PRENTA TÖFLU ---
    print_results_table(results)

    # --- VISTA CSV ---
    save_results_csv(results, args.output_csv)
    print(f"  CSV vistað: {args.output_csv}")


if __name__ == "__main__":
    main()
