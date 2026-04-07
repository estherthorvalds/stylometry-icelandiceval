#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
prepare_paired_experiment.py — Búa til pöruð gögn fyrir Milička-tilraun
========================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta undirbýr gögn fyrir aðaltilraunina í stílmælingaverkefninu.
    Aðferðin fylgir Milička o.fl. (2025): taka mennskan texta, klippa hann
    í tvennt, gefa fyrri helming sem „prompt“ til LLM-líkans, og bera saman
    framhald líkansins við seinni helming mannsins.

    This script prepares data for the main experiment following Milička et al.
    (2025): take a human text, split it in half, give the first half as a prompt
    to an LLM, and compare the LLM's continuation against the human's second half.

HVERS VEGNA ÞESSI AÐFERÐ? / WHY THIS METHOD?
    Milička-formúlurnar (Δv, SE, b_d, B) bera saman stíleinkenni mannlegra
    texta og LLM-texta. Til að samanburðurinn sé sanngjarn þurfa textarnir
    að vera „jafn nálægir“ og hægt er — sama textategund, sama umfjöllunarefni,
    og sama „loft“. Með því að gefa LLM-líkaninu fyrri helming mennsks texta
    sem og skipun tryggjum við:

        1. SAMA EFNI (topic): Líkanið skrifar um sama efni og manneskjan
        2. SAMA TEXTATEGUND (register): Prompturinn „setur tóninn“ —
           fréttir, fræðigrein, eða blogg
        3. SAMANBURÐARHÆFUR TEXTI: Seinni helmingur mannsins og
           framhald líkansins eru beinlínis samanburðarhæf

    Þetta er miklu strangara en að biðja líkanið einfaldlega „skrifa frétt“ —
    við neyðum líkanið til að halda áfram í sama stíl.

SKREFIN / THE STEPS:
    1. Velja 15 slembiúrtök úr hverri af 3 textategundum (45 alls)
    2. Klippa hvert úrtak í tvennt við setningamörk nálægt miðju
    3. Vista fyrri helming sem prompt-skrá (til að senda á LLM)
    4. Vista seinni helming sem reference-skrá (mennskt framhald)
    5. Búa til tómar möppur fyrir LLM-framhald

ÚTTAK / OUTPUT:
    data/experiment/
    ├── selected_samples.csv          # Hvaða úrtök voru valin
    ├── prompts/                      # Promptar til LLM-líkana
    │   ├── news_prompt_001.txt
    │   ├── blog_prompt_001.txt
    │   └── ...
    ├── human_reference/              # Mannleg framhöld (seinni helmingur)
    │   ├── news_ref_001.txt
    │   └── ...
    └── llm_continuations/            # Tómar möppur fyrir LLM-úttak
        ├── gemini_3_thinking/
        ├── gpt_5/
        ├── le_chat_thinking/
        └── le_chat_fast/

KEYRSLA / USAGE:
    python scripts/prepare_paired_experiment.py \\
        --human-dir data/human_texts/ \\
        --output-dir data/experiment/ \\
        --samples-per-category 15 \\
        --seed 42
