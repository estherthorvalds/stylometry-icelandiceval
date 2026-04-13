#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
run_milicka.py — AÐALSKRIFTA: Keyrir allar víddir og reiknar Milička-formúlur
===============================================================================

TILGANGUR / PURPOSE:
    Þetta er aðalskriftið sem tengir allt saman. Það keyrir allar sjö
    víddir (dim1–dim7) á mannlegum og LLM-framleiddun textum, reiknar
    Milička-formúlurnar og prentar niðurstöður.

    This is the main orchestrator script. It runs all seven dimensions on
    human and LLM texts, computes Milička's formulas, and prints results.

MILIČKA-FORMÚLURNAR / THE FORMULAS:
    Formúla 1: Δv = v_human - v_model
        Frávik líkans frá mannlegum texta á einni vídd.
        Jákvætt Δv = líkanið hefur minna af stíleinkenninu.
        Neikvætt Δv = líkanið hefur meira af stíleinkenninu.

    Formúla 2: i = v_prompt - v_ref  (per pör)
        Náttúrulegt frávik í mennskum gögnum. Mennsku gögnunum er skipt
        í tvo helminga (prompt og reference) og mismunurinn reiknaður.
        Þetta segir hversu mikil náttúruleg sveifla er í eiginleikanum.

    Formúla 3: b_d = mean(Δv) / SE(I_d)
        Staðlað frávik per vídd. Meðal-Δv yfir úrtök er deilt með
        staðalskekkju (standard error) náttúrulegs fráviks.

    Formúla 4: B = ‖b‖ = √(Σ b_d²)
        Heildarskor yfir allar víddir. Evklíðskt norm af öllum b_d gildum.

