#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
run_milicka.py — AÐALSKRIFTA: Keyrir allar víddir og reiknar Milička-formúlur
===============================================================================

TILGANGUR / PURPOSE:
    Þetta er aðalskriftið sem tengir allt saman. Það keyrir allar þrjár
    víddir (dim1, dim2, dim3) á mannlegum og LLM-framleiddun textum,
    reiknar Milička-formúlurnar, og prentar stigatöflu.

    This is the main orchestrator script. It runs all three dimensions on
    human and LLM texts, computes Milička's formulas, and prints a score table.

MILIČKA-FORMÚLURNAR / THE FORMULAS:
    Formúla 1: Δv = v_human - v_model
        Frávik líkans frá mannlegum texta á einni vídd.
        Jákvætt Δv = líkanið hefur minna af stíleinkenninu.
        Neikvætt Δv = líkanið hefur meira af stíleinkenninu.

    Formúla 2: i = v_half2 - v_half1
        Náttúrulegt frávik í mennskum gögnum. Mennsku gögnunum er skipt í
        tvö helminga og mismunurinn er reiknaður. Þetta segir okkur hversu
        mikil náttúruleg sveifla er í eiginleikanum — þetta er „baseline noise".

    Formúla 3: b_d = Δv / SE(I_d)
        Staðlað frávik per vídd. Δv er deilt með staðalskekkju (standard error)
        sem reiknuð er með bootstrap. Þetta staðlar frávikið svo hægt sé
        að bera saman víddir sem mælast á mjög ólíkum kvörðum.

    Formúla 4: B = ‖b‖ = √(Σ b_d²)
        Heildarskor yfir allar víddir. Evklíðskt norm af öllum b_d gildum.
        Þetta er eitt tala sem segir hversu langt líkanið er frá mannlegum
        texta yfir allar stílvíddir samtímis.

FLÆÐI / FLOW:
    1. Lesa þáttuð tré (human + LLM)
    2. Keyra dim1, dim2, dim3 á hvert skráarpar
    3. Reikna bootstrap SE per vídd
    4. Reikna b_d per vídd per líkan (formúla 3)
    5. Reikna B per líkan (formúla 4)
    6. Prenta stigatöflu

KEYRSLA / USAGE:
    python scripts/run_milicka.py
    python scripts/run_milicka.py --human-dir data/parsed/human --llm-dir data/parsed/llm
