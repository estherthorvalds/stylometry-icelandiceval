#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
prepare_unseen_authored_texts.py — Undirbúa óséð höfundatexta fyrir Milička-tilraun
=====================================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta undirbýr óséða höfundatexta (heild rit eða hluta rita) fyrir
    stílmælingatilraunina. Aðferðin er sú sama og í prepare_paired_experiment.py:
    klippa texta í tvennt við setningamörk nálægt miðju, búa til prompt-skrá
    og viðmiðsskrá (reference), og búa til tómar LLM-möppur.

    This script prepares unseen authored texts (full or partial literary works)
    for the stylometry experiment. The method is identical to
    prepare_paired_experiment.py: split each text at a sentence boundary near
    its midpoint, create prompt and reference files, and prepare empty LLM
    output directories.

MISMUNUR FRÁ prepare_paired_experiment.py / DIFFERENCES:
    - Inntakið er EINAR SKRÁR (heild rit), ekki ~2.000 orða úrtök úr RMH
    - Engir slembiúrtakslyklar (random sampling) — öll skrár í möppunni eru unnar
    - Skráarlengdir eru mjög misjafnar (1.500–45.000 orð)
    - HUSVORDURINN hefur sérstaka „kafli/skrif" uppbyggingu sem þarf að
      virða við klippingu (sjá SKRIF-MEÐHÖNDLUN hér að neðan)

SKRIF-MEÐHÖNDLUN / SKRIF HANDLING (HUSVORDURINN):
    HUSVORDURINN_For_LLM_test.txt inniheldur tvenns konar kafla:
        - „Kafli N" — aðalsöguþráður (narrative)
        - „SKRIF N" — dagbókar-/skjalasetningar í öðrum stíl (diary/document)

    SKRIF-hlutar hafa greinilega annan stíl en kafli-hlutar. Ef öll
    SKRIF-efni lenda aðeins í promptinu en ekkert í viðmiðinu verður
    stílsamanburðurinn ósanngjarn — LLM-líkanið fær SKRIF í prompti en
    viðmiðstextinn hefur ekkert SKRIF.

    AÐFERÐ:
        1. Greina hvort skráin innihaldi '^SKRIF' merkingar
        2. Ef svo, finna hvar SKRIF-hlutar byrja (stafastaðsetningu)
        3. Við val á klippipunkti: krefjast þess að a.m.k. einn SKRIF-
           hluti sé í seinni helmingi (reference)
        4. Ef miðpunkts-setningamörk uppfylla ekki þetta, leita víðar
           (fyrst til vinstri, þ.e. klippa fyrr í textanum)
        5. Gefa viðvörun ef leitargluggi þarf að stækka

