"""
generate_claude_continuations.py
Býr til LLM-framhöld fyrir stílmælingatilraun með Anthropic API.
Generates LLM continuations for the stylometry benchmark using the Anthropic API.

================================================================================
CLI — fullyfirlit / Full command-line interface
================================================================================

  --experiment {main,unseen}
      main   : prompt-skrár úr data/experiment/prompts/ (academic/blog/news),
               úttak í data/experiment/llm_continuations/
                       claude_sonnet46_api_t{temp}/{register}/
      unseen : prompt-skrár úr data/experiment_unseen/prompts/ (flatt),
               úttak í data/experiment_unseen/llm_continuations/
                       claude_sonnet46_api_t{temp}/unseen/

  --model MODEL
      Anthropic líkanheiti. Sjálfgefið: claude-sonnet-4-5.
      (Default. The directory label keeps the "46" suffix — see MODEL_DIR_MAP.)

  --temperature FLOAT
      Hitastig (Milička o.fl. 2025 nota 0.0 og 1.0). Sjálfgefið: 1.0.

  --max-tokens INT
      Hámarksfjöldi tókana. Sjálfgefið: 3000 (áður 1024, sem framleiddi
      ~400 orða framhöld þrátt fyrir 2000-orða beiðni í prompt).

  --overwrite
      Skrifa yfir skrár sem þegar eru til. Án hans er skráum sleppt ef til
      (sem gerir kleift að halda áfram eftir truflun / resume after interruption).

  --dry-run
      Prenta lista yfir (prompt, úttak, líkan, hitastig, max-tokens) og hætta
      án API-kalls. Notist til að sannreyna slóðir áður en peningum er eytt.

  --check-only
      Gæðamat á þegar skrifuðu úttaki fyrir gefna --experiment og --temperature.
      Engin API-köll. Prentar orðafjölda, flaggar stuttar skrár, flaggar skrár
      sem eru líklega ekki íslenskar, og flaggar ensk meta-inngangsorð.

================================================================================
RANNSÓKN: hvað takmarkar lengd framhalds / Investigation: what caps length
================================================================================

Farið var yfir skriftuna í leit að öllu sem myndi hindra 2000+ orða svar:

  * max_tokens=1024 (gömul sjálfgefin) — AÐAL-orsök. Breytt í 3000.
    Athugið: Sonnet 4.x getur framleitt 8192+ tóka. 3000 dugir fyrir
    ~2000 orð íslensku (ísl. orð = ~1.3 tókar að meðaltali).
  * Engar stop-sequences eru sendar — óbreytt.
  * Ekkert system-prompt er sett — óbreytt (Milička-aðferð notar aðeins
    leiðbeiningar í user-skilaboði, sem prompt-skrárnar innihalda nú þegar).
  * Engin svartrunkun í kóða — response.content er lesið í heild.
  * Einn subtílalgengur villa: `message.content[0].text` gengur út frá því að
    fyrsta efnisblokkin sé texti. Fyrir líkön með thinking/extended-output
    getur fyrsta blokkin verið `thinking` — þá hrynur kóði eða skilar röngum
    streng. Lagað: sameina alla blokka af gerðinni "text".
  * SLEEP_SECONDS=1.5 hægir aðeins á keyrslu — hefur engin áhrif á lengd.
  * MIN_WORDS=50 er aðeins viðvörun, ekki klippi-mark.

================================================================================
"""

import anthropic
import argparse
import os
import re
import statistics
import sys
import time
from pathlib import Path

# --- GRUNNSLOÐIR (alltaf absolute) / Base paths (always absolute) ---

BASE_DIR = Path("/Users/esther/Documents/GitHub/stylometry-icelandiceval")

# Aðaltilraun / Main experiment (RMH-gögn)
MAIN_PROMPTS_DIR = BASE_DIR / "data" / "experiment" / "prompts"
MAIN_CONTINUATIONS_DIR = BASE_DIR / "data" / "experiment" / "llm_continuations"
MAIN_HUMAN_REF_DIR = BASE_DIR / "data" / "experiment" / "human_reference"
MAIN_REGISTERS = ["academic", "blog", "news"]

