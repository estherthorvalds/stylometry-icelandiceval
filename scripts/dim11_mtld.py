#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
dim11_mtld.py — VÍDD 11: Orðaforðafjölbreytni (Lexical diversity via MTLD)
============================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta reiknar MTLD-skor (Measure of Textual Lexical Diversity,
    McCarthy & Jarvis 2010) úr hráum textaskrám. MTLD mælir hversu
    fjölbreyttan orðaforða textinn hefur og er LENGDARSTÖÐUGT — ólíkt
    barefnu TTR (type/token ratio) sem minnkar kerfisbundið með lengd
    texta af stærðfræðilegum ástæðum.

    This script computes MTLD (Measure of Textual Lexical Diversity,
    McCarthy & Jarvis 2010) from raw text files. MTLD quantifies the
    lexical diversity of a text and is length-robust — unlike plain TTR,
    which declines systematically with text length for purely mathematical
    reasons.

MÁLVÍSINDI / LINGUISTICS:
    Orðaforðafjölbreytni (lexical diversity) er klassískt stíleinkenni.
    Formlegur, fræðilegur texti notar fjölbreyttari orðaforða en
    hversdagslegt mál og samræður (þar sem algeng orð endurtaka sig oft).
    Textar sem endurtaka sömu orðmyndir margsinnis (t.d. tæknileg
    hugtök í efnisgrein um eitt efni, eða — sem hefur áhrif á þetta
    verkefni — LLM-úttak sem festist í endurtekningarmynstri) hafa
    LÆGRI MTLD.

    TENGSL VIÐ BIBER-RAMMA / CONNECTION TO BIBER'S MDA:
        Biber (1988) notaði TTR sem einn af eiginleikum
        „Informational Production“-víddarinnar. Hærra TTR gekk saman
        við formlegri, upplýsingaþéttari texta. MTLD er lengdarstöðugur
        arftaki þeirrar mælingar.

    TENGSL VIÐ MILIČKA-RAMMA / CONNECTION TO MILIČKA (2025):
        Milička o.fl. (2025, arxiv 2509.10179v2) nota Biber-MDA með 6
        ensk víddum (67 eiginleikum) og 8 tékkneskum víddum (137
        eiginleikum). Í HVORUGU tilfelli er MTLD, TTR, vocd-D eða HD-D
        hluti af víddarsettinu. Dim11 er því ekki hliðstæða neinna
        Milička-vídda heldur sjálfstæð Biber-hvött framlenging.
        Ákvörðun 027 skjalfestir þessa stöðu.

    VÆNTAR NIÐURSTÖÐUR:
        - Fræðitextar (Læknablaðið): HÁTT — fjölbreytt tæknileg hugtök.
        - Fréttir (RÚV): Á MILLI — staðalmál með reglulegum
          endurtekningum á staðanöfnum og nöfnum viðmælenda.
        - Blogg (Jonas.is): LÁGT TIL Á MILLI — hversdagslegt mál
          endurtekur algeng orð.
        - LLM-úttak með template-endurtekningum: LÁGT — endurtekning
          sömu frása lækkar MTLD beint.

REIKNIRIT / ALGORITHM (McCarthy & Jarvis 2010):
    Fyrir tókaröð (lowercased wordforms):

    FORWARD-GANGA:
        Halda tveimur talara (cumulative_types, cumulative_tokens).
        Fyrir hvern tóka:
            1. Bæta við cumulative_tokens += 1.
            2. Ef tóki er nýr, bæta við cumulative_types += 1.
            3. Reikna running_TTR = cumulative_types / cumulative_tokens.
            4. Ef running_TTR < 0.72 → loka faktor:
                 factor_count += 1; reset bæði talara.
        Í lok tókaraðar (incomplete factor):
            Ef einhverjir tókar eftir í opnum faktor, reikna
            partial_factor = (1 - final_TTR) / (1 - 0.72)
            og bæta við: factor_count += partial_factor.
        forward_mtld = total_tokens / factor_count

    REVERSE-GANGA:
        Sama reiknirit á tókaröðinni SNÚINNI (reversed). Lokagildi:
        reverse_mtld = total_tokens / factor_count_reversed

    LOKAGILDI:
        final_mtld = (forward_mtld + reverse_mtld) / 2

    LYKILATRIÐI / KEY POINTS:
        - Þröskuldur 0.72 er STAÐLAÐUR (McCarthy & Jarvis könnuðu
          [0.660, 0.750]; 0.72 er það sem koRpus, lexical-diversity
          og allar síðari útfærslur nota).
        - Samanburður er STRÖNG (strictly less than, „<“), ekki „≤“.
          Heimild: koRpus („drops below threshold“), metacpan
          („falls below“).
        - Forward+reverse meðaltal leiðréttir fyrir óklárðu faktor
          í lok — fram-ganga klárar ekki endurteknar myndir í lok,
          afturábak-ganga jafnar þá bjögun.
        - Hlutafaktor-formúlan er STAÐAL-ÚTFÆRSLA: (1-TTR)/(1-0.72).
          Þetta er „fjarlægð frá 1 sem eftir er“ deild með
          „heildarbilinu milli 1 og þröskuldar“. Sumar lauslegar
          lýsingar („hlutfall núverandi TTR og þröskulds“) eru
          villandi — staðalformúlan er sú að ofan. Sjá ákvörðun 027.