GAGNASKIPULAG / DATA LAYOUT:
    Þáttuð tré (frá parse_texts.py):
        output/parsed/prompts/*_parsed.psd                            (45 skrár)
        output/parsed/human_reference/*_parsed.psd                    (45 skrár)
        output/parsed/llm_continuations_preprocessed/{model}/{reg}/   (per líkan)

    Hrár texti (fyrir dim6 — orðalengd):
        data/experiment/prompts/*.txt                                 (45 skrár)
        data/experiment/human_reference/*.txt                         (45 skrár)
        data/experiment/llm_continuations_preprocessed/{model}/{reg}/ (per líkan)

FLÆÐI / FLOW:
    1. Finna öll úrtök (15 per textategund × 3 tegundir = 45)
    2. Finna öll LLM-líkön og tengja við samsvarandi úrtök
    3. Mæla dim1–dim7 á mannlegum viðmiðstextum (human_reference)
    4. Mæla dim1–dim7 á prompttextum (prompts) — til SE-útreiknings
    5. Reikna náttúrulegt frávik i_k per pör og SE per textategund
    6. Mæla dim1–dim7 á LLM-framhöldum
    7. Reikna Δv, b_d, B per líkan × textategund
    8. Prenta niðurstöður og vista CSV

KEYRSLA / USAGE:
    python scripts/run_milicka.py
    python scripts/run_milicka.py --output-csv output/milicka_results.csv
"""

import argparse
import csv
import math
import re
import sys
import tempfile
from pathlib import Path

# ============================================================
# INNFLUTNINGUR Á VÍDDARSKRIFTUM / DIMENSION SCRIPT IMPORTS
# Bætum scripts/ möppunni við sys.path svo Python finni
# víddarföllin (dim1–dim7) þegar skriftið er keyrt frá
# rótarmöppu verkefnisins.
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dim1_frumlagsnafnfall import measure_subject_drop
from dim2_aukasetningar import measure_subordination
from dim3_nafnlidalengd import measure_np_length
from dim4_past_tense import measure_past_tense
from dim5_thirdperson_pronouns import measure_third_person_pronouns
from dim6_word_length import measure_word_length
from dim7_complementizers import measure_complementizers
from style_score import compute_style_score


# ============================================================
# SJÁLFGEFNAR SLÓÐIR / DEFAULT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- ÞÁTTUÐ TRÉ / PARSED TREES ---
# Frá parse_texts.py — .psd skrár í output/parsed/
PARSED_DIR = PROJECT_ROOT / "output" / "parsed"
PARSED_PROMPTS_DIR = PARSED_DIR / "prompts"
PARSED_HUMAN_REF_DIR = PARSED_DIR / "human_reference"
PARSED_LLM_DIR = PARSED_DIR / "llm_continuations_preprocessed"

# --- HRÁR TEXTI / RAW TEXT ---
# Fyrir dim6 (orðalengd) sem les hrátexta, ekki þáttuð tré.
RAW_PROMPTS_DIR = PROJECT_ROOT / "data" / "experiment" / "prompts"
RAW_HUMAN_REF_DIR = PROJECT_ROOT / "data" / "experiment" / "human_reference"
RAW_LLM_DIR = (
    PROJECT_ROOT / "data" / "experiment" / "llm_continuations_preprocessed"
)

# Sjálfgefin úttaksskrá fyrir CSV-niðurstöður.
DEFAULT_OUTPUT_CSV = PROJECT_ROOT / "output" / "milicka_results.csv"

# Textategundir / Registers
REGISTERS = ('academic', 'blog', 'news')

# ============================================================
# LEIÐBEININGARLÍNA Í PROMPTSKRÁM / PROMPT INSTRUCTION LINE
# ============================================================
# Sama leiðbeining og í parse_texts.py — þarf að fjarlægja hana
# úr hráum promptskrám áður en dim6 (orðalengd) er mæld.
# Þáttaðar promptskrár (.psd) hafa þegar verið strippaðar af
# parse_texts.py, svo þetta snertir aðeins dim6.
# ============================================================

PROMPT_INSTRUCTION = (
    "Haltu áfram með textann á sama hátt og í sama stíl og sjáðu til þess "
    "að hann innihaldi að minnsta kosti tvö þúsund orð. Textinn þarf ekki "
    "að innihalda réttar staðreyndir en gættu þess að hann passi við stílinn:"
)


# ============================================================
# VÍDDARSKRÁ / DIMENSION REGISTRY
# ============================================================
# Listi af öllum sjö víddum sem við mælum. Hvert stak skilgreinir:
#   id    — Stutt auðkenni (notað í töflum og CSV)
#   name  — Íslenski nafnið
#   label — Enskt nafn (stytt)
#   fn    — Mælifallið sem tekur Path og skilar niðurstöðu
#   key   — Lykillinn til að draga aðalgildi (v) úr niðurstöðunni:
#            int → tuple-vísir (dim1–3 skila tuple)
#            str → dict-lykill (dim4–7 skila dict)
#   input — 'parsed' ef víddin les þáttuð tré (.psd),
#            'raw' ef hún les hrátexta (.txt) (aðeins dim6)
# ============================================================

DIMENSIONS = [
    {
        'id': 'dim1',
        'name': 'Frumlagsleysi',
        'label': 'Subject drop',
        'fn': measure_subject_drop,
        'key': 0,
        'input': 'parsed',
    },
    {
        'id': 'dim2',
        'name': 'Aukasetningar',
        'label': 'Subordination',
        'fn': measure_subordination,
        'key': 0,
        'input': 'parsed',
    },
    {
        'id': 'dim3',
        'name': 'Nafnliðalengd',
        'label': 'NP length',
        'fn': measure_np_length,
        'key': 0,
        'input': 'parsed',
    },
    {
        'id': 'dim4',
        'name': 'Þátíðarhlutfall',
        'label': 'Past tense',
        'fn': measure_past_tense,
        'key': 'past_tense_ratio',
        'input': 'parsed',
    },
    {
        'id': 'dim5',
        'name': 'Þriðjupersóna',
        'label': '3rd person',
        'fn': measure_third_person_pronouns,
        'key': 'third_person_per_1000_words',
        'input': 'parsed',
    },
    {
        'id': 'dim6',
        'name': 'Orðalengd',
        'label': 'Word length',
        'fn': measure_word_length,
        'key': 'mean_length',
        'input': 'raw',
    },
    {
        'id': 'dim7',
        'name': 'Tengiorð',
        'label': 'Complementizers',
        'fn': measure_complementizers,
        'key': 'comp_per_1000_words',
        'input': 'parsed',
    },
]


# ============================================================
# MÆLIHJÁLPARFÖLL / MEASUREMENT HELPERS
# ============================================================

def extract_value(result, key) -> float:
    """Draga aðalgildi (v) úr niðurstöðu víddarmælingar.

    Dim1–3 skila tuple þar sem v er fyrsta stakið (index 0).
    Dim4–7 skila dict þar sem v er undir ákveðnum lykli.

    Args:
        result: Niðurstaða frá mælifalli (tuple eða dict).
        key: Vísir (int) eða lykill (str) til að sækja gildi.

    Returns:
        Aðalgildi (v) sem float.
    """
    if isinstance(key, int):
        return float(result[key])
    return float(result[key])


def measure_file(dim: dict, file_path: Path) -> float:
    """Keyra vídd á einni skrá og skila aðalgildi.

    Args:
        dim: Víddarskrá-dict úr DIMENSIONS.
        file_path: Slóð á skrá (þáttuð .psd eða hrá .txt).

    Returns:
        Aðalgildi (v) sem float.
    """
    result = dim['fn'](file_path)
    return extract_value(result, dim['key'])


def measure_word_length_stripped(prompt_path: Path) -> float:
    """Mæla orðalengd á promptskrá eftir að leiðbeiningarlína er fjarlægð.

    Dim6 les hrátexta (.txt). Promptskrár byrja á leiðbeiningarlínu
    sem er EKKI hluti af mannlega textanum og þarf að fjarlægja
    áður en orðalengd er mæld.

    Notar tímabundna skrá (tempfile) þar sem measure_word_length
    tekur Path, ekki streng.

    Args:
        prompt_path: Slóð á hráa promptskrá (.txt).

    Returns:
        Meðalorðalengd (mean_length) sem float.
    """
    text = prompt_path.read_text(encoding='utf-8').strip()

    # Fjarlægja leiðbeiningarlínu ef hún er til staðar
    if text.startswith(PROMPT_INSTRUCTION):
        text = text[len(PROMPT_INSTRUCTION):].lstrip()

    # Skrifa strippaðan texta í tímabundna skrá
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.txt', encoding='utf-8', delete=False,
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)

    try:
        result = measure_word_length(tmp_path)
        return result['mean_length']
    finally:
        tmp_path.unlink()


# ============================================================
# ÚRTAKAGREINUNG / SAMPLE DISCOVERY
# ============================================================
# Finnum öll úrtök og tengja saman pör:
#   prompt ↔ reference ↔ LLM-framhöld
#
# Skráarheitamynstur:
#   Prompt:   academic_prompt_001_parsed.psd   (þáttað)
#             academic_prompt_001.txt           (hrátt)
#   Ref:      academic_ref_001_parsed.psd       (þáttað)
#             academic_ref_001.txt               (hrátt)
#   LLM:      gpt5_academic_prompt_001_parsed.psd (þáttað)
#             gpt5_academic_prompt_001.txt        (hrátt)
#
# Allt er tengt saman eftir (textategund, númer) = (register, number).
# ============================================================

# Regex til að draga út (register, number) úr skráarheitum.
# Passar við bæði prompt og ref mynstur:
#   academic_prompt_001... → ('academic', '001')
#   academic_ref_001...    → ('academic', '001')
#   gpt5_academic_prompt_001... → ('academic', '001')
SAMPLE_ID_RE = re.compile(
    r'(?P<register>academic|blog|news)_(?:prompt|ref)_(?P<number>\d+)'
)


def extract_sample_id(filename: str) -> tuple[str, str] | None:
    """Draga út (textategund, númer) úr skráarheiti.

    Dæmi:
        'academic_prompt_001_parsed.psd'       → ('academic', '001')
        'academic_ref_001_parsed.psd'          → ('academic', '001')
        'gpt5_academic_prompt_001_parsed.psd'  → ('academic', '001')
        'academic_prompt_001.txt'              → ('academic', '001')

    Args:
        filename: Skráarheiti (án möppuslóðar).

    Returns:
        Tuple (register, number) eða None ef mynstur passar ekki.
    """
    m = SAMPLE_ID_RE.search(filename)
    if m:
        return (m.group('register'), m.group('number'))
    return None


def discover_samples() -> tuple[dict, dict]:
    """Finna öll úrtök og LLM-líkön og tengja saman.

    Skilar tvennt:
        1. samples — dict af mannlegum gögnum:
            {(register, number): {
                'prompt_parsed': Path,   # Þáttað prompt (.psd)
                'ref_parsed': Path,      # Þáttað viðmið (.psd)
                'prompt_raw': Path,      # Hrátt prompt (.txt) — fyrir dim6
                'ref_raw': Path,         # Hrátt viðmið (.txt) — fyrir dim6
            }}

        2. models — dict af LLM-framhöldum per líkan:
            {model_name: {(register, number): {
                'llm_parsed': Path,
                'llm_raw': Path,
            }}}

    Returns:
        Tuple af (samples, models).
    """
    samples: dict[tuple[str, str], dict[str, Path]] = {}
    models: dict[str, dict[tuple[str, str], dict[str, Path]]] = {}

    # --- 1. ÞÁTTUÐ MANNLEG GÖGN / PARSED HUMAN DATA ---

    # Prompt-tré (.psd)
    if PARSED_PROMPTS_DIR.exists():
        for f in sorted(PARSED_PROMPTS_DIR.glob('*_parsed.psd')):
            sid = extract_sample_id(f.name)
            if sid:
                samples.setdefault(sid, {})['prompt_parsed'] = f

    # Viðmiðstré (.psd)
    if PARSED_HUMAN_REF_DIR.exists():
        for f in sorted(PARSED_HUMAN_REF_DIR.glob('*_parsed.psd')):
            sid = extract_sample_id(f.name)
            if sid:
                samples.setdefault(sid, {})['ref_parsed'] = f

    # --- 2. HRÁR MANNLEGUR TEXTI / RAW HUMAN TEXT (fyrir dim6) ---

    if RAW_PROMPTS_DIR.exists():
        for f in sorted(RAW_PROMPTS_DIR.glob('*.txt')):
            sid = extract_sample_id(f.name)
            if sid:
                samples.setdefault(sid, {})['prompt_raw'] = f

    if RAW_HUMAN_REF_DIR.exists():
        for f in sorted(RAW_HUMAN_REF_DIR.glob('*.txt')):
            sid = extract_sample_id(f.name)
            if sid:
                samples.setdefault(sid, {})['ref_raw'] = f

    # --- 3. LLM-GÖGN / LLM DATA ---

    # Þáttuð LLM-tré (.psd) — ein undirmappa per líkan
    if PARSED_LLM_DIR.exists():
        for model_dir in sorted(PARSED_LLM_DIR.iterdir()):
            if not model_dir.is_dir():
                continue
            model_name = model_dir.name
            for f in sorted(model_dir.rglob('*_parsed.psd')):
                sid = extract_sample_id(f.name)
                if sid:
                    models.setdefault(model_name, {}).setdefault(
                        sid, {}
                    )['llm_parsed'] = f

    # Hrár LLM-texti (.txt) — fyrir dim6
    if RAW_LLM_DIR.exists():
        for model_dir in sorted(RAW_LLM_DIR.iterdir()):
            if not model_dir.is_dir():
                continue
            model_name = model_dir.name
            for f in sorted(model_dir.rglob('*.txt')):
                sid = extract_sample_id(f.name)
                if sid:
                    models.setdefault(model_name, {}).setdefault(
                        sid, {}
                    )['llm_raw'] = f

    return samples, models


# ============================================================
# MÆLA ALLAR VÍDDIR Á EINNI SKRÁ / MEASURE ALL DIMS ON ONE FILE
# ============================================================

def measure_all_dims(
    file_paths: dict[str, Path],
    is_prompt: bool = False,
) -> dict[str, float]:
    """Mæla allar 7 víddir á einni skrá og skila aðalgildum.

    Dim1–5 og dim7 nota þáttuð tré (.psd).
    Dim6 notar hrátexta (.txt).
    Ef skrá vantar fyrir ákveðna vídd er NaN skilað.

    Args:
        file_paths: Dict með lyklum eins og 'prompt_parsed',
            'ref_parsed', 'llm_parsed', 'prompt_raw', 'ref_raw',
            'llm_raw' — slóðir á viðeigandi skrár.
        is_prompt: Ef True, þetta eru promptgögn og dim6 þarf
            að fjarlægja leiðbeiningarlínu áður en mælt er.

    Returns:
        Dict {dim_id: v_value} t.d. {'dim1': 0.42, 'dim2': 0.31, ...}
    """
    values: dict[str, float] = {}

    for dim in DIMENSIONS:
        dim_id = dim['id']

        if dim['input'] == 'parsed':
            # Nota þáttaða skrá (.psd)
            # Velja rétt slóð eftir tegund: prompt, ref, eða llm
            parsed_path = (
                file_paths.get('prompt_parsed')
                or file_paths.get('ref_parsed')
                or file_paths.get('llm_parsed')
            )
            if parsed_path and parsed_path.exists():
                try:
                    values[dim_id] = measure_file(dim, parsed_path)
                except Exception as e:
                    print(f"  VILLA í {dim_id} á {parsed_path.name}: {e}")
                    values[dim_id] = float('nan')
            else:
                values[dim_id] = float('nan')

        elif dim['input'] == 'raw':
            # Dim6: nota hrátexta (.txt)
            raw_path = (
                file_paths.get('prompt_raw')
                or file_paths.get('ref_raw')
                or file_paths.get('llm_raw')
            )
            if raw_path and raw_path.exists():
                try:
                    if is_prompt:
                        # Fjarlægja leiðbeiningarlínu úr promptskrá
                        values[dim_id] = measure_word_length_stripped(
                            raw_path
                        )
                    else:
                        values[dim_id] = measure_file(dim, raw_path)
                except Exception as e:
                    print(f"  VILLA í {dim_id} á {raw_path.name}: {e}")
                    values[dim_id] = float('nan')
            else:
                values[dim_id] = float('nan')

    return values


def measure_ref(file_paths: dict[str, Path]) -> dict[str, float]:
    """Mæla allar víddir á viðmiðstexta (human reference).

    Args:
        file_paths: Dict með 'ref_parsed' og 'ref_raw' slóðum.

    Returns:
        Dict {dim_id: v_value}.
    """
    paths = {
        'ref_parsed': file_paths.get('ref_parsed'),
        'ref_raw': file_paths.get('ref_raw'),
    }
    # Inni í measure_all_dims velur fallback-röðin 'ref_parsed' / 'ref_raw'
    # þar sem prompt/llm eru ekki til
    return _measure_with_explicit_paths(paths)


def measure_prompt(file_paths: dict[str, Path]) -> dict[str, float]:
    """Mæla allar víddir á prompttexta (fyrri helmingur).

    Leiðbeiningarlína er fjarlægð úr dim6-mælingu.

    Args:
        file_paths: Dict með 'prompt_parsed' og 'prompt_raw' slóðum.

    Returns:
        Dict {dim_id: v_value}.
    """
    paths = {
        'prompt_parsed': file_paths.get('prompt_parsed'),
        'prompt_raw': file_paths.get('prompt_raw'),
    }
    return _measure_with_explicit_paths(paths, is_prompt=True)


def measure_llm(file_paths: dict[str, Path]) -> dict[str, float]:
    """Mæla allar víddir á LLM-framhaldi.

    Args:
        file_paths: Dict með 'llm_parsed' og 'llm_raw' slóðum.

    Returns:
        Dict {dim_id: v_value}.
    """
    paths = {
        'llm_parsed': file_paths.get('llm_parsed'),
        'llm_raw': file_paths.get('llm_raw'),
    }
    return _measure_with_explicit_paths(paths)


def _measure_with_explicit_paths(
    paths: dict[str, Path | None],
    is_prompt: bool = False,
) -> dict[str, float]:
    """Innra hjálparfall — mæla allar víddir á skrá.

    Args:
        paths: Dict af mögulegum skráarslóðum.
        is_prompt: Ef True, strippa leiðbeiningarlínu fyrir dim6.

    Returns:
        Dict {dim_id: v_value}.
    """
    values: dict[str, float] = {}

    for dim in DIMENSIONS:
        dim_id = dim['id']

        if dim['input'] == 'parsed':
            # Finna þáttaða skrá — prófa alla þekkta lykla
            parsed_path = None
            for key in ('ref_parsed', 'prompt_parsed', 'llm_parsed'):
                p = paths.get(key)
                if p and p.exists():
                    parsed_path = p
                    break

            if parsed_path:
                try:
                    values[dim_id] = measure_file(dim, parsed_path)
                except Exception as e:
                    print(f"  VILLA í {dim_id} á {parsed_path.name}: {e}")
                    values[dim_id] = float('nan')
            else:
                values[dim_id] = float('nan')

        elif dim['input'] == 'raw':
            # Dim6: finna hráa textaskrá
            raw_path = None
            for key in ('ref_raw', 'prompt_raw', 'llm_raw'):
                p = paths.get(key)
                if p and p.exists():
                    raw_path = p
                    break

            if raw_path:
                try:
                    if is_prompt:
                        values[dim_id] = measure_word_length_stripped(
                            raw_path
                        )
                    else:
                        values[dim_id] = measure_file(dim, raw_path)
                except Exception as e:
                    print(f"  VILLA í {dim_id} á {raw_path.name}: {e}")
                    values[dim_id] = float('nan')
            else:
                values[dim_id] = float('nan')

    return values


# ============================================================
# REIKNA STAÐALSKEKKJU / COMPUTE STANDARD ERROR
# ============================================================
# Milička-formúla 2 skilgreinir náttúrulegt frávik:
#     i_k = v_prompt_k - v_ref_k
# þar sem k er úrtaksnúmer innan textategundar.
#
# SE(I_d) = std(i_1, ..., i_n) / sqrt(n)
# þar sem n = fjöldi para í textategundinni (15).
#
# Þetta mælir hversu mikil breytileiki er EÐLILEGUR milli
# tveggja helminga mannlegs texta á sömu vídd — þ.e. hversu
# mikið má búast við af náttúrulegum sveiflum.
# ============================================================

def compute_se_per_register(
    samples: dict[tuple[str, str], dict[str, Path]],
) -> dict[str, dict[str, float]]:
    """Reikna staðalskekkju (SE) per vídd per textategund.

    Notar Milička-formúlu 2: i_k = v_prompt_k - v_ref_k
    og reiknar SE = std(i_1..i_n) / sqrt(n) per vídd.

    Args:
        samples: Dict frá discover_samples() — mannleg gögn.

    Returns:
        Dict {register: {dim_id: SE_value}}.
        Dæmi: {'academic': {'dim1': 0.03, 'dim2': 0.02, ...}, ...}
    """
    se_by_register: dict[str, dict[str, float]] = {}

    for register in REGISTERS:
        print(f"\n  Reikna SE fyrir {register}...")

        # Finna öll úrtök í þessari textategund
        register_samples = {
            (reg, num): paths
            for (reg, num), paths in samples.items()
            if reg == register
        }

        n = len(register_samples)
        if n < 2:
            print(f"    AÐVÖRUN: Aðeins {n} úrtök — of fá til SE-útreiknings")
            se_by_register[register] = {
                dim['id']: 0.0 for dim in DIMENSIONS
            }
            continue

        # Mæla allar víddir á öllum prompt/ref pörum
        i_values: dict[str, list[float]] = {
            dim['id']: [] for dim in DIMENSIONS
        }

        for (reg, num), paths in sorted(register_samples.items()):
            # Athuga hvort bæði prompt og ref séu til
            has_prompt = (
                paths.get('prompt_parsed') and paths.get('prompt_raw')
            )
            has_ref = (
                paths.get('ref_parsed') and paths.get('ref_raw')
            )

            if not (has_prompt and has_ref):
                continue

            # Mæla prompt (fyrri helmingur)
            v_prompt = measure_prompt(paths)

            # Mæla viðmið (seinni helmingur)
            v_ref = measure_ref(paths)

            # Reikna i_k = v_prompt_k - v_ref_k per vídd
            for dim in DIMENSIONS:
                dim_id = dim['id']
                vp = v_prompt.get(dim_id, float('nan'))
                vr = v_ref.get(dim_id, float('nan'))
                if not (math.isnan(vp) or math.isnan(vr)):
                    i_values[dim_id].append(vp - vr)

        # Reikna SE per vídd
        se_register: dict[str, float] = {}
        for dim in DIMENSIONS:
            dim_id = dim['id']
            vals = i_values[dim_id]
            n_vals = len(vals)

            if n_vals >= 2:
                mean_i = sum(vals) / n_vals
                variance = sum(
                    (x - mean_i) ** 2 for x in vals
                ) / (n_vals - 1)
                se = math.sqrt(variance) / math.sqrt(n_vals)
            else:
                se = 0.0

            se_register[dim_id] = se
            print(f"    {dim_id}: SE = {se:.4f}  (n = {n_vals})")

        se_by_register[register] = se_register

    return se_by_register


# ============================================================
# AÐALFLÆÐI / MAIN BENCHMARK FLOW
# ============================================================

def run_benchmark(output_csv: Path | None = None) -> None:
    """Keyra Milička-viðmið á öllum textum og prenta niðurstöður.

    Args:
        output_csv: Ef gefin, vista niðurstöður í CSV-skrá.
    """

    # ── SKREF 1: Finna öll úrtök og LLM-líkön ──
    print("=" * 80)
    print("MILIČKA STÍLVIÐMIÐ — ICELANDIC STYLOMETRY BENCHMARK")
    print("=" * 80)
    print("\nSKREF 1: Finna gögn...")

    samples, models = discover_samples()

    # Telja úrtök per textategund
    for register in REGISTERS:
        n = sum(1 for (r, _) in samples if r == register)
        print(f"  {register}: {n} úrtök")

    print(f"\n  LLM-líkön: {len(models)}")
    for model_name in sorted(models):
        n = len(models[model_name])
        print(f"    {model_name}: {n} framhöld")

    if not samples:
        print("VILLA: Engin mannleg úrtök fundust.")
        sys.exit(1)

    if not models:
        print("VILLA: Engin LLM-framhöld fundust.")
        sys.exit(1)

    # ── SKREF 2: Mæla mannleg viðmið ──
    print(f"\n{'=' * 80}")
    print("SKREF 2: Mæla mannleg viðmið (human reference)...")
    print("=" * 80)

    # Dict: {(register, number): {dim_id: v_value}}
    human_ref_values: dict[tuple[str, str], dict[str, float]] = {}

    for (register, number), paths in sorted(samples.items()):
        sid = f"{register}_{number}"
        print(f"\n  Mæli viðmið: {sid}")
        human_ref_values[(register, number)] = measure_ref(paths)

    # ── SKREF 3: Reikna SE per textategund ──
    print(f"\n{'=' * 80}")
    print("SKREF 3: Reikna staðalskekkju (SE) per textategund...")
    print("=" * 80)

    se_by_register = compute_se_per_register(samples)

    # ── SKREF 4: Mæla LLM-framhöld ──
    print(f"\n{'=' * 80}")
    print("SKREF 4: Mæla LLM-framhöld og reikna formúlur...")
    print("=" * 80)

    # Safna öllum niðurstöðum í lista fyrir CSV-úttak.
    # Hvert stak: {model, register, number, dim_id, v_human, v_model,
    #              delta_v, se, b_d, score}
    all_rows: list[dict] = []

    # B-gildi per líkan per textategund
    # {model: {register: B_value}}
    B_values: dict[str, dict[str, float]] = {}

    for model_name in sorted(models):
        print(f"\n{'─' * 60}")
        print(f"LÍKAN: {model_name}")
        print(f"{'─' * 60}")

        B_values[model_name] = {}

        for register in REGISTERS:
            # Finna öll úrtök sem þetta líkan hefur í þessari textategund
            register_llm = {
                (reg, num): paths
                for (reg, num), paths in models[model_name].items()
                if reg == register
            }

            n_llm = len(register_llm)
            if n_llm == 0:
                print(f"\n  {register}: Engin framhöld")
                continue

            print(f"\n  {register}: {n_llm} framhöld")

            # Safna Δv gildum per vídd yfir öll úrtök í þessari textategund
            delta_v_sums: dict[str, list[float]] = {
                dim['id']: [] for dim in DIMENSIONS
            }

            for (reg, num), llm_paths in sorted(register_llm.items()):
                sid = f"{register}_{num}"

                # Sækja mannleg viðmiðsgildi
                v_human = human_ref_values.get((register, num))
                if v_human is None:
                    print(f"    {sid}: VANTAR mannlegt viðmið — sleppi")
                    continue

                # Mæla LLM-framhald
                v_model_vals = measure_llm(llm_paths)

                # Reikna per vídd
                for dim in DIMENSIONS:
                    dim_id = dim['id']
                    vh = v_human.get(dim_id, float('nan'))
                    vm = v_model_vals.get(dim_id, float('nan'))

                    if math.isnan(vh) or math.isnan(vm):
                        continue

                    delta_v = vh - vm
                    delta_v_sums[dim_id].append(delta_v)

                    se = se_by_register[register][dim_id]
                    if se > 0.0001:
                        b_d = delta_v / se
                    else:
                        b_d = (
                            float('inf')
                            if abs(delta_v) > 0.0001
                            else 0.0
                        )

                    score = compute_style_score(vh, vm)

                    all_rows.append({
                        'model': model_name,
                        'register': register,
                        'number': num,
                        'dim_id': dim_id,
                        'dim_label': dim['label'],
                        'v_human': vh,
                        'v_model': vm,
                        'delta_v': delta_v,
                        'se': se,
                        'b_d': b_d,
                        'score': score,
                    })

            # ── Reikna meðal-b_d per vídd og B per textategund ──
            b_d_per_dim: dict[str, float] = {}

            print(f"\n    {'Vídd':<14} {'v̄_hum':>8} {'v̄_llm':>8} "
                  f"{'Δv':>8} {'SE':>8} {'b_d':>8} {'Stig':>6}")
            print(f"    {'─'*14} {'─'*8} {'─'*8} {'─'*8} {'─'*8} "
                  f"{'─'*8} {'─'*6}")

            for dim in DIMENSIONS:
                dim_id = dim['id']
                deltas = delta_v_sums[dim_id]

                if not deltas:
                    print(f"    {dim['label']:<14} {'—':>8} {'—':>8} "
                          f"{'—':>8} {'—':>8} {'—':>8} {'—':>6}")
                    b_d_per_dim[dim_id] = 0.0
                    continue

                mean_delta = sum(deltas) / len(deltas)
                se = se_by_register[register][dim_id]

                if se > 0.0001:
                    b_d = mean_delta / se
                else:
                    b_d = (
                        float('inf')
                        if abs(mean_delta) > 0.0001
                        else 0.0
                    )

                b_d_per_dim[dim_id] = b_d

                # Meðalgildi mannlegs og LLM til útprentunar
                relevant_sids = [
                    (r, n) for (r, n) in register_llm
                    if (r, n) in human_ref_values
                ]
                mean_v_human = sum(
                    human_ref_values[sid].get(dim_id, 0.0)
                    for sid in relevant_sids
                ) / max(len(relevant_sids), 1)

                mean_v_model = mean_v_human - mean_delta

                score = compute_style_score(mean_v_human, mean_v_model)

                print(
                    f"    {dim['label']:<14} {mean_v_human:>8.4f} "
                    f"{mean_v_model:>8.4f} {mean_delta:>+8.4f} "
                    f"{se:>8.4f} {b_d:>+8.2f} {score:>6.1f}"
                )

            # FORMÚLA 4: B = ‖b‖ = √(Σ b_d²)
            b_d_list = list(b_d_per_dim.values())

            if any(b == float('inf') for b in b_d_list):
                B = float('inf')
            else:
                B = math.sqrt(sum(b ** 2 for b in b_d_list))

            B_values[model_name][register] = B

            print(f"    {'─'*14} {'─'*8} {'─'*8} {'─'*8} {'─'*8} "
                  f"{'─'*8} {'─'*6}")
            print(f"    {'B (heild)':<14} {'':>8} {'':>8} {'':>8} "
                  f"{'':>8} {B:>8.2f}")

            # Túlkun
            print(f"    TÚLKUN: ", end="")
            if B < 1:
                print("Mjög nálægt mannlegum texta.")
            elif B < 2:
                print("Í viðunandi fjarlægð.")
            elif B < 5:
                print("Greinilegur munur.")
            else:
                print("Verulegur munur — líkanið hermist illa eftir stílnum.")

    # ── SKREF 5: Heildarsamantekt / Overall summary ──
    print(f"\n\n{'=' * 80}")
    print("HEILDARSAMANTEKT / OVERALL SUMMARY")
    print("=" * 80)

    # Tafla: líkan × textategund → B
    header = f"  {'Líkan':<28}"
    for reg in REGISTERS:
        header += f" {reg:>10}"
    header += f" {'Meðaltal':>10}"
    print(header)
    print(f"  {'─'*28}" + f" {'─'*10}" * (len(REGISTERS) + 1))

    for model_name in sorted(B_values):
        row = f"  {model_name:<28}"
        b_list = []
        for reg in REGISTERS:
            b = B_values[model_name].get(reg)
            if b is not None:
                row += f" {b:>10.2f}"
                b_list.append(b)
            else:
                row += f" {'—':>10}"
        if b_list:
            mean_B = sum(b_list) / len(b_list)
            row += f" {mean_B:>10.2f}"
        else:
            row += f" {'—':>10}"
        print(row)

    # ── LEIÐBEININGAR UM TÚLKUN / INTERPRETATION GUIDE ──
    print(f"\n{'=' * 80}")
    print("HVERNIG Á AÐ TÚLKA NIÐURSTÖÐURNAR:")
    print("=" * 80)
    print("  Δv  = v_human - v_model (frávik per vídd)")
    print("        Jákvætt: líkanið hefur minna af eiginleikanum")
    print("        Neikvætt: líkanið hefur meira af eiginleikanum")
    print()
    print("  b_d = mean(Δv) / SE (staðlað frávik per vídd)")
    print("        |b_d| < 1: innan náttúrulegrar sveiflu")
    print("        |b_d| 1-2: veikt frávik")
    print("        |b_d| > 2: verulegt frávik")
    print()
    print("  B   = √(Σ b_d²) (heildarskor yfir allar víddir)")
    print("        B < 1: mjög nálægt mannlegum texta")
    print("        B < 2: viðunandi")
    print("        B > 5: verulegur munur")
    print()
    print("  Stig = 0-100 einkunn per vídd")
    print("        100 = fullkomið samræmi")
    print("          0 = ekkert samræmi")
    print("=" * 80)

    # ── VISTA CSV / SAVE CSV ──
    if output_csv:
        save_csv(all_rows, output_csv)


# ============================================================
# VISTA NIÐURSTÖÐUR SEM CSV / SAVE RESULTS AS CSV
# ============================================================

def save_csv(rows: list[dict], output_path: Path) -> None:
    """Vista nákvæmar niðurstöður í CSV-skrá til frekari greiningar.

    Args:
        rows: Listi af dict — ein lína per (líkan, textategund, úrtak, vídd).
        output_path: Slóð á CSV-skrá.
    """
    if not rows:
        print("  Engar niðurstöður til að vista.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'model', 'register', 'number', 'dim_id', 'dim_label',
        'v_human', 'v_model', 'delta_v', 'se', 'b_d', 'score',
    ]

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            # Slétta tölur til 6 aukastafa í CSV
            row_out = dict(row)
            for key in ('v_human', 'v_model', 'delta_v', 'se', 'b_d', 'score'):
                val = row_out[key]
                if isinstance(val, float) and not math.isinf(val):
                    row_out[key] = f"{val:.6f}"
                elif math.isinf(val):
                    row_out[key] = "inf"
            writer.writerow(row_out)

    print(f"\n  Niðurstöður vistaðar í: {output_path}")
    print(f"  ({len(rows)} raðir)")


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra Milička-viðmið."""
    parser = argparse.ArgumentParser(
        description="Keyra Milička stílviðmið á öllum tilraunatextum.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Keyra viðmið á öllum gögnum:
  python scripts/run_milicka.py

  # Keyra og vista CSV-niðurstöður:
  python scripts/run_milicka.py --output-csv output/milicka_results.csv
        """
    )
    parser.add_argument(
        '--output-csv',
        type=Path,
        default=None,
        help="Slóð á CSV-skrá til að vista nákvæmar niðurstöður "
             "(ein lína per líkan × textategund × úrtak × vídd)."
    )

    args = parser.parse_args()
    run_benchmark(output_csv=args.output_csv)


if __name__ == "__main__":
    main()
