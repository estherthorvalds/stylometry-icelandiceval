#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dim5_thirdperson_pronouns.py — VÍDD 5: Hlutfall þriðjupersónufornafna
=======================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta mælir hlutfall þriðjupersónufornafna (third person pronouns)
    í texta. Þetta er kjarnavídd í Biber-greiningarrammanum (MDA — Multi-
    Dimensional Analysis) og segir okkur hvort texti er FRÁSAGNARTENGDUR
    (narrative/informational — talar um aðra) eða VIÐTÖKUTENGDUR (involved/
    interactive — höfundur talar um sjálfan sig eða lesandann).

    This script measures the ratio of third person pronouns (hann, hún, það,
    þeir, þær, þau, etc.) to total pronouns and to total words, as a core
    Biber register dimension.

MÁLVÍSINDI / LINGUISTICS:
    Þriðjupersónufornöfn (hann, hún, það, þeir, þær, þau, o.s.frv.) eru
    notuð þegar höfundur vísar til ANNARRA aðila eða hluta. Hátt hlutfall
    þeirra bendir til frásagnartexta (texti um atburði, fólk, fyrirbæri).
    Lágt hlutfall bendir til þess að höfundurinn tali frekar um sjálfan sig
    (ég, mig, mér — fyrsta persóna) eða ávarpi lesandann (þú, þig — önnur
    persóna).

    VÆNTAR NIÐURSTÖÐUR Í OKKAR TEXTATEGUNDUM:
    - Fræðitextar (Læknablaðið): HÁTT — ópersónulegt, fjallar um
      sjúklinga/fyrirbæri sem þriðju aðila.
    - Fréttir (RÚV): HÁTT — fjallar um fólk og atburði.
    - Blogg (Jonas.is): LÆGRA — meira af „ég“ (fyrsta persóna),
      beint ávarp til lesandans.

    TENGSL VIÐ BIBER-RAMMA / CONNECTION TO BIBER'S MDA:
        Biber (1988) skilgreindi „Involved vs. Informational Production“
        sem meginvídd 1. Þriðjupersónufornöfn eru einn af lykilvísunum
        (features) á „Informational“ endanum. Fyrsta- og önnurpersónu-
        fornöfn eru hins vegar „Involved“.

HVERS VEGNA AÐ NOTA ORÐFORM, EKKI MERKI:
    IcePaHC-þáttarinn merkir fornöfn sem PRO-N, PRO-A, PRO-D, PRO-G
    (nefnifall, þolfall, þágufall, eignarfall) en GREINIR EKKI PERSÓNU
    í merkinu sjálfu. „Hann“ (þriðja persóna) og „ég“ (fyrsta persóna)
    fá bæði merkið PRO-N. Þess vegna þurfum við að bera saman
    ORÐFORMIÐ SJÁLFT við þekktan lista þriðjupersónuforma.

    Þetta er hreint (clean) vegna þess að þriðjupersónufornöfn á íslensku
    eru LOKAÐ MENGI (closed set) — nýjar myndir bætast ekki við.

