#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dim3_nafnlidalengd.py — VÍDD 3: Meðallengd nafnliða (mean NP length)
======================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta mælir meðallengd nafnliða (noun phrases / NP) í texta.

    This script measures the mean length (in tokens) of noun phrases (NPs)
    in constituency-parsed text.

MÁLVÍSINDI / LINGUISTICS:
    Lengd nafnliða er mælikvarði á upplýsingaþéttleika (information density).
    Lengri nafnliðir fela í sér fleiri lýsingarorð (adjectives), eignarfallsliði
    (genitive phrases), forsetningarliði (prepositional phrases) o.fl.

    - Stutt NP (1-2 orð): „bíllinn“, „hún“ — algengt í talmáli og bloggum
    - Meðallöng NP (3-4 orð): „stóri rauði bíllinn“ — algeng í fréttum
    - Löng NP (5+ orð): „nýja aðgerðaráætlun ríkisstjórnarinnar um loftslagsmál“
      — algeng í fræðitextum og stjórnsýslutextum

AÐFERÐ / METHOD:
    Til að telja orð í NP notar skriftan einfalda talningu í svigum:
    Finna NP í trénu, lesa allt textainnihald (laufblöð/leaves)
    undir honum, og telja orðin. Innfeldir NP eru taldir sérstaklega.