"""

import argparse
import csv
import random
import re
import sys
from pathlib import Path


# ============================================================
# SJÁLFGEFNAR SLÓÐIR OG STILLINGAR / DEFAULT PATHS & SETTINGS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_HUMAN_DIR = PROJECT_ROOT / "data" / "human_texts"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "experiment"

# Textategundir og möppuheiti þeirra undir data/human_texts/
# Þetta tengir saman heiti möppunnar, stutt auðkenni (prefix) sem notað
# er í skráarheitum, og heiti til birtingar.
CATEGORIES = [
    {
        'dir_name': 'news',       # Mappa: data/human_texts/news/
        'prefix': 'news',         # Skráarheiti: news_prompt_001.txt
        'display': 'Fréttir',     # Til birtingar
    },
    {
        'dir_name': 'blog',
        'prefix': 'blog',
        'display': 'Blogg',
    },
    {
        'dir_name': 'academic',
        'prefix': 'academic',
        'display': 'Fræðitextar',
    },
]

# LLM-líkön sem verða prófuð — tómar möppur búnar til fyrir hvert
LLM_MODELS = [
    'gemini_3_thinking',
    'gpt_5',
    'le_chat_thinking',
    'le_chat_fast',
]

# Íslenski prompturinn sem sendur er á LLM-líkön.
# Þetta er „leiðbeiningarhlutinn" sem kemur á undan textanum.
# Hann biður líkanið um að halda áfram í sama stíl.
PROMPT_INSTRUCTION = (
    "Haltu áfram með textann á sama hátt og í sama stíl og sjáðu til þess að hann innihaldi að minnsta kosti tvö þúsund orð. Textinn þarf ekki að innihalda réttar staðreyndir en gættu þess að hann passi við stílinn:"
)


# ============================================================
# FINNA OG LESA ÚRTÖK / FIND AND READ SAMPLES
# ============================================================

def find_samples(category_dir: Path) -> list[Path]:
    """Finna öll textaúrtök í möppu og skila sem raðaðan lista.

    Leitar að .txt skrám í möppunni (ekki endurkvæmt).

    Args:
        category_dir: Mappa með textaúrtökum (t.d. data/human_texts/news/).

    Returns:
        Raðaður listi af Path hlutum.
    """
    if not category_dir.exists():
        print(f"  AÐVÖRUN: Mappa finnst ekki: {category_dir}")
        return []

    # sorted() tryggir fyrirsjáanlega röð óháð stýrikerfi
    return sorted(category_dir.glob('*.txt'))


def read_sample(filepath: Path) -> str:
    """Lesa textaúrtak úr skrá og skila sem streng.

    Args:
        filepath: Slóð á .txt skrá.

    Returns:
        Innihald skrárinnar sem einn strengur.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()


# ============================================================
# SKIPTA TEXTA Í TVENNT VIÐ SETNINGAMÖRK / SPLIT AT MIDPOINT
# ============================================================

def find_sentence_boundaries(text: str) -> list[int]:
    """Finna allar staðsetningar setningamarka í texta.

    Setningamörk eru staðsetningar þar sem setningarendamerki (. ? !)
    er fylgt af bili og upphafsstaf (eða enda textans).

    HVERS VEGNA SETNINGAMÖRK?
        Við megum aldrei klippa í miðri setningu. Ef prompturinn endar
        í miðri setningu, myndi LLM-líkanið fyrst „klára" setninguna
        á sinn hátt, og sá texti væri ekki samanburðarhæfur við
        mannlega framhaldið sem byrjar á nýrri setningu.

    Args:
        text: Textastrengur.

    Returns:
        Listi af heiltölum — hvert gildi er staðsetning (index) á
        enda setninga í strengnum. Staðsetningin er rétt á eftir
        setningarendamerkinu (og bili á eftir).

    Dæmi:
        "Hún fór. Hann kom. Þeir komu."
        → [9, 19, 30]   (staðsetningar rétt á eftir hverju . + bili)
    """
    boundaries = []

    # Leita að setningarendamerkjum sem fylgt er af bili og upphafsstaf
    # eða enda textans.
    # Regluleg segð:
    #   [.?!]    = setningarendamerki
    #   \s+      = eitt eða fleiri bil / línuskipti
    #   (?=[A-ZÁÉÍÓÚÝÞÆÖÐ„"]) = lookahead: næsti stafur er stór eða
    #             gæsalappir (byrjun nýrrar setningar)
    for match in re.finditer(r'[.?!]\s+(?=[A-ZÁÉÍÓÚÝÞÆÖÐ„""])', text):
        # match.end() er staðsetningin rétt á eftir bilinu —
        # þ.e. byrjun næstu setningar
        boundaries.append(match.end())

    return boundaries