"""

import argparse
import math
import random
import sys
from pathlib import Path

# Innflutt frá öðrum skriftum í verkefninu.
# Þetta virkar vegna þess að Python leitar í scripts/ möppunni
# ef skriftið er keyrt þaðan, eða ef við bætum við slóðinni.
# Til öryggis bætum við scripts/ slóðinni við sys.path.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dim1_frumlagsnafnfall import measure_subject_drop
from dim2_aukasetningar import measure_subordination
from dim3_nafnlidalengd import measure_np_length
from style_score import compute_style_score, format_score_table


# ============================================================
# SJÁLFGEFNAR SLÓÐIR / DEFAULT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_HUMAN_DIR = PROJECT_ROOT / "data" / "parsed" / "human"
DEFAULT_LLM_DIR = PROJECT_ROOT / "data" / "parsed" / "llm"


# ============================================================
# VÍDDARFÖLLIN / DIMENSION FUNCTIONS
# Listi af öllum víddum sem við mælum. Þetta gerir auðvelt
# að bæta við nýjum víddum seinna — bara bæta við í listann.
# ============================================================

# Hvert stak er tuple af (nafn, mælifall).
# Mælifallið tekur Path og skilar (v, ...) þar sem v er fyrsta gildið.
DIMENSIONS = [
    ("dim1_frumlagsleysi", measure_subject_drop),
    ("dim2_aukasetningar", measure_subordination),
    ("dim3_nafnlidalengd", measure_np_length),
]


# ============================================================
# BOOTSTRAP SE / STANDARD ERROR VIA BOOTSTRAP
# Bootstrap er tölfræðileg aðferð til að meta staðalskekkju (SE)
# þegar formúla er ekki tiltæk. Aðferðin endurúrtekur (resample)
# gögnin oft, reiknar mæligildið á hverju úrtaki, og metur
# staðalskekkjuna út frá dreifingu niðurstaðnanna.
# ============================================================

def bootstrap_se(
    parsed_trees_path: Path,
    measure_fn,
    n_resamples: int = 1000,
    seed: int = 42,
) -> tuple[float, float, float]:
    """Reikna bootstrap staðalskekkju (SE) á vídd.

    AÐFERÐ:
        1. Lesa þáttuð tré úr skrá
        2. Skipta í tvennt (helminga 1 og 2)
        3. Mæla víddina á hvorum helmingi
        4. Reikna i = v_half2 - v_half1 (formúla 2: náttúrulegt frávik)
        5. Endurtaka 1000 sinnum með slembiraðaðri röð (bootstrap)
        6. Reikna SE úr dreifingu i-gilda

    HVERS VEGNA BOOTSTRAP?
        Milička-formúlurnar þurfa staðalskekkju til að staðla frávikið
        (formúla 3: b_d = Δv / SE). Ef við höfum ekki nóg gögn eða
        dreifingin er óregluleg, er bootstrap einfaldasta leiðin til
        að meta SE áreiðanlega.

    Args:
        parsed_trees_path: Slóð á þáttuð mannleg tré.
        measure_fn: Mælifall (t.d. measure_subject_drop) sem tekur Path.
        n_resamples: Fjöldi bootstrap endurúrtaka (sjálfgefið 1000).
        seed: Slembifræ (random seed) fyrir endurtekjanleika.

    Returns:
        Tuple af:
            - v_full: Mælt gildi á öllum gögnunum
            - i_observed: Raunverulegt náttúrulegt frávik (formúla 2)
            - se: Bootstrap staðalskekkja
    """
    # Lesa allar línur (þáttuð tré) úr skránni
    with open(parsed_trees_path, 'r', encoding='utf-8') as f:
        all_lines = [line.strip() for line in f if line.strip()]

    n = len(all_lines)
    if n < 4:
        # Of fá gögn til bootstrap — þarf minnst 4 setningar
        # (2 í hvorum helmingi)
        print(f"  AÐVÖRUN: Of fá gögn ({n} setningar) til bootstrap.")
        return 0.0, 0.0, 0.0

    mid = n // 2

    # Búa til tímabundnar skrár fyrir hvorn helming.
    # Við notum sama snið og upprunalega skráin (ein lína = eitt tré)
    # svo mælifallið geti lesið þær eins og venjulega.
    import tempfile

    def measure_from_lines(lines: list[str]) -> float:
        """Skrifa línur í tímabundna skrá og mæla."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.txt', encoding='utf-8', delete=False
        ) as tmp:
            tmp.write('\n'.join(lines) + '\n')
            tmp_path = Path(tmp.name)
        try:
            # Mælifallið skilar tuple — fyrsta gildið er v
            result = measure_fn(tmp_path)
            return result[0]
        finally:
            tmp_path.unlink()  # Eyða tímabundinni skrá

    # Mæla á öllum gögnunum
    v_full = measure_from_lines(all_lines)

    # Mæla á hvorum helmingi (formúla 2)
    v_half1 = measure_from_lines(all_lines[:mid])
    v_half2 = measure_from_lines(all_lines[mid:])
    i_observed = v_half2 - v_half1

    # Bootstrap: endurúrtaka og reikna i-gildi
    random.seed(seed)
    i_values = []
    indices = list(range(n))

    for _ in range(n_resamples):
        # Slembiröðun (shuffle) á vísitölum
        random.shuffle(indices)

        # Skipta í tvo helminga eftir slembiröðun
        resample_half1 = [all_lines[j] for j in indices[:mid]]
        resample_half2 = [all_lines[j] for j in indices[mid:]]

        # Mæla hvorn helming
        r1 = measure_from_lines(resample_half1)
        r2 = measure_from_lines(resample_half2)

        # Reikna i-gildi (frávik milli helminga)
        i_values.append(r2 - r1)

    # Reikna staðalskekkju (SE) úr dreifingu i-gilda
    # SE = staðalfrávik (standard deviation) dreifingar i-gildanna
    mean_i = sum(i_values) / len(i_values)
    variance = sum((x - mean_i) ** 2 for x in i_values) / (len(i_values) - 1)
    se = math.sqrt(variance)

    return v_full, i_observed, se


# ============================================================
# FINNA ÞÁTTAÐAR SKRÁR / FIND PARSED FILES
# Finnur hvaða textaskrár eru til í human/ og llm/ möppunum
# og tengir saman pör (human vs LLM) á grundvelli textategundar.
# ============================================================

def find_human_files(human_dir: Path) -> list[Path]:
    """Finna allar þáttaðar mannlegar textaskrár.

    Args:
        human_dir: Mappa með þáttuðum mannlegum trjám.

    Returns:
        Raðaður listi af Path hlutum.
    """
    if not human_dir.exists():
        print(f"VILLA: Mappa finnst ekki: {human_dir}")
        return []

    return sorted(human_dir.glob('*_parsed.txt'))


def find_llm_files(llm_dir: Path) -> list[Path]:
    """Finna allar þáttaðar LLM textaskrár.

    Args:
        llm_dir: Mappa með þáttuðum LLM trjám.

    Returns:
        Raðaður listi af Path hlutum.
    """
    if not llm_dir.exists():
        print(f"VILLA: Mappa finnst ekki: {llm_dir}")
        return []

    return sorted(llm_dir.glob('*_parsed.txt'))