INNTAK / INPUT:
    Þáttuð tré úr data/parsed/human/*.txt og data/parsed/llm/*.txt

ÚTTAK / OUTPUT:
    v-gildi (meðallengd) per textaskrá, til notkunar í run_milicka.py

KEYRSLA / USAGE:
    from dim3_nafnlidalengd import measure_np_length
    v_value = measure_np_length("data/parsed/human/news_ruv_parsed.txt")

    python scripts/dim3_nafnlidalengd.py --parsed-file data/parsed/human/news_ruv_parsed.txt
"""

import argparse
import re
from pathlib import Path


# ============================================================
# LESA ÞÁTTUÐ TRÉ / READ PARSED TREES
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
# FINNA NAFNLIÐI Í TRÉ / FIND NOUN PHRASES IN TREE
# Þessi aðferð notar svigatalningu (bracket counting) til
# að finna alla nafnliði (NP) og draga út innihald þeirra.
# ============================================================

def extract_np_spans(tree_str: str) -> list[str]:
    """Finna alla nafnliði (NP) í þáttunartré og skila innihaldi þeirra.

    AÐFERÐ:
        Leita að „(NP“ í strengnum og nota svigatalningu til að finna
        hvar NP-liðurinn endar (þegar opnunar- og lokasvigar eru jafnir). Þetta er 
        nauðsynlegt vegna þess að NP-liðir geta innihaldið innfelda NP-liði.

    MIKILVÆGT: Við finnum NP sem er upphafsstafur merkis, þ.e.a.s. „(NP “,
    „(NP-SBJ “, „(NP-OB1 “, o.s.frv. Öll NP-afbrigði eru nafnliðir.

    Dæmi:
        Tré: (ROOT (IP-MAT (NP-SBJ (NPR-N Fyrirtækið)) (VBPI opnar) (NP-OB1 (N-A skrifstofu))))
        Skilar: ["(NP-SBJ (NPR-N Fyrirtækið))", "(NP-OB1 (N-A skrifstofu))"]

    Args:
        tree_str: Þáttunartré sem strengur.

    Returns:
        Listi af strengjum — hvert NP-undirtré sem heill strengur.
    """
    np_spans = []

    # Leita að öllum stöðum þar sem „(NP“ kemur fyrir.
    # Eftir „(NP“ verður annað hvort bil „ “ (ef NP er bara NP) eða
    # bandstrik „-“ (ef NP hefur viðskeyti, t.d. NP-SBJ, NP-OB1).
    # Eða opnunarsvigrúmur „(“ ef NP inniheldur strax undirtré.
    i = 0
    while i < len(tree_str):
        # Finna næsta „(NP“ í strengnum
        pos = tree_str.find('(NP', i)
        if pos == -1:
            break  # Enginn NP-liður eftir

        # Athuga hvort þetta sé raunverulegt NP-merki.
        # Næsti stafur á eftir „(NP“ verður að vera bil, bandstrik eða svigi.
        # Þetta kemur í veg fyrir rangar niðurstöður ef „NP“ er hluti af öðru orði
        # (þó það sé mjög ólíklegt í IcePaHC-þáttunartrjám).
        next_pos = pos + 3  # Staðsetning á eftir „(NP“
        if next_pos < len(tree_str) and tree_str[next_pos] not in (' ', '-', '('):
            # Ekki raunverulegt NP-merki, halda áfram
            i = next_pos
            continue

        # Nota svigatalningu (bracket counting) til að finna hvar NP-liðurinn endar.
        # Byrja á 1 vegna þess að við höfum fundið opnunarsvigrúm „(“.
        # Þegar teljari nær 0, erum við komin út úr NP-liðnum.
        depth = 0
        j = pos
        while j < len(tree_str):
            if tree_str[j] == '(':
                depth += 1
            elif tree_str[j] == ')':
                depth -= 1
                if depth == 0:
                    # Fundið lokunarsvigrúm NP-liðarins
                    np_span = tree_str[pos:j + 1]
                    np_spans.append(np_span)
                    break
            j += 1

        # Halda áfram leit á eftir þessum NP-lið
        i = j + 1

    return np_spans


# ============================================================
# TELJA ORÐ Í NAFNLIÐ / COUNT TOKENS IN NP
# Laufblöð (leaves) í þáttunartré eru orðin sjálf.
# Þau eru stafir sem koma á eftir orðflokkamerki og eru
# lokaðir af loka-sviga „)“.
# ============================================================

def count_tokens_in_np(np_str: str) -> int:
    """Telja orð (laufblöð / leaves) í nafnliðastreng.

    AÐFERÐ:
        Laufblöð (terminal nodes / leaves) í svigastreng eru orðin sjálf —
        þ.e. stafir sem koma á eftir bili á eftir orðflokkamerki,
        rétt á undan loka-sviga.

        Til dæmis í „(NP-SBJ (D-N Sá) (ADJ-N stóri) (N-N hundur))“:
            - „Sá“ er laufblað undir D-N
            - „stóri“ er laufblað undir ADJ-N
            - „hundur“ er laufblað undir N-N
            → 3 orð

    Þessi aðferð notar regluleg segð til að finna laufblöð:
    leita að mynstri þar sem bil er á undan orði og „)“ á eftir.

    Args:
        np_str: Nafnliður sem strengur í svigaformi.

    Returns:
        Fjöldi orða (laufblaða) í nafnliðnum.
    """
    # Regluleg segð sem finnur laufblöð (leaves) í svigastreng.
    # Mynstur: eitt eða fleiri stafir sem eru ekki svigrúm eða bil,
    # strax á undan loka-sviga „)“.
    # [^\s\(\)]+ nær yfir: hvaða stafi sem er nema bil, ( og )
    # (?=\))     er „lookahead“ sem tryggir að næsti stafur sé )
    #            án þess að taka hann inn í samsvörunina.
    leaves = re.findall(r'[^\s\(\)]+(?=\))', np_str)

    return len(leaves)


# ============================================================
# MÆLA MEÐALLENGD NAFNLIÐA / MEASURE MEAN NP LENGTH
# Þetta er aðalmælingin: meðalfjöldi orða per nafnlið
# yfir allan textann.
# ============================================================

def measure_np_length(parsed_file: Path) -> tuple[float, int, list[int]]:
    """Mæla meðallengd nafnliða (mean NP length in tokens) í textaskrá.

    REIKNIAÐFERÐ:
        1. Finna alla NP-liði í öllum trjám
        2. Telja orð (laufblöð) í hverjum NP-lið
        3. Reikna meðaltal

    ATHUGASEMD UM INNFELDA NP:
        NP sem er innfeldur í öðrum NP er talinn sérstaklega.
        Dæmi: „(NP (D-N Sá) (NP (N-N hundur) (PP (P frá) (NP (NPR-D Keflavík)))))“
        Hér finnast þrír NP-liðir:
            1. Ytri NP: „Sá hundur frá Keflavík“ (4 orð)
            2. Innri NP: „hundur frá Keflavík“ (3 orð)
            3. Innsti NP: „Keflavík“ (1 orð)

    Args:
        parsed_file: Slóð á skrá með þáttuðum trjám.

    Returns:
        Samstæðu (tuple) af:
            - v: meðallengd nafnliða (meðalfjöldi orða per NP)
            - n_nps: heildarfjöldi nafnliða sem fundust
            - lengths: listi af lengdum allra nafnliða (til greiningar)
    """
    trees = load_parsed_trees(parsed_file)

    lengths = []  # Lengd hvers NP-liðar (fjöldi orða)

    for tree_str in trees:
        # Finna alla NP-liði í þessu tré
        np_spans = extract_np_spans(tree_str)

        for np_str in np_spans:
            # Telja orð í þessum NP-lið
            n_tokens = count_tokens_in_np(np_str)

            # Sleppa NP-liðum með 0 orð (ætti ekki að gerast, en öryggisráðstöfun)
            if n_tokens > 0:
                lengths.append(n_tokens)

    # Reikna meðaltal. Vernda gegn tómum lista.
    n_nps = len(lengths)
    v = sum(lengths) / n_nps if n_nps > 0 else 0.0

    return v, n_nps, lengths


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra mælingu á einni þáttaðri skrá og prenta niðurstöðu."""
    parser = argparse.ArgumentParser(
        description="Vídd 3: Mæla meðallengd nafnliða (mean NP length).",
        epilog="""
Dæmi:
  python scripts/dim3_nafnlidalengd.py --parsed-file data/parsed/human/news_ruv_parsed.txt
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
    v, n_nps, lengths = measure_np_length(args.parsed_file)

    # Reikna aukaupplýsingar til birtingar
    if lengths:
        min_len = min(lengths)
        max_len = max(lengths)
        # Miðgildi (median) — raða lengdum og taka miðjugildi
        sorted_lengths = sorted(lengths)
        mid = len(sorted_lengths) // 2
        if len(sorted_lengths) % 2 == 0:
            median_len = (sorted_lengths[mid - 1] + sorted_lengths[mid]) / 2
        else:
            median_len = sorted_lengths[mid]
    else:
        min_len = max_len = median_len = 0

    # Prenta niðurstöðu
    print(f"\nVÍDD 3: Meðallengd nafnliða (mean NP length)")
    print(f"{'=' * 50}")
    print(f"  Skrá: {args.parsed_file.name}")
    print(f"  Heildarfjöldi nafnliða: {n_nps}")
    print(f"  Meðallengd (v): {v:.3f} orð per NP")
    print(f"  Miðgildi: {median_len:.1f}")
    print(f"  Lágmark: {min_len}")
    print(f"  Hámark: {max_len}")
    print(f"{'=' * 50}")
    print()
    print("  TÚLKUN:")
    print("    v ~ 1.5-2.5 → stutt NP (algengt í bloggum, talmáli)")
    print("    v ~ 2.5-3.5 → meðallöng NP (algengt í fréttum)")
    print("    v ~ 3.5+    → löng NP (algengt í fræðitextum)")


if __name__ == "__main__":
    main()
