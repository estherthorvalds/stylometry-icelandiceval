#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dim1_frumlagsnafnfall.py — VÍDD 1: Fyrirsagnir/setningar án frumlagsnafnliðar
===============================================================================

TILGANGUR / PURPOSE:
    Þetta skrifta mælir hlutfall setninga sem innihalda sögn en hafa ekkert
    frumlag (NP-SBJ). Þetta er klassískt stíleinkenni fréttafyrirsagna á íslensku:
    „Fengu verkfærakistur að gjöf" — sögnin „Fengu" er í persónu en ekkert nafnorð
    er frumlag.

    This script measures the proportion of sentences that contain a finite verb
    but lack a subject noun phrase (NP-SBJ). This is a classic stylistic feature
    of Icelandic news headlines.

MÁLVÍSINDI / LINGUISTICS:
    Í íslensku fréttamáli er algengt að sleppa frumlagi í fyrirsögnum, sem er
    óvenjulegt í flestum öðrum germönskum tungumálum. Þetta er stíleinkenni sem
    mannlegir fréttamenn hafa og LLM-líkön kunna ekki endilega.

    Milička-formúlan mælir hvort líkön hermast eftir þessu áberandi stíleinkennni.

INNTAK / INPUT:
    Þáttuð tré úr data/parsed/human/*.txt og data/parsed/llm/*.txt
    (ein lína = eitt þáttunartré í svigaformi)

ÚTTAK / OUTPUT:
    v-gildi (hlutfall) per textaskrá, til notkunar í run_milicka.py

KEYRSLA / USAGE:
    # Sem eininga:
    from dim1_frumlagsnafnfall import measure_subject_drop
    v_value = measure_subject_drop("data/parsed/human/news_ruv_parsed.txt")

    # Frá skipanalínu:
    python scripts/dim1_frumlagsnafnfall.py --parsed-file data/parsed/human/news_ruv_parsed.txt
"""

import argparse
import re
import sys
from pathlib import Path


# ============================================================
# LESA ÞÁTTUÐ TRÉ / READ PARSED TREES
# Þáttuð tré eru geymd ein per línu. Hvert tré er strengur í
# svigaformi, t.d. "(ROOT (IP-MAT (NP-SBJ ...) (VBPI ...)))".
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
        # Sleppa tómum línum — þetta er öryggisráðstöfun ef einhverjar
        # auðar línur slæddust inn í skrána.
        trees = [line.strip() for line in f if line.strip()]

    return trees


# ============================================================
# GREINA EITT TRÉ / ANALYZE ONE TREE
# Athuga hvort setning hafi:
#   1. Persónubeygða sögn (finite verb) — gefur til kynna fullsetningu
#   2. Frumlagsnafnlið (NP-SBJ) — ef ekki, er frumlagslaust
#   3. Boðháttur (IP-IMP) — útilokaður, þar sem boðháttur hefur
#      aldrei frumlag í íslensku
# ============================================================

def analyze_tree(tree_str: str) -> dict:
    """Greina eitt þáttunartré og skila niðurstöðum.

    LYKLAR IcePaHC-SKEMANS SEM VIÐ NOTUM:
        NP-SBJ  = Frumlagsnafnliður (subject noun phrase)
        IP-IMP  = Boðháttur (imperative clause)
        VBPI/VBDI = Sögn í framsöguhætti (indicative verb, present/past)
        VBPS/VBDS = Sögn í viðtengingarhætti (subjunctive verb)
        BEPI/BEDI = „vera" beygð (be-verb, present/past indicative)
        DOPI/DODI = „gera" beygð (do-verb)
        HVPI/HVDI = „hafa" beygð (have-verb)
        MDPI/MDDI = Hjálparsögn (modal verb)
        RDPI/RDDI = „verða" beygð (become-verb)

    Args:
        tree_str: Eitt þáttunartré sem strengur í svigaformi.

    Returns:
        dict með lyklum:
            - has_subject: True ef NP-SBJ finnst í trénu
            - has_verb: True ef persónubeygð sögn finnst
            - is_imperative: True ef setningin er í boðhætti
    """
    # --- ATHUGA FRUMLAG ---
    # Einfaldasta leitin: er strengurinn „NP-SBJ" í trénu?
    # Þetta virkar vel vegna þess að IcePaHC-þáttarinn notar
    # einungis NP-SBJ sem merki fyrir frumlag.
    has_subject = 'NP-SBJ' in tree_str

    # --- ATHUGA BOÐHÁTT ---
    # IP-IMP táknar boðháttarsetningu (imperative clause).
    # Boðháttur hefur aldrei frumlag á íslensku, svo við viljum
    # ekki telja boðháttur-setningar sem „frumlagslausar" —
    # þær eru frumlagslausar af öðrum ástæðum.
    is_imperative = 'IP-IMP' in tree_str

    # --- ATHUGA PERSÓNUBEYGÐA SÖGN ---
    # Regluleg segð (regular expression / regex) leitar að sagnmerkjum
    # IcePaHC-skemans. Munstur:
    #   (VB|BE|DO|HV|MD|RD) = sagnstofn (vera, gera, hafa, modal, verða)
    #   [PD]                 = P (present/nútíð) eða D (past/þátíð)
    #   [IS]                 = I (indicative/framsöguháttur) eða S (subjunctive/viðtengingarh.)
    #
    # Þetta nær yfir allar persónubeygar sagnir, t.d.:
    #   VBPI = venjuleg sögn, nútíð, framsöguháttur
    #   BEDI = „vera", þátíð, framsöguháttur
    #   MDPS = hjálparsögn, nútíð, viðtengingarh.
    #
    # \b er „word boundary" — tryggir að við finnum ekki „VBPI" sem hluta
    # af lengra orði (þó slíkt sé ólíklegt í þáttunartréum).
    has_verb = bool(re.search(r'\b(VB|BE|DO|HV|MD|RD)[PD][IS]\b', tree_str))

    return {
        'has_subject': has_subject,
        'has_verb': has_verb,
        'is_imperative': is_imperative,
    }


# ============================================================
# MÆLA HLUTFALL — AÐALMÆLING / MAIN MEASUREMENT
# Þetta er kjarnafallið: það tekur lista af þáttuðum trjám,
# greinir hvert tré, og reiknar hlutfall setninga án
# frumlagsnafnliðar.
# ============================================================

def measure_subject_drop(parsed_file: Path) -> tuple[float, int, int]:
    """Mæla hlutfall setninga án frumlagsnafnliðar (subject-drop rate).

    REIKNIAÐFERÐ:
        1. Lesa öll þáttuð tré úr skrá
        2. Greina hvert tré: hefur það sögn? frumlag? boðhátt?
        3. Sía burtu setningar sem eru:
           - Án sagnar (nafnliðar-fyrirsagnir, t.d. „Nýr forstjóri Landsbankans")
           - Í boðhætti (t.d. „Sjáðu hér!")
        4. Af þeim sem eftir standa: hve margar hafa ekkert NP-SBJ?

    Args:
        parsed_file: Slóð á skrá með þáttuðum trjám (ein lína = eitt tré).

    Returns:
        Tuple af:
            - v: hlutfall setninga án frumlagsnafnliðar (0.0 til 1.0)
            - n_dropped: fjöldi setninga án frumlagsnafnliðar
            - n_total: heildarfjöldi gildra setninga (með sögn, ekki boðháttur)
    """
    trees = load_parsed_trees(parsed_file)

    n_dropped = 0   # Setningar ÁN frumlagsnafnliðar
    n_total = 0     # Heildarfjöldi gildra setninga (með sögn, ekki boðháttur)

    for tree_str in trees:
        result = analyze_tree(tree_str)

        # Sleppa setningum án sagnar — t.d. nafnliðarfyrirsagnir eins og
        # „Nýr forstjóri Landsbankans". Þessar setningar hafa ekki frumlag
        # af öðrum ástæðum en stíleinkenni.
        if not result['has_verb']:
            continue

        # Sleppa boðhættisetningum — t.d. „Sjáðu þetta!"
        # Boðháttur er aldrei með frumlagi á íslensku, svo þetta er
        # málkerfisregla, ekki stílval.
        if result['is_imperative']:
            continue

        # Þetta er gild setning: hún hefur sögn og er ekki boðháttur.
        n_total += 1

        # Ef engin NP-SBJ finnst → setningin er frumlagslaus
        if not result['has_subject']:
            n_dropped += 1

    # Reikna hlutfall. Vernda gegn deilingu með núlli.
    v = n_dropped / n_total if n_total > 0 else 0.0

    return v, n_dropped, n_total


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# Gerir kleift að keyra skriftið sjálfstætt til prófunar.
# ============================================================

def main() -> None:
    """Keyra mælingu á einni þáttaðri skrá og prenta niðurstöðu."""
    parser = argparse.ArgumentParser(
        description="Vídd 1: Mæla hlutfall setninga án frumlagsnafnliðar.",
        epilog="""
Dæmi:
  python scripts/dim1_frumlagsnafnfall.py --parsed-file data/parsed/human/news_ruv_parsed.txt
        """
    )
    parser.add_argument(
        '--parsed-file',
        type=Path,
        required=True,
        help="Slóð á skrá með þáttuðum trjám"
    )

    args = parser.parse_args()

    # Keyra mælinguna
    v, n_dropped, n_total = measure_subject_drop(args.parsed_file)

    # Prenta niðurstöðu á skipanalínu
    print(f"\nVÍDD 1: Frumlagsnafnliðarleysi (subject drop)")
    print(f"{'=' * 50}")
    print(f"  Skrá: {args.parsed_file.name}")
    print(f"  Gildar setningar (með sögn, ekki boðháttur): {n_total}")
    print(f"  Án frumlagsnafnliðar: {n_dropped}")
    print(f"  Hlutfall (v): {v:.4f} ({v:.1%})")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