def split_at_midpoint(text: str) -> tuple[str, str]:
    """Skipta texta í tvennt við setningamörk næst miðju.

    AÐFERÐ:
        1. Finna orðafjölda textans og miðpunktinn (50% orða)
        2. Finna allar setningamerkur í textanum
        3. Velja þau setningamörk sem eru næst 50% markinu
        4. Klippa þar

    Ef engin setningamörk finnast (mjög stutt texti), er textanum
    skipt á næsta bili eftir miðjuna.

    Args:
        text: Textastrengur (~2.000 orð).

    Returns:
        Tuple af (fyrri_helmingur, seinni_helmingur).
        Bæði eru strengir. Fyrri helmingurinn inniheldur setninguna
        sem endar við klippipunktinn.
    """
    # Finna setningamörk
    boundaries = find_sentence_boundaries(text)

    if not boundaries:
        # Engir setningamörk fundust — klippa á næsta bili eftir miðju.
        # Þetta ætti sjaldnast að gerast með ~2.000 orða textum.
        mid_char = len(text) // 2
        # Finna næsta bil eftir miðju
        space_pos = text.find(' ', mid_char)
        if space_pos == -1:
            space_pos = mid_char
        return text[:space_pos].strip(), text[space_pos:].strip()

    # Finna miðpunkt í orðum — þ.e. staðsetningu þar sem ~50% orðanna
    # eru komin. Við getum ekki bara notað len(text)//2 vegna þess að
    # orð eru misjafnlega löng.
    words = text.split()
    total_words = len(words)
    target_word_idx = total_words // 2

    # Umbreyta orðavísitölu í stafavísitölu (character index).
    # Teljum stafir þar til við höfum náð target_word_idx orðum.
    char_count = 0
    for i, word in enumerate(words):
        if i >= target_word_idx:
            break
        char_count += len(word) + 1  # +1 fyrir bilið á eftir

    target_char = char_count

    # Finna setningamörkin sem eru næst target_char
    # Notum min() með lykli (key) sem mælir fjarlægð frá markmiði.
    best_boundary = min(boundaries, key=lambda b: abs(b - target_char))

    first_half = text[:best_boundary].strip()
    second_half = text[best_boundary:].strip()

    return first_half, second_half


# ============================================================
# BÚA TIL PROMPT-SKRÁ / CREATE PROMPT FILE
# ============================================================

def create_prompt_text(first_half: str) -> str:
    """Búa til prompt-texta sem sendur verður á LLM-líkan.

    Prompturinn samanstendur af:
        1. Leiðbeiningu á íslensku (PROMPT_INSTRUCTION)
        2. Tómri línu
        3. Fyrri helmingi mannlega textans

    HVERS VEGNA ÍSLENSKA?
        Við erum að prófa íslensku stílframleiðslu — prompturinn
        þarf að vera á íslensku til að „setja tóninn" og tryggja
        að líkanið svari á íslensku.

    Args:
        first_half: Fyrri helmingur mannlegs texta.

    Returns:
        Fullbúinn prompt-strengur.
    """
    return f"{PROMPT_INSTRUCTION}\n\n{first_half}"


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