TAKMARKANIR / LIMITATIONS:
    1. WORDFORMS, EKKI LEMMA:
       Þessi útfærsla telur YFIRBORÐSFORM — „hestur“, „hests“, „hesti“
       og „hesta“ teljast sem FJÓRAR ólíkar gerðir. Íslenska hefur ríkt
       beygingarkerfi og þetta blæs upp fjölbreytni miðað við
       lemma-MTLD. Val: (a) wordform er staðall í bókmenntum
       (McCarthy & Jarvis notuðu wordforms), (b) íslensk fallabeyging
       er sjálf stíltengd — formlegur fræðitexti nýtir fleiri fall-
       og tíðarform en hversdagsmál. Lemma-MTLD getur verið bætt við
       í MA-ritgerð sem viðbótarsamanburður.

    2. SAMPLE-LENGD:
       McCarthy & Jarvis (2010) könnuðu texta ≥ 100 tókar. MTLD verður
       óstöðugt undir ~100 tókum (lokagildi ræðst af einum eða tveimur
       faktorum). Úrtökin í þessu verkefni (prompts/reference/
       continuations) eru ~200–500 tókar eftir hreinsun, sem er vel
       yfir mörkunum, en stutt LLM-framhöld gætu lent undir. Aðvörun
       prentuð fyrir texta með < 100 tóka.

    3. TEMPLATE-ENDURTEKNINGAR SEM HLIÐARVERKUN (EKKI BEIN MÆLING):
       Dim11 greinir EKKI beint hvort texti endurtekur sömu frásir
       (t.d. LLM sem festist í mynstri). Slíkar endurtekningar lækka
       MTLD sem HLIÐARVERKUN — endurteknar orðmyndir þýða lægri TTR
       og fleiri faktora. Það er JÁKVÆÐ hliðarverkun fyrir þetta
       verkefni en EKKI sjálfstæð endurtekningargreining.

    4. UMORÐUN / PARAPHRASE:
       MTLD er BLINT á merkingu. Texti sem endurtekur sömu hugmynd
       með mismunandi orðmyndum („kötturinn hlýtur að vera svangur“ →
       „dýrið þarf líklega að fá að borða“) skorar HÆRRA en texti sem
       endurtekur sama hugtak með sömu orðmyndum. Þetta er
       eðlileg takmörkun allra yfirborðsmælinga á orðaforða.

AÐFERÐ / METHOD:
    1. Lesa hráan texta úr .txt skrá.
    2. Tóka: `text.split()` á hvítbili, strippa greinarmerki með
       dim6.PUNCT_TO_STRIP, sía út tóka án bókstafs (HAS_LETTER).
       Sömu reglur og dim6/dim10 — tryggir samræmi milli vídda.
    3. Lágstafrænt tókalisti (wordform-MTLD stendur og fellur með
       þessu; annars myndu byrjunarstafir setninga telja sem nýjar
       gerðir).
    4. Keyra `compute_mtld` fram og afturábak.
    5. Skila dict með `final_mtld` sem aðal-v, plús forward/reverse/
       faktorafjöldum til villuleitar.

