#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
integrity_check.py — Heilleikaskoðun fyrir LLM-framhöld / Pre-pipeline integrity checker
=========================================================================================

TILGANGUR / PURPOSE:
    Skoðar LLM-framhöld í data/experiment/llm_continuations_preprocessed/
    (eftir forvinnslu, fyrir þáttun) og gefur viðvörunarskýrslu ef gögn
    virðast röng. LYKUR EKKI pípunum — aðeins viðvaranir.

    Checks preprocessed LLM continuations for common human errors
    (copy-paste duplicates, prompt bleed-through, missing files, etc.)
    before parsing begins. Non-blocking — warnings only.

ATHUGANIR / CHECKS:
    1. Tvítekin efni          — sha256 hash, finna eins skrár
    2. Prompt-leki            — seinustu 3 setningar prompt í upphafi framhalds
    3. Lágmarkslengd          — viðvara ef < 700 orð
    4. Möppu/skráarheitamisræmi — textategund í skráarheiti vs undirmappa
    5. Pör sem vantar         — prompt til staðar en framhald vantar per líkan
    6. Tungumálsathugun       — < 20% orða með íslenskum sérstöfum
    7. NaN-hlutfall (valfrjálst) — ef --results-csv gefið

KEYRSLA / USAGE:
    python scripts/integrity_check.py
    python scripts/integrity_check.py --llm-dir data/experiment/llm_continuations_preprocessed/
    python scripts/integrity_check.py --results-csv output/milicka_results.csv
