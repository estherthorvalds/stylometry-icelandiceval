#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
dim9_tree_depth.py — VÍDD 9: Setningarþyngd / tréhæð (syntactic complexity)
=============================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta mælir setningaflækjustig með TRÉDÝPT (tree depth) á
    þáttunartrjám frá IceConParse. Dýpri tré → þyngri, innfelldari
    setningagerð. Þar sem dim2 mælir TÍÐNI aukasetninga (IP-SUB / IP-MAT+IP-SUB),
    mælir dim9 DÝPT — hversu langt er milli rótar og dýpsta liðar.

    This script measures syntactic complexity by CONSTITUENCY TREE DEPTH.
    Deeper trees → more deeply nested / complex sentence structure.
    Where dim2 measures how FREQUENT subordination is, dim9 measures how
    DEEPLY NESTED syntactic structure is.

MÁLVÍSINDI / LINGUISTICS:
    Aðlagað úr fyrirlestri Steinþórs Steingrímssonar um „sentence weight“
    (byggt á UD-dependency-trjám). Hér er sama hugmynd yfirfærð á IcePaHC
    liðgerðartré (constituency): fjöldi hreiða (nested constituents)
    milli rótar og dýpsta laufa.

    Biber/MDA-rammi: Meðal-trédýpt er klassísk vísbending á „informational
    production“ víddinni. Fræðitextar og bókmenntir ná meiri dýpt; tal og
    óformlegt mál halda sér flatara.

    ORTHOGONAL VIÐ DIM2 / ORTHOGONAL TO DIM2:
        Texti getur haft margar aukasetningar á lítilli dýpt (dim2 hátt,
        dim9 lágt) — eða færri en dýpra innfelldar (dim2 miðlungs,
        dim9 hátt). Merkin eru því ekki víxltengd.

ÞRJÁR UNDIRMÆLINGAR / THREE SUB-MEASURES:
    1. mean_tree_depth — aðal-v. Meðal hámarksdýpt tréa per setningu.
       Rót = dýpt 0 (ROOT), börn rótar = dýpt 1, o.s.frv.
    2. pct_complex_trees — hlutfall setninga með tree_depth ≥ 3.
       Þröskuldurinn er sami og í fyrirlestri Steinþórs (UD-byggt). Í
       IcePaHC-liðgerð birta flestar setningar dýpt ≥ 3 vegna POS-hnúta;
       þessi þröskuldur er aðferðafræðileg hliðstæða, ekki kvarðaður.
    3. mean_ip_sub_nesting — meðal-hreiðslu IP-SUB-hnúta. Fyrir hvern
       IP-SUB, fjöldi IP-SUB forfeðra (0 ef engir). Skrár án IP-SUB → 0.

AÐFERÐ / METHOD:
    Þáttuð tré eru lesin eitt per línu (.psd snið, sama og dim1–dim5, dim7).
    Dýpt: einfaldur svigatalning — hámarksfjöldi opnaðra sviga í einni stöðu.
    IP-SUB-hreiðsla: stafavísi-gönguferli með stafl af opnuðum merkjum;
    fyrir hvern IP-SUB sem er pushaður, talin fjöldi IP-SUB sem fyrir eru
    í staflanum.

    Engin ytri söfn notuð — allar tölfræðiaðgerðir nota stöðluð Python-föll.
    Tölfræði-hjálparföllin `mean`/`stdev` fengin að láni úr dim6.

INNTAK / INPUT:
    Þáttuð tré (.psd) — t.d. úr:
        output/parsed/human_reference/
        output/parsed/prompts/
        output/parsed/llm_continuations_preprocessed/{model}/{reg}/

ÚTTAK / OUTPUT:
    1. CSV-skrá: output/dim9_tree_depth.csv
    2. Tafla á skipanalínu

KEYRSLA / USAGE:
    python scripts/dim9_tree_depth.py --parsed-dir output/parsed/human_reference/
    python scripts/dim9_tree_depth.py --files file1.psd file2.psd
    python scripts/dim9_tree_depth.py --parsed-dir ... --dry-run
    python scripts/dim9_tree_depth.py --parsed-dir ... --debug