INNTAK / INPUT:
    Þáttuð tré úr data/parsed/human/*.txt og data/parsed/llm/*.txt
    (ein lína = eitt þáttunartré í svigaformi)

ÚTTAK / OUTPUT:
    1. CSV-skrá: output/dim5_thirdperson_pronouns.csv
    2. Tafla á skipanalínu

KEYRSLA / USAGE:
    # Á möppu:
    python scripts/dim5_thirdperson_pronouns.py --parsed-dir output/parsed/

    # Á tilgreindum skrám:
    python scripts/dim5_thirdperson_pronouns.py --files output/parsed/news_001.parsed output/parsed/blog_001.parsed

    # Sem innflutt eining:
    from dim5_thirdperson_pronouns import measure_third_person_pronouns
    result = measure_third_person_pronouns(Path("data/parsed/human/news_ruv_parsed.txt"))
"""

import argparse
import csv
import re
from pathlib import Path


# ============================================================
# ÞRIÐJUPERSÓNUFORNAFNAFORMAR / THIRD PERSON PRONOUN FORMS
# ============================================================
# Íslensku þriðjupersónufornöfnin eru lokaður mengi (closed set).
# Hér eru öll beygingarform þeirra, skipuð eftir kyni og tölu.
#
# EINTALA / SINGULAR:
#   Karlkyn (masculine):  hann, hann, honum, hans
#   Kvenkyn (feminine):   hún, hana, henni, hennar
#   Hvorugkyn (neuter):   það, það, því, þess
#
# FLEIRTALA / PLURAL:
#   Karlkyn (masculine):  þeir, þá, þeim, þeirra
#   Kvenkyn (feminine):   þær, þær, þeim, þeirra
#   Hvorugkyn (neuter):   þau, þau, þeim, þeirra
#
# ATHUGASEMD UM MARGRÆÐNI / AMBIGUITY NOTES:
#   - „það“ getur verið laust frumlag / expletive / dummy subject
#     (t.d. „Það rignir“). IcePaHC merkir gervifrumlag yfirleitt sem
#     ES (expletive subject) frekar en PRO. Ef við finnum „það“ merkt
#     sem PRO-N er það yfirleitt RAUNVERULEGT fornafn. Passað er upp á
#     að útiloka „það“ sem er merkt sem ES.
#   - „því" getur verið samtenging („því að“ = vegna þess að) en
#     þegar það er merkt PRO-D er það örugglega fornafnið.
#   - „þeim" og „þá“ gætu fræðilega tilheyrt öðrum orðflokkum en
#     þegar merkt sem PRO-* er öruggt að telja.
#   - „Hans“ getur verið eiginnafn.
#   - „hana“ getur verið orðmynd af dýrinu „hani“. 
#   - „þess“ getur verið orðmynd af ábendingarfornafninu „sá“. 
#
# Við lágstöfum ALLT til samsvörunar (case-insensitive),
# vegna þess að „Hann“ getur verið í upphafi setningar.
# ============================================================

THIRD_PERSON_FORMS: frozenset[str] = frozenset({
    # --- EINTALA / SINGULAR ---
    # Karlkyn / Masculine: hann (he)
    'hann',     # Nefnifall (NOM) OG þolfall (ACC) — sama form
    'honum',    # Þágufall (DAT)
    'hans',     # Eignarfall (GEN)

    # Kvenkyn / Feminine: hún (she)
    'hún',      # Nefnifall (NOM)
    'hana',     # Þolfall (ACC)
    'henni',    # Þágufall (DAT)
    'hennar',   # Eignarfall (GEN)

    # Hvorugkyn / Neuter: það (it)
    'það',      # Nefnifall (NOM) OG þolfall (ACC) — sama form
    'því',      # Þágufall (DAT)
    'þess',     # Eignarfall (GEN)

    # Kynsegin / Non-binary: hán (they)
    'hán',      # Nefnifall (NOM) OG þolfall (ACC) — sama form
    'háni',     # Þágufall (DAT)
    'háns',     # Eignarfall (GEN)

    # Kynsegin / Non-binary: hé (they)
    'hé',       # Nefnifall (NOM) OG þolfall (ACC) — sama form
    'héi',      # Þágufall (DAT)
    'hés',      # Eignarfall (GEN)

    # Kynsegin / Non-binary: hín (they)
    'hín',      # Nefnifall (NOM) OG þolfall (ACC) — sama form
    'híni',     # Þágufall (DAT)
    'híns',     # Eignarfall (GEN)

    # --- FLEIRTALA / PLURAL ---
    # Karlkyn / Masculine: þeir (they, masc.)
    'þeir',    # Nefnifall (NOM)
    'þá',      # Þolfall (ACC)

    # Kvenkyn / Feminine: þær (they, fem.)
    'þær',     # Nefnifall (NOM) OG þolfall (ACC) — sama form

    # Hvorugkyn / Neuter: þau (they, neut.)
    'þau',     # Nefnifall (NOM) OG þolfall (ACC) — sama form

    # Sameiginleg form fleirtölu / Shared plural forms:
    'þeim',    # Þágufall (DAT) — öll kyn
    'þeirra',  # Eignarfall (GEN) — öll kyn
})


# ============================================================
# LESA ÞÁTTUÐ TRÉ / READ PARSED TREES
# Sama aðferð og í dim1/dim2/dim3 — les þáttuð tré úr skrá,
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
# DRAGA ÚT FORNÖFN ÚR EINU TRÉ / EXTRACT PRONOUNS FROM TREE
# ============================================================
# IcePaHC-þáttunarsnið notar svigaform þar sem hver hnútur er:
#   (MERKI orð)
# Fornöfn eru merkt PRO-N, PRO-A, PRO-D, PRO-G.
#
# Dæmi úr raunverulegum þáttunartré:
#   (PRO-N Hann) (VBDI fór) (PP (P til) (NP (PRO-G hennar)))
#   → „Hann“ er PRO-N, „hennar“ er PRO-G
#
# Við þurfum einnig að varast ES (expletive subject):
#   (ES það) — gervifrumlag, EKKI raunverulegt fornafn
#   (NP-SBJ (ES það)) — sama
# ES-merkt „það“ á EKKI að teljast sem fornafn.
#
# REGLULEG SEGÐ / REGEX PATTERN:
#   \(PRO-[NADG]\s+([^\s\)]+)\)
#   Þetta finnur:
#     \(PRO-    = opnunarsvigrúm + „PRO-“
#     [NADG]    = fallmerki: N(om), A(cc), D(at), G(en)
#     \s+       = eitt eða fleiri bil
#     ([^\s\)]+) = orðformið sjálft (hópur 1) — stafir sem eru
#                  hvorki bil né lokunarsvigrúmur
#     \)        = lokunarsvigrúmur
# ============================================================

# Regex sem finnur öll PRO-* fornöfn og dregur út orðformið.
# Hópur 1 = fallmerkið (N/A/D/G), hópur 2 = orðformið.
PRO_PATTERN = re.compile(r'\(PRO-([NADG])\s+([^\s\)]+)\)')

# Regex sem finnur ES (expletive subject) merkt „það“.
# Þetta nær yfir bæði „(ES það)" og „(ES Það)".
ES_PATTERN = re.compile(r'\(ES\s+[Þþ]að\)')

# Regex sem finnur ÖLL laufblöð (terminal nodes / leaves) í trénu.
# Laufblað = orð sem kemur á eftir merki og er lokað af ).
# Þetta notar sama mynstur og dim3_nafnlidalengd.py.
LEAF_PATTERN = re.compile(r'[^\s\(\)]+(?=\))')


def extract_pronouns_from_tree(tree_str: str) -> tuple[list[str], int]:
    """Draga út öll PRO-* merkt orð úr einu þáttunartré.

    AÐFERÐ:
        1. Finna öll PRO-N/A/D/G merkt orð með regex.
        2. Skila lista af orðformum (lágstöfuðum).
        3. Telja einnig heildarfjölda orða (laufblaða) í trénu
           til að reikna hlutfall per 1.000 orð.

    ATHUGASEMD UM ES / EXPLETIVE SUBJECT:
        IcePaHC notar „ES“ merki fyrir gervifrumlag:
            (NP-SBJ (ES það)) — „Það rignir“
        Þetta „það“ er EKKI raunverulegt fornafn — það vísar ekki
        til neins. Ef ES-merkt „það“ er einnig merkt sem PRO (sem
        er ólíklegt en mögulegt), útilokum við það.

        Nálgun: Telja fjölda ES-merkts „það“ og draga frá ef
        „það“ birtist bæði sem ES og PRO.

    Args:
        tree_str: Eitt þáttunartré sem strengur í svigaformi.

    Returns:
        Samstæða af:
            - pronoun_forms: listi af lágstöfuðum fornafnaformum
              (t.d. ['hann', 'hennar', 'þeir'])
            - total_words: heildarfjöldi orða (laufblaða) í trénu
    """
    # --- FINNA FORNÖFN ---
    # Draga út öll (PRO-X orð) og halda orðforminu.
    pronoun_forms = []
    for match in PRO_PATTERN.finditer(tree_str):
        word = match.group(2)  # Hópur 2 = orðformið
        pronoun_forms.append(word.lower())

    # --- ATHUGASEMD UM ES (GERVIFRUMLAG) ---
    # IcePaHC notar „(ES það)“ fyrir gervifrumlag, t.d. „Það rignir“.
    # ES er ANNAÐ MERKI en PRO — PRO_PATTERN samsvörun finnur ALDREI
    # ES-merkt orð. Þess vegna þurfum við EKKI að sía „það“ sérstaklega.
    #
    # Ef þáttarinn merkir „það“ sem PRO-N (nefnifall) frekar en ES,
    # er það merki um að þáttarinn telji orðið vera RAUNVERULEGT
    # fornafn (vísar til einhvers). Gert er ráð fyrir að þáttarinn virki.
    #
    # Dæmi:
    #   (NP-SBJ (ES Það)) (VBPI rignir) → ES, ekki PRO → ekki talið
    #   (NP-OB1 (PRO-A það))            → PRO-A        → TALIÐ

    # --- TELJA HEILDARORÐ ---
    # Öll laufblöð í trénu = öll orð. Sama mynstur og í dim3.
    total_words = len(LEAF_PATTERN.findall(tree_str))

    return pronoun_forms, total_words


# ============================================================
# AÐALMÆLING / MAIN MEASUREMENT
# Keyra á heila skrá af þáttuðum trjám.
# ============================================================

def measure_third_person_pronouns(
    parsed_file: Path,
) -> dict:
    """Mæla hlutfall þriðjupersónufornafna í textaskrá.

    REIKNIAÐFERÐ:
        1. Lesa öll þáttuð tré úr skrá
        2. Draga út öll fornöfn (PRO-*) og orðafjölda per tré
        3. Flokka fornöfn í þriðjupersónu vs. annað
        4. Reikna hlutföll

    ÚTREIKNINGAR:
        - third_person_to_pronoun = þriðjup. / öll fornöfn
          (Hversu stórt hlutfall fornafnanna eru í þriðju persónu)
        - third_person_per_1000 = (þriðjup. / heildarorð) × 1000
          (Tíðni þriðjupersónufornafna á hverja 1.000 orð)

    Args:
        parsed_file: Slóð á skrá með þáttuðum trjám.

    Returns:
        Dict með lyklum:
            - filename: skráarheiti
            - third_person_count: fjöldi þriðjupersónufornafna
            - total_pronoun_count: fjöldi allra fornafna (PRO-*)
            - total_word_count: heildarfjöldi orða
            - third_person_to_pronoun_ratio: hlutfall 3p / öll fornöfn
            - third_person_per_1000_words: þriðjupersóna per 1.000 orð
    """
    trees = load_parsed_trees(parsed_file)

    # Heildartalningar yfir allar setningar í skránni
    all_pronouns: list[str] = []  # Öll fornöfn (í lágstafum)
    total_words = 0

    for tree_str in trees:
        pronouns, n_words = extract_pronouns_from_tree(tree_str)
        all_pronouns.extend(pronouns)
        total_words += n_words

    # --- FLOKKA FORNÖFN / CLASSIFY PRONOUNS ---
    # Bera saman hvert fornafn við mengi þriðjupersónuforma.
    third_person_count = 0
    for form in all_pronouns:
        if form in THIRD_PERSON_FORMS:
            third_person_count += 1

    total_pronoun_count = len(all_pronouns)

    # --- REIKNA HLUTFÖLL ---
    # 1. Hlutfall þriðjupersónu af öllum fornöfnum
    if total_pronoun_count > 0:
        tp_to_pron = third_person_count / total_pronoun_count
    else:
        tp_to_pron = 0.0

    # 2. Þriðjupersóna per 1.000 orð (algengur mælikvarði í MDA)
    if total_words > 0:
        tp_per_1000 = (third_person_count / total_words) * 1000
    else:
        tp_per_1000 = 0.0

    return {
        'filename': parsed_file.name,
        'third_person_count': third_person_count,
        'total_pronoun_count': total_pronoun_count,
        'total_word_count': total_words,
        'third_person_to_pronoun_ratio': tp_to_pron,
        'third_person_per_1000_words': tp_per_1000,
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
        filename, third_person_count, total_pronoun_count,
        total_word_count, third_person_to_pronoun_ratio,
        third_person_per_1000_words

    Args:
        results: Listi af dict frá measure_third_person_pronouns.
        output_path: Slóð á CSV-skrá til að vista.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'filename',
        'third_person_count',
        'total_pronoun_count',
        'total_word_count',
        'third_person_to_pronoun_ratio',
        'third_person_per_1000_words',
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            # Slétta hlutfallstölur til 4 aukastafa í CSV
            row_out = dict(row)
            row_out['third_person_to_pronoun_ratio'] = (
                f"{row['third_person_to_pronoun_ratio']:.4f}"
            )
            row_out['third_person_per_1000_words'] = (
                f"{row['third_person_per_1000_words']:.2f}"
            )
            writer.writerow(row_out)


# ============================================================
# PRENTA TÖFLU / PRINT TABLE
# Prenta töflu á skipanalínu.
# ============================================================

def print_results_table(results: list[dict]) -> None:
    """Prenta niðurstöður á skipanalínu í töfluformi.

    Args:
        results: Listi af dict frá measure_third_person_pronouns.
    """
    print(f"\nVÍDD 5: Hlutfall þriðjupersónufornafna (third person pronouns)")
    print("=" * 90)

    # Hauslína / Header
    print(f"  {'Skrá':<35} {'3.p.':<6} {'Alls':<6} {'Orð':<7} "
          f"{'3p/forn':<8} {'3p/1000':<8}")
    print(f"  {'-'*35} {'-'*6} {'-'*6} {'-'*7} {'-'*8} {'-'*8}")

    for r in results:
        print(
            f"  {r['filename']:<35} "
            f"{r['third_person_count']:<6} "
            f"{r['total_pronoun_count']:<6} "
            f"{r['total_word_count']:<7} "
            f"{r['third_person_to_pronoun_ratio']:<8.4f} "
            f"{r['third_person_per_1000_words']:<8.2f}"
        )

    # --- MEÐALTÖL / AVERAGES ---
    if results:
        avg_ratio = (
            sum(r['third_person_to_pronoun_ratio'] for r in results)
            / len(results)
        )
        avg_per_1000 = (
            sum(r['third_person_per_1000_words'] for r in results)
            / len(results)
        )
        print(f"  {'-'*35} {'-'*6} {'-'*6} {'-'*7} {'-'*8} {'-'*8}")
        print(
            f"  {'MEÐALTAL':<35} "
            f"{'':6} {'':6} {'':7} "
            f"{avg_ratio:<8.4f} {avg_per_1000:<8.2f}"
        )

    print("=" * 90)
    print()
    print("  SKÝRING DÁLKA / COLUMN KEY:")
    print("    3.p.    = Fjöldi þriðjupersónufornafna (hann, hún, þeir...)")
    print("    Alls    = Heildarfjöldi fornafna (PRO-*)")
    print("    Orð     = Heildarfjöldi orða (laufblöð í þáttunartréum)")
    print("    3p/forn = Hlutfall: þriðjupersónufornöfn / öll fornöfn")
    print("    3p/1000 = Þriðjupersónufornöfn per 1.000 orð")
    print()
    print("  TÚLKUN:")
    print("    3p/forn ~ 0.6-0.8 → mikil þriðjupersónunotkun (fréttir, fræðitextar)")
    print("    3p/forn ~ 0.3-0.5 → blönduð (blogg, skoðanagreinar)")
    print("    3p/1000 > 40      → mikil notkun þriðjupersónu")
    print("    3p/1000 < 20      → lítil notkun þriðjupersónu")


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
        description="Vídd 5: Mæla hlutfall þriðjupersónufornafna.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Á möppu:
  python scripts/dim5_thirdperson_pronouns.py \\
      --parsed-dir output/parsed/

  # Á tilgreindum skrám:
  python scripts/dim5_thirdperson_pronouns.py \\
      --files output/parsed/news_001.parsed output/parsed/blog_001.parsed

  # Stýra úttak-CSV staðsetningu:
  python scripts/dim5_thirdperson_pronouns.py \\
      --parsed-dir output/parsed/ \\
      --output-csv output/dim5_custom.csv
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
        default=Path('output/dim5_thirdperson_pronouns.csv'),
        help="Slóð á CSV-úttaksskrá (sjálfgefið: output/dim5_thirdperson_pronouns.csv)"
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
        result = measure_third_person_pronouns(pf)
        results.append(result)

    # --- PRENTA TÖFLU ---
    print_results_table(results)

    # --- VISTA CSV ---
    save_results_csv(results, args.output_csv)
    print(f"  CSV vistað: {args.output_csv}")


if __name__ == "__main__":
    main()