AF HVERJU EKKI YTRI PAKKI? / WHY NOT AN EXTERNAL PACKAGE?
    `lexical-diversity` og `textstat` eru til á PyPI, en:
    (a) bætir við háð sem er EKKI til í öðrum víddum.
    (b) felur reiknirit — við þurfum gagnsæi um lágstafrænun,
        tokenization og lemma-status (sem stafar á íslenskri beygingu).
    (c) McCarthy & Jarvis-reikniritið er einfalt og rúmast í ~50
        línum af staðal-Python. Sjálf-útfærsla með skjalfestingu er
        bestu kaupin fyrir MA-ritgerð sem vill geta útskýrt hvert
        skref.

INNTAK / INPUT:
    Hreinar textaskrár (.txt) — t.d. úr:
        data/experiment/human_reference/
        data/experiment/llm_continuations_preprocessed/{model}/

ÚTTAK / OUTPUT:
    1. CSV-skrá: output/dim11_mtld.csv
    2. Tafla á skipanalínu

KEYRSLA / USAGE:
    python scripts/dim11_mtld.py --text-dir data/experiment/human_reference/
    python scripts/dim11_mtld.py --files file1.txt file2.txt
    python scripts/dim11_mtld.py --text-dir ... --dry-run
    python scripts/dim11_mtld.py --text-dir ... --debug

HEIMILD / REFERENCE:
    McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D:
    A validation study of sophisticated approaches to lexical
    diversity assessment. *Behavior Research Methods*, 42(2), 381–392.
    DOI: 10.3758/BRM.42.2.381
