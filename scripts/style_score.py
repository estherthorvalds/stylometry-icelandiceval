#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
style_score.py — Hjálparfall: Reikna 0-100 stigatöflueinkunn
==============================================================

TILGANGUR / PURPOSE:
    Þetta skrifta inniheldur hjálparföll til að reikna stigatöflueinkunn (score)
    sem segir hversu vel LLM-líkan hermist eftir stíleinkenni mannlegra texta.

    This module provides utility functions to calculate a 0-100 style score
    that measures how well an LLM mimics a particular stylistic feature of
    human-written text.

FORMÚLA / FORMULA:
    score = 100 × (1 - |v_human - v_model| / v_human)

    Þar sem:
        v_human = gildi stíleinkennisins í mannlegum texta (t.d. 0.42 = 42%)
        v_model = sama gildi í texta LLM-líkansins
        |...| = algildi (absolute value) — viðsnúningur ef líkan er yfir/undir

    Einkunn:
        100 = líkan framleiðir nákvæmlega sama hlutfall og mannlegir textar
          0 = líkan framleiðir ekkert af stíleinkenninu (eða meira en tvöfalt)

DÆMI / EXAMPLES:
    Ef v_human = 0.40 (40% setninga án frumlags) og v_model = 0.36 (36%):
        score = 100 × (1 - |0.40 - 0.36| / 0.40)
              = 100 × (1 - 0.04 / 0.40)
              = 100 × (1 - 0.10)
              = 90.0

    Ef v_human = 0.40 og v_model = 0.10 (10%):
        score = 100 × (1 - |0.40 - 0.10| / 0.40)
              = 100 × (1 - 0.30 / 0.40)
              = 100 × (1 - 0.75)
              = 25.0

KEYRSLA / USAGE:
    from style_score import compute_style_score
    score = compute_style_score(v_human=0.40, v_model=0.36)
    print(f"Stig: {score:.1f}")  # 90.0
"""


def compute_style_score(v_human: float, v_model: float) -> float:
    """Reikna 0-100 stigatöflueinkunn fyrir stílhermu LLM-líkans.

    Formúla:
        score = 100 × (1 - |v_human - v_model| / v_human)
        Niðurstaðan er klippt (clamped) á bilinu [0, 100].

    Sértilfelli:
        - Ef v_human = 0 og v_model = 0 → 100 (bæði hafa ekkert af eiginleikanum)
        - Ef v_human = 0 og v_model > 0 → 0 (líkan hefur eitthvað sem mannlegt á ekki)

    HVERS VEGNA KLIPPA Á [0, 100]?
        Ef v_model er meira en tvöfalt v_human, verður reiknað gildi neikvætt.
        Til dæmis: v_human = 0.20, v_model = 0.50
        → 100 × (1 - 0.30/0.20) = 100 × (1 - 1.5) = -50
        Við klippum þetta á 0, vegna þess að neikvætt stig er ekki upplýsandi.

    Args:
        v_human: Gildi stíleinkennisins í mannlegum texta (t.d. hlutfall,
                 meðaltal, eða annað tölugildi frá víddarskriftu).
        v_model: Sama gildi í texta LLM-líkansins.

    Returns:
        Einkunn á bilinu 0.0 til 100.0
    """
    # Sértilfelli: ef mannleg gildi eru 0
    if v_human == 0:
        # Ef bæði eru 0, þá eru þau eins → fullkomin einkunn
        return 100.0 if v_model == 0 else 0.0

    # Aðalformúla
    raw_score = 100.0 * (1.0 - abs(v_human - v_model) / v_human)

    # Klippa á bilinu [0, 100] — ekki leyfa neikvætt eða yfir 100
    return max(0.0, min(100.0, raw_score))


def format_score_table(results: list[dict]) -> str:
    """Sníða niðurstöður sem textatöflu til birtingar.

    Nytsamleg hjálparfunktía sem run_milicka.py getur notað til að
    prenta snyrtileg niðurstöður.

    Args:
        results: Listi af dict með lyklum:
            - name: Nafn líkans (t.d. "Gemini_3_Thinking")
            - v_model: Mælt gildi líkansins
            - delta_v: Frávik frá mannlegu gildi (Formúla 1)
            - b_d: Staðlað frávik (Formúla 3)
            - score: Stigatöflueinkunn (0-100)

    Returns:
        Strengur með snyrtilega sniðinni töflu.
    """
    # Fyrirsagnarlína
    header = f"  {'Líkan':<25} {'v_model':>8} {'Δv':>8} {'b_d':>8} {'Stig':>8}"
    separator = f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8} {'-'*8}"

    lines = [header, separator]

    for r in results:
        line = (
            f"  {r['name']:<25} "
            f"{r['v_model']:>8.4f} "
            f"{r['delta_v']:>+8.3f} "
            f"{r['b_d']:>+8.2f} "
            f"{r['score']:>8.1f}"
        )
        lines.append(line)

    return '\n'.join(lines)


# ============================================================
# SJÁLFSTÆÐ KEYRSLA / STANDALONE USAGE
# Þetta er aðallega til prófunar og dæma.
# ============================================================

if __name__ == "__main__":
    # Prófunardæmi
    print("Prófun á style_score.py")
    print("=" * 40)

    # Dæmi 1: Líkan nálægt mannlegu gildi
    score1 = compute_style_score(v_human=0.40, v_model=0.36)
    print(f"v_human=0.40, v_model=0.36 → stig={score1:.1f}")  # 90.0

    # Dæmi 2: Líkan langt frá mannlegu gildi
    score2 = compute_style_score(v_human=0.40, v_model=0.10)
    print(f"v_human=0.40, v_model=0.10 → stig={score2:.1f}")  # 25.0

    # Dæmi 3: Líkan nákvæmlega eins
    score3 = compute_style_score(v_human=0.30, v_model=0.30)
    print(f"v_human=0.30, v_model=0.30 → stig={score3:.1f}")  # 100.0

    # Dæmi 4: Líkan með of miklu
    score4 = compute_style_score(v_human=0.20, v_model=0.50)
    print(f"v_human=0.20, v_model=0.50 → stig={score4:.1f}")  # 0.0

    # Dæmi 5: Bæði núll
    score5 = compute_style_score(v_human=0.0, v_model=0.0)
    print(f"v_human=0.00, v_model=0.00 → stig={score5:.1f}")  # 100.0