# Óséð tilraun / Unseen experiment
UNSEEN_PROMPTS_DIR = BASE_DIR / "data" / "experiment_unseen" / "prompts"
UNSEEN_CONTINUATIONS_DIR = BASE_DIR / "data" / "experiment_unseen" / "llm_continuations"
UNSEEN_HUMAN_REF_DIR = BASE_DIR / "data" / "experiment_unseen" / "human_reference"
UNSEEN_SUBDIR = "unseen"  # flat register

# --- LÍKAN → MÖPPUHEITI / Model identifier → directory label ---
#
# ATHUGIÐ / NOTE: Möppuheitið "claude_sonnet46_api" heldur "46"-viðskeytinu
# VIÐVISANDI þótt sjálfgefið líkan sé núna claude-sonnet-4-5. Þetta er gert
# til að halda samræmi við fyrri úttak og svo greiningarskrífturnar
# (preprocess_llm_output.py, run_milicka.py o.fl.) þurfi ekki breytingar.
# Ef rannsóknin uppfærist í 4.6 síðar þarf ekki að endurnefna möppuna.
#
# The directory label intentionally keeps "46" even though the default model
# is now claude-sonnet-4-5. This preserves continuity with existing output
# directories and downstream scripts (preprocess_llm_output.py, run_milicka).
MODEL_DIR_MAP = {
    "claude-sonnet-4-5": "claude_sonnet46_api",
    "claude-sonnet-4-6": "claude_sonnet46_api",
    "claude-opus-4-5":   "claude_opus46_api",
    "claude-opus-4-6":   "claude_opus46_api",
}

# Bil milli API-kalla / Delay between API calls (rate-limit guard)
SLEEP_SECONDS = 1.5

# Viðvörunarmörk fyrir orðafjölda / Warn if continuation has fewer words
MIN_WORDS = 50

# Gæðamat — þröskuldar / Quality-check thresholds
CHECK_MIN_WORDS = 500           # flaggað ef undir 500 orðum
CHECK_IS_CHARS_PER_1000 = 20    # sjá ICELANDIC_THRESHOLD_RATIONALE

# Íslenskir sér-stafir (bæði lág- og hástafir teljast)
# Icelandic-specific characters (both cases counted)
ICELANDIC_CHARS = set("þðæáéíóúýöÞÐÆÁÉÍÓÚÝÖ")

# ICELANDIC_THRESHOLD_RATIONALE:
# Venjulegur íslenskur texti inniheldur sér-stafi á bilinu ~40–80 per 1000
# stafa (þ/ð/æ og hljóðstafir með broddi eru mjög algengir). Enskur texti
# hefur nánast 0. Þröskuldurinn 20/1000 er verulega undir eðlilegu íslensku
# bili og því öruggt flagg fyrir "þetta er líklega ekki íslenska eða
# blanda af ensku". Þessi þröskuldur grípur blandaðar útskýringar eins og
# "Here is the continuation: [örfá íslensk orð]" án þess að flagga eðlilega
# íslensku.
#
# Typical Icelandic prose: ~40–80 Icelandic-specific chars per 1000 chars.
# English: near 0. Threshold 20/1000 is well below typical Icelandic and is
# a safe flag for "probably not Icelandic, or mostly English."

# Ensk meta-inngangsorð sem LLM-líkön slá stundum fram
# English meta-commentary phrases LLMs sometimes emit before continuing
META_COMMENTARY_PATTERNS = [
    r"\bhere is\b",
    r"\bhere's\b",
    r"\bcontinuation\b",
    r"\bfollowing\b",
    r"\bi'll continue\b",
    r"\bi will continue\b",
    r"\bsure,?\s",
    r"\bcertainly,?\s",
    r"\bof course,?\s",
    r"\bcontinuing\b",
]
META_RE = re.compile("|".join(META_COMMENTARY_PATTERNS), re.IGNORECASE)