def extract_base_category(filename: str) -> str:
    """Draga út grunntextategund úr skráarheiti.

    Dæmi:
        "news_ruv_parsed.txt" → "news_ruv"
        "news_ruv_gemini_parsed.txt" → "news_ruv"
        "journals_islmal_gpt5_parsed.txt" → "journals_islmal"

    Aðferðin fjarlægir "_parsed" viðskeytið og þekkt líkananöfn.

    Args:
        filename: Skráarheiti (t.d. "news_ruv_gemini_parsed.txt").

    Returns:
        Grunntextategund sem strengur.
    """
    # Fjarlægja "_parsed.txt"
    name = filename.replace('_parsed.txt', '').replace('_parsed', '')

    # Þekkt líkananöfn sem gætu verið í skráarheitinu.
    # Bættu nöfnum við hér ef ný líkön eru prófuð.
    known_models = [
        'gemini', 'gpt5', 'gpt4', 'lechat', 'claude', 'llama',
        'mistral', 'command', 'le_chat',
    ]

    # Fjarlægja líkananafn ef það er í lok strengsins
    for model in known_models:
        if name.endswith(f'_{model}'):
            name = name[:-(len(model) + 1)]
            break

    return name


# ============================================================
# AÐALFLÆÐI / MAIN FLOW
# Þetta fall tengir allt saman:
# 1. Finnur mannlegar og LLM skrár
# 2. Keyrir allar víddir á mannlegum gögnum
# 3. Reiknar bootstrap SE per vídd
# 4. Keyrir allar víddir á LLM gögnum
# 5. Reiknar b_d og B per líkan
# 6. Prentar niðurstöður
# ============================================================