"""

import argparse
import csv
from pathlib import Path

# Endurnýtum tölfræði-hjálparföllin úr dim6 til að halda háðni í lágmarki
# og samræma talningu á milli vídda.
from dim6_word_length import mean, stdev


# ============================================================
# ÞRÖSKULDUR FYRIR „FLÓKIÐ“ TRÉ / COMPLEX-TREE THRESHOLD
# ============================================================
# Sami þröskuldur og í fyrirlestri Steinþórs (UD-byggt). Í IcePaHC
# liðgerðartrjám eru dýptir kerfisbundið hærri en í UD-háðartrjám
# vegna POS-hnúta sem vefja utan um orð. Þröskuldurinn er því
# AÐFERÐAFRÆÐILEG HLIÐSTÆÐA — hann er ekki kvarðaður fyrir IcePaHC.
# ============================================================

COMPLEX_DEPTH_THRESHOLD = 3


# ============================================================
# LESA ÞÁTTUÐ TRÉ / READ PARSED TREES
# Sama aðferð og í dim2/dim3: eitt tré per línu.
# ============================================================

def load_parsed_trees(path: Path) -> list[str]:
    """Lesa þáttuð tré úr .psd skrá. Eitt tré per línu.

    Args:
        path: Slóð á .psd skrá með þáttuðum trjám.

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
# TRÉDÝPT / TREE DEPTH
# ============================================================
# Reiknum hámarksdýpt svigahreiðrunar í trénu. Rót = dýpt 0 samkvæmt
# sammæli: þegar fyrsti „(“ opnast erum við inni í rótinni og
# teljarinn nær gildinu 1; frádragur -1 í lokin gerir ROOT að 0.
# ============================================================

def tree_depth(tree_str: str) -> int:
    """Reikna hámarksdýpt eins þáttunartrés.

    Gengur í gegnum strenginn staf fyrir staf og telur opnaða sviga.
    Hámarksteljari á gönguferlinum gefur dýpstu stöðu; frádragur -1
    endurspeglar að ROOT-sjálft sé á dýpt 0.

    Args:
        tree_str: Þáttunartré sem strengur í svigaformi.

    Returns:
        Hámarksdýpt sem heiltala. Skilar 0 ef tréið er tómt eða
        hefur færri en 2 hnúta.
    """
    max_depth = 0
    current = 0
    for ch in tree_str:
        if ch == '(':
            current += 1
            if current > max_depth:
                max_depth = current
        elif ch == ')':
            current -= 1

    # Rót = dýpt 0 → draga 1 frá hámarks-svigadýpt.
    # Ef tréið var tómt eða hafði aðeins rótarliðinn (hámark = 1),
    # þá er dýptin 0.
    return max(0, max_depth - 1)


# ============================================================
# IP-SUB HREIÐSLA / IP-SUB NESTING DEPTH
# ============================================================
# Gengur tréð staf fyrir staf og heldur stafla af opnuðum merkjum.
# Fyrir hvern IP-SUB sem er pushaður er talin fjöldi IP-SUB sem
# FYRIR ERU í staflanum = fjöldi IP-SUB forfeðra = hreiðslustig.
#
# Dæmi:
#   „Ég sagði [að hann vissi [að hún kæmi]]“
#   → ytri IP-SUB hefur 0 IP-SUB forfeður (hreiðsla = 0)
#   → innri IP-SUB hefur 1 IP-SUB forföður (hreiðsla = 1)
# ============================================================

def collect_ip_sub_nesting(tree_str: str) -> list[int]:
    """Finna öll IP-SUB í trénu og skila hreiðslustigi hvers þeirra.

    AÐFERÐ:
        Viðhöldum stafla af opnuðum merkjum. Þegar nýtt „(LABEL“
        opnast:
            1. Dregur út merkið (LABEL).
            2. Ef LABEL == 'IP-SUB': teljum fjölda 'IP-SUB' sem eru
               nú þegar í staflanum — það er hreiðslustig þessa
               IP-SUB-hnúts. Bætist í útkomulistann.
            3. Pushum LABEL á staflann.
        Þegar „)“ kemur: poppum efsta merki.

    Args:
        tree_str: Þáttunartré sem strengur.

    Returns:
        Listi af heiltölum — hreiðslustig hvers IP-SUB-hnúts sem
        fannst. Tómur listi ef engin IP-SUB eru í trénu.
    """
    stack: list[str] = []
    nestings: list[int] = []

    i = 0
    n = len(tree_str)
    while i < n:
        ch = tree_str[i]
        if ch == '(':
            # Draga út merki á milli „(“ og næsta bils / sviga.
            j = i + 1
            while j < n and tree_str[j] not in ' \t()':
                j += 1
            label = tree_str[i + 1:j]
            if label == 'IP-SUB':
                # Telja IP-SUB forfeður í staflanum
                nesting = sum(1 for lbl in stack if lbl == 'IP-SUB')
                nestings.append(nesting)
            stack.append(label)
            i = j
        elif ch == ')':
            if stack:
                stack.pop()
            i += 1
        else:
            i += 1

    return nestings


