#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dim4_past_tense.py — VÍDD 4: Hlutfall þátíðarsagna (past tense ratio)
=======================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta mælir hlutfall þátíðarsagna (past tense verbs) af öllum
    persónubeygðum sögnum (finite verbs) í texta. Þetta er klassísk Biber-
    vídd sem tengist frásagnar- og fréttastíl (narrative / reportive register).

    This script measures the ratio of past tense verbs to all finite verbs
    in constituency-parsed text, as a core Biber register dimension.

MÁLVÍSINDI / LINGUISTICS:
    Þátíðartíðni er einn af lykilmælikvörðum í greiningarlíkani Bibers
    (Multi-Dimensional Analysis, MDA). Textar sem segja frá atburðum nota
    meiri þátíð en textar sem lýsa almennum lögmálum eða aðferðum nota
    frekar nútíð.

    VÆNTANLEGAR NIÐURSTÖÐUR Í TEXTATEGUNDUM:
    - Fréttir (RÚV): HÁTT — fjallar um atburði sem hafa gerst
      („Forsætisráðherra sagði...“, „Eldur kviknaði...“)
    - Blogg (Jonas.is): HÁTT — persónulegar frásagnir, endurminningar
      („Ég fór þangað...“, „Við sáum hann...“)
    - Fræðitextar (Læknablaðið): LÆGRA — nútíðaryfirlit, aðferðalýsingar
      („Rannsóknin sýnir...“, „Sjúklingarnir fá meðferð...“)

    TENGSL VIÐ BIBER-RAMMA / CONNECTION TO BIBER'S MDA:
        Biber (1988) tengdi þátíðarnotkun við „Narrative vs. Non-Narrative
        Concerns“ (vídd 2 í sínu kerfi). Þátíð hleðst jákvætt (positive
        loading) á frásagnarvíddina ásamt þriðjupersónufornöfnum og
        fullkomnu beygingarformi (perfect aspect).

        Í okkar verkefni: Ef LLM-líkan framleiðir of lítið af þátíð í
        fréttastíl, bendir það til þess að líkanið nái ekki frásagnarstíl
        mannlegra frétta.

ICEPAHC SAGNMERKJAKERFI / ICEPAHC VERB TAG SYSTEM:
    IcePaHC notar kerfisbundið sagnmerkjakerfi þar sem HVERT merki
    samanstendur af þremur hlutum:

        [SAGNSTOFN] [TÍÐ] [HÁTTUR]

    SAGNSTOFNAR (verb stems):
        VB = lexical verb (venjuleg sögn, t.d. fara, sjá, tala)
        BE = „vera“ (to be)
        MD = modal / hjálparsögn (geta, skulu, vilja, munu, mega)
        DO = „gera“ (to do)
        HV = „hafa“ (to have)
        RD = „verða“ (to become)

    TÍÐIR (tenses):
        P = nútíð (present tense)
        D = þátíð (past tense)  ← ÞETTA TELJUM VIÐ

    HÆTTIR (moods):
        I = framsöguháttur (indicative mood — „hann fer“, „hún fór“)
        S = viðtengingarh. (subjunctive mood — „hann fari“, „hún færi“)

    SAMSETNINGAR OG DÆMI / COMBINATIONS AND EXAMPLES:
        VBPI = sögn, nútíð, framsöguháttur    (t.d. „fer“, „sér“)
        VBDI = sögn, þátíð, framsöguháttur     (t.d. „fór“, „sá“)     ← ÞÁTÍÐ
        VBPS = sögn, nútíð, viðtengingarh.     (t.d. „fari“, „sjái“)
        VBDS = sögn, þátíð, viðtengingarh.     (t.d. „færi“, „sæi“)   ← ÞÁTÍÐ
        BEPI = vera, nútíð, framsöguh.          (t.d. „er“)
        BEDI = vera, þátíð, framsöguh.          (t.d. „var“)          ← ÞÁTÍÐ
        MDPI = modal, nútíð, framsöguh.         (t.d. „getur“)
        MDDI = modal, þátíð, framsöguh.         (t.d. „gat“)          ← ÞÁTÍÐ
        HVPI = hafa, nútíð, framsöguh.          (t.d. „hefur“)
        HVDI = hafa, þátíð, framsöguh.          (t.d. „hafði“)        ← ÞÁTÍÐ
        DOPI = gera, nútíð, framsöguh.          (t.d. „gerir“)
        DODI = gera, þátíð, framsöguh.          (t.d. „gerði“)        ← ÞÁTÍÐ
        RDPI = verða, nútíð, framsöguh.         (t.d. „verður“)
        RDDI = verða, þátíð, framsöguh.         (t.d. „varð“)         ← ÞÁTÍÐ

    HVAÐ VIÐ TELJUM EKKI / WHAT WE EXCLUDE:
        Ópersónubeygð form (non-finite forms) hafa EKKI tíð og eru
        ÚTILOKUÐ:
        - VB  (nafnháttur / infinitive: „að fara“)
        - VBN (lýsingarháttur þátíðar / past participle: „farinn“)
        - VAG (lýsingarháttur nútíðar / present participle: „farandi“)
        - VBI (boðháttur / imperative: „farðu!“)

        Þessi form hafa enga tíðarmerkingu í málvísindafræðilegum
        skilningi, svo þau eiga ekki heima í tíðarhlutfallsmælingu.

