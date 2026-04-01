#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
validation_harness.py — Sannprófunartól: Skoða og yfirfara þáttun og mælingar
================================================================================

TILGANGUR / PURPOSE:
    Þetta skrifta er sannprófunartól (validation harness) sem tekur slembiúrtak
    af þáttuðum setningum og sýnir hvað hvert víddarskrifta (dim1, dim2, dim3)
    dró út úr trénu. Þetta gerir nemandanum kleift að „sjá" hvort þáttarinn
    og mælingarnar virki rétt — handvirk yfirferð á litlu úrtaki.

    This is a validation tool that random-samples parsed sentences and shows
    what each dimension script extracted, enabling manual review.

HVERS VEGNA / WHY:
    Þáttunar- og mælingarvillur eru erfiðar að finna án þess að skoða gögnin.
    Þetta tól leyfir nemandanum að:
    - Sjá upprunalegu setninguna og þáttunartréð hlið við hlið
    - Athuga hvort dim1 fann NP-SBJ rétt
    - Athuga hvort dim2 taldi IP-MAT/IP-SUB rétt
    - Athuga hvort dim3 fann NP-liði og taldi orð rétt
    - Skrá niðurstöður í skýrslu til síðari yfirferðar

INNTAK / INPUT:
    - data/parsed/ mappa með þáttuðum trjám (*_parsed.txt)
    - Valfrjálst: data/human_texts/ eða data/llm_texts/ fyrir upprunalegan texta

ÚTTAK / OUTPUT:
    - output/validation_report.txt — ítarleg skýrsla
    - Samantekt á skipanalínu (terminal)

KEYRSLA / USAGE:
    python scripts/validation_harness.py --parsed-dir data/parsed/human/ --sample-size 20 --seed 42
    python scripts/validation_harness.py --parsed-dir data/parsed/llm/ --sample-size 10