def run_benchmark(human_dir: Path, llm_dir: Path, n_resamples: int = 1000) -> None:
    """Keyra Milička-viðmið á öllum textum og prenta niðurstöður.

    Args:
        human_dir: Mappa með þáttuðum mannlegum trjám.
        llm_dir: Mappa með þáttuðum LLM trjám.
        n_resamples: Fjöldi bootstrap endurúrtaka.
    """
    # --- SKREF 1: Finna skrár ---
    human_files = find_human_files(human_dir)
    llm_files = find_llm_files(llm_dir)

    if not human_files:
        print("VILLA: Engar mannlegar þáttaðar skrár fundust.")
        sys.exit(1)

    print("=" * 80)
    print("MILIČKA STÍLVIÐMIÐ — ICELANDIC STYLOMETRY BENCHMARK")
    print("=" * 80)
    print(f"\nMannlegar skrár: {len(human_files)}")
    for f in human_files:
        print(f"  - {f.name}")
    print(f"\nLLM skrár: {len(llm_files)}")
    for f in llm_files:
        print(f"  - {f.name}")
    print()

    # --- SKREF 2: Mæla mannleg gögn og reikna bootstrap SE per vídd per skrá ---
    # Geyma niðurstöður í dict: {skráarheiti: {víddarheiti: (v, se)}}
    human_results = {}

    for h_file in human_files:
        h_name = h_file.stem.replace('_parsed', '')
        human_results[h_name] = {}

        print(f"\n{'─' * 60}")
        print(f"MANNLEG GÖGN: {h_name}")
        print(f"{'─' * 60}")

        for dim_name, measure_fn in DIMENSIONS:
            print(f"\n  {dim_name}:")

            # Mæla vídd og reikna bootstrap SE
            v_full, i_observed, se = bootstrap_se(
                h_file, measure_fn, n_resamples=n_resamples
            )

            human_results[h_name][dim_name] = {
                'v': v_full,
                'i': i_observed,
                'se': se,
            }

            print(f"    v (heild)  = {v_full:.4f}")
            print(f"    i (frávik) = {i_observed:+.4f}")
            print(f"    SE         = {se:.4f}")

    # --- SKREF 3: Mæla LLM gögn og reikna formúlur ---
    if not llm_files:
        print("\nEngar LLM skrár fundust. Sleppi samanburði.")
        return

    print(f"\n\n{'=' * 80}")
    print("SAMANBURÐUR VIÐ RISAMÁLLÍKÖN")
    print("=" * 80)

    # Búa til heildartöflu
    for h_file in human_files:
        h_name = h_file.stem.replace('_parsed', '')
        h_data = human_results[h_name]

        # Finna LLM skrár sem tilheyra sömu textategund
        h_category = extract_base_category(h_file.name)

        matching_llm = [
            f for f in llm_files
            if extract_base_category(f.name) == h_category
        ]

        if not matching_llm:
            continue

        print(f"\n{'─' * 60}")
        print(f"TEXTATEGUND: {h_category}")
        print(f"{'─' * 60}")

        for llm_file in matching_llm:
            llm_name = llm_file.stem.replace('_parsed', '')

            # Fjarlægja textategundina úr nafninu til að fá líkananafnið
            model_label = llm_name.replace(h_category + '_', '')

            print(f"\n  Líkan: {model_label}")

            b_d_values = []  # Safna b_d gildum yfir allar víddir

            for dim_name, measure_fn in DIMENSIONS:
                # Mæla LLM gildi
                v_model = measure_fn(llm_file)[0]

                # Sækja mannleg gildi og SE
                v_human = h_data[dim_name]['v']
                se = h_data[dim_name]['se']

                # FORMÚLA 1: Δv = v_human - v_model
                delta_v = v_human - v_model

                # FORMÚLA 3: b_d = Δv / SE
                # Ef SE er mjög lítil (nálægt 0), þá er deiling óstöðug.
                # Við notum þröskuldinn 0.0001 til að forðast deilingu með ~0.
                if se > 0.0001:
                    b_d = delta_v / se
                else:
                    # Ef SE er ~0, þá er frávik annað hvort mjög stórt eða 0
                    b_d = float('inf') if abs(delta_v) > 0.0001 else 0.0

                b_d_values.append(b_d)

                # Stigatöflueinkunn
                score = compute_style_score(v_human, v_model)

                print(f"    {dim_name}:")
                print(f"      v_human={v_human:.4f}  v_model={v_model:.4f}  "
                      f"Δv={delta_v:+.4f}  b_d={b_d:+.2f}  stig={score:.1f}")

            # FORMÚLA 4: B = ‖b‖ = √(Σ b_d²)
            # Evklíðskt norm — þetta er „fjarlægðin" frá mannlegum texta
            # í fjölvíddarrými allra stílvídda.
            # Ef eitthvert b_d gildi er inf, verður B líka inf.
            if any(b == float('inf') for b in b_d_values):
                B = float('inf')
            else:
                B = math.sqrt(sum(b ** 2 for b in b_d_values))

            print(f"    ────────────────────────────")
            print(f"    B (heild) = {B:.2f}")
            print(f"    TÚLKUN: ", end="")
            if B < 1:
                print("Líkanið er mjög nálægt mannlegum texta.")
            elif B < 2:
                print("Líkanið er í viðunandi fjarlægð.")
            elif B < 5:
                print("Greinilegur munur á milli líkans og mannlegs texta.")
            else:
                print("Verulegur munur — líkanið hermist illa eftir stílnum.")

    # --- LOKAORÐ ---
    print(f"\n\n{'=' * 80}")
    print("HVERNIG Á AÐ TÚLKA NIÐURSTÖÐURNAR:")
    print("=" * 80)
    print("  Δv  = v_human - v_model (frávik per vídd)")
    print("        Jákvætt: líkanið hefur minna af eiginleikanum")
    print("        Neikvætt: líkanið hefur meira af eiginleikanum")
    print()
    print("  b_d = Δv / SE (staðlað frávik per vídd)")
    print("        |b_d| < 1: innan náttúrulegrar sveiflu")
    print("        |b_d| 1-2: veikt frávik")
    print("        |b_d| > 2: verulegt frávik")
    print()
    print("  B   = √(Σ b_d²) (heildarskor yfir allar víddir)")
    print("        B < 1: mjög nálægt mannlegum texta")
    print("        B < 2: viðunandi")
    print("        B > 5: verulegur munur")
    print()
    print("  Stig = 0-100 einkunn per vídd")
    print("        100 = fullkomið samræmi")
    print("          0 = ekkert samræmi")
    print("=" * 80)


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra Milička-viðmið."""
    parser = argparse.ArgumentParser(
        description="Keyra Milička stílviðmið á öllum textum.",
        epilog="""
Dæmi:
  python scripts/run_milicka.py
  python scripts/run_milicka.py --human-dir data/parsed/human --llm-dir data/parsed/llm
  python scripts/run_milicka.py --n-resamples 500
        """
    )
    parser.add_argument(
        '--human-dir',
        type=Path,
        default=DEFAULT_HUMAN_DIR,
        help=f"Mappa með þáttuðum mannlegum trjám (sjálfgefið: {DEFAULT_HUMAN_DIR})"
    )
    parser.add_argument(
        '--llm-dir',
        type=Path,
        default=DEFAULT_LLM_DIR,
        help=f"Mappa með þáttuðum LLM trjám (sjálfgefið: {DEFAULT_LLM_DIR})"
    )
    parser.add_argument(
        '--n-resamples',
        type=int,
        default=1000,
        help="Fjöldi bootstrap endurúrtaka (sjálfgefið: 1000)"
    )

    args = parser.parse_args()

    run_benchmark(args.human_dir, args.llm_dir, args.n_resamples)


if __name__ == "__main__":
    main()