# =============================================================================
# SLODAR-REIKNINGAR / PATH HELPERS
# =============================================================================

def model_dir_label(model: str, temperature: float) -> str:
    """
    Skila möppuheiti eins og 'claude_sonnet46_api_t1.0'.
    Return directory label such as 'claude_sonnet46_api_t1.0'.
    """
    if model not in MODEL_DIR_MAP:
        raise ValueError(
            f"Óþekkt líkanheiti: {model}. Leyfð: {list(MODEL_DIR_MAP)}"
        )
    return f"{MODEL_DIR_MAP[model]}_t{temperature}"


def list_work_items(experiment: str, model: str, temperature: float):
    """
    Skila lista af (prompt_path, output_path, register) fyrir valið tilraunasnið.
    Return list of (prompt_path, output_path, register) for chosen experiment.

    register er tómur strengur fyrir 'unseen' til einfaldleika / is "" for unseen.
    """
    label = model_dir_label(model, temperature)
    items = []

    if experiment == "main":
        for register in MAIN_REGISTERS:
            # Flatt prompt-skipulag: academic_prompt_001.txt o.s.frv.
            # Flat prompt layout: academic_prompt_001.txt etc.
            prompt_files = sorted(
                MAIN_PROMPTS_DIR.glob(f"{register}_prompt_*.txt")
            )
            for pf in prompt_files:
                number = pf.stem.split("_")[-1]  # "001"
                out_name = f"{register}_cont_{number}.txt"
                out_path = MAIN_CONTINUATIONS_DIR / label / register / out_name
                items.append((pf, out_path, register))

    elif experiment == "unseen":
        prompt_files = sorted(UNSEEN_PROMPTS_DIR.glob("unseen_prompt_*.txt"))
        for pf in prompt_files:
            number = pf.stem.split("_")[-1]
            out_name = f"unseen_cont_{number}.txt"
            out_path = UNSEEN_CONTINUATIONS_DIR / label / UNSEEN_SUBDIR / out_name
            items.append((pf, out_path, UNSEEN_SUBDIR))

    else:
        raise ValueError(f"Óþekkt --experiment: {experiment}")

    return items


def output_root_for(experiment: str, model: str, temperature: float) -> Path:
    """Rót úttak-möppu fyrir --check-only / Output root for --check-only."""
    label = model_dir_label(model, temperature)
    if experiment == "main":
        return MAIN_CONTINUATIONS_DIR / label
    if experiment == "unseen":
        return UNSEEN_CONTINUATIONS_DIR / label
    raise ValueError(f"Óþekkt --experiment: {experiment}")


# =============================================================================
# API-KALL / API CALL
# =============================================================================

def extract_text(message) -> str:
    """
    Sameina alla text-blokkir í svari. Vernd gegn thinking-blokkum í fyrstu stöðu.
    Concatenate all text blocks in the response. Guards against non-text first
    blocks (e.g. thinking blocks on extended-output models).
    """
    parts = []
    for block in message.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "".join(parts)


def generate_continuation(
    client: "anthropic.Anthropic",
    prompt_text: str,
    model: str,
    temperature: float,
    max_tokens: int,
) -> str:
    """Kalla á Anthropic API og skila framhaldi sem streng."""
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt_text}],
    )
    return extract_text(message)


# =============================================================================
# GÆÐAMAT / QUALITY CHECK
# =============================================================================

def icelandic_density_per_1000(text: str) -> float:
    """
    Fjöldi íslenskra sér-stafa per 1000 stafa (bilum meðtalið).
    Icelandic-specific chars per 1000 chars (whitespace included).
    """
    if not text:
        return 0.0
    count = sum(1 for ch in text if ch in ICELANDIC_CHARS)
    return (count / len(text)) * 1000.0


def has_meta_commentary(text: str) -> bool:
    """Athuga fyrstu 200 stafi fyrir ensku meta-inngangi."""
    head = text[:200]
    return bool(META_RE.search(head))