"""

import argparse
import csv
from pathlib import Path

# Samnýtum tokenization-reglur dim6 beint — sömu orð teljast í
# dim6, dim10 og dim11. Reusing dim6 rules ensures cross-dim
# comparability.
from dim6_word_length import PUNCT_TO_STRIP, HAS_LETTER, mean


# ============================================================
# MTLD-þröskuldur / MTLD FACTOR SIZE THRESHOLD
# ============================================================
# 0.72 er staðlað gildi frá McCarthy & Jarvis (2010). Höfundar
# könnuðu [0.660, 0.750]; 0.72 er það sem koRpus, lexical-diversity,
# Lingua::Diversity::MTLD og allar síðari útfærslur nota.
# Samanburður er STRÖNG (strictly less than, „<“), sjá ákvörðun 027.
# ============================================================

MTLD_THRESHOLD = 0.72
MIN_RECOMMENDED_TOKENS = 100  # McCarthy & Jarvis; undir þessu er MTLD óáreiðanlegt.


# ============================================================
# TÓKNUN / TOKENIZATION
# ============================================================

def tokenize_for_mtld(text: str) -> list[str]:
    """Tóka hráan texta í lista af lágstöfum orðmynda.

    Nákvæmlega sömu reglur og dim6/dim10:
        1. Skipta á hvítbili.
        2. Strippa greinarmerki (PUNCT_TO_STRIP).
        3. Sleppa tókum án bókstafs (HAS_LETTER).
    Síðan lágstafrænt — wordform-MTLD krefst þess að „Kötturinn“ og
    „kötturinn“ teljist sem sama gerð, annars teljast byrjunarstafir
    setninga sem falskar nýjar gerðir.

    Args:
        text: Hráður texti.

    Returns:
        Listi af hreinsuðum lágstafs-orðmyndum.
    """
    tokens: list[str] = []
    for tok in text.split():
        cleaned = tok.strip(PUNCT_TO_STRIP)
        if not cleaned:
            continue
        if not HAS_LETTER.search(cleaned):
            continue
        tokens.append(cleaned.lower())
    return tokens


# ============================================================
# KJARNAREIKNIRITIÐ / CORE ALGORITHM
# ============================================================

def _mtld_one_direction(tokens: list[str]) -> tuple[float, float]:
    """Reikna MTLD í EINA átt á tókaröð.

    Gengur í gegn tókana og telur faktor-heild hvenær TTR fer undir
    MTLD_THRESHOLD. Síðasti opni faktor (incomplete factor) meðhöndlaður
    með hlutafaktor-formúlu: partial = (1 - TTR_end) / (1 - threshold).

    Args:
        tokens: Listi lágstafs-orðmynda.

    Returns:
        (mtld_value, factor_count) — mtld_value = len(tokens)/factor_count.
        Ef tómur listi er gefinn eða engir faktorar lokaðir og TTR = 1.0
        skilar 0.0.
    """
    if not tokens:
        return 0.0, 0.0

    factor_count = 0.0
    seen: set[str] = set()
    running_types = 0
    running_tokens = 0

    for tok in tokens:
        running_tokens += 1
        if tok not in seen:
            seen.add(tok)
            running_types += 1
        ttr = running_types / running_tokens
        # Ströng „<“ samanburður — sjá ákvörðun 027.
        if ttr < MTLD_THRESHOLD:
            factor_count += 1
            seen = set()
            running_types = 0
            running_tokens = 0

    # Óklárður faktor í lok — hlutafaktor.
    # (1 - TTR_at_end) / (1 - threshold): fjarlægð frá 1 sem eftir er
    # deild með heildarbili milli 1 og þröskulds.
    if running_tokens > 0:
        ttr_end = running_types / running_tokens
        partial = (1 - ttr_end) / (1 - MTLD_THRESHOLD)
        factor_count += partial

    if factor_count == 0:
        # Jaðartilfelli: allir tókar einstakir OG aldrei ttr < þröskuldur.
        # (Gerist í reynd aðeins ef textinn er styttri en örfá orð.)
        # Skilgreinum MTLD = lengd tókaraðar; þá fer v-gildið eftir
        # því hversu fá orð eru — sem er rétt hegðun fyrir mjög stutta
        # texta (og aðvörun hefur verið prentuð úr measure_mtld).
        return float(len(tokens)), 0.0

    return len(tokens) / factor_count, factor_count


def compute_mtld(tokens: list[str]) -> dict:
    """Reikna MTLD í báðar áttir og skila fram, aftur og meðal gildum.

    McCarthy & Jarvis (2010) aðferðin:
        final_mtld = (forward_mtld + reverse_mtld) / 2

    Forward-ganga klárar oft ekki endurteknar orðmyndir í lok texta,
    afturábak-ganga jafnar þá bjögun með því að hefja við hinn endinn.

    Args:
        tokens: Listi af lágstafs-orðmyndum.

    Returns:
        Dict með:
            - forward_mtld: MTLD-gildi fram á við.
            - reverse_mtld: MTLD-gildi afturábak.
            - final_mtld: Meðaltal þessara tveggja (aðal-v).
            - factor_count_forward: Fjöldi faktora (með hluta) fram.
            - factor_count_reverse: Fjöldi faktora (með hluta) aftur.
            - total_tokens: Heildarfjöldi gildra tóka.
            - total_types: Fjöldi einstakra gerða (type count).
    """
    forward_mtld, factor_count_forward = _mtld_one_direction(tokens)
    reverse_mtld, factor_count_reverse = _mtld_one_direction(list(reversed(tokens)))
    final_mtld = (forward_mtld + reverse_mtld) / 2

    return {
        'forward_mtld': forward_mtld,
        'reverse_mtld': reverse_mtld,
        'final_mtld': final_mtld,
        'factor_count_forward': factor_count_forward,
        'factor_count_reverse': factor_count_reverse,
        'total_tokens': len(tokens),
        'total_types': len(set(tokens)),
    }


# ============================================================
# AÐALMÆLING / MAIN MEASUREMENT (pípuinngangur)
# ============================================================

def measure_mtld(
    text_file: Path,
    debug: bool = False,
) -> dict:
    """Reikna MTLD úr einni textaskrá.

    Pípuinngangur fyrir run_milicka.py. Tóka, hreinsar, lágstafrænir
    og kallar compute_mtld.

    AÐVÖRUN: Ef textinn hefur færri en MIN_RECOMMENDED_TOKENS (100)
    er prentuð viðvörun — MTLD er óáreiðanlegt fyrir svona stutta texta.

    Args:
        text_file: Slóð á .txt skrá.
        debug: Ef True, prenta sundurliðun reiknings.

    Returns:
        Dict með mælingum (sjá compute_mtld) plús `filename`.
    """
    if not text_file.exists():
        raise FileNotFoundError(f"Textaskrá fannst ekki: {text_file}")

    text = text_file.read_text(encoding='utf-8')
    tokens = tokenize_for_mtld(text)

    if len(tokens) < MIN_RECOMMENDED_TOKENS:
        print(
            f"  AÐVÖRUN: {text_file.name} hefur aðeins "
            f"{len(tokens)} tóka — MTLD er óáreiðanlegt fyrir "
            f"texta undir ~{MIN_RECOMMENDED_TOKENS} tókum."
        )

    result = compute_mtld(tokens)
    result['filename'] = text_file.name

    if debug:
        print(f"\n  [DEBUG] Skrá: {text_file.name}")
        print(
            f"  [DEBUG] Tókar: {result['total_tokens']}, "
            f"Gerðir: {result['total_types']}, "
            f"TTR (heild): "
            f"{(result['total_types'] / result['total_tokens'] if result['total_tokens'] else 0):.3f}"
        )
        print(
            f"  [DEBUG] Forward MTLD: {result['forward_mtld']:.2f} "
            f"({result['factor_count_forward']:.2f} faktorar)"
        )
        print(
            f"  [DEBUG] Reverse MTLD: {result['reverse_mtld']:.2f} "
            f"({result['factor_count_reverse']:.2f} faktorar)"
        )
        print(f"  [DEBUG] Final MTLD: {result['final_mtld']:.2f}")

    return result


# ============================================================
# VISTA NIÐURSTÖÐUR SEM CSV / SAVE RESULTS AS CSV
# ============================================================

def save_results_csv(
    results: list[dict],
    output_path: Path,
) -> None:
    """Vista niðurstöður sem CSV-skrá.

    Dálkar:
        filename, total_tokens, total_types,
        forward_mtld, reverse_mtld, final_mtld,
        factor_count_forward, factor_count_reverse

    Args:
        results: Listi af dict frá measure_mtld.
        output_path: Slóð á CSV-skrá.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'filename',
        'total_tokens',
        'total_types',
        'forward_mtld',
        'reverse_mtld',
        'final_mtld',
        'factor_count_forward',
        'factor_count_reverse',
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            row_out = {k: row[k] for k in fieldnames}
            row_out['forward_mtld'] = f"{row['forward_mtld']:.2f}"
            row_out['reverse_mtld'] = f"{row['reverse_mtld']:.2f}"
            row_out['final_mtld'] = f"{row['final_mtld']:.2f}"
            row_out['factor_count_forward'] = (
                f"{row['factor_count_forward']:.2f}"
            )
            row_out['factor_count_reverse'] = (
                f"{row['factor_count_reverse']:.2f}"
            )
            writer.writerow(row_out)


