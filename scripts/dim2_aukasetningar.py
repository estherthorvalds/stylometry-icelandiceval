#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dim2_aukasetningar.py — VÍDD 2: Hlutfall aukasetninga (subordination ratio)
=============================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta mælir hlutfall aukasetninga (subordinate clauses) í texta.
    Aukasetningar eru setningar sem eru háðar aðalsetningu, t.d.
    „Hún sagði [að hann kæmi]" þar sem „að hann kæmi" er aukasetningin.

    This script measures the ratio of subordinate clauses (IP-SUB) to
    matrix/main clauses (IP-MAT) in text.

MÁLVÍSINDI / LINGUISTICS:
    Gott er að nota hlutfall aukasetninga til að mæla setningaflækjustig
    (syntactic complexity). Fræðitextar hafa yfirleitt hærra hlutfall
    aukasetninga en fréttir eða blogg, vegna þess að akademískt ritmál
    notar fleiri setningaliði innan sömu málsgreinar til að lýsa flóknum 
    hugmyndum.

    - Hátt hlutfall → flóknari setningagerð (fræðitextar, akademískt ritmál)
    - Lágt hlutfall → einfaldari setningagerð (fréttir, blogg)

LYKLAR IcePaHC SEM VIÐ NOTUM:
    IP-MAT    = Aðalsetning (matrix clause) — sjálfstæð setning
    IP-SUB    = Aukasetning (subordinate clause) — háð setning
    CP-REL    = Tilvísunaraukasetning (relative clause, t.d. „sem ég þekki“)
    CP-ADV    = Atviksorðsaukasetning (adverbial clause, t.d. „þegar hann kom“)
    CP-THT    = Að-setning (that-clause, t.d. „sagði að hann kæmi“)
    CP-QUE    = Spurnaraukasetning (indirect question, t.d. „spurði hvort...“)