def run_check(experiment: str, model: str, temperature: float) -> int:
    """
    Skanna þegar skrifað úttak og prenta gæðaskýrslu.
    Skilar fjölda flagga (0 = allt í lagi).
    """
    root = output_root_for(experiment, model, temperature)
    if not root.exists():
        print(f"[villa] Úttak-mappa fannst ekki: {root}")
        return 1

    # Safna skrám per flokki / Gather files per category
    groups: dict[str, list[Path]] = {}
    if experiment == "main":
        for register in MAIN_REGISTERS:
            groups[register] = sorted((root / register).glob("*.txt"))
    else:
        groups[UNSEEN_SUBDIR] = sorted((root / UNSEEN_SUBDIR).glob("*.txt"))

    total_files = sum(len(v) for v in groups.values())
    print(f"Gæðamat: {root}")
    print(f"Skrár alls: {total_files}\n")

    short_files: list[tuple[Path, int]] = []
    non_icelandic: list[tuple[Path, float]] = []
    meta_flagged: list[Path] = []

    for category, files in groups.items():
        if not files:
            print(f"[{category}] engar skrár")
            continue

        word_counts = []
        for fp in files:
            try:
                text = fp.read_text(encoding="utf-8")
            except Exception as e:
                print(f"  [villa] les {fp.name}: {e}")
                continue

            wc = len(text.split())
            word_counts.append(wc)

            if wc < CHECK_MIN_WORDS:
                short_files.append((fp, wc))

            density = icelandic_density_per_1000(text)
            if density < CHECK_IS_CHARS_PER_1000:
                non_icelandic.append((fp, density))

            if has_meta_commentary(text):
                meta_flagged.append(fp)

        if word_counts:
            mean_wc = statistics.mean(word_counts)
            median_wc = statistics.median(word_counts)
            print(
                f"[{category}] n={len(word_counts)}  "
                f"meðaltal={mean_wc:,.0f} orð  miðgildi={median_wc:,.0f} orð"
            )

    # --- Flöggun / Flagging ---
    print()
    if short_files:
        print(f"⚠️  Stuttar skrár (< {CHECK_MIN_WORDS} orð): {len(short_files)}")
        for fp, wc in short_files:
            print(f"    {wc:4d} orð  {fp.relative_to(BASE_DIR)}")
    else:
        print(f"✓ Engin skrá undir {CHECK_MIN_WORDS} orðum")

    print()
    if non_icelandic:
        print(
            f"⚠️  Líklega ekki íslenska "
            f"(< {CHECK_IS_CHARS_PER_1000} sérstafir/1000): {len(non_icelandic)}"
        )
        for fp, dens in non_icelandic:
            print(f"    {dens:5.1f}/1000  {fp.relative_to(BASE_DIR)}")
    else:
        print("✓ Öll úttak lítur út sem íslenska (yfir þröskuldi)")

    print()
    if meta_flagged:
        print(f"⚠️  Ensk meta-inngangsorð í fyrstu 200 stöfum: {len(meta_flagged)}")
        for fp in meta_flagged:
            print(f"    {fp.relative_to(BASE_DIR)}")
    else:
        print("✓ Engin ensk meta-inngangsorð greind")

    flags = len(short_files) + len(non_icelandic) + len(meta_flagged)
    print()
    print("─" * 60)
    print(f"Alls flögg: {flags}")
    return flags