INNTAK / INPUT:
    data/unseen_authored_texts/*.txt og *.rtf
    Hvert skrá er eitt verk (eða hluti verks). Engir undirmöppur.

ÚTTAK / OUTPUT:
    data/experiment_unseen/
    ├── selected_samples.csv          # Upplýsingar um öll úrtök
    ├── prompts/                      # Promptar til LLM-líkana
    │   ├── unseen_prompt_001.txt
    │   └── ...
    ├── human_reference/              # Mannleg framhöld (seinni helmingur)
    │   ├── unseen_ref_001.txt
    │   └── ...
    └── llm_continuations/            # Tómar möppur fyrir LLM-úttak
        ├── gemini_3_thinking/
        ├── gpt_5/
        ├── le_chat_thinking/
        └── le_chat_fast/

KEYRSLA / USAGE:
    python scripts/prepare_unseen_authored_texts.py
    python scripts/prepare_unseen_authored_texts.py --dry-run
    python scripts/prepare_unseen_authored_texts.py --input-dir data/unseen_authored_texts/
"""

import argparse
import csv
import re
import sys
from pathlib import Path


# ============================================================
# SJÁLFGEFNAR SLÓÐIR OG STILLINGAR / DEFAULT PATHS & SETTINGS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_INPUT_DIR = PROJECT_ROOT / "data" / "unseen_authored_texts"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "experiment_unseen"

# LLM-líkön — sömu og í aðaltilrauninni (prepare_paired_experiment.py)
LLM_MODELS = [
    'gemini_3_thinking',
    'gpt_5',
    'le_chat_thinking',
    'le_chat_fast',
]

# Sama leiðbeining og í prepare_paired_experiment.py — þetta tryggir
# að LLM-líkönin fái nákvæmlega sömu skipun í báðum tilraunum.
PROMPT_INSTRUCTION = (
    "Haltu áfram með textann á sama hátt og í sama stíl og sjáðu til "
    "þess að hann innihaldi að minnsta kosti tvö þúsund orð. Textinn "
    "þarf ekki að innihalda réttar staðreyndir en gættu þess að hann "
    "passi við stílinn:"
)

# Lágmarksorðafjöldi til að skipta texta á skynsamlegan hátt.
# Styttri textar myndu gefa mjög stutt prompt eða reference.
# Lækkaður úr 3000 í 500 þar sem sumir óséðir textar eru styttri
# en RMH-úrtökin en þurfa enn að vera með í tilrauninni.
# Lowered from 3000 to 500 since some unseen texts are shorter
# than the RMH samples but still need to be included.
MIN_WORDS_FOR_SPLIT = 500

# Regex til að finna SKRIF-merkingar í HUSVORDURINN.
# Passar við línur sem byrja á „SKRIF" (rómverskar tölur á eftir).
SKRIF_MARKER_RE = re.compile(r'^SKRIF\b', re.MULTILINE)


# ============================================================
# ENDURNOTAÐAR AÐFERÐIR / REUSED FUNCTIONS
# ============================================================
# Eftirfarandi föll eru endurútfærð hér (ekki innflutt) til að
# halda skriftinu sjálfstæðu. Rökfræðin er SÚ SAMA og í
# prepare_paired_experiment.py.
# ============================================================

def find_sentence_boundaries(text: str) -> list[int]:
    """Finna allar staðsetningar setningamarka í texta.

    Setningamörk eru staðsetningar þar sem setningarendamerki (. ? !)
    er fylgt af bili og upphafsstaf (eða enda textans).

    SÚ SAMA rökfræði og í prepare_paired_experiment.py.

    Args:
        text: Textastrengur.

    Returns:
        Listi af heiltölum — hvert gildi er staðsetning (index) á
        byrjun næstu setningar (rétt á eftir setningarendamerkinu + bili).
    """
    boundaries = []
    for match in re.finditer(r'[.?!]\s+(?=[A-ZÁÉÍÓÚÝÞÆÖÐ„""])', text):
        boundaries.append(match.end())
    return boundaries


def split_at_midpoint(text: str) -> tuple[str, str]:
    """Skipta texta í tvennt við setningamörk næst miðju.

    SÚ SAMA rökfræði og í prepare_paired_experiment.py.

    Args:
        text: Textastrengur.

    Returns:
        Tuple af (fyrri_helmingur, seinni_helmingur).
    """
    boundaries = find_sentence_boundaries(text)

    if not boundaries:
        mid_char = len(text) // 2
        space_pos = text.find(' ', mid_char)
        if space_pos == -1:
            space_pos = mid_char
        return text[:space_pos].strip(), text[space_pos:].strip()

    # Finna miðpunkt í orðum
    words = text.split()
    total_words = len(words)
    target_word_idx = total_words // 2

    # Umbreyta orðavísitölu í stafavísitölu
    char_count = 0
    for i, word in enumerate(words):
        if i >= target_word_idx:
            break
        char_count += len(word) + 1

    target_char = char_count

    # Velja setningamörk næst miðju
    best_boundary = min(boundaries, key=lambda b: abs(b - target_char))

    first_half = text[:best_boundary].strip()
    second_half = text[best_boundary:].strip()

    return first_half, second_half


# ============================================================
# SKRIF-MEÐHÖNDLUN / SKRIF-AWARE SPLITTING
# ============================================================
# HUSVORDURINN hefur „Kafli N" og „SKRIF N" hluta sem skipta sér
# á. SKRIF-hlutarnir hafa annan stíl. Ef allir SKRIF-hlutar lenda
# aðeins í promptinu verður samanburðurinn ósanngjarn.
#
# Aðferðin: finna SKRIF-staðsetningar, athuga hvort valin
# klippipunktur skilar a.m.k. einum SKRIF-hluta í seinni helmingi.
# Ef ekki, leita fyrr í textanum (víkka leitarglugga til vinstri).
# ============================================================

def find_skrif_positions(text: str) -> list[int]:
    """Finna stafastaðsetningar allra SKRIF-merkinga í texta.

    Args:
        text: Textastrengur.

    Returns:
        Listi af stafastaðsetningum (index) þar sem SKRIF-hluti byrja.
        Tómur listi ef engar SKRIF-merkingar finnast.
    """
    return [m.start() for m in SKRIF_MARKER_RE.finditer(text)]


def has_skrif_in_range(skrif_positions: list[int], start: int, end: int) -> bool:
    """Athuga hvort einhver SKRIF-hluti byrji innan gefins stafabils.

    Args:
        skrif_positions: Listi af SKRIF-staðsetningum.
        start: Byrjunarstaðsetning bils.
        end: Endasetning bils (exclusive).

    Returns:
        True ef a.m.k. einn SKRIF-hluti byrjar í [start, end).
    """
    return any(start <= pos < end for pos in skrif_positions)


def split_with_skrif_constraint(text: str) -> tuple[str, str, bool]:
    """Skipta texta í tvennt og tryggja SKRIF-efni í báðum helmingum.

    AÐFERÐ:
        1. Finna öll setningamörk og SKRIF-staðsetningar
        2. Reikna miðpunkt í orðum → stafastaðsetningu
        3. Raða setningamörkum eftir fjarlægð frá miðju
        4. Prófa hvern kandídat: er a.m.k. einn SKRIF í seinni helmingi?
        5. Velja fyrsta kandídat sem uppfyllir skilyrðið
        6. Ef enginn kandídatanna nálægt miðju uppfyllir skilyrðið,
           víkka leitargluggann (fara lengra frá miðju)

    Args:
        text: Textastrengur (HUSVORDURINN).

    Returns:
        Tuple af (fyrri_helmingur, seinni_helmingur, widened).
        widened er True ef leitarglugginn þurfti að stækka.
    """
    boundaries = find_sentence_boundaries(text)
    skrif_positions = find_skrif_positions(text)

    if not boundaries:
        first, second = split_at_midpoint(text)
        return first, second, False

    if not skrif_positions:
        # Engar SKRIF-merkingar — ætti ekki að gerast en öryggisnet
        first, second = split_at_midpoint(text)
        return first, second, False

    # Finna miðpunkt í stöfum (sama rökfræði og split_at_midpoint)
    words = text.split()
    total_words = len(words)
    target_word_idx = total_words // 2

    char_count = 0
    for i, word in enumerate(words):
        if i >= target_word_idx:
            break
        char_count += len(word) + 1
    target_char = char_count

    # Raða setningamörkum eftir fjarlægð frá miðju
    sorted_boundaries = sorted(boundaries, key=lambda b: abs(b - target_char))

    # Prófa hvern kandídat — næst miðju fyrst
    text_len = len(text)
    for boundary in sorted_boundaries:
        # Athuga hvort a.m.k. einn SKRIF-hluti sé í seinni helmingi
        if has_skrif_in_range(skrif_positions, boundary, text_len):
            first_half = text[:boundary].strip()
            second_half = text[boundary:].strip()

            # Athuga hvort þetta sé „langt" frá miðju
            # Ef fjarlægðin er meira en 20% af textanum er þetta „víkkað"
            distance_pct = abs(boundary - target_char) / text_len * 100
            widened = distance_pct > 20

            return first_half, second_half, widened

    # Engin setningamörk uppfylla skilyrðið — ætti ekki að gerast
    # en ef svo, nota venjulega miðpunktsklippingu og vara við
    print("    AÐVÖRUN: Ekkert setningamark uppfyllir SKRIF-skilyrðið!")
    first, second = split_at_midpoint(text)
    return first, second, True


# ============================================================
# VISTA NIÐURSTÖÐUR / SAVE RESULTS
# ============================================================

def save_text_file(filepath: Path, text: str) -> None:
    """Vista texta í skrá með UTF-8 kóðun.

    Búr til yfirmöppur ef þær eru ekki til.

    Args:
        filepath: Slóð á úttaksskrá.
        text: Textinn sem á að vista.
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text + '\n')


def create_prompt_text(first_half: str) -> str:
    """Búa til prompt-texta sem sendur verður á LLM-líkan.

    Sama snið og í prepare_paired_experiment.py:
        1. Leiðbeining á íslensku
        2. Tóm lína
        3. Fyrri helmingur textans

    Args:
        first_half: Fyrri helmingur mannlegs texta.

    Returns:
        Fullbúinn prompt-strengur.
    """
    return f"{PROMPT_INSTRUCTION}\n\n{first_half}"


def save_selected_samples_csv(
    filepath: Path,
    records: list[dict],
) -> None:
    """Vista upplýsingar um öll úrtök í CSV-skrá.

    Args:
        filepath: Slóð á CSV-skrá.
        records: Listi af dict með upplýsingum um hvert úrtak.
    """
    if not records:
        return

    filepath.parent.mkdir(parents=True, exist_ok=True)
    # Collect all keys across all records to handle skipped entries
    seen: dict[str, None] = {}
    for rec in records:
        for k in rec:
            seen.setdefault(k, None)
    fieldnames = list(seen)

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


# ============================================================
# AÐALFLÆÐI / MAIN PIPELINE
# ============================================================

def run_preparation(
    input_dir: Path,
    output_dir: Path,
    dry_run: bool = False,
) -> None:
    """Keyra undirbúning á öllum óséðum höfundatextum.

    SKREF:
        1. Finna allar .txt skrár í inntaksmöppu
        2. Lesa hverja skrá, athuga orðafjölda
        3. Greina SKRIF-merki (ef til staðar) og velja klippiaðferð
        4. Klippa í tvennt og vista prompt/reference skrár
        5. Búa til tómar LLM-möppur
        6. Vista CSV-skrá

    Args:
        input_dir: Mappa með .txt skrám (data/unseen_authored_texts/).
        output_dir: Yfirmappa fyrir tilraunagögn (data/experiment_unseen/).
        dry_run: Ef True, prenta tölfræði en skrifa engar skrár.
    """
    print("=" * 70)
    print("UNDIRBÚNINGUR ÓSÉÐRA HÖFUNDATEXTA / UNSEEN AUTHORED TEXT PREPARATION")
    print("=" * 70)
    print(f"  Inntak:  {input_dir}")
    print(f"  Úttak:   {output_dir}")
    if dry_run:
        print(f"  ÞURR KEYRSLA (dry run) — engar skrár verða vistaðar")
    print()

    # Finna allar .txt og .rtf skrár / Find all .txt and .rtf files
    if not input_dir.exists():
        print(f"VILLA: Inntaksmappa finnst ekki: {input_dir}")
        sys.exit(1)

    txt_files = sorted(
        [f for f in input_dir.iterdir()
         if f.suffix.lower() in ('.txt', '.rtf') and f.is_file()]
    )

    if not txt_files:
        print(f"VILLA: Engar .txt/.rtf skrár fundust í {input_dir}")
        sys.exit(1)

    print(f"  Skrár fundnar: {len(txt_files)}")
    for f in txt_files:
        print(f"    {f.name}")
    print()

    # Safna niðurstöðum
    all_records: list[dict] = []
    summary_lines: list[str] = []

    print(f"{'─' * 70}")
    print("VINNSLA SKRÁA / PROCESSING FILES")
    print(f"{'─' * 70}")

    for i, txt_file in enumerate(txt_files, start=1):
        filename = txt_file.name

        # Lesa texta — styður .txt (UTF-8) og .rtf (RTF → hreinn texti)
        # Read text — supports .txt (UTF-8) and .rtf (RTF → plain text)
        try:
            if txt_file.suffix.lower() == '.rtf':
                from striprtf.striprtf import rtf_to_text
                raw_bytes = txt_file.read_bytes()
                # RTF skrár eru oftast í cp1252 kóðun / RTF files typically cp1252
                text = rtf_to_text(raw_bytes.decode('cp1252')).strip()
            else:
                text = txt_file.read_text(encoding='utf-8-sig').strip()
        except Exception as exc:
            print(f"\n  [{i:>2}/{len(txt_files)}] {filename}")
            print(f"    AÐVÖRUN: Ekki hægt að lesa — {exc} — sleppi")
            summary_lines.append(
                f"  {filename:<45}          SLEPPT (lesvilla)"
            )
            all_records.append({
                'source_file': filename,
                'prompt_file': '',
                'reference_file': '',
                'total_words': 0,
                'prompt_words': 0,
                'reference_words': 0,
                'has_skrif': False,
                'skrif_split_widened': False,
                'status': 'SKIPPED_READ_ERROR',
            })
            continue
        total_words = len(text.split())

        print(f"\n  [{i:>2}/{len(txt_files)}] {filename}  ({total_words:,} orð)")

        # --- Athuga lágmarkslengd ---
        if total_words < MIN_WORDS_FOR_SPLIT:
            print(f"    AÐVÖRUN: Of stutt ({total_words} orð < {MIN_WORDS_FOR_SPLIT})"
                  f" — sleppi skiptingu")
            summary_lines.append(
                f"  {filename:<45} {total_words:>7,} orð  SLEPPT (of stutt)"
            )

            # Skrá í CSV samt — til upplýsinga
            all_records.append({
                'source_file': filename,
                'prompt_file': '',
                'reference_file': '',
                'total_words': total_words,
                'prompt_words': 0,
                'reference_words': 0,
                'has_skrif': False,
                'skrif_split_widened': False,
                'status': 'SKIPPED_TOO_SHORT',
            })
            continue

        # --- Greina SKRIF-merki ---
        skrif_positions = find_skrif_positions(text)
        has_skrif = len(skrif_positions) > 0

        if has_skrif:
            print(f"    SKRIF-merki fundin: {len(skrif_positions)} hlutar")

        # --- Klippa texta ---
        widened = False
        if has_skrif:
            first_half, second_half, widened = split_with_skrif_constraint(text)
            if widened:
                print(f"    AÐVÖRUN: Leitargluggi víkkaður til að tryggja "
                      f"SKRIF-efni í báðum helmingum")
        else:
            first_half, second_half = split_at_midpoint(text)

        first_wc = len(first_half.split())
        second_wc = len(second_half.split())
        split_pct = first_wc / total_words * 100

        # Athuga SKRIF-dreifingu eftir klippingu (ef við á)
        if has_skrif:
            skrif_in_first = sum(
                1 for pos in skrif_positions if pos < len(first_half)
            )
            skrif_in_second = len(skrif_positions) - skrif_in_first
            print(f"    SKRIF-dreifing: {skrif_in_first} í prompt, "
                  f"{skrif_in_second} í reference")

        print(f"    Skipting: {first_wc:,} / {second_wc:,} orð "
              f"({split_pct:.1f}% / {100-split_pct:.1f}%)")

        # --- Skráarheiti ---
        prompt_filename = f"unseen_prompt_{i:03d}.txt"
        ref_filename = f"unseen_ref_{i:03d}.txt"

        # --- Vista (nema dry-run) ---
        if not dry_run:
            prompt_text = create_prompt_text(first_half)
            prompt_path = output_dir / "prompts" / prompt_filename
            save_text_file(prompt_path, prompt_text)

            ref_path = output_dir / "human_reference" / ref_filename
            save_text_file(ref_path, second_half)

            print(f"    Vistað: {prompt_filename}, {ref_filename}")

        # Safna tölfræði
        all_records.append({
            'source_file': filename,
            'prompt_file': prompt_filename,
            'reference_file': ref_filename,
            'total_words': total_words,
            'prompt_words': first_wc,
            'reference_words': second_wc,
            'has_skrif': has_skrif,
            'skrif_split_widened': widened,
            'status': 'OK',
        })

        summary_lines.append(
            f"  {filename:<45} {total_words:>7,} orð  "
            f"→  {first_wc:>6,} / {second_wc:>6,}"
            + (f"  [SKRIF]" if has_skrif else "")
        )

    # --- Búa til LLM-möppur ---
    if not dry_run:
        print(f"\n{'─' * 70}")
        print("BÝ TIL LLM-MÖPPUR")
        print(f"{'─' * 70}")

        for model_name in LLM_MODELS:
            model_dir = output_dir / "llm_continuations" / model_name
            model_dir.mkdir(parents=True, exist_ok=True)
            print(f"  Búin til: llm_continuations/{model_name}/")

    # --- Vista CSV ---
    if not dry_run:
        csv_path = output_dir / "selected_samples.csv"
        save_selected_samples_csv(csv_path, all_records)
        print(f"\nCSV vistuð: {csv_path}")

    # --- Samantekt ---
    print(f"\n{'=' * 70}")
    print("SAMANTEKT / SUMMARY")
    print(f"{'=' * 70}")
    print()

    n_processed = sum(1 for r in all_records if r['status'] == 'OK')
    n_skipped = sum(1 for r in all_records if r['status'] != 'OK')

    print(f"  Skrár fundnar:   {len(txt_files)}")
    print(f"  Unnar (split):   {n_processed}")
    print(f"  Sleppt:          {n_skipped}")
    print()

    print(f"  {'Skrá':<45} {'Orð':>9}  {'Prompt':>8} / {'Ref':>8}")
    print(f"  {'─'*45} {'─'*9}  {'─'*8}   {'─'*8}")
    for line in summary_lines:
        print(line)
    print()

    if n_processed > 0:
        total_prompt = sum(
            r['prompt_words'] for r in all_records if r['status'] == 'OK'
        )
        total_ref = sum(
            r['reference_words'] for r in all_records if r['status'] == 'OK'
        )
        print(f"  Heildarorðafjöldi prompt:    {total_prompt:>10,}")
        print(f"  Heildarorðafjöldi reference: {total_ref:>10,}")
        print()

    if not dry_run:
        print("  MÖPPUSKIPULAG:")
        print(f"  {output_dir}/")
        print(f"  ├── selected_samples.csv")
        print(f"  ├── prompts/              ← Senda á LLM-líkön")
        print(f"  ├── human_reference/      ← Mannlegt framhald (samanburðargögn)")
        print(f"  └── llm_continuations/    ← Setja LLM-framhöld hér")
        for model_name in LLM_MODELS:
            print(f"      ├── {model_name}/")
        print()

        print("  NÆSTU SKREF:")
        print("    1. Senda promptana í prompts/ á hvert LLM-líkan")
        print("    2. Vista framhöld í llm_continuations/<líkan>/")
        print("    3. Keyra preprocess_llm_output.py á LLM-framhöldin")
        print("    4. Keyra parse_texts.py og run_milicka.py")

    if dry_run:
        print("  ÞURR KEYRSLA — engar skrár voru vistaðar.")
        print("  Keyrðu aftur án --dry-run til að vista.")

    print(f"\n{'=' * 70}")


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Aðalfall: Lesa skipanalínubreytur og keyra undirbúning."""
    parser = argparse.ArgumentParser(
        description="Undirbúa óséða höfundatexta fyrir Milička-tilraun.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi um keyrslu:
  # Þurr keyrsla — sýna hvað myndi gerast:
  python scripts/prepare_unseen_authored_texts.py --dry-run

  # Keyra og vista:
  python scripts/prepare_unseen_authored_texts.py

  # Nota aðra möppu:
  python scripts/prepare_unseen_authored_texts.py \\
      --input-dir data/unseen_authored_texts/ \\
      --output-dir data/experiment_unseen/
        """
    )
    parser.add_argument(
        '--input-dir',
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Mappa með .txt skrám (sjálfgefið: {DEFAULT_INPUT_DIR.relative_to(PROJECT_ROOT)})"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Yfirmappa fyrir tilraunagögn (sjálfgefið: {DEFAULT_OUTPUT_DIR.relative_to(PROJECT_ROOT)})"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Sýna tölfræði án þess að vista skrár."
    )

    args = parser.parse_args()

    run_preparation(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
