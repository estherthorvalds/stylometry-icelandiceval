#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
dim7_complementizers.py — VÍDD 7: Tíðni tengiorða/samtenginga (complementizer frequency)
==========================================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta mælir tíðni tengiorða (complementizers) í þáttuðum trjám.
    Tengiorð kynna aukasetningar (subordinate clauses) og eru hér skoðuð til að
    mæla setningaflækjustig (syntactic complexity).

    This script measures the frequency of complementizer nodes (C sem, C að)
    in IceConParse constituency-parsed output.

MÁLVÍSINDI / LINGUISTICS:
    Tengiorð (complementizers) opna aukasetningar. Í þessari skriftu er aðallega
    litið á eftirfarandi tengiorð:

    1. „að“ (that) — kynna fallsetningar (declarative complement
       clauses). Dæmi: „Hún sagði **að** hann væri veikur.“
       Þessi setning er í CP-THT (that-clause) í IcePaHC.

    2. „sem“ (which/that/who) — kynna tilvísunaraukasetningar (relative
       clauses). Dæmi: „Maðurinn **sem** kom í gær er veikur.“
       Þessi setning er í CP-REL (relative clause) í IcePaHC.

    Há tíðni tengiorða gefur til kynna flókna setningagerð með mörgum
    innfelldum aukasetningum — algeng í formlegum textum með mikið af
    upplýsingum. Þetta bætir við vídd 2 (subordination ratio) án þess að
    endurtaka hana: vídd 2 telur hversu margar setningar eru aukasetningar,
    vídd 7 skoðar HVERNIG aukasetning er kynnt.

    HVERS VEGNA TVÆR MISMUNANDI VÍDDIR FYRIR UNDIRSKIPUN:
        Vídd 2 (aukasetningarhlutfall): Telur IP-SUB vs IP-MAT — mælir
            HLUTFALL aukasetninga af öllum setningum.
        Vídd 7 (að/sem-tengiorðatíðni): Telur C-hnúta — mælir AÐFERÐ undirskipunar
            (hvernig aukasetningar eru tengdar aðalsetningu).
        
    TENGSL VIÐ BIBER-RAMMA / CONNECTION TO BIBER'S MDA:

        Þessar tvær víddir hjálpast að við að skoða aukasetningar í textum. 
        Í Biber er fjallað um hvers lags textategundir eru líklegri en aðrar
        til að innihalda mikið af slíkum setningum. 

        Í MDA-ramma Bibers (1988) eru tengiorð hluti af „elaborated vs.
        situation-dependent reference“ víddinni. Textar með mikla notkun
        tengiorða hafa „elaborated reference“ — höfundurinn treystir
        ekki á samhengi (context) heldur skilgreinir allt í setningunni.
        Textar sem nota fá tengiorð treysta á samhengi (talmál, blogg
        þar sem lesandinn og höfundurinn deila reynslu).

        Ekki verður stuðst við þessa staðhæfingu hér þar sem verið er að 
        mæla íslenskt mál og ekki hægt að vísa í góða heimild sem heldur þessu 
        fram. Þessar skriftur gera það sem þær gera sem er einfaldlega að 
        telja aukasentingar og tengiorð. 

    MARGRÆÐNI „AÐ“ / AMBIGUITY OF „AÐ“:
        Orðið „að“ á íslensku hefur mörg hlutverk:
            1. Tengiorð / Complementizer (C að): „Hún sagði **að** hann kæmi“
            2. Forsetning / Preposition (P að): „Ég fór **að** húsinu“
            3. Nafnháttarmerki / Infinitive marker (TO að): „Hún ætlar **að** fara“

        Þáttarinn (IceConParse) sér um þessa aðgreiningu. Í þáttunartrjám:
            (C að)  = tengiorð    ← ÞETTA TELJUM VIÐ
            (P að)  = forsetning  ← EKKI talið
            (TO að) = nafnháttur  ← EKKI talið

        Regex-mynstrið okkar leitar EINGÖNGU að „(C að)“ svo engin margræðni
        er til staðar í talningunni. Þetta er helsti kosturinn við að nota
        þáttuð tré frekar en hrátexta.

    MARGRÆÐNI „SEM“ / AMBIGUITY OF „SEM“:
        Er orðið „sem“ á íslensku nánast eingöngu tilvísunartengiorð?
        Í IcePaHC-svigaformi birtist það sem (C sem) í CP-REL-hnútum.
        ATHUGA MÖGULEGA MARGRÆÐNI??