"""

import argparse
import random
import re
import sys
from pathlib import Path

# Bæta scripts/ möppunni við sys.path svo hægt sé að flytja inn
# víddarskriftin (dim1, dim2, dim3) sem einingar (modules).
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Flytja inn greiningarföll úr víddarskriftum.
# Við notum analyze_tree úr dim1 og count_label úr dim2.
# Fyrir dim3 notum við extract_np_spans og count_tokens_in_np.
from dim1_frumlagsnafnfall import analyze_tree
from dim2_aukasetningar import count_label
from dim3_nafnlidalengd import extract_np_spans, count_tokens_in_np

# Sjálfgefin úttaksmappa
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "validation_report.txt"


# ============================================================
# LESA ÞÁTTUÐ TRÉ ÚR MÖPPU / LOAD PARSED TREES FROM DIRECTORY
# Les allar *_parsed.txt skrár og býr til sameinaðan lista af
# (skráarheiti, línunúmer, tréstrengur) tupplum.
# ============================================================

def load_all_trees(parsed_dir: Path) -> list[dict]:
    """Lesa öll þáttuð tré úr öllum skrám í möppu.

    Hvert tré er skráð sem dict með upplýsingum um uppruna:
        - file: skráarheiti (t.d. "news_ruv_parsed.txt")
        - line_num: línunúmer í skránni (byrjar á 1)
        - tree: þáttunartréð sem strengur

    Args:
        parsed_dir: Mappa með *_parsed.txt skrám.

    Returns:
        Listi af dict — eitt per þáttunartré.
    """
    all_trees = []

    if not parsed_dir.exists():
        print(f"VILLA: Mappa finnst ekki: {parsed_dir}")
        return []

    # Finna allar þáttaðar skrár
    parsed_files = sorted(parsed_dir.glob('*_parsed.txt'))

    if not parsed_files:
        print(f"AÐVÖRUN: Engar *_parsed.txt skrár í {parsed_dir}")
        return []

    for pf in parsed_files:
        with open(pf, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                tree = line.strip()
                if tree:
                    all_trees.append({
                        'file': pf.name,
                        'line_num': line_num,
                        'tree': tree,
                    })

    return all_trees


# ============================================================
# REYNA AÐ FINNA UPPRUNALEGAN TEXTA / TRY TO FIND SOURCE TEXT
# Ef upprunalegir textar eru til, reynum við að tengja hvert
# þáttunartré við upprunalegu setninguna.
# ============================================================

def try_find_source_text(
    file_name: str, line_num: int, parsed_dir: Path
) -> str:
    """Reyna að finna upprunalegan texta sem samsvarar þáttuðu tréi.

    Hvert þáttunartré í *_parsed.txt samsvarar sömu línu í
    upprunalegri textaskrá (án _parsed viðskeytisins).

    Dæmi: data/parsed/human/news_ruv_parsed.txt lína 5
           samsvarar data/human_texts/news_ruv.txt lína 5

    Args:
        file_name: Heiti þáttuðu skráarinnar (t.d. "news_ruv_parsed.txt").
        line_num: Línunúmer í þáttuðu skránni (byrjar á 1).
        parsed_dir: Mappa sem inniheldur þáttuðu skrána.

    Returns:
        Upprunalegur texti ef hann finnst, annars "(upprunalegur texti ekki fundinn)".
    """
    # Búa til nafn á upprunalegri skrá: fjarlægja "_parsed" úr heitinu
    source_name = file_name.replace('_parsed', '')

    # Leita í nokkrum mögulegum slóðum
    # Þáttuð skrá gæti verið í data/parsed/human/ — upprunalegur texti
    # gæti verið í data/human_texts/ eða data/llm_texts/
    possible_dirs = [
        parsed_dir.parent.parent / "human_texts",   # data/human_texts/
        parsed_dir.parent.parent / "llm_texts",      # data/llm_texts/
    ]

    for source_dir in possible_dirs:
        source_path = source_dir / source_name
        if source_path.exists():
            try:
                with open(source_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f, start=1):
                        if i == line_num:
                            return line.strip()
            except Exception:
                pass

    return "(upprunalegur texti ekki fundinn)"


# ============================================================
# DRAGA ÚT LAUFBLÖÐ ÚR TRÉI / EXTRACT LEAVES FROM TREE
# Þetta hjálparfall dregur út öll orð (laufblöð/leaves) úr
# þáttunartrénu til að sýna setninguna sem texta.
# ============================================================

def extract_leaves(tree_str: str) -> str:
    """Draga út öll laufblöð (orð) úr þáttunartréi og skila sem streng.

    Laufblöð eru orðin sjálf — allt annað í trénu eru merki (labels)
    og svigrúm. Þetta fall fjarlægir alla merkingafræðilegan búnað og
    skilar hreinum texta.

    Args:
        tree_str: Þáttunartré sem strengur í svigaformi.

    Returns:
        Samsettur texti allra laufblaða með bilum á milli.
    """
    # Regluleg segð sem finnur laufblöð: orð rétt á undan „)"
    leaves = re.findall(r'[^\s\(\)]+(?=\))', tree_str)
    return ' '.join(leaves)


# ============================================================
# GREINA EITT TRÉ MEÐ ÖLLUM VÍDDUM / ANALYZE ONE TREE WITH ALL DIMS
# Keyrir allar þrjár mælingar á einu tréi og skilar
# mannlæsilegri samantekt.
# ============================================================

def analyze_tree_all_dims(tree_str: str) -> dict:
    """Greina eitt þáttunartré með öllum þremur víddum.

    Args:
        tree_str: Þáttunartré sem strengur.

    Returns:
        dict með niðurstöðum allra vídda:
            - dim1: dict frá analyze_tree()
            - dim2_ip_mat: fjöldi IP-MAT
            - dim2_ip_sub: fjöldi IP-SUB
            - dim3_nps: listi af (np_strengur, orðafjöldi) pörum
            - leaves: allir laufblöð sem strengur
    """
    # --- VÍDD 1: Frumlagsnafnliður ---
    dim1 = analyze_tree(tree_str)

    # --- VÍDD 2: Aukasetningar ---
    n_mat = count_label(tree_str, 'IP-MAT')
    n_sub = count_label(tree_str, 'IP-SUB')

    # --- VÍDD 3: Nafnliðalengd ---
    np_spans = extract_np_spans(tree_str)
    np_details = []
    for np_str in np_spans:
        n_tokens = count_tokens_in_np(np_str)
        np_details.append((np_str, n_tokens))

    # --- LAUFBLÖÐ ---
    leaves = extract_leaves(tree_str)

    return {
        'dim1': dim1,
        'dim2_ip_mat': n_mat,
        'dim2_ip_sub': n_sub,
        'dim3_nps': np_details,
        'leaves': leaves,
    }


# ============================================================
# BÚA TIL SKÝRSLU / GENERATE REPORT
# Býr til texta-skýrslu (plain text) sem sýnir hvert úrtak
# með öllum greiningarupplýsingum.
# ============================================================

def generate_report(
    samples: list[dict],
    parsed_dir: Path,
) -> str:
    """Búa til sannprófunarskýrslu úr úrtökum.

    Args:
        samples: Listi af dict — hvert stak er eitt slembiúrtak.
        parsed_dir: Mappa sem inniheldur þáttuðu skrárnar.

    Returns:
        Strengur með allri skýrslunni.
    """
    lines = []
    lines.append("=" * 80)
    lines.append("SANNPRÓFUNARSKÝRSLA / VALIDATION REPORT")
    lines.append(f"Fjöldi úrtaka: {len(samples)}")
    lines.append(f"Þáttunarmappa: {parsed_dir}")
    lines.append("=" * 80)
    lines.append("")

    for i, sample in enumerate(samples, start=1):
        lines.append(f"{'─' * 80}")
        lines.append(f"ÚRTAK {i}/{len(samples)}")
        lines.append(f"  Skrá: {sample['file']}, lína {sample['line_num']}")
        lines.append(f"{'─' * 80}")

        # Upprunalegur texti
        source = try_find_source_text(
            sample['file'], sample['line_num'], parsed_dir
        )
        lines.append(f"\n  UPPRUNALEGUR TEXTI:")
        lines.append(f"    {source}")

        # Laufblöð úr tréi (svo hægt sé að bera saman)
        analysis = analyze_tree_all_dims(sample['tree'])
        lines.append(f"\n  LAUFBLÖÐ ÚR TRÉI:")
        lines.append(f"    {analysis['leaves']}")

        # Þáttunartré (stytt ef of langt)
        tree_display = sample['tree']
        if len(tree_display) > 200:
            tree_display = tree_display[:200] + "..."
        lines.append(f"\n  ÞÁTTUNARTRÉ:")
        lines.append(f"    {tree_display}")

        # --- VÍDD 1: Frumlagsnafnliður ---
        d1 = analysis['dim1']
        lines.append(f"\n  VÍDD 1 — Frumlagsnafnliður:")
        lines.append(f"    NP-SBJ fundið: {'JÁ' if d1['has_subject'] else 'NEI'}")
        lines.append(f"    Persónubeygð sögn: {'JÁ' if d1['has_verb'] else 'NEI'}")
        lines.append(f"    Boðháttur: {'JÁ' if d1['is_imperative'] else 'NEI'}")

        # Ályktun um dim1
        if not d1['has_verb']:
            lines.append(f"    → Ekki metin (engin sögn — t.d. nafnliðarfyrirsögn)")
        elif d1['is_imperative']:
            lines.append(f"    → Ekki metin (boðháttur)")
        elif not d1['has_subject']:
            lines.append(f"    → FRUMLAGSLAUS setning (telst í dim1)")
        else:
            lines.append(f"    → Setning með frumlagi (telst EKKI í dim1)")

        # --- VÍDD 2: Aukasetningar ---
        lines.append(f"\n  VÍDD 2 — Aukasetningar:")
        lines.append(f"    IP-MAT (aðalsetningar): {analysis['dim2_ip_mat']}")
        lines.append(f"    IP-SUB (aukasetningar): {analysis['dim2_ip_sub']}")
        total_clauses = analysis['dim2_ip_mat'] + analysis['dim2_ip_sub']
        if total_clauses > 0:
            ratio = analysis['dim2_ip_sub'] / total_clauses
            lines.append(f"    Hlutfall: {ratio:.2f} ({analysis['dim2_ip_sub']}/{total_clauses})")
        else:
            lines.append(f"    Hlutfall: Engar setningar fundust")

        # --- VÍDD 3: Nafnliðalengd ---
        lines.append(f"\n  VÍDD 3 — Nafnliðalengd:")
        lines.append(f"    Fjöldi NP: {len(analysis['dim3_nps'])}")
        if analysis['dim3_nps']:
            np_lengths = [n for _, n in analysis['dim3_nps']]
            lines.append(f"    Lengdir: {np_lengths}")
            avg = sum(np_lengths) / len(np_lengths)
            lines.append(f"    Meðallengd: {avg:.1f} orð")
            # Sýna dæmi um NP-liði (stytt ef of margir)
            for j, (np_str, n_tok) in enumerate(analysis['dim3_nps'][:5]):
                if len(np_str) > 80:
                    np_str = np_str[:80] + "..."
                lines.append(f"      NP{j+1}: [{n_tok} orð] {np_str}")
            if len(analysis['dim3_nps']) > 5:
                lines.append(f"      ... og {len(analysis['dim3_nps']) - 5} í viðbót")
        else:
            lines.append(f"    Engir nafnliðir fundust")

        lines.append("")

    # Samantekt
    lines.append("=" * 80)
    lines.append("SAMANTEKT")
    lines.append("=" * 80)

    # Reikna yfirlit yfir öll úrtök
    n_with_verb = sum(
        1 for s in samples
        if analyze_tree_all_dims(s['tree'])['dim1']['has_verb']
    )
    n_subjectless = sum(
        1 for s in samples
        if analyze_tree_all_dims(s['tree'])['dim1']['has_verb']
        and not analyze_tree_all_dims(s['tree'])['dim1']['is_imperative']
        and not analyze_tree_all_dims(s['tree'])['dim1']['has_subject']
    )

    lines.append(f"  Heildarúrtök: {len(samples)}")
    lines.append(f"  Setningar með sögn: {n_with_verb}")
    lines.append(f"  Frumlagslausar (dim1): {n_subjectless}")
    lines.append("")
    lines.append("  ATHUGIÐ: Farðu yfir skýrsluna og athugaðu hvort:")
    lines.append("    1. NP-SBJ greining sé rétt (ber saman við upprunalegan texta)")
    lines.append("    2. IP-MAT/IP-SUB talning sé rétt")
    lines.append("    3. NP-lengdir séu sanngjarnar")
    lines.append("=" * 80)

    return '\n'.join(lines)


# ============================================================
# AÐALFLÆÐI / MAIN FLOW
# ============================================================

def main() -> None:
    """Keyra sannprófunartólið."""
    parser = argparse.ArgumentParser(
        description="Sannprófunartól: Skoða þáttun og mælingar á slembiúrtaki.",
        epilog="""