def save_selected_samples_csv(
    filepath: Path,
    records: list[dict],
) -> None:
    """Vista upplýsingar um valin úrtök í CSV-skrá.

    Þetta er mikilvægt fyrir endurtekjanleika (reproducibility) —
    ef einhver vill vita nákvæmlega hvaða úrtök voru notuð í
    tilrauninni, er hægt að fletta upp í þessari skrá.

    Args:
        filepath: Slóð á CSV-skrá.
        records: Listi af dict með upplýsingum um hvert úrtak.
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Ákvarða dálkaheiti úr fyrsta færslunni
    if not records:
        return

    fieldnames = list(records[0].keys())

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


# ============================================================
# AÐALFLÆÐI / MAIN PIPELINE
# ============================================================

def run_experiment_prep(
    human_dir: Path,
    output_dir: Path,
    samples_per_category: int,
    seed: int,
) -> None:
    """Keyra alla undirbúningsaðgerðina.

    SKREF:
        1. Finna öll úrtök per textategund
        2. Velja slembiúrtök (jafnmörg úr hverri tegund)
        3. Klippa hvert úrtak í tvennt við setningamörk
        4. Vista prompt-skrár og reference-skrár
        5. Búa til tómar LLM-möppur
        6. Vista CSV-skrá með upplýsingum
        7. Prenta samantekt

    Args:
        human_dir: Yfirmappa með textategundum (data/human_texts/).
        output_dir: Yfirmappa fyrir tilraunagögn (data/experiment/).
        samples_per_category: Fjöldi slembiúrtaka per textategund.
        seed: Slembifræ (random seed) fyrir endurtekjanleika.
    """
    # Stilla slembifræ svo sama niðurstaðan fáist ef sama fræ er notað.
    # Þetta er mikilvægt fyrir endurtekjanleika (reproducibility) —
    # ef nemandinn eða leiðbeinandi vill endurtaka tilraunina, gefur
    # sama seed sömu úrtökin.
    random.seed(seed)

    print("=" * 70)
    print("UNDIRBÚNINGUR PÖRUÐRAR TILRAUNAR / PAIRED EXPERIMENT PREPARATION")
    print("=" * 70)
    print(f"  Mannleg gögn: {human_dir}")
    print(f"  Úttaksmappa: {output_dir}")
    print(f"  Úrtök per tegund: {samples_per_category}")
    print(f"  Slembifræ (seed): {seed}")
    print()

    # Safna öllum CSV-færslum til að vista í selected_samples.csv
    all_records = []

    # Safna tölfræði til samantektar
    summary_stats = []

    # --- SKREF 1-4: Vinna hverja textategund ---
    for cat in CATEGORIES:
        cat_dir = human_dir / cat['dir_name']
        prefix = cat['prefix']
        display = cat['display']

        print(f"{'─' * 70}")
        print(f"TEXTATEGUND: {display} ({cat['dir_name']}/)")
        print(f"{'─' * 70}")

        # Finna öll úrtök í möppunni
        all_sample_files = find_samples(cat_dir)

        if not all_sample_files:
            print(f"  VILLA: Engin úrtök fundust í {cat_dir}")
            continue

        print(f"  Tiltæk úrtök: {len(all_sample_files)}")

        # Athuga hvort nóg úrtök séu til
        if len(all_sample_files) < samples_per_category:
            print(f"  AÐVÖRUN: Aðeins {len(all_sample_files)} úrtök tiltæk, "
                  f"en {samples_per_category} óskuð.")
            print(f"  Nota öll {len(all_sample_files)} úrtök.")
            n_select = len(all_sample_files)
        else:
            n_select = samples_per_category

        # Velja slembiúrtök
        # random.sample() velur n stök úr lista ÁN endurvals (without replacement)
        selected_files = random.sample(all_sample_files, n_select)

        # Raða eftir nafni til samræmis
        selected_files.sort()

        # Vinna hvert valið úrtak
        prompt_word_counts = []
        ref_word_counts = []

        for i, sample_path in enumerate(selected_files, start=1):
            # Lesa textaúrtakið
            full_text = read_sample(sample_path)
            full_word_count = len(full_text.split())

            # Klippa í tvennt við setningamörk nálægt miðju
            first_half, second_half = split_at_midpoint(full_text)

            first_wc = len(first_half.split())
            second_wc = len(second_half.split())

            # Búa til prompt-texta (leiðbeining + fyrri helmingur)
            prompt_text = create_prompt_text(first_half)

            # Vista prompt-skrá
            prompt_filename = f"{prefix}_prompt_{i:03d}.txt"
            prompt_path = output_dir / "prompts" / prompt_filename
            save_text_file(prompt_path, prompt_text)

            # Vista reference-skrá (seinni helmingur)
            ref_filename = f"{prefix}_ref_{i:03d}.txt"
            ref_path = output_dir / "human_reference" / ref_filename
            save_text_file(ref_path, second_half)

            # Safna tölfræði
            prompt_word_counts.append(first_wc)
            ref_word_counts.append(second_wc)

            # Bæta við CSV-færslu
            all_records.append({
                'category': cat['dir_name'],
                'source_file': sample_path.name,
                'prompt_file': prompt_filename,
                'reference_file': ref_filename,
                'total_words': full_word_count,
                'prompt_words': first_wc,
                'reference_words': second_wc,
                'seed': seed,
            })

            # Sýna framvindu
            print(f"  [{i:>2}/{n_select}] {sample_path.name}"
                  f"  →  prompt: {first_wc} orð, ref: {second_wc} orð")

        # Reikna tölfræði fyrir þessa textategund
        if prompt_word_counts:
            mean_prompt = sum(prompt_word_counts) / len(prompt_word_counts)
            mean_ref = sum(ref_word_counts) / len(ref_word_counts)
            summary_stats.append({
                'display': display,
                'n': len(prompt_word_counts),
                'mean_prompt': mean_prompt,
                'mean_ref': mean_ref,
            })

        print()

    # --- SKREF 5: Búa til tómar LLM-möppur ---
    # Þessar möppur eru tómar — nemandinn mun handvirkt (eða sjálfvirkt
    # gegnum API) setja LLM-framhöldin í þær seinna.
    print(f"{'─' * 70}")
    print("BÝ TIL LLM-MÖPPUR")
    print(f"{'─' * 70}")

    for model_name in LLM_MODELS:
        model_dir = output_dir / "llm_continuations" / model_name
        model_dir.mkdir(parents=True, exist_ok=True)
        print(f"  Búin til: llm_continuations/{model_name}/")

    print()

    # --- SKREF 6: Vista CSV-skrá ---
    csv_path = output_dir / "selected_samples.csv"
    save_selected_samples_csv(csv_path, all_records)
    print(f"CSV vistuð: {csv_path}")
    print()

    # --- SKREF 7: Samantekt ---
    print("=" * 70)
    print("SAMANTEKT / SUMMARY")
    print("=" * 70)
    print()

    total_samples = sum(s['n'] for s in summary_stats)
    print(f"  Heildarfjöldi úrtaka: {total_samples}")
    print(f"  Slembifræ (seed): {seed}")
    print()

    # Tafla per textategund
    print(f"  {'Tegund':<15} {'Fjöldi':>8} {'Meðal prompt':>14} {'Meðal ref':>12}")
    print(f"  {'-'*15} {'-'*8} {'-'*14} {'-'*12}")
    for s in summary_stats:
        print(f"  {s['display']:<15} {s['n']:>8} {s['mean_prompt']:>14.0f} {s['mean_ref']:>12.0f}")
    print()

    # Útskýring á möppuskipulagi
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
    print("       Skráarheiti: sama og prompt en _prompt_ → _cont_")
    print("       t.d. news_prompt_001.txt → news_cont_001.txt")
    print("    3. Keyra parse_texts.py á mannleg og LLM framhöld")
    print("    4. Keyra run_milicka.py til að bera saman")
    print("=" * 70)


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Aðalfall: Lesa skipanalínubreytur og keyra undirbúning."""
    parser = argparse.ArgumentParser(
        description="Undirbúa pöruð gögn fyrir Milička-tilraun.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi um keyrslu:
  python scripts/prepare_paired_experiment.py \\
      --human-dir data/human_texts/ \\
      --output-dir data/experiment/ \\
      --samples-per-category 15 \\
      --seed 42

Hvað gerist:
  1. 15 slembiúrtök valin úr hverri textategund (news, blog, academic)
  2. Hvert úrtak klippt í tvennt við setningamörk
  3. Fyrri helmingur → prompts/   (senda á LLM)
  4. Seinni helmingur → human_reference/  (mannlegt framhald)
  5. Tómar möppur búnar til í llm_continuations/

Eftir keyrslu: Sendu promptana á LLM-líkön og vistaðu framhöldin
í llm_continuations/<líkan>/.
        """
    )
    parser.add_argument(
        '--human-dir',
        type=Path,
        default=DEFAULT_HUMAN_DIR,
        help=f"Yfirmappa með textategundum (sjálfgefið: {DEFAULT_HUMAN_DIR})"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Yfirmappa fyrir tilraunagögn (sjálfgefið: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        '--samples-per-category',
        type=int,
        default=15,
        help="Fjöldi slembiúrtaka per textategund (sjálfgefið: 15)"
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help="Slembifræ (random seed) fyrir endurtekjanleika (sjálfgefið: 42)"
    )

    args = parser.parse_args()

    run_experiment_prep(
        human_dir=args.human_dir,
        output_dir=args.output_dir,
        samples_per_category=args.samples_per_category,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