INNTAK / INPUT:
    Þáttuð tré úr data/parsed/human/*.txt og data/parsed/llm/*.txt
    (ein lína = eitt þáttunartré í svigaformi)

ÚTTAK / OUTPUT:
    1. CSV-skrá: output/dim7_complementizers.csv
    2. Tafla á skipanalínu (með villuleitarupplýsingum)

KEYRSLA / USAGE:
    # Í möppu:
    python scripts/dim7_complementizers.py --parsed-dir output/parsed/

    # Í tilgreindum skrám:
    python scripts/dim7_complementizers.py --files output/parsed/news_001.parsed

    # Sem innflutt eining:
    from dim7_complementizers import measure_complementizers
    result = measure_complementizers(Path("data/parsed/human/news_ruv_parsed.txt"))
"""

import argparse
import csv
import re
from pathlib import Path


# ============================================================
# LESA ÞÁTTUÐ TRÉ / READ PARSED TREES
# Sama aðferð og í dim1–dim6 — les þáttuð tré úr skrá,
# eitt per línu.
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
# REGLULEGAR SEGÐIR / REGEX PATTERNS
# ============================================================
#
# TENGIORÐ Í ICEPAHC-SVIGAFORMI / COMPLEMENTIZERS IN BRACKET NOTATION:
#   Tengiorð birtast sem endahnútar (terminal nodes) með merkið „C“:
#       (C sem)   — tilvísunartengiorð (relative complementizer)
#       (C að)    — fallsetningatengiorð (declarative complementizer)
#
#   MIKILVÆGT: „að“ birtist einnig sem:
#       (P að)   — forsetning (preposition) → EKKI talið
#       (TO að)  — nafnháttarmerki (infinitive marker) → EKKI talið
#   Regex-mynstrið \(C\s+að\) tryggir að við teljum EINGÖNGU „(C að)“.
#
# LAUFBLÖÐ OG SETNINGAMERKI:
#   LEAF_PATTERN finnur öll orð (laufblöð) í trénu til heildarorðatalningar.
#   IP-MAT og IP-SUB eru notuð til setningatalningar (endurnýtt frá dim2).
# ============================================================

# --- „SEM“ TENGIORÐ / RELATIVE COMPLEMENTIZER ---
# Finnur endahnúta (C sem) — tilvísunartengiorð í CP-REL hnútum.
# Mynstur: \( + C + eitt-eða-fleiri-bil + sem + \)
# Dæmi sem samsvara:   (C sem)
# Dæmi sem SAMSVARA EKKI: (CONJ sem), (N-N sem) — ef slíkt væri til
C_SEM_PATTERN = re.compile(r'\(C\s+sem\)')

# --- „AÐ“ TENGIORÐ / DECLARATIVE COMPLEMENTIZER ---
# Finnur endahnúta (C að) — fallsetningatengiorð í CP-THT hnútum.
# Mynstur: \( + C + eitt-eða-fleiri-bil + að + \)
# Dæmi sem samsvara:    (C að)
# Dæmi sem SAMSVARA EKKI: (P að), (TO að), (C sem)
C_AD_PATTERN = re.compile(r'\(C\s+að\)')

# --- ÖLL LAUFBLÖÐ / ALL LEAVES (for total word count) ---
# Sama mynstur og í dim3, dim4, dim5. Laufblað = orðmynd á
# undan lokunarsviga ).
LEAF_PATTERN = re.compile(r'[^\s\(\)]+(?=\))')

# --- SETNINGAMERKI / CLAUSE LABELS (endurnýtt frá dim2) ---
# IP-MAT = aðalsetning (matrix clause)
# IP-SUB = aukasetning (subordinate clause)
# Þessi regex-mynstur finna merkin í trénu á eftir opnunarsviga.
# [\s\(] á eftir merkinu = finna heilt merki, ekki hluta.
IP_MAT_PATTERN = re.compile(r'\(IP-MAT[\s\(]')
IP_SUB_PATTERN = re.compile(r'\(IP-SUB[\s\(]')


# ============================================================
# DRAGA ÚT TENGIORÐAUPPLÝSINGAR ÚR EINU TRÉ
# EXTRACT COMPLEMENTIZER INFO FROM ONE TREE
# ============================================================

def extract_comp_counts_from_tree(tree_str: str) -> dict:
    """Telja tengiorð, orð og setningar í einu þáttunartré.

    AÐFERÐ:
        1. Nota regex til að finna (C sem) og (C að) endahnúta.
        2. Telja heildarfjölda orða (öll laufblöð).
        3. Telja aðalsetningar (IP-MAT) og aukasetningar (IP-SUB).

    DÆMI ÚR RAUNVERULEGUM TRJÁM:
        Tré: (ROOT (IP-MAT (NP-SBJ (D-N Maðurinn) (CP-REL (C sem)
             (IP-SUB (VBDI kom)))) (VBDI fór)))
        → 1 „sem“, 0 „að“, 4 orð, 1 IP-MAT, 1 IP-SUB

        Tré: (ROOT (IP-MAT (NP-SBJ (PRO-N Hún)) (VBDI sagði)
             (CP-THT (C að) (IP-SUB (NP-SBJ (PRO-N hann))
             (MDDS myndi) (VB koma)))))
        → 0 „sem“, 1 „að“, 6 orð, 1 IP-MAT, 1 IP-SUB

        Tré: (ROOT (IP*MAT (NP*SBJ (N-N Maðurinn) (CP*REL (C sem) 
            (TO að) (IP*SUB (VB koma) (PP (P í) (NP (N-A gær)))))) 
            (BEPI er) (VBN farinn) (. .)))
        → Í tilfellinu „sem að“ telur þáttarinn „að“ ranglega vera 
            nafnháttarmerki, sem er gott í þessu tilfelli því annars
            yrði dæmið ranglega talið tvisvar. 
    Args:
        tree_str: Eitt þáttunartré sem strengur í svigaformi.

    Returns:
        Dict með lyklum:
            - n_sem: fjöldi (C sem) hnúta
            - n_ad: fjöldi (C að) hnúta
            - n_words: heildarfjöldi orða (laufblaða)
            - n_mat: fjöldi aðalsetninga (IP-MAT)
            - n_sub: fjöldi aukasetninga (IP-SUB)
    """
    n_sem = len(C_SEM_PATTERN.findall(tree_str))
    n_ad = len(C_AD_PATTERN.findall(tree_str))
    n_words = len(LEAF_PATTERN.findall(tree_str))
    n_mat = len(IP_MAT_PATTERN.findall(tree_str))
    n_sub = len(IP_SUB_PATTERN.findall(tree_str))

    return {
        'n_sem': n_sem,
        'n_ad': n_ad,
        'n_words': n_words,
        'n_mat': n_mat,
        'n_sub': n_sub,
    }


# ============================================================
# AÐALMÆLING / MAIN MEASUREMENT
# Keyra skrá af þáttuðum trjám og reikna öll hlutföll.
# ============================================================

def measure_complementizers(parsed_file: Path, debug: bool = False) -> dict:
    """Mæla tíðni tengiorða (complementizers) í textaskrá.

    REIKNIAÐFERÐ:
        1. Lesa öll þáttuð tré úr skrá
        2. Telja (C sem) og (C að) per tré
        3. Telja öll tré
        4. Reikna hlutfall og tíðni

    ÚTREIKNINGAR:
        - comp_per_1000_words = (sem + að) / heildarorð × 1000
          Tíðni tengiorða á hverja 1.000 orð — aðalmælikvarðinn.
        - comp_per_clause = (sem + að) / (IP-MAT + IP-SUB)
          Hversu mörg tengiorð per setningu — viðbótarmælikvarði.
        - sem_ratio = sem / (sem + að)
          Hlutfall tilvísunaraukasetninga (relative clauses) af öllum
          tengiorðum. Hátt gildi → margar CP-REL, lágt → margar CP-THT.
        - sem_per_1000_words, ad_per_1000_words
          Tíðni hvers tengiorðs fyrir sig.

    Args:
        parsed_file: Slóð á skrá með þáttuðum trjám.
        debug: Ef True, prenta villuleitarupplýsingar.

    Returns:
        Dict með lyklum:
            - filename
            - sem_count, ad_count, total_complementizers
            - total_words, total_clauses
            - comp_per_1000_words, comp_per_clause
            - sem_ratio
            - sem_per_1000_words, ad_per_1000_words
    """
    trees = load_parsed_trees(parsed_file)

    if debug:
        print(f"\n  [DEBUG] Skrá: {parsed_file.name}")
        print(f"  [DEBUG] Fjöldi þáttaðra trjáa: {len(trees)}")

    # Heildartalningar yfir allar setningar í skránni
    total_sem = 0
    total_ad = 0
    total_words = 0
    total_mat = 0
    total_sub = 0

    for i, tree_str in enumerate(trees):
        counts = extract_comp_counts_from_tree(tree_str)
        total_sem += counts['n_sem']
        total_ad += counts['n_ad']
        total_words += counts['n_words']
        total_mat += counts['n_mat']
        total_sub += counts['n_sub']

        # --- VILLULEIT: Sýna fyrstu 5 trén ef debug er virkt ---
        if debug and i < 5:
            print(f"  [DEBUG] Tré #{i+1}: sem={counts['n_sem']}, "
                  f"að={counts['n_ad']}, orð={counts['n_words']}, "
                  f"IP-MAT={counts['n_mat']}, IP-SUB={counts['n_sub']}")
            # Sýna stutta útgáfu af trénu (fyrstu 120 stafir)
            preview = tree_str[:120] + ('...' if len(tree_str) > 120 else '')
            print(f"  [DEBUG]   Tré: {preview}")

    total_comp = total_sem + total_ad
    total_clauses = total_mat + total_sub

    if debug:
        print(f"  [DEBUG] Heildarsamantekt: sem={total_sem}, að={total_ad}, "
              f"samtals={total_comp}")
        print(f"  [DEBUG] Orð={total_words}, setningar={total_clauses} "
              f"(IP-MAT={total_mat}, IP-SUB={total_sub})")

    # --- REIKNA HLUTFÖLL ---

    # 1. Tengiorð per 1.000 orð — aðalmælikvarði
    #    Þetta er sambærilegt við Biber-mælikvarða „that-deletions“ og
    #    „WH-relative clauses“ nema við teljum bæði sem og að.
    if total_words > 0:
        comp_per_1000 = (total_comp / total_words) * 1000
    else:
        comp_per_1000 = 0.0

    # 2. Tengiorð per setningu
    #    Hversu mörg tengiorð eru á hverja setningu (aðal + auka)?
    #    Gildi > 1 gæti þýtt innfelldar aukasetningar.
    if total_clauses > 0:
        comp_per_clause = total_comp / total_clauses
    else:
        comp_per_clause = 0.0

    # 3. sem-hlutfall (relative complementizer ratio)
    #    Hlutfall „sem“ af öllum tengiorðum. Ef hátt → flestar
    #    aukasetningar eru tilvísunaraukasetningar (CP-REL).
    if total_comp > 0:
        sem_ratio = total_sem / total_comp
    else:
        sem_ratio = 0.0

    # 4. Tíðni hvers tengiorðs — til fíngreindar
    if total_words > 0:
        sem_per_1000 = (total_sem / total_words) * 1000
        ad_per_1000 = (total_ad / total_words) * 1000
    else:
        sem_per_1000 = 0.0
        ad_per_1000 = 0.0

    if debug:
        print(f"  [DEBUG] comp/1000={comp_per_1000:.2f}, "
              f"comp/clause={comp_per_clause:.4f}, "
              f"sem_ratio={sem_ratio:.4f}")
        print(f"  [DEBUG] sem/1000={sem_per_1000:.2f}, "
              f"að/1000={ad_per_1000:.2f}")

    return {
        'filename': parsed_file.name,
        'sem_count': total_sem,
        'ad_count': total_ad,
        'total_complementizers': total_comp,
        'total_words': total_words,
        'total_clauses': total_clauses,
        'comp_per_1000_words': comp_per_1000,
        'comp_per_clause': comp_per_clause,
        'sem_ratio': sem_ratio,
        'sem_per_1000_words': sem_per_1000,
        'ad_per_1000_words': ad_per_1000,
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
        filename, sem_count, ad_count, total_complementizers,
        total_words, total_clauses, comp_per_1000_words,
        comp_per_clause, sem_ratio, sem_per_1000_words, ad_per_1000_words

    Args:
        results: Listi af dict frá measure_complementizers.
        output_path: Slóð á CSV-skrá til að vista.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'filename',
        'sem_count',
        'ad_count',
        'total_complementizers',
        'total_words',
        'total_clauses',
        'comp_per_1000_words',
        'comp_per_clause',
        'sem_ratio',
        'sem_per_1000_words',
        'ad_per_1000_words',
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            # Slétta hlutfallstölur til 4 aukastafa í CSV
            row_out = dict(row)
            row_out['comp_per_1000_words'] = (
                f"{row['comp_per_1000_words']:.2f}"
            )
            row_out['comp_per_clause'] = f"{row['comp_per_clause']:.4f}"
            row_out['sem_ratio'] = f"{row['sem_ratio']:.4f}"
            row_out['sem_per_1000_words'] = (
                f"{row['sem_per_1000_words']:.2f}"
            )
            row_out['ad_per_1000_words'] = (
                f"{row['ad_per_1000_words']:.2f}"
            )
            writer.writerow(row_out)


# ============================================================
# PRENTA TÖFLU / PRINT TABLE
# Prenta greinargóða töflu á skipanalínu með öllum mælikvörðum.
# ============================================================

def print_results_table(results: list[dict]) -> None:
    """Prenta niðurstöður á skipanalínu sem töflu.

    DÁLKASKÝRINGAR:
        sem   = Fjöldi (C sem) — tilvísunartengiorð
        að    = Fjöldi (C að) — fallsetningatengiorð
        Σteng = Heildarfjöldi tengiorða (sem + að)
        Orð   = Heildarfjöldi orða (laufblöð)
        Setn  = Heildarfjöldi setninga (IP-MAT + IP-SUB)
        /1000 = Tengiorð per 1.000 orð
        /setn = Tengiorð per setningu
        s-hlf = sem-hlutfall (sem / heildar tengiorð)

    Args:
        results: Listi af dict frá measure_complementizers.
    """
    print(f"\nVÍDD 7: Tíðni tengiorða (complementizer frequency)")
    print("=" * 110)

    # Hauslína / Header
    print(f"  {'Skrá':<35} {'sem':<5} {'að':<5} {'Σteng':<5} "
          f"{'Orð':<7} {'Setn':<6} {'/1000':<7} {'/setn':<7} "
          f"{'s-hlf':<7} {'sem/k':<7} {'að/k':<7}")
    print(f"  {'-'*35} {'-'*5} {'-'*5} {'-'*5} "
          f"{'-'*7} {'-'*6} {'-'*7} {'-'*7} "
          f"{'-'*7} {'-'*7} {'-'*7}")

    for r in results:
        print(
            f"  {r['filename']:<35} "
            f"{r['sem_count']:<5} "
            f"{r['ad_count']:<5} "
            f"{r['total_complementizers']:<5} "
            f"{r['total_words']:<7} "
            f"{r['total_clauses']:<6} "
            f"{r['comp_per_1000_words']:<7.2f} "
            f"{r['comp_per_clause']:<7.4f} "
            f"{r['sem_ratio']:<7.4f} "
            f"{r['sem_per_1000_words']:<7.2f} "
            f"{r['ad_per_1000_words']:<7.2f}"
        )

    # --- MEÐALTÖL / AVERAGES ---
    if results:
        n = len(results)
        avg_comp_1000 = sum(r['comp_per_1000_words'] for r in results) / n
        avg_comp_clause = sum(r['comp_per_clause'] for r in results) / n
        avg_sem_ratio = sum(r['sem_ratio'] for r in results) / n
        avg_sem_1000 = sum(r['sem_per_1000_words'] for r in results) / n
        avg_ad_1000 = sum(r['ad_per_1000_words'] for r in results) / n

        # Heildarsamantekt
        total_sem = sum(r['sem_count'] for r in results)
        total_ad = sum(r['ad_count'] for r in results)
        total_comp = sum(r['total_complementizers'] for r in results)

        print(f"  {'-'*35} {'-'*5} {'-'*5} {'-'*5} "
              f"{'-'*7} {'-'*6} {'-'*7} {'-'*7} "
              f"{'-'*7} {'-'*7} {'-'*7}")
        print(
            f"  {'MEÐALTAL':<35} "
            f"{'':<5} {'':<5} {'':<5} "
            f"{'':<7} {'':<6} "
            f"{avg_comp_1000:<7.2f} "
            f"{avg_comp_clause:<7.4f} "
            f"{avg_sem_ratio:<7.4f} "
            f"{avg_sem_1000:<7.2f} "
            f"{avg_ad_1000:<7.2f}"
        )
        print(
            f"  {'SAMTALS':<35} "
            f"{total_sem:<5} {total_ad:<5} {total_comp:<5} "
            f"{'':<7} {'':<6} "
            f"{'':<7} {'':<7} {'':<7} {'':<7} {'':<7}"
        )

    print("=" * 110)
    print()
    print("  SKÝRING DÁLKA / COLUMN KEY:")
    print("    sem   = Fjöldi (C sem) — tilvísunartengiorð (relative complementizer)")
    print("    að    = Fjöldi (C að) — fallsetningatengiorð (declarative complementizer)")
    print("    Σteng  = Heildarfjöldi tengiorða (sem + að)")
    print("    Orð   = Heildarfjöldi orða (laufblöð í þáttunartrjám)")
    print("    Setn  = Heildarfjöldi setninga (IP-MAT + IP-SUB)")
    print("    /1000 = Tengiorð per 1.000 orð")
    print("    /setn = Tengiorð per setningu (IP-MAT + IP-SUB)")
    print("    s-hlf = sem-hlutfall: sem / (sem + að)")
    print('    sem/k = „sem“ per 1.000 orð')
    print('    að/k  = „að“ per 1.000 orð')
    print()
    print("  TÚLKUN:")
    print("    /1000 > 40  → mikil tengiorðanotkun")
    print("    /1000 ~ 25-40 → miðlungs")
    print("    /1000 < 25  → lág tengiorðanotkun")
    print("    s-hlf > 0.5 → flestar aukasetningar eru tilvísanar (CP-REL)")
    print("    s-hlf < 0.5 → flestar aukasetningar eru fallsetningar (CP-THT)")


# ============================================================
# FINNA ALLAR ÞÁTTAÐAR SKRÁR / FIND ALL PARSED FILES
# ============================================================

def find_parsed_files(parsed_dir: Path) -> list[Path]:
    """Finna allar þáttaðar skrár í möppu (endurkvæmt).

    Leitar að .txt skrám sem innihalda þáttuð tré (ein lína = eitt tré).
    Raðar skrám í stafrófsröð til endurtaka (reproducible) keyrslu.

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
        description="Vídd 7: Mæla tíðni tengiorða / complementizer frequency.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Á möppu:
  python scripts/dim7_complementizers.py \\
      --parsed-dir output/parsed/

  # Á tilgreindum skrám:
  python scripts/dim7_complementizers.py \\
      --files output/parsed/news_001.parsed output/parsed/blog_001.parsed

  # Með villuleit:
  python scripts/dim7_complementizers.py \\
      --parsed-dir output/parsed/ --debug

  # Stýra úttak-CSV staðsetningu:
  python scripts/dim7_complementizers.py \\
      --parsed-dir output/parsed/ \\
      --output-csv output/dim7_custom.csv
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
        default=Path('output/dim7_complementizers.csv'),
        help="Slóð á CSV-úttaksskrá (sjálfgefið: output/dim7_complementizers.csv)"
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help="Sýna villuleitarupplýsingar (debug output)"
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
    if args.debug:
        print("  [DEBUG] Villuleitarhamur virkur — sýni ítarlegar upplýsingar")

    # --- KEYRA MÆLINGU ---
    results = []
    for pf in parsed_files:
        result = measure_complementizers(pf, debug=args.debug)
        results.append(result)

    # --- PRENTA TÖFLU ---
    print_results_table(results)

    # --- VISTA CSV ---
    save_results_csv(results, args.output_csv)
    print(f"\n  CSV vistað: {args.output_csv}")


if __name__ == "__main__":
    main()