# ============================================================
# PRENTA TÖFLU / PRINT TABLE
# ============================================================

def print_results_table(results: list[dict]) -> None:
    """Prenta niðurstöður á skipanalínu sem töflu.

    Args:
        results: Listi af dict frá measure_mtld.
    """
    print(f"\nVÍDD 11: Orðaforðafjölbreytni (MTLD)")
    print("=" * 90)

    # Hauslína / Header
    print(
        f"  {'Skrá':<35} {'Tókar':<7} {'Gerðir':<7} "
        f"{'Fwd':<8} {'Rev':<8} {'MTLD':<8}"
    )
    print(
        f"  {'-'*35} {'-'*7} {'-'*7} {'-'*8} {'-'*8} {'-'*8}"
    )

    for r in results:
        print(
            f"  {r['filename']:<35} "
            f"{r['total_tokens']:<7} "
            f"{r['total_types']:<7} "
            f"{r['forward_mtld']:<8.2f} "
            f"{r['reverse_mtld']:<8.2f} "
            f"{r['final_mtld']:<8.2f}"
        )

    # --- MEÐALTÖL / AVERAGES ---
    if results:
        avg_fwd = mean([r['forward_mtld'] for r in results])
        avg_rev = mean([r['reverse_mtld'] for r in results])
        avg_mtld = mean([r['final_mtld'] for r in results])
        print(
            f"  {'-'*35} {'-'*7} {'-'*7} {'-'*8} {'-'*8} {'-'*8}"
        )
        print(
            f"  {'MEÐALTAL':<35} "
            f"{'':7} "
            f"{'':7} "
            f"{avg_fwd:<8.2f} "
            f"{avg_rev:<8.2f} "
            f"{avg_mtld:<8.2f}"
        )

    print("=" * 90)
    print()
    print("  SKÝRING DÁLKA / COLUMN KEY:")
    print("    Tókar   = Heildarfjöldi gildra tóka (dim6-reglur,")
    print("              lágstafrænt)")
    print("    Gerðir  = Fjöldi einstakra orðmynda (type count)")
    print("    Fwd     = Forward MTLD (fram-ganga)")
    print("    Rev     = Reverse MTLD (afturábak-ganga)")
    print("    MTLD    = Meðaltal forward og reverse — AÐAL-V")
    print()
    print("  TÚLKUN (MTLD er EKKI kvörðuð fyrir íslensku):")
    print("    MTLD er yfirborðsmæling á orðaforðafjölbreytni. Hærra")
    print("    = fjölbreyttari orðaforði; lægra = fleiri endurteknar")
    print("    orðmyndir. Stöðluð þröskuldagildi eru EKKI til fyrir")
    print("    íslensku — raunverulegir kvarðar verða að byggjast á")
    print("    reynslugögnum úr þessu mælipróf sjálfu.")
    print()
    print("    TAKMÖRK: Notar WORDFORM-talningu, ekki lemma. Íslensk")
    print("    fallabeyging getur blásið upp fjölbreytni miðað við")
    print("    málum með minni beygingu. Texti < ~100 tókum gefur")
    print("    óáreiðanleg gildi (aðvörun prentuð).")