# =============================================================================
# CLI
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Búa til LLM-framhöld með Anthropic API "
                    "(eða gæðameta þegar skrifað úttak)."
    )
    parser.add_argument(
        "--experiment",
        choices=["main", "unseen"],
        default="main",
        help="Hvaða tilraun (main = RMH, unseen = óséðir höfundatextar). "
             "Sjálfgefið: main.",
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-5",
        choices=list(MODEL_DIR_MAP.keys()),
        help="Anthropic líkanheiti. Sjálfgefið: claude-sonnet-4-5.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Hitastig (sjálfgefið: 1.0). Milička keyra 0.0 og 1.0.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=3000,
        help="Hámarksfjöldi tókana. Sjálfgefið: 3000 (~2000 ísl. orð).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Sýna lista yfir verkefni án API-kalls.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Skrifa yfir skrár sem þegar eru til "
             "(annars er sleppt fyrir endurræsingu).",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Gæðamat á þegar skrifuðu úttaki. Engin API-köll.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # --- Gæðamat-greinin endar fljótt / Quality-check branch exits early ---
    if args.check_only:
        flags = run_check(args.experiment, args.model, args.temperature)
        sys.exit(0 if flags == 0 else 2)

    # --- Venjuleg keyrsla / Normal run ---
    items = list_work_items(args.experiment, args.model, args.temperature)

    if not items:
        print("Engar prompt-skrár fundust — hættir.")
        sys.exit(1)

    label = model_dir_label(args.model, args.temperature)

    print(f"Tilraun:    {args.experiment}")
    print(f"Líkan:      {args.model}")
    print(f"Möppuheiti: {label}")
    print(f"Hitastig:   {args.temperature}")
    print(f"Max tókar:  {args.max_tokens}")
    print(f"Dry run:    {args.dry_run}")
    print(f"Overwrite:  {args.overwrite}")
    print(f"Prompt-skrár alls: {len(items)}")
    print()

    # --- Dry-run: prenta fulla töflu og hætta / dry-run: print table, exit ---
    if args.dry_run:
        print("DRY RUN — engin API-köll:")
        print(f"{'prompt':<60} {'→':^3} {'output':<70} "
              f"{'model':<24} {'temp':<5} {'max_tok'}")
        for prompt_path, out_path, _reg in items:
            exists_marker = "  [exists]" if out_path.exists() else ""
            print(
                f"{str(prompt_path.relative_to(BASE_DIR)):<60}  →  "
                f"{str(out_path.relative_to(BASE_DIR)):<70} "
                f"{args.model:<24} {args.temperature:<5} "
                f"{args.max_tokens}{exists_marker}"
            )
        sys.exit(0)

    # --- API-lykill skylda þegar ekki dry-run / API key required for live run ---
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY umhverfisbreyta vantar. "
            "Keyrðu: export ANTHROPIC_API_KEY='sk-ant-...'"
        )
    client = anthropic.Anthropic(api_key=api_key)

    total_generated = 0
    total_skipped = 0
    total_short = 0
    total_errors = 0

    for prompt_path, out_path, register in items:
        # Sleppa ef til og ekki --overwrite / skip if exists and not overwriting
        if out_path.exists() and not args.overwrite:
            print(f"  SLEPPI (til þegar): {out_path.name}")
            total_skipped += 1
            continue

        prompt_text = prompt_path.read_text(encoding="utf-8")
        print(f"  [{register}] {prompt_path.name} ...", end=" ", flush=True)

        try:
            continuation = generate_continuation(
                client=client,
                prompt_text=prompt_text,
                model=args.model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
            )
        except anthropic.APIError as e:
            print(f"API-VILLA: {e}")
            total_errors += 1
            continue
        except Exception as e:
            # Grípa ófyrirsjáanlegar villur en halda lykkjunni gangandi
            print(f"VILLA: {e}")
            total_errors += 1
            continue

        word_count = len(continuation.split())
        if word_count < MIN_WORDS:
            print(f"STUTT ({word_count} orð) ⚠️")
            total_short += 1
        else:
            print(f"OK ({word_count} orð)")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(continuation, encoding="utf-8")
        total_generated += 1

        time.sleep(SLEEP_SECONDS)

    print()
    print("─" * 60)
    print(f"Búin til:  {total_generated}")
    print(f"Sleppt:    {total_skipped}")
    if total_short:
        print(f"Of stutt:  {total_short}  ← skoðaðu þessi handvirkt")
    if total_errors:
        print(f"Villur:    {total_errors}")


if __name__ == "__main__":
    main()