INNTAK / INPUT:
    Þáttuð tré úr data/parsed/human/*.txt og data/parsed/llm/*.txt
    (ein lína = eitt þáttunartré í svigaformi)

ÚTTAK / OUTPUT:
    1. CSV-skrá: output/dim4_past_tense.csv
    2. Tafla á skipanalínu

KEYRSLA / USAGE:
    # Á möppu:
    python scripts/dim4_past_tense.py --parsed-dir output/parsed/

    # Á tilgreindum skrám:
    python scripts/dim4_past_tense.py --files output/parsed/news_001.parsed

    # Sem innflutt eining:
    from dim4_past_tense import measure_past_tense
    result = measure_past_tense(Path("data/parsed/human/news_ruv_parsed.txt"))
"""

import argparse
import csv
import re
from pathlib import Path


# ============================================================
# LESA ÞÁTTUÐ TRÉ / READ PARSED TREES
# Sama aðferð og í dim1/dim2/dim3/dim5 — les þáttuð tré
# úr skrá, eitt per línu.
# ============================================================

def load_parsed_trees(path: Path) -> list[str]:
    """Lesa þáttuð tré úr skrá. Eitt tré per línu.

    Args:
        path: Slóð á textaskrá með þáttuðum trjám.

    Returns:
        Listi af strengjum — hvert tré er einn strengur.

    Raises:
        FileNotFoundError: Ef skráin finnst ekki.
    """
    if not path.exists():
        raise FileNotFoundError(f"Þáttuð skrá fannst ekki: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        trees = [line.strip() for line in f if line.strip()]

    return trees


# ============================================================
# REGLULEGAR SEGÐIR FYRIR SAGNMERKI / VERB TAG REGEX PATTERNS
# ============================================================
#
# HVERS VEGNA VIÐ NOTUM REGEX Á ENDAHNÚTA (TERMINAL NODES):
#   Í IcePaHC-svigaformi er endahnútur (terminal node) skrifaður:
#       (MERKI orð)
#   Dæmi: (VBDI fór), (BEDI var), (MDPI getur)
#
#   Við leitum einungis að merkjum sem birtast strax á eftir „(“
#   og hafa orðform á eftir. Þetta kemur í veg fyrir rangar
#   niðurstöður þar sem óendahnútar (non-terminals) eins og IP-MAT
#   eða IP-SUB passa ekki við mynstur sagnmerkja.
#
# MYNSTUR / PATTERNS:
#   ENDAHNÚTUR = \( + MERKI + \s+ + ORÐ + \)
#   þar sem MERKI er sagnmerkið sem við leitum að.
#
# ============================================================

# --- ÖLLUM PERSÓNUBEYGÐUM SÖGNUM / ALL FINITE VERBS ---
# Persónubeygt form: [STOFN][TÍÐ][HÁTTUR]
# þar sem STOFN ∈ {VB, BE, MD, DO, HV, RD}
#         TÍÐ   ∈ {P (nútíð), D (þátíð)}
#         HÁTTUR ∈ {I (framsöguh.), S (viðtengingarh.)}
#
# Regexið finnur öll persónubeygð form — bæði nútíð og þátíð.
# Þetta er NEFNARINN (denominator) í hlutfallinu.
#
# Mynstur á endahnút:  \((VB|BE|MD|DO|HV|RD)[PD][IS]\s+
# Dæmi sem SAMSVARA:   (VBDI fór), (BEPI er)
# Dæmi sem SAMSVARA EKKI: (VBN farinn), (VBI farðu), (IP-MAT ...
FINITE_VERB_PATTERN = re.compile(
    r'\((VB|BE|MD|DO|HV|RD)[PD][IS]\s+[^\s\)]+\)'
)

# --- ÞÁTÍÐARSAGNIR / PAST TENSE VERBS ---
# Sama og ofan en TÍÐ er bundin við D (þátíð).
# Þetta er TELJARINN (numerator) í hlutfallinu.
#
# Munur á þessu og FINITE_VERB_PATTERN:
#   [PD]  →  D       (aðeins þátíð, ekki nútíð)
#
# Mynstur á endahnút:  \((VB|BE|MD|DO|HV|RD)D[IS]\s+
# Dæmi sem SAMSVARA:   (VBDI fór), (BEDI var), (MDDI gat), (HVDS hefði)
# Dæmi sem SAMSVARA EKKI: (VBPI fer), (BEPI er), (MDPI getur)
PAST_TENSE_PATTERN = re.compile(
    r'\((VB|BE|MD|DO|HV|RD)D[IS]\s+[^\s\)]+\)'
)

# --- LAUFBLÖÐ (LEAVES) / TERMINAL NODES ---
# Regex sem finnur öll laufblöð í trénu til orðatalningar.
# Sama mynstur og í dim3 og dim5.
# Laufblað = orðform rétt á undan lokunarsvigrúmi ).
LEAF_PATTERN = re.compile(r'[^\s\(\)]+(?=\))')

# ============================================================
# DRAGA ÚT SAGNUPPLÝSINGAR ÚR EINU TRÉ / EXTRACT VERB INFO
# ============================================================

def extract_verb_counts_from_tree(tree_str: str) -> tuple[int, int, int]:
    """Telja persónubeygðar sagnir og þátíðarsagnir í einu þáttunartré.

    AÐFERÐ:
        1. Nota regex til að finna öll endahnútamynstur sem samsvara
           persónubeygðum sögnum.
        2. Af þeim, finna þau sem eru þátíð (D í tíðarstöðu).
        3. Telja einnig heildarfjölda orða til hlutfallsútreikninga.

    DÆMI ÚR RAUNVERULEGUM TRJÁM:
        Tré: (ROOT (IP-MAT (NP-SBJ (NPR-N Jón)) (VBDI fór) (PP (P til)
             (NP (NPR-G Reykjavíkur)))))
        → 1 persónubeygt form (VBDI fór), 1 þátíð, 3 orð (Jón, fór, til, Reykjavíkur = 4)

        Tré: (ROOT (IP-MAT (NP-SBJ (PRO-N Hún)) (BEPI er) (ADJP (ADJ-N fljót))))
        → 1 persónubeygt form (BEPI er), 0 þátíð, 3 orð

    Args:
        tree_str: Eitt þáttunartré sem strengur í svigaformi.

    Returns:
        Samstæða (tuple) af:
            - n_past: fjöldi þátíðarsagna
            - n_finite: fjöldi allra persónubeygðra sagna
            - n_words: heildarfjöldi orða (laufblaða)
    """
    # Finna allar persónubeygðar sagnir
    # findall skilar lista af samsvarandi strengjum (hópunum),
    # en við þurfum bara fjöldann.
    n_finite = len(FINITE_VERB_PATTERN.findall(tree_str))

    # Finna þátíðarsagnir (undirmengi af persónubeygðum sögnum)
    n_past = len(PAST_TENSE_PATTERN.findall(tree_str))

    # Telja heildarorð (öll laufblöð)
    n_words = len(LEAF_PATTERN.findall(tree_str))

    return n_past, n_finite, n_words


# ============================================================
# AÐALMÆLING / MAIN MEASUREMENT
# Keyra á heila skrá af þáttuðum trjám.
# ============================================================

def measure_past_tense(parsed_file: Path) -> dict:
    """Mæla hlutfall þátíðarsagna í textaskrá.

    REIKNIAÐFERÐ:
        1. Lesa öll þáttuð tré úr skrá
        2. Telja persónubeygðar sagnir og þátíðarsagnir per tré
        3. Leggja saman yfir öll tré
        4. Reikna hlutföll

    ÚTREIKNINGAR:
        - past_tense_ratio = þátíð / öll persónubeygt form
          (Hversu stórt hlutfall persónubeygðra sagna er í þátíð)
        - past_tense_per_1000 = (þátíð / heildarorð) × 1000
          (Tíðni þátíðarsagna á hverja 1.000 orð — til samanburðar
          við önnur MDA-verkefni sem nota þennan mælikvarða)

    Args:
        parsed_file: Slóð á skrá með þáttuðum trjám.

    Returns:
        Dict með lyklum:
            - filename: skráarheiti
            - past_tense_count: fjöldi þátíðarsagna
            - finite_verb_count: fjöldi allra persónubeygðra sagna
            - total_word_count: heildarfjöldi orða
            - past_tense_ratio: hlutfall þátíðar / persónubeygt
            - past_tense_per_1000_words: þátíð per 1.000 orð
    """
    trees = load_parsed_trees(parsed_file)

    # Heildartalningar yfir alla setningar í skránni
    total_past = 0
    total_finite = 0
    total_words = 0

    for tree_str in trees:
        n_past, n_finite, n_words = extract_verb_counts_from_tree(tree_str)
        total_past += n_past
        total_finite += n_finite
        total_words += n_words

    # --- REIKNA HLUTFÖLL ---
    # 1. Hlutfall þátíðar af öllum persónubeygðum sögnum
    #    Þetta er aðalgildi víddarinnar (v-gildi).
    if total_finite > 0:
        past_ratio = total_past / total_finite
    else:
        past_ratio = 0.0

    # 2. Þátíð per 1.000 orð
    #    Algengur mælikvarði í MDA-rannsóknum. Gerir kleift að bera
    #    saman texta af mismunandi lengd og bera saman við
    #    alþjóðlegar rannsóknir.
    if total_words > 0:
        past_per_1000 = (total_past / total_words) * 1000
    else:
        past_per_1000 = 0.0

    return {
        'filename': parsed_file.name,
        'past_tense_count': total_past,
        'finite_verb_count': total_finite,
        'total_word_count': total_words,
        'past_tense_ratio': past_ratio,
        'past_tense_per_1000_words': past_per_1000,
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
        filename, past_tense_count, finite_verb_count,
        total_word_count, past_tense_ratio, past_tense_per_1000_words

    Args:
        results: Listi af dict frá measure_past_tense.
        output_path: Slóð á CSV-skrá til að vista.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'filename',
        'past_tense_count',
        'finite_verb_count',
        'total_word_count',
        'past_tense_ratio',
        'past_tense_per_1000_words',
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            # Slétta hlutfallstölur til 4 aukastafa í CSV
            row_out = dict(row)
            row_out['past_tense_ratio'] = f"{row['past_tense_ratio']:.4f}"
            row_out['past_tense_per_1000_words'] = (
                f"{row['past_tense_per_1000_words']:.2f}"
            )
            writer.writerow(row_out)


# ============================================================
# PRENTA TÖFLU / PRINT TABLE
# Prenta greinargóða töflu á skipanalínu.
# ============================================================

def print_results_table(results: list[dict]) -> None:
    """Prenta niðurstöður á skipanalínu sem töflu.

    Args:
        results: Listi af dict frá measure_past_tense.
    """
    print(f"\nVÍDD 4: Hlutfall þátíðarsagna (past tense ratio)")
    print("=" * 90)

    # Hauslína / Header
    #   Þátíð  = fjöldi þátíðarsagna
    #   Pers.  = fjöldi persónubeygðra sagna (finite)
    #   Orð    = heildarfjöldi orða
    #   Hlutf. = þátíð / persónubeygt (aðalhlutfall)
    #   /1000  = þátíð per 1.000 orð
    print(f"  {'Skrá':<35} {'Þátíð':<7} {'Pers.':<7} {'Orð':<7} "
          f"{'Hlutf.':<8} {'/1000':<8}")
    print(f"  {'-'*35} {'-'*7} {'-'*7} {'-'*7} {'-'*8} {'-'*8}")

    for r in results:
        print(
            f"  {r['filename']:<35} "
            f"{r['past_tense_count']:<7} "
            f"{r['finite_verb_count']:<7} "
            f"{r['total_word_count']:<7} "
            f"{r['past_tense_ratio']:<8.4f} "
            f"{r['past_tense_per_1000_words']:<8.2f}"
        )

    # --- MEÐALTÖL / AVERAGES ---
    if results:
        avg_ratio = (
            sum(r['past_tense_ratio'] for r in results) / len(results)
        )
        avg_per_1000 = (
            sum(r['past_tense_per_1000_words'] for r in results)
            / len(results)
        )
        print(f"  {'-'*35} {'-'*7} {'-'*7} {'-'*7} {'-'*8} {'-'*8}")
        print(
            f"  {'MEÐALTAL':<35} "
            f"{'':7} {'':7} {'':7} "
            f"{avg_ratio:<8.4f} {avg_per_1000:<8.2f}"
        )

    print("=" * 90)
    print()
    print("  SKÝRING DÁLKA / COLUMN KEY:")
    print("    Þátíð  = Fjöldi þátíðarsagna (VBDI, BEDI, MDDI, ...)")
    print("    Pers.  = Heildarfjöldi persónubeygðra sagna (VB/BE/MD/DO/HV/RD + P/D + I/S)")
    print("    Orð    = Heildarfjöldi orða (laufblöð í þáttunartréum)")
    print("    Hlutf. = Hlutfall: þátíð / persónubeygt")
    print("    /1000  = Þátíðarsagnir per 1.000 orð")
    print()
    print("  TÚLKUN:")
    print("    Hlutf. ~ 0.5-0.7  → mikil þátíð (fréttir, frásagnir)")
    print("    Hlutf. ~ 0.3-0.5  → blönduð (blogg, skoðanagreinar)")
    print("    Hlutf. ~ 0.1-0.3  → lítil þátíð (fræðitextar, leiðbeiningar)")


# ============================================================
# FINNA ALLAR ÞÁTTAÐAR SKRÁR / FIND ALL PARSED FILES
# ============================================================

def find_parsed_files(parsed_dir: Path) -> list[Path]:
    """Finna allar þáttaðar skrár í möppu (endurkvæmt).

    Leitar að .txt skrám sem innihalda þáttuð tré (ein lína = eitt tré).
    Raðar skrám í stafrófsröð til endurtekjanlegrar (reproducible) keyrslu.

    Args:
        parsed_dir: Mappa með þáttuðum skrám.

    Returns:
        Raðaður listi af Path-hlutum.
    """
    txt_files = sorted(parsed_dir.rglob('*.txt'))

    if not txt_files:
        print(f"  AÐVÖRUN: Engar .txt skrár fundust í {parsed_dir}")

    return txt_files


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra mælingu á þáttuðum skrám og prenta/vista niðurstöður."""
    parser = argparse.ArgumentParser(
        description="Vídd 4: Mæla hlutfall þátíðarsagna (past tense ratio).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Á möppu:
  python scripts/dim4_past_tense.py \\
      --parsed-dir output/parsed/

  # Á tilgreindum skrám:
  python scripts/dim4_past_tense.py \\
      --files output/parsed/news_001.parsed output/parsed/blog_001.parsed

  # Stýra úttak-CSV staðsetningu:
  python scripts/dim4_past_tense.py \\
      --parsed-dir output/parsed/ \\
      --output-csv output/dim4_custom.csv
        """
    )

    # Tveir innstakmöguleikar: --parsed-dir (mappa) eða --files (stök skrár)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--parsed-dir',
        type=Path,
        help="Mappa með þáttuðum skrám (.txt). Leit er endurkvæm."
    )
    group.add_argument(
        '--files',
        type=Path,
        nargs='+',
        help="Ein eða fleiri þáttaðar skrár til að greina."
    )

    parser.add_argument(
        '--output-csv',
        type=Path,
        default=Path('output/dim4_past_tense.csv'),
        help="Slóð á CSV-úttaksskrá (sjálfgefið: output/dim4_past_tense.csv)"
    )

    args = parser.parse_args()

    # --- FINNA SKRÁR ---
    if args.parsed_dir:
        if not args.parsed_dir.is_dir():
            print(f"VILLA: Mappa finnst ekki: {args.parsed_dir}")
            return
        parsed_files = find_parsed_files(args.parsed_dir)
    else:
        parsed_files = args.files
        # Staðfesta að allar skrár séu til
        for f in parsed_files:
            if not f.exists():
                print(f"VILLA: Skrá finnst ekki: {f}")
                return

    if not parsed_files:
        print("VILLA: Engar skrár til að greina.")
        return

    print(f"\n  Greini {len(parsed_files)} skrá(r)...")

    # --- KEYRA MÆLINGU ---
    results = []
    for pf in parsed_files:
        result = measure_past_tense(pf)
        results.append(result)

    # --- PRENTA TÖFLU ---
    print_results_table(results)

    # --- VISTA CSV ---
    save_results_csv(results, args.output_csv)
    print(f"  CSV vistað: {args.output_csv}")


if __name__ == "__main__":
    main()