# ============================================================
# AÐALMÆLING / MAIN MEASUREMENT
# ============================================================

def measure_tree_depth(
    parsed_file: Path,
    debug: bool = False,
) -> dict:
    """Mæla trédýpt og IP-SUB-hreiðslu í þáttaðri skrá.

    MÆLINGAR:
        - total_sentences: Fjöldi setninga (trjáa).
        - mean_tree_depth: Meðal-hámarksdýpt per tré. AÐAL-v.
        - std_tree_depth: Staðalfrávik trédýpta (population).
        - pct_complex_trees: Hlutfall trjáa með dýpt ≥ 3.
        - total_ip_sub: Heildarfjöldi IP-SUB-hnúta í skrá.
        - mean_ip_sub_nesting: Meðal-hreiðslustig IP-SUB (0 ef engin).

    AÐVÖRUN: Ef total_sentences < 10 birtist viðvörun í debug-ham —
    tölfræði á svona litlu úrtaki er óáreiðanleg.

    VILLU-SÍUN:
        - Tóm tré (tómur strengur) eru sleppt þegjandi.
        - Tré með færri en 2 hnúta (hámarks-svigadýpt ≤ 1) eru sleppt
          og birt viðvörun í debug-ham (líklega þáttunarvilla).

    Args:
        parsed_file: Slóð á .psd skrá.
        debug: Ef True, prenta trédýptir fyrstu 10 setninga og dýpsta tré.

    Returns:
        Dict með mælingum (sjá ofan). Lykill `filename` er bætt við.
    """
    trees = load_parsed_trees(parsed_file)

    depths: list[int] = []
    all_ip_sub_nestings: list[int] = []
    skipped_short = 0

    # Geymum dýpsta tré til villuleitar
    deepest_tree = ''
    deepest_depth = -1

    for tree_str in trees:
        if not tree_str:
            continue

        # Reikna hámarksdýpt með svigatalningu beint á strengnum
        # (áður en við filterum) svo við getum athugað stærð.
        max_bracket = 0
        current = 0
        for ch in tree_str:
            if ch == '(':
                current += 1
                if current > max_bracket:
                    max_bracket = current
            elif ch == ')':
                current -= 1

        # Sleppa tré með færri en 2 hnúta (hámarks-svigadýpt ≤ 1)
        if max_bracket < 2:
            skipped_short += 1
            if debug:
                snippet = tree_str[:80] + ('…' if len(tree_str) > 80 else '')
                print(
                    f"  [DEBUG] Sleppi of litlu tré (max_bracket="
                    f"{max_bracket}): {snippet}"
                )
            continue

        depth = max_bracket - 1  # rót = dýpt 0
        depths.append(depth)

        if depth > deepest_depth:
            deepest_depth = depth
            deepest_tree = tree_str

        # IP-SUB-hreiðsla í þessu tré
        nestings = collect_ip_sub_nesting(tree_str)
        all_ip_sub_nestings.extend(nestings)

    total_sentences = len(depths)
    total_ip_sub = len(all_ip_sub_nestings)

    # Reikna tölfræði — vernda gegn tómum listum
    if total_sentences > 0:
        mean_depth = mean(depths)
        std_depth = stdev(depths)
        n_complex = sum(1 for d in depths if d >= COMPLEX_DEPTH_THRESHOLD)
        pct_complex = n_complex / total_sentences * 100
    else:
        mean_depth = 0.0
        std_depth = 0.0
        pct_complex = 0.0

    # IP-SUB hreiðsla: 0 ef engin IP-SUB
    if total_ip_sub > 0:
        mean_ip_sub_nesting = mean(all_ip_sub_nestings)
    else:
        mean_ip_sub_nesting = 0.0

    # Aðvörun fyrir stuttar skrár — aðeins í debug-ham svo batch-keyrslur
    # verði ekki hávaðasamar.
    if debug and total_sentences < 10:
        print(
            f"  AÐVÖRUN: {parsed_file.name} hefur aðeins "
            f"{total_sentences} setningar — tölfræði er óáreiðanleg."
        )

    if debug:
        print(f"\n  [DEBUG] Skrá: {parsed_file.name}")
        print(
            f"  [DEBUG] Setningar: {total_sentences}, "
            f"sleppt (of stutt tré): {skipped_short}"
        )
        print(
            f"  [DEBUG] Meðal-trédýpt: {mean_depth:.2f}, "
            f"Staðalfrávik: {std_depth:.2f}, "
            f"Flóknar (≥{COMPLEX_DEPTH_THRESHOLD}): {pct_complex:.1f}%"
        )
        print(
            f"  [DEBUG] IP-SUB hnútar: {total_ip_sub}, "
            f"Meðal-hreiðsla: {mean_ip_sub_nesting:.2f}"
        )
        print(f"  [DEBUG] Trédýpt fyrstu 10 setninga: {depths[:10]}")
        if deepest_tree:
            snippet = deepest_tree
            if len(snippet) > 200:
                snippet = snippet[:200] + '…'
            print(f"  [DEBUG] Dýpsta tréið (dýpt={deepest_depth}):")
            print(f"    {snippet}")

    return {
        'filename': parsed_file.name,
        'total_sentences': total_sentences,
        'mean_tree_depth': mean_depth,
        'std_tree_depth': std_depth,
        'pct_complex_trees': pct_complex,
        'total_ip_sub': total_ip_sub,
        'mean_ip_sub_nesting': mean_ip_sub_nesting,
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
        filename, total_sentences, mean_tree_depth, std_tree_depth,
        pct_complex_trees, total_ip_sub, mean_ip_sub_nesting

    Args:
        results: Listi af dict frá measure_tree_depth.
        output_path: Slóð á CSV-skrá.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'filename',
        'total_sentences',
        'mean_tree_depth',
        'std_tree_depth',
        'pct_complex_trees',
        'total_ip_sub',
        'mean_ip_sub_nesting',
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            row_out = dict(row)
            row_out['mean_tree_depth'] = f"{row['mean_tree_depth']:.2f}"
            row_out['std_tree_depth'] = f"{row['std_tree_depth']:.2f}"
            row_out['pct_complex_trees'] = f"{row['pct_complex_trees']:.1f}"
            row_out['mean_ip_sub_nesting'] = (
                f"{row['mean_ip_sub_nesting']:.2f}"
            )
            writer.writerow(row_out)


# ============================================================
# PRENTA TÖFLU / PRINT TABLE
# ============================================================

def print_results_table(results: list[dict]) -> None:
    """Prenta niðurstöður á skipanalínu sem töflu.

    Args:
        results: Listi af dict frá measure_tree_depth.
    """
    print(f"\nVÍDD 9: Setningarþyngd — trédýpt (syntactic complexity)")
    print("=" * 100)

    # Hauslína / Header
    print(
        f"  {'Skrá':<35} {'Setn.':<6} {'Dýpt':<6} {'Staðfr.':<8} "
        f"{'%flók':<7} {'IP-SUB':<7} {'Hreiðs.':<8}"
    )
    print(
        f"  {'-'*35} {'-'*6} {'-'*6} {'-'*8} {'-'*7} {'-'*7} {'-'*8}"
    )

    for r in results:
        print(
            f"  {r['filename']:<35} "
            f"{r['total_sentences']:<6} "
            f"{r['mean_tree_depth']:<6.2f} "
            f"{r['std_tree_depth']:<8.2f} "
            f"{r['pct_complex_trees']:<7.1f} "
            f"{r['total_ip_sub']:<7} "
            f"{r['mean_ip_sub_nesting']:<8.2f}"
        )

    # --- MEÐALTÖL / AVERAGES ---
    if results:
        avg_depth = mean([r['mean_tree_depth'] for r in results])
        avg_pct = mean([r['pct_complex_trees'] for r in results])
        avg_nest = mean([r['mean_ip_sub_nesting'] for r in results])
        print(
            f"  {'-'*35} {'-'*6} {'-'*6} {'-'*8} {'-'*7} {'-'*7} {'-'*8}"
        )
        print(
            f"  {'MEÐALTAL':<35} "
            f"{'':6} "
            f"{avg_depth:<6.2f} "
            f"{'':8} "
            f"{avg_pct:<7.1f} "
            f"{'':7} "
            f"{avg_nest:<8.2f}"
        )

    print("=" * 100)
    print()
    print("  SKÝRING DÁLKA / COLUMN KEY:")
    print("    Setn.    = Fjöldi setninga (trjáa í skrá)")
    print("    Dýpt     = Meðal-hámarksdýpt tréa (rót = 0). AÐAL-v.")
    print("    Staðfr.  = Staðalfrávik trédýpta")
    print(f"    %flók    = Hlutfall setninga með dýpt ≥ "
          f"{COMPLEX_DEPTH_THRESHOLD}")
    print("    IP-SUB   = Heildarfjöldi aukasetningarhnúta í skrá")
    print("    Hreiðs.  = Meðal-hreiðslustig IP-SUB "
          "(fjöldi IP-SUB forfeðra)")
    print()
    print("  TÚLKUN / INTERPRETATION:")
    print("    Dýpt > 4.0   → djúpt innfelld (formlegt, bókmenntir, fræði)")
    print("    Dýpt 3.0-4.0 → miðlungs (fréttir, staðlað ritmál)")
    print("    Dýpt < 3.0   → flöt (óformlegt, talmál, fyrirsagnir)")
    print("    %flók > 50%  → mikil tíðni flókinna setninga í skránni")
    print()
    print("  ATHUGASEMD / NOTE:")
    print("    Þröskuldurinn dýpt ≥ 3 er tekinn úr UD-byggðum „sentence")
    print("    weight“ fyrirlestri Steinþórs Steingrímssonar. IcePaHC")
    print("    liðgerðartré eru kerfisbundið dýpri en UD-háðartré (POS-")
    print("    hnútar bæta við lagi), svo %flók verður hærra fyrir sama")
    print("    innihald. Þröskuldurinn er AÐFERÐAFRÆÐILEG HLIÐSTÆÐA —")
    print("    hann er ekki kvarðaður sérstaklega fyrir IcePaHC.")


# ============================================================
# FINNA ALLAR ÞÁTTAÐAR SKRÁR / FIND ALL PARSED FILES
# ============================================================

def find_parsed_files(parsed_dir: Path) -> list[Path]:
    """Finna allar .psd skrár í möppu (endurkvæmt).

    Args:
        parsed_dir: Mappa með .psd skrám.

    Returns:
        Raðaður listi af Path-hlutum.
    """
    psd_files = sorted(parsed_dir.rglob('*.psd'))

    if not psd_files:
        print(f"  AÐVÖRUN: Engar .psd skrár fundust í {parsed_dir}")

    return psd_files


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra trédýptarmælingu á þáttuðum skrám."""
    parser = argparse.ArgumentParser(
        description=(
            "Vídd 9: Mæla setningarþyngd (trédýpt, "
            "IP-SUB-hreiðslu) úr þáttuðum trjám."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Á möppu:
  python scripts/dim9_tree_depth.py \\
      --parsed-dir output/parsed/human_reference/

  # Á tilgreindum skrám:
  python scripts/dim9_tree_depth.py \\
      --files output/parsed/human_reference/news_ref_001_parsed.psd

  # Með villuleit (sýnir dýptir fyrstu 10 setninga og dýpsta tréð):
  python scripts/dim9_tree_depth.py \\
      --parsed-dir output/parsed/human_reference/ --debug

  # Dry-run (reikna, prenta, ekki vista CSV):
  python scripts/dim9_tree_depth.py \\
      --parsed-dir output/parsed/human_reference/ --dry-run
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--parsed-dir',
        type=Path,
        help="Mappa með þáttuðum .psd skrám. Leit er endurkvæm."
    )
    group.add_argument(
        '--files',
        type=Path,
        nargs='+',
        help="Ein eða fleiri .psd skrár til að greina."
    )

    parser.add_argument(
        '--output-csv',
        type=Path,
        default=Path('output/dim9_tree_depth.csv'),
        help="Slóð á CSV-úttaksskrá (sjálfgefið: output/dim9_tree_depth.csv)"
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Prenta trédýptir fyrstu 10 setninga og dýpsta tréð per skrá."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Reikna og prenta — ekki vista CSV."
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
        for f in parsed_files:
            if not f.exists():
                print(f"VILLA: Skrá finnst ekki: {f}")
                return

    if not parsed_files:
        print("VILLA: Engar skrár til að greina.")
        return

    print(f"\n  Greini {len(parsed_files)} skrá(r)...")
    if args.debug:
        print("  [DEBUG] Villuleitarhamur virkur")

    # --- KEYRA MÆLINGU ---
    results = []
    for pf in parsed_files:
        result = measure_tree_depth(pf, debug=args.debug)
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