Dæmi:
  python scripts/validation_harness.py --parsed-dir data/parsed/human/ --sample-size 20 --seed 42
  python scripts/validation_harness.py --parsed-dir data/parsed/llm/ --sample-size 10
        """
    )
    parser.add_argument(
        '--parsed-dir',
        type=Path,
        required=True,
        help="Mappa með þáttuðum trjám (*_parsed.txt)"
    )
    parser.add_argument(
        '--sample-size',
        type=int,
        default=20,
        help="Fjöldi setninga í úrtaki (sjálfgefið: 20)"
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help="Slembifræ (random seed) fyrir endurtekjanleika (sjálfgefið: 42)"
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Slóð á úttaksskýrslu (sjálfgefið: {DEFAULT_OUTPUT})"
    )

    args = parser.parse_args()

    # --- SKREF 1: Lesa öll tré ---
    print(f"Les þáttuð tré úr {args.parsed_dir}...")
    all_trees = load_all_trees(args.parsed_dir)

    if not all_trees:
        print("VILLA: Engin þáttuð tré fundust.")
        sys.exit(1)

    print(f"  Fann {len(all_trees)} þáttuð tré alls.")

    # --- SKREF 2: Taka slembiúrtak ---
    # Stilla slembifræ svo sama úrtakið fáist aftur ef sama fræ er notað
    random.seed(args.seed)

    # Takmarka úrtaksstærð við fjölda tiltækra trjáa
    sample_size = min(args.sample_size, len(all_trees))
    samples = random.sample(all_trees, sample_size)

    print(f"  Tók {sample_size} slembiúrtök (seed={args.seed}).")

    # --- SKREF 3: Búa til skýrslu ---
    print("Bý til sannprófunarskýrslu...")
    report = generate_report(samples, args.parsed_dir)

    # --- SKREF 4: Vista skýrslu ---
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"  Skýrsla vistuð: {args.output}")

    # --- SKREF 5: Prenta samantekt á skipanalínu ---
    print(f"\n{'=' * 60}")
    print(f"SAMANTEKT")
    print(f"{'=' * 60}")
    print(f"  Þáttuð tré alls: {len(all_trees)}")
    print(f"  Slembiúrtök: {sample_size}")
    print(f"  Seed: {args.seed}")
    print(f"  Skýrsla: {args.output}")
    print(f"\n  Farðu yfir {args.output.name} til að sannprófa þáttunina.")
    print(f"  Leitaðu sérstaklega að:")
    print(f"    - Röngum NP-SBJ greiningum (dim1)")
    print(f"    - Röngum IP-MAT/IP-SUB talningum (dim2)")
    print(f"    - Ósanngjarnum NP-lengdum (dim3)")


if __name__ == "__main__":
    main()