INNTAK / INPUT:
    Þáttuð tré úr data/parsed/human/*.txt og data/parsed/llm/*.txt

ÚTTAK / OUTPUT:
    v-gildi (hlutfall) per textaskrá, til notkunar í run_milicka.py

KEYRSLA / USAGE:
    from dim2_aukasetningar import measure_subordination
    v_value = measure_subordination("data/parsed/human/journals_islmal_parsed.txt")

    python scripts/dim2_aukasetningar.py --parsed-file data/parsed/human/journals_islmal_parsed.txt
"""

import argparse
import re
from pathlib import Path


# ============================================================
# LESA ÞÁTTUÐ TRÉ / READ PARSED TREES
# Sama aðferð og í dim1 — les þáttuð tré úr skrá, eitt per línu.
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
# TELJA MERKINGAR Í EINU TRÉ / COUNT LABELS IN ONE TREE
# Telur hversu oft tiltekið merki (label) kemur fyrir í trénu.
# Við notum reglulegar segðir (regex) til að finna merkin.
# ============================================================

def count_label(tree_str: str, label: str) -> int:
    """Telja hversu oft tiltekið merki kemur fyrir í þáttunartré.

    Notar reglulegar segðir til að finna merki sem koma á eftir sviga '('.
    Til dæmis, til að finna „IP-MAT“ í trénu, leitar segðin að „(IP-MAT“
    þar sem næsti stafur er bil eða annar svigi.

    HVERS VEGNA REGEX EN EKKI EINFÖLD STRENGJALEIT?
    Ef við notuðum einfaldlega `tree_str.count('IP-MAT')`, gætu verið
    rangar niðurstöður ef „IP-MAT“ birtist sem hluti af öðru orði.
    Með regex tryggjum við að „IP-MAT“ sé merkið sjálft, ekki hluti af
    lengra heiti.

    Args:
        tree_str: Þáttunartré sem strengur.
        label: Merkið sem á að telja (t.d. 'IP-MAT', 'IP-SUB').

    Returns:
        Fjöldi tilfella af merkinu í trénu.
    """
    # re.escape() tryggir að sérstakir regex-stafir í merkinu (eins og -)
    # séu meðhöndlaðir sem venjulegir stafir.
    # \( leitar að opnunarsviga og (\s|\() leitar að bili eða sviga strax í kjölfarið.
    pattern = r'\(' + re.escape(label) + r'[\s\(]'
    return len(re.findall(pattern, tree_str))


# ============================================================
# MÆLA HLUTFALL AUKASETNINGA / MEASURE SUBORDINATION RATIO
# Þetta er aðalmælingin: hlutfall aukasetninga af öllum
# setningum (aðal + auka).
# ============================================================

def measure_subordination(parsed_file: Path) -> tuple[float, int, int]:
    """Mæla hlutfall aukasetninga (subordination ratio) í textaskrá.

    REIKNIAÐFERÐ:
        Subordination ratio = IP-SUB / (IP-MAT + IP-SUB)

    Þar sem:
        IP-MAT = aðalsetning (matrix clause) — sjálfstæð setning
        IP-SUB = aukasetning (subordinate clause) — háð aðalsetningu

    Þetta hlutfall segir okkur hversu flókin setningagerð textans er.
    Gildi nálægt 0 þýðir aðallega aðalsetningar (einföld gerð).
    Gildi nálægt 1 þýðir aðallega aukasetningar (mjög flókin gerð).
    Fræðitextar eru venjulega á bilinu 0.25-0.40.

    Args:
        parsed_file: Slóð á skrá með þáttuðum trjám.

    Returns:
        Samstæða - tuple:
            - v: hlutfall aukasetninga (0.0 til 1.0)
            - n_sub: fjöldi aukasetninga (IP-SUB)
            - n_mat: fjöldi aðalsetninga (IP-MAT)
    """
    trees = load_parsed_trees(parsed_file)

    # Heildarfjöldi allra setninga í textanum
    n_mat = 0   # Aðalsetningar (IP-MAT)
    n_sub = 0   # Aukasetningar (IP-SUB)

    for tree_str in trees:
        # Telja aðalsetningar (IP-MAT) í þessu .
        # Hvert tré getur innihaldið fleiri en eina aðalsetningu ef
        # þáttarinn greinir samtengt form (coordinate structure).
        n_mat += count_label(tree_str, 'IP-MAT')

        # Telja aukasetningar (IP-SUB) í þessu tré.
        # Ein aðalsetning getur innihaldið margar aukasetningar,
        # t.d. „Hún sagði [að hann kæmi] [þegar hún kæmi]“ hefur
        # eina IP-MAT og tvær IP-SUB.
        n_sub += count_label(tree_str, 'IP-SUB')

    # Reikna hlutfall. Passa að deila ekki með núlli.
    total = n_mat + n_sub
    v = n_sub / total if total > 0 else 0.0

    return v, n_sub, n_mat


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra mælingu á einni þáttaðri skrá og prenta niðurstöðu."""
    parser = argparse.ArgumentParser(
        description="Vídd 2: Mæla hlutfall aukasetninga (subordination ratio).",
        epilog="""
Dæmi:
  python scripts/dim2_aukasetningar.py --parsed-file data/parsed/human/journals_islmal_parsed.txt
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
    v, n_sub, n_mat = measure_subordination(args.parsed_file)

    # Prenta niðurstöðu
    print(f"\nVÍDD 2: Hlutfall aukasetninga (subordination ratio)")
    print(f"{'=' * 55}")
    print(f"  Skrá: {args.parsed_file.name}")
    print(f"  Aðalsetningar (IP-MAT): {n_mat}")
    print(f"  Aukasetningar (IP-SUB): {n_sub}")
    print(f"  Samtals: {n_mat + n_sub}")
    print(f"  Hlutfall (v): {v:.4f} ({v:.1%})")
    print(f"{'=' * 55}")
    print()
    print("  TÚLKUN:")
    print("    v nálægt 0.0 → aðallega aðalsetningar (einfaldari texti)")
    print("    v nálægt 0.5 → helmingur aukasetninga (flókinn texti)")
    print("    Fréttir: venjulega 0.15-0.25")
    print("    Fræðitextar: venjulega 0.25-0.40")


if __name__ == "__main__":
    main()