# ============================================================
# FINNA ALLAR TEXTASKRÁR / FIND ALL TEXT FILES
# ============================================================

def find_text_files(text_dir: Path) -> list[Path]:
    """Finna allar .txt skrár í möppu (endurkvæmt).

    Args:
        text_dir: Mappa með textaskrám.

    Returns:
        Raðaður listi af Path-hlutum.
    """
    txt_files = sorted(text_dir.rglob('*.txt'))

    if not txt_files:
        print(f"  AÐVÖRUN: Engar .txt skrár fundust í {text_dir}")

    return txt_files


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra MTLD-mælingu á textaskrám."""
    parser = argparse.ArgumentParser(
        description=(
            "Vídd 11: Reikna MTLD (Measure of Textual Lexical Diversity, "
            "McCarthy & Jarvis 2010). Lengdarstöðug orðaforðafjölbreytni."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Á möppu:
  python scripts/dim11_mtld.py \\
      --text-dir data/experiment/human_reference/

  # Á tilgreindum skrám:
  python scripts/dim11_mtld.py \\
      --files data/experiment/human_reference/news_ref_001.txt

  # Með villuleit (sýnir forward/reverse/faktorafjölda):
  python scripts/dim11_mtld.py \\
      --text-dir data/experiment/human_reference/ --debug

  # Dry-run (reikna, prenta, ekki vista CSV):
  python scripts/dim11_mtld.py \\
      --text-dir data/experiment/human_reference/ --dry-run
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--text-dir',
        type=Path,
        help="Mappa með textaskrám (.txt). Leit er endurkvæm."
    )
    group.add_argument(
        '--files',
        type=Path,
        nargs='+',
        help="Ein eða fleiri textaskrár til að greina."
    )

    parser.add_argument(
        '--output-csv',
        type=Path,
        default=Path('output/dim11_mtld.csv'),
        help="Slóð á CSV-úttaksskrá (sjálfgefið: output/dim11_mtld.csv)"
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Prenta forward/reverse/faktorafjölda per skrá."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Reikna og prenta — ekki vista CSV."
    )

    args = parser.parse_args()

    # --- FINNA SKRÁR ---
    if args.text_dir:
        if not args.text_dir.is_dir():
            print(f"VILLA: Mappa finnst ekki: {args.text_dir}")
            return
        text_files = find_text_files(args.text_dir)
    else:
        text_files = args.files
        for f in text_files:
            if not f.exists():
                print(f"VILLA: Skrá finnst ekki: {f}")
                return

    if not text_files:
        print("VILLA: Engar skrár til að greina.")
        return

    print(f"\n  Greini {len(text_files)} skrá(r)...")
    if args.debug:
        print("  [DEBUG] Villuleitarhamur virkur")

    # --- KEYRA MÆLINGU ---
    results = []
    for tf in text_files:
        result = measure_mtld(tf, debug=args.debug)
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