"""

import argparse
import csv
import hashlib
import math
import re
import sys
from pathlib import Path


# ============================================================
# SJÁLFGEFNAR SLÓÐIR / DEFAULT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_LLM_DIR = (
    PROJECT_ROOT / "data" / "experiment" / "llm_continuations_preprocessed"
)
DEFAULT_PROMPT_DIR = PROJECT_ROOT / "data" / "experiment" / "prompts"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "output" / "integrity_report.txt"

# Möppur sem á að hundsá / Directories to skip
EXCLUDED_DIR_NAMES = {'excluded'}

# Textategundir / Registers
REGISTERS = ('academic', 'blog', 'news')

# Íslenskir sérstafir / Icelandic-specific characters
ICELANDIC_CHARS = set('áðéíóúýþæöÁÐÉÍÓÚÝÞÆÖ')

# Regex til að draga út (textategund, númer) úr skráarheitum.
# Sama mynstur og í run_milicka.py — passar við bæði prompt og framhaldsskrár.
# Same pattern as run_milicka.py — matches both prompt and continuation files.
SAMPLE_ID_RE = re.compile(
    r'(?P<register>academic|blog|news)_(?:prompt|cont|ref)_(?P<number>\d+)'
)

# Setningamörk — einföld regex fyrir punkt/spurningarmerki/upphrópunarmerki
# Sentence boundary — simple regex for period/question/exclamation marks
SENTENCE_END_RE = re.compile(r'[.?!]\s+')


# ============================================================
# HJÁLPARFÖLL / HELPER FUNCTIONS
# ============================================================

def find_llm_files(llm_dir: Path) -> list[Path]:
    """Finna allar .txt skrár í LLM-möppu (endurkvæmt), sleppa excluded/.

    Find all .txt files in LLM dir (recursive), skipping excluded/.

    Args:
        llm_dir: Rót LLM-framhaldsmöppunnar.

    Returns:
        Raðaður listi af Path.
    """
    files = []
    for f in llm_dir.rglob('*.txt'):
        rel_parts = f.relative_to(llm_dir).parts
        if any(part in EXCLUDED_DIR_NAMES for part in rel_parts):
            continue
        files.append(f)
    return sorted(files)


def extract_sample_id(filename: str) -> tuple[str, str] | None:
    """Draga út (textategund, númer) úr skráarheiti.

    Extract (register, number) from filename.

    Dæmi / Examples:
        'gpt5_academic_prompt_001.txt' → ('academic', '001')
        'academic_prompt_001.txt'      → ('academic', '001')

    Returns:
        Tuple (register, number) eða None.
    """
    m = SAMPLE_ID_RE.search(filename)
    if m:
        return (m.group('register'), m.group('number'))
    return None


def extract_last_sentences(text: str, n: int = 3) -> list[str]:
    """Draga út síðustu n setningar úr texta.

    Extract the last n sentences from text.

    Args:
        text: Textastrengur.
        n: Fjöldi setninga.

    Returns:
        Listi af strengjum (setningar).
    """
    # Klippa texta í setningar við setningamörk
    parts = SENTENCE_END_RE.split(text.strip())
    # Fjarlægja tóma strengi
    sentences = [s.strip() for s in parts if s.strip()]
    return sentences[-n:] if len(sentences) >= n else sentences


def token_overlap(tokens_a: list[str], tokens_b: list[str]) -> float:
    """Reikna token overlap milli tveggja lista.

    Compute token overlap between two lists (Jaccard-like on multiset).

    Returns:
        Hlutfall sameiginlegra orða (0.0 – 1.0).
    """
    if not tokens_a or not tokens_b:
        return 0.0
    set_a = set(tokens_a)
    set_b = set(tokens_b)
    intersection = set_a & set_b
    # Nota minni mengið sem nefnara — ef prompt-setningin er heil
    # í framhaldinu þá er overlap ~1.0
    # Use smaller set as denominator
    return len(intersection) / min(len(set_a), len(set_b))


def has_icelandic_chars(word: str) -> bool:
    """Athuga hvort orð innihaldi íslensku sérstafi.

    Check whether a word contains Icelandic-specific characters.
    """
    return any(ch in ICELANDIC_CHARS for ch in word)


def file_hash(path: Path) -> str:
    """Reikna sha256 hash af efni skráar.

    Compute sha256 hash of file contents.
    """
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


# ============================================================
# ATHUGANIRNAR / THE CHECKS
# ============================================================

def check_duplicate_content(
    llm_files: list[Path],
) -> list[str]:
    """Athugun 1: Tvítekin efni — sha256 hash / Duplicate content check.

    Args:
        llm_files: Listi af skráarslóðum.

    Returns:
        Listi af viðvörunum.
    """
    warnings: list[str] = []
    hash_to_paths: dict[str, list[Path]] = {}

    for f in llm_files:
        h = file_hash(f)
        hash_to_paths.setdefault(h, []).append(f)

    for h, paths in hash_to_paths.items():
        if len(paths) > 1:
            path_list = '\n    '.join(str(p) for p in paths)
            warnings.append(
                f"TVÍTEKIN EFNI / DUPLICATE CONTENT (sha256: {h[:16]}...):\n"
                f"    {path_list}"
            )

    return warnings


def check_prompt_bleedthrough(
    llm_files: list[Path],
    prompt_dir: Path,
) -> list[str]:
    """Athugun 2: Prompt-leki / Prompt bleed-through check.

    Skoðar hvort seinustu 3 setningar prompt birtast í upphafi framhalds.
    Checks if the last 3 sentences of the prompt appear at the start of
    the continuation.

    Args:
        llm_files: Listi af LLM-skráarslóðum.
        prompt_dir: Mappa með promptskrám.

    Returns:
        Listi af viðvörunum.
    """
    warnings: list[str] = []

    if not prompt_dir.exists():
        warnings.append(
            f"PROMPT-MAPPA FINNST EKKI / PROMPT DIR NOT FOUND: {prompt_dir}\n"
            f"    Sleppi prompt-lekaathugun."
        )
        return warnings

    # Hlaða öllum prompt-textum í minnið, vísað eftir (register, number)
    # Load all prompt texts into memory, keyed by (register, number)
    prompt_cache: dict[tuple[str, str], str] = {}
    for pf in sorted(prompt_dir.glob('*.txt')):
        sid = extract_sample_id(pf.name)
        if sid:
            prompt_cache[sid] = pf.read_text(encoding='utf-8', errors='replace')

    for f in llm_files:
        sid = extract_sample_id(f.name)
        if sid is None or sid not in prompt_cache:
            continue

        prompt_text = prompt_cache[sid]
        prompt_sentences = extract_last_sentences(prompt_text, n=3)
        if not prompt_sentences:
            continue

        cont_text = f.read_text(encoding='utf-8', errors='replace')
        # Taka fyrstu 500 orðin úr framhaldinu til samanburðar
        # Take first 500 words of continuation for comparison
        cont_start = ' '.join(cont_text.split()[:500])
        cont_start_lower = cont_start.lower()

        for sent in prompt_sentences:
            sent_tokens = sent.lower().split()
            if len(sent_tokens) < 3:
                continue

            # Athuga orðasamsvarun við upphaf framhalds
            # Check token overlap with start of continuation
            cont_start_tokens = cont_start_lower.split()
            # Rennisamsvarun: bera saman gluggann af sömu lengd
            # Sliding window comparison
            window_size = len(sent_tokens)
            for start_idx in range(
                min(len(cont_start_tokens) - window_size + 1, 100)
            ):
                window = cont_start_tokens[start_idx:start_idx + window_size]
                overlap = token_overlap(sent_tokens, window)
                if overlap > 0.80:
                    rel_path = f.relative_to(f.parents[3])
                    warnings.append(
                        f"PROMPT-LEKI / PROMPT BLEED-THROUGH: {rel_path}\n"
                        f"    Setning úr prompt ({overlap:.0%} samsvarun): "
                        f"\"{sent[:80]}...\""
                    )
                    break  # Ein viðvörun per setningu nægir

    return warnings


def check_minimum_length(
    llm_files: list[Path],
    min_words: int = 700,
) -> list[str]:
    """Athugun 3: Lágmarkslengd / Minimum length check.

    Viðvarar ef skrá hefur færri en min_words orð.
    Warns if a file has fewer than min_words words.

    Args:
        llm_files: Listi af skráarslóðum.
        min_words: Lágmarksfjöldi orða.

    Returns:
        Listi af viðvörunum.
    """
    warnings: list[str] = []

    for f in llm_files:
        text = f.read_text(encoding='utf-8', errors='replace')
        word_count = len(text.split())
        if word_count < min_words:
            rel_path = f.relative_to(f.parents[3])
            warnings.append(
                f"OF STUTT / TOO SHORT: {rel_path}\n"
                f"    {word_count} orð (lágmark: {min_words})"
            )

    return warnings


def check_folder_filename_mismatch(
    llm_files: list[Path],
    llm_dir: Path,
) -> list[str]:
    """Athugun 4: Möppu/skráarheitamisræmi / Folder-filename mismatch check.

    Textategund í skráarheiti verður að samsvara undirmöppunni.
    Register in filename must match the subfolder it lives in.

    Args:
        llm_files: Listi af skráarslóðum.
        llm_dir: Rót LLM-möppunnar.

    Returns:
        Listi af viðvörunum.
    """
    warnings: list[str] = []

    for f in llm_files:
        sid = extract_sample_id(f.name)
        if sid is None:
            rel_path = f.relative_to(llm_dir)
            warnings.append(
                f"ÓÞEKKT SKRÁARHEITI / UNRECOGNIZED FILENAME: {rel_path}\n"
                f"    Gat ekki dregið textategund úr heiti."
            )
            continue

        register_in_name = sid[0]

        # Finna undirmöppu — hlutfallsleg slóð: líkan/textategund/skrá
        # Find subfolder — relative path: model/register/file
        rel_parts = f.relative_to(llm_dir).parts
        # parts[0] = model, parts[1] = register subfolder (ef til)
        if len(rel_parts) >= 2:
            folder_register = rel_parts[1]
            if folder_register != register_in_name:
                rel_path = f.relative_to(llm_dir)
                warnings.append(
                    f"MISRÆMI MÖPPU/HEITIS / FOLDER-FILENAME MISMATCH: "
                    f"{rel_path}\n"
                    f"    Textategund í heiti: '{register_in_name}', "
                    f"mappa: '{folder_register}'"
                )

    return warnings


def check_missing_pairs(
    llm_dir: Path,
    prompt_dir: Path,
) -> list[str]:
    """Athugun 5: Pör sem vantar / Missing pair detection.

    Fyrir hvert prompt, athuga hvort öll líkön hafi samsvarandi framhald.
    For each prompt, check whether all models have a matching continuation.

    Args:
        llm_dir: Rót LLM-möppunnar.
        prompt_dir: Mappa með promptskrám.

    Returns:
        Listi af viðvörunum.
    """
    warnings: list[str] = []

    if not prompt_dir.exists():
        return warnings

    # Safna öllum prompt-auðkennum / Collect all prompt sample IDs
    prompt_ids: set[tuple[str, str]] = set()
    for pf in sorted(prompt_dir.glob('*.txt')):
        sid = extract_sample_id(pf.name)
        if sid:
            prompt_ids.add(sid)

    if not prompt_ids:
        return warnings

    # Finna öll líkön og framhöld þeirra / Find all models and their files
    if not llm_dir.exists():
        return warnings

    models: dict[str, set[tuple[str, str]]] = {}
    for model_dir in sorted(llm_dir.iterdir()):
        if not model_dir.is_dir():
            continue
        model_name = model_dir.name
        model_ids: set[tuple[str, str]] = set()
        for f in model_dir.rglob('*.txt'):
            rel_parts = f.relative_to(model_dir).parts
            if any(part in EXCLUDED_DIR_NAMES for part in rel_parts):
                continue
            sid = extract_sample_id(f.name)
            if sid:
                model_ids.add(sid)
        models[model_name] = model_ids

    # Bera saman / Compare
    for model_name in sorted(models):
        missing = prompt_ids - models[model_name]
        if missing:
            missing_list = ', '.join(
                f"{reg}_{num}" for reg, num in sorted(missing)
            )
            warnings.append(
                f"VANTAR FRAMHÖLD / MISSING CONTINUATIONS: {model_name}\n"
                f"    Vantar {len(missing)} skrár: {missing_list}"
            )

    return warnings


def check_language(
    llm_files: list[Path],
    threshold: float = 0.20,
) -> list[str]:
    """Athugun 6: Tungumálsathugun / Language check.

    Skoðar fyrstu 100 orðin. Ef < 20% innihalda íslenska sérstafi
    er viðvörun gefin.
    Checks the first 100 words. Warns if < 20% contain Icelandic characters.

    Args:
        llm_files: Listi af skráarslóðum.
        threshold: Lágmarkshlutfall orða með íslenskum stöfum.

    Returns:
        Listi af viðvörunum.
    """
    warnings: list[str] = []

    for f in llm_files:
        text = f.read_text(encoding='utf-8', errors='replace')
        words = text.split()[:100]
        if not words:
            continue

        icelandic_count = sum(1 for w in words if has_icelandic_chars(w))
        ratio = icelandic_count / len(words)

        if ratio < threshold:
            rel_path = f.relative_to(f.parents[3])
            warnings.append(
                f"TUNGUMÁLSGRUNUR / LANGUAGE WARNING: {rel_path}\n"
                f"    Aðeins {ratio:.0%} orða með íslenskum sérstöfum "
                f"({icelandic_count}/{len(words)} orð)"
            )

    return warnings


def check_nan_rate(
    results_csv: Path,
    max_nan_dims: int = 3,
) -> list[str]:
    """Athugun 7: NaN-hlutfall / NaN rate check (post-measurement).

    Ef milicka_results.csv er til, athuga hvort einhver skrá hafi
    NaN á fleiri en max_nan_dims víddum.

    If milicka_results.csv exists, check if any file has NaN on more
    than max_nan_dims dimensions.

    Args:
        results_csv: Slóð á CSV-niðurstöðuskrá.
        max_nan_dims: Hámarksfjöldi NaN-vídda áður en viðvörun kemur.

    Returns:
        Listi af viðvörunum.
    """
    warnings: list[str] = []

    if not results_csv.exists():
        warnings.append(
            f"CSV-SKRÁ FINNST EKKI / CSV NOT FOUND: {results_csv}\n"
            f"    Sleppi NaN-athugun."
        )
        return warnings

    # Lesa CSV og safna NaN-talningu per (model, register, number)
    # Read CSV and count NaN per (model, register, number)
    nan_counts: dict[tuple[str, str, str], int] = {}
    dim_counts: dict[tuple[str, str, str], int] = {}

    with open(results_csv, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['model'], row['register'], row['number'])
            dim_counts[key] = dim_counts.get(key, 0) + 1

            # Athuga hvort v_model eða v_human er NaN / tómt
            v_model = row.get('v_model', '')
            v_human = row.get('v_human', '')
            is_nan = False
            for val in (v_model, v_human):
                try:
                    if val == '' or val == 'nan' or math.isnan(float(val)):
                        is_nan = True
                        break
                except (ValueError, TypeError):
                    is_nan = True
                    break

            if is_nan:
                nan_counts[key] = nan_counts.get(key, 0) + 1

    for key, nan_n in nan_counts.items():
        if nan_n > max_nan_dims:
            model, register, number = key
            total = dim_counts.get(key, 7)
            warnings.append(
                f"HÁTT NaN-HLUTFALL / HIGH NaN RATE: "
                f"{model} / {register}_{number}\n"
                f"    NaN í {nan_n}/{total} víddum (hámark: {max_nan_dims})"
            )

    return warnings


# ============================================================
# SKÝRSLUGERÐ / REPORT GENERATION
# ============================================================

def write_report(
    all_warnings: dict[str, list[str]],
    total_files: int,
    report_path: Path,
) -> None:
    """Skrifa viðvörunarskýrslu í skrá og prenta samantekt.

    Write warning report to file and print summary.

    Args:
        all_warnings: Dict {flokkur: [viðvaranir]}.
        total_files: Heildarfjöldi skoðaðra skráa.
        report_path: Slóð á skýrsluskrá.
    """
    report_path.parent.mkdir(parents=True, exist_ok=True)

    total_warnings = sum(len(w) for w in all_warnings.values())

    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("HEILLEIKASKÝRSLA / INTEGRITY REPORT")
    lines.append("=" * 70)
    lines.append(f"  Skrár skoðaðar / Files checked: {total_files}")
    lines.append(f"  Viðvaranir samtals / Total warnings: {total_warnings}")
    lines.append("")

    # Samantekt per flokk / Summary per category
    lines.append("SAMANTEKT PER FLOKK / SUMMARY BY CATEGORY:")
    lines.append("-" * 50)

    category_labels = {
        'duplicate':  'Tvítekin efni / Duplicates',
        'bleed':      'Prompt-leki / Bleed-through',
        'length':     'Of stutt / Too short',
        'mismatch':   'Misræmi möppu / Folder mismatch',
        'missing':    'Vantar pör / Missing pairs',
        'language':   'Tungumál / Language',
        'nan':        'NaN-hlutfall / NaN rate',
    }

    for cat_key, cat_label in category_labels.items():
        n = len(all_warnings.get(cat_key, []))
        status = "✓" if n == 0 else f"⚠ {n}"
        lines.append(f"  {cat_label:<40} {status}")

    lines.append("")

    # Nákvæmar viðvaranir / Detailed warnings
    if total_warnings > 0:
        lines.append("=" * 70)
        lines.append("NÁKVÆMAR VIÐVARANIR / DETAILED WARNINGS")
        lines.append("=" * 70)

        for cat_key, cat_label in category_labels.items():
            cat_warnings = all_warnings.get(cat_key, [])
            if not cat_warnings:
                continue

            lines.append(f"\n--- {cat_label} ({len(cat_warnings)}) ---")
            for w in cat_warnings:
                lines.append(f"\n  {w}")

    lines.append("")
    lines.append("=" * 70)

    report_text = '\n'.join(lines)

    # Vista í skrá / Write to file
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text + '\n')

    # Prenta á skjá / Print to screen
    print(report_text)
    print(f"\n  Skýrsla vistuð í / Report saved to: {report_path}")


# ============================================================
# AÐALFLÆÐI / MAIN FLOW
# ============================================================

def run_integrity_check(
    llm_dir: Path,
    prompt_dir: Path,
    report_path: Path,
    results_csv: Path | None = None,
) -> None:
    """Keyra allar heilleikaskoðanir og skrifa skýrslu.

    Run all integrity checks and write report.

    Args:
        llm_dir: Rót LLM-framhaldsmöppunnar.
        prompt_dir: Mappa með promptskrám.
        report_path: Slóð á skýrsluskrá.
        results_csv: Valfrjáls slóð á milicka_results.csv.
    """
    print("=" * 70)
    print("HEILLEIKASKOÐUN / INTEGRITY CHECK")
    print("=" * 70)
    print(f"  LLM-mappa:    {llm_dir}")
    print(f"  Prompt-mappa: {prompt_dir}")
    if results_csv:
        print(f"  CSV-skrá:     {results_csv}")
    print()

    if not llm_dir.exists():
        print(f"VILLA: LLM-mappa finnst ekki: {llm_dir}")
        sys.exit(1)

    # Finna skrár / Find files
    llm_files = find_llm_files(llm_dir)
    total_files = len(llm_files)
    print(f"  Skrár fundnar: {total_files}")

    if total_files == 0:
        print("  Engar skrár — ekkert að skoða.")
        return

    # Keyra athuganir / Run checks
    all_warnings: dict[str, list[str]] = {}

    print("\n  [1/7] Tvítekin efni / Duplicate content...")
    all_warnings['duplicate'] = check_duplicate_content(llm_files)

    print("  [2/7] Prompt-leki / Prompt bleed-through...")
    all_warnings['bleed'] = check_prompt_bleedthrough(llm_files, prompt_dir)

    print("  [3/7] Lágmarkslengd / Minimum length...")
    all_warnings['length'] = check_minimum_length(llm_files)

    print("  [4/7] Möppu/skráarheitamisræmi / Folder-filename mismatch...")
    all_warnings['mismatch'] = check_folder_filename_mismatch(
        llm_files, llm_dir
    )

    print("  [5/7] Vantar pör / Missing pairs...")
    all_warnings['missing'] = check_missing_pairs(llm_dir, prompt_dir)

    print("  [6/7] Tungumálsathugun / Language check...")
    all_warnings['language'] = check_language(llm_files)

    print("  [7/7] NaN-hlutfall / NaN rate...")
    if results_csv:
        all_warnings['nan'] = check_nan_rate(results_csv)
    else:
        all_warnings['nan'] = []
        print("        (sleppt — enginn --results-csv gefinn)")

    print()

    # Skrifa skýrslu / Write report
    write_report(all_warnings, total_files, report_path)


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra heilleikaskoðun."""
    parser = argparse.ArgumentParser(
        description="Heilleikaskoðun á LLM-framhöldum fyrir þáttun.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Keyra á sjálfgefnum möppum:
  python scripts/integrity_check.py

  # Tilgreina möppur:
  python scripts/integrity_check.py --llm-dir data/experiment/llm_continuations_preprocessed/

  # Með NaN-athugun eftir keyrslu run_milicka.py:
  python scripts/integrity_check.py --results-csv output/milicka_results.csv
        """
    )
    parser.add_argument(
        '--llm-dir',
        type=Path,
        default=DEFAULT_LLM_DIR,
        help="Mappa með forunnum LLM-framhöldum "
             f"(sjálfgefið: {DEFAULT_LLM_DIR.relative_to(PROJECT_ROOT)})"
    )
    parser.add_argument(
        '--prompt-dir',
        type=Path,
        default=DEFAULT_PROMPT_DIR,
        help="Mappa með promptskrám "
             f"(sjálfgefið: {DEFAULT_PROMPT_DIR.relative_to(PROJECT_ROOT)})"
    )
    parser.add_argument(
        '--report-path',
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="Slóð á skýrsluskrá "
             f"(sjálfgefið: {DEFAULT_REPORT_PATH.relative_to(PROJECT_ROOT)})"
    )
    parser.add_argument(
        '--results-csv',
        type=Path,
        default=None,
        help="Valfrjáls slóð á milicka_results.csv til NaN-athugunar."
    )

    args = parser.parse_args()

    run_integrity_check(
        llm_dir=args.llm_dir,
        prompt_dir=args.prompt_dir,
        report_path=args.report_path,
        results_csv=args.results_csv,
    )


if __name__ == "__main__":
    main()
