#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
run_milicka.py — AÐALSKRIFTA: Keyrir allar víddir og reiknar Milička-formúlur
===============================================================================

TILGANGUR / PURPOSE:
    Þetta er aðalskriftið sem tengir allt saman. Það keyrir allar
    víddirnar (dim1–dim11) á mannlegum og LLM-framleiddun textum,
    reiknar Milička-formúlurnar og prentar niðurstöður.

    This is the main orchestrator script. It runs all dimensions
    (dim1–dim11) on human and LLM texts, computes Milička's formulas,
    and prints results.

ATHUGIÐ — VÍDD 8 KREFST FORUTREIKNINGS / NOTE — DIM8 REQUIRES PRECOMPUTATION:
    Vídd 8 (BÍN-orðaforðaþekja) notar „parse-once“ cache-lagi. Keyrðu
    `scripts/dim8_bin_ratio.py` á öllum textaskrám ÁÐUR en þetta skrift
    er keyrt. Ef output/dim8_bin_summary.csv vantar er vídd 8 sleppt og
    viðvörun prentað — aðrar víddir halda áfram.

    Dim8 (BÍN vocabulary coverage) uses a parse-once cache. Run
    `scripts/dim8_bin_ratio.py` on all text directories BEFORE running
    this script. If output/dim8_bin_summary.csv is missing, dim8 is
    skipped with a warning; other dimensions continue to run.

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

    Formúla 4 (aðlöguð): B = √(meðaltal(b_d²))    [RMS-form]
        Upphafleg formúla Milička (2025) er B = ‖b‖ = √(Σ b_d²) —
        evklíðskt norm. Hér notum við RMS-form (root-mean-square) til
        að halda B-skori sambærilegu þvert á málsýni með ólíkum fjölda
        gildra vídda (þegar t.d. vídd 7 skilar NaN fyrir stök málsýni).
        Þegar allar n víddir eru gildar gildir
            sqrt(mean(b_d²)) = ‖b‖ / sqrt(n)
        — sama sjálfgildi og hjá Milička upp að fastri kvarðabreytingu
        sqrt(n). Röðun líkana helst óbreytt þegar n er fast; aðeins
        algild B-gildi skala niður um sqrt(n)≈3.16 fyrir n=10. Sjá
        ákvörðun 028 fyrir röksemdir.

GAGNASKIPULAG / DATA LAYOUT:
    Þáttuð tré (frá parse_texts.py):
        output/parsed/prompts/*_parsed.psd                       (60 skrár)
        output/parsed/human_texts/*_parsed.psd                   (60 skrár)
        output/parsed/llm_continuations_clean/{model}/{reg}/     (per líkan)

    Hrár texti (fyrir dim6 = orðalengd, dim10 = LIX, dim11 = MTLD):
        data/experiment/prompts/*.txt                            (60 skrár)
        data/experiment/human_texts/*.txt                        (60 skrár)
        data/experiment/llm_continuations_clean/{model}/{reg}/   (per líkan, ~342 alls)

FLÆÐI / FLOW:
    1. Finna öll úrtök (15 per textategund × 4 tegundir = 60)
    2. Finna öll LLM-líkön og tengja við samsvarandi úrtök
    3. Mæla dim1–dim11 á mannlegum viðmiðstextum (human_texts)
    4. Mæla dim1–dim11 á prompttextum (prompts) — til SE-útreiknings
    5. Reikna náttúrulegt frávik i_k per pör og SE per textategund
    6. Mæla dim1–dim11 á LLM-framhöldum
    7. Reikna Δv, b_d, B per líkan × textategund
    8. Prenta niðurstöður og vista CSV

KEYRSLA / USAGE:
    python scripts/run_milicka.py
    python scripts/run_milicka.py --output-csv output/milicka_results.csv
    python scripts/run_milicka.py --plot
    python scripts/run_milicka.py --plot --figure-dir output/figures
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
# víddarföllin (dim1–dim11, nema dim8 sem les cache-CSV) þegar
# skriftið er keyrt frá rótarmöppu verkefnisins.
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
# ATHUGIÐ: dim8 er EKKI flutt inn sem fall hér — það les cache CSV
# svo islenska er valfrjáls háðni. Sjá lookup_dim8_value() neðar.
from dim9_tree_depth import measure_tree_depth
from dim10_lix import measure_lix
from dim11_mtld import measure_mtld
from style_score import compute_style_score


# ============================================================
# SJÁLFGEFNAR SLÓÐIR / DEFAULT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- ÞÁTTUÐ TRÉ / PARSED TREES ---
# Frá parse_texts.py — .psd skrár í output/parsed/
PARSED_DIR = PROJECT_ROOT / "output" / "parsed"
PARSED_PROMPTS_DIR = PARSED_DIR / "prompts"
PARSED_HUMAN_REF_DIR = PARSED_DIR / "human_texts"
PARSED_LLM_DIR = PARSED_DIR / "llm_continuations_clean"

# --- HRÁR TEXTI / RAW TEXT ---
# Fyrir dim6 (orðalengd) sem les hrátexta, ekki þáttuð tré.
RAW_PROMPTS_DIR = PROJECT_ROOT / "data" / "experiment" / "prompts"
RAW_HUMAN_REF_DIR = PROJECT_ROOT / "data" / "experiment" / "human_texts"
RAW_LLM_DIR = (
    PROJECT_ROOT / "data" / "experiment" / "llm_continuations_clean"
)

# Sjálfgefin úttaksskrá fyrir CSV-niðurstöður.
DEFAULT_OUTPUT_CSV = PROJECT_ROOT / "output" / "milicka_results.csv"

# Forútreiknuð CSV fyrir dim8 (búin til af scripts/dim8_bin_ratio.py)
# Precomputed CSV for dim8 (produced by scripts/dim8_bin_ratio.py)
DIM8_SUMMARY_CSV = PROJECT_ROOT / "output" / "dim8_bin_summary.csv"

# Textategundir / Registers
REGISTERS = ('academic', 'blog', 'news', 'unseen')

# Le Chat Fast (lagt niður á söfnunartíma) og Le Chat Balanced eru bæði Mistral's free-tier Le Chat á ólíkum tímapunktum; aggregað sem le_chat_free.
MODEL_ALIASES = {
    "le_chat_fast": "le_chat_free",
    "le_chat_balanced": "le_chat_free",
}

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
# Listi af öllum tíu víddum sem við mælum. Hvert stak skilgreinir:
#   id    — Stutt auðkenni (notað í töflum og CSV)
#   name  — Íslenski nafnið
#   label — Enskt nafn (stytt)
#   fn    — Mælifallið sem tekur Path og skilar niðurstöðu.
#            Fyrir dim8 er þetta None — gildi er flett upp úr cache CSV.
#   key   — Lykillinn til að draga aðalgildi (v) úr niðurstöðunni:
#            int → tuple-vísir (dim1–3 skila tuple)
#            str → dict-lykill (dim4–7, dim9, dim10, dim11 skila dict)
#            Ónotað fyrir dim8 (gildið kemur beint úr CSV-dálki).
#   input — 'parsed' ef víddin les þáttuð tré (.psd)  (dim1–5, dim7, dim9)
#           'raw' ef hún les hrátexta (.txt)          (dim6, dim10, dim11)
#           'precomputed_csv' ef hún les forunna CSV-skrá (dim8)
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
        # VÍDD 7: Hlutfall sem-tengiorða af öllum tengiorðum.
        # Aðal-v er `comp_ratio = sem / (sem + að)`, bil [0, 1] eða
        # NaN ef sem+að == 0. Pípan útilokar NaN-víddir frá b-vektor
        # þess málsýnis (sjá summary report neðar). Sjá ákvörðun 028.
        'id': 'dim7',
        'name': 'Tengiorð',
        'label': 'Complementizers',
        'fn': measure_complementizers,
        'key': 'comp_ratio',
        'input': 'parsed',
    },
    {
        'id': 'dim8',
        'name': 'BÍN-þekja',
        'label': 'BÍN coverage',
        'fn': None,  # Les úr cache — sjá lookup_dim8_value()
        'key': 'in_bin_ratio',  # Dálkur í dim8_bin_summary.csv
        'input': 'precomputed_csv',
    },
    {
        # VÍDD 9: Trédýpt (setningarþyngd). Aðlagað úr UD-byggðum
        # „sentence weight“ fyrirlestri Steinþórs Steingrímssonar á
        # IcePaHC liðgerðartré. Orthogonal við dim2: dim2 mælir TÍÐNI
        # aukasetninga, dim9 mælir DÝPT innfelldra liða.
        'id': 'dim9',
        'name': 'Trédýpt',
        'label': 'Tree depth',
        'fn': measure_tree_depth,
        'key': 'mean_tree_depth',
        'input': 'parsed',
    },
    {
        # VÍDD 10: LIX-læsilegskor. Hliðstæð dim6 — báðar mæla
        # orðalengd/þyngd en dim10 bætir setningalengd við. Verður
        # borin saman við dim6 í greiningarkafla; ein eða hvorug
        # gæti fallið út við dimension selection í MA-lokaverkefni.
        'id': 'dim10',
        'name': 'LIX-læsilegskor',
        'label': 'LIX readability',
        'fn': measure_lix,
        'key': 'lix_score',
        'input': 'raw',
    },
    {
        # VÍDD 11: MTLD (Measure of Textual Lexical Diversity,
        # McCarthy & Jarvis 2010). Lengdarstöðugur arftaki TTR.
        # Ekki hliðstæða Milička-vídda — Biber-hvött framlenging
        # (Informational production / lexical diversity). Sjá
        # ákvörðun 027 fyrir forathugun og hönnunarrökstuðning.
        'id': 'dim11',
        'name': 'Orðaforðafjölbreytni',
        'label': 'Lexical diversity (MTLD)',
        'fn': measure_mtld,
        'key': 'final_mtld',
        'input': 'raw',
    },
]


# ============================================================
# DIM8 CACHE / DIM8 CACHE
# ============================================================
# Vídd 8 notar parse-once arkítektúr: scripts/dim8_bin_ratio.py
# keyrir allar BÍN-flettingar og vistar niðurstöður í CSV.
# run_milicka.py les CSV-skrána einu sinni í dict og flettir upp
# eftir skráarheiti.
#
# AF HVERJU CACHE?
#   1. islenska (BinPackage) er dýrt að hlaða í minnið.
#   2. Fletting er auðveld að keyra sjálfstætt ef notandi vill
#      kanna hvaða orð eru OOV áður en Milička er keyrt.
#   3. islenska helst VALFRJÁLS háðni fyrir run_milicka.py — ef
#      notandi hefur ekki dim8_bin_summary.csv, heldur pípan
#      áfram án vídd 8 (skilar NaN fyrir dim8 og prentar aðvörun).
# ============================================================

# Einka-cache og boolean fyrir hvort CSV sé til.
# None = ekki reynt að hlaða; dict = hlaðið; {} = reyndi en mistókst.
_DIM8_CACHE: dict[str, float] | None = None
_DIM8_WARNED: bool = False


def _load_dim8_cache() -> dict[str, float]:
    """Hlaða dim8_bin_summary.csv inn í dict {filename: in_bin_ratio}.

    Aðeins keyrt einu sinni per ferli — niðurstaðan er geymd í
    _DIM8_CACHE. Ef CSV er ekki til, skilum tómu dict og prentum
    viðvörun EINU SINNI (með leiðbeiningum um hvernig má búa til).

    Returns:
        Dict {filename: in_bin_ratio}. Tómt dict ef CSV vantar.
    """
    global _DIM8_CACHE, _DIM8_WARNED
    if _DIM8_CACHE is not None:
        return _DIM8_CACHE

    if not DIM8_SUMMARY_CSV.exists():
        if not _DIM8_WARNED:
            print(
                f"\n  AÐVÖRUN: dim8 krefst {DIM8_SUMMARY_CSV} — "
                f"finnst ekki."
            )
            print(
                f"  Keyrðu: python scripts/dim8_bin_ratio.py "
                f"--text-dir data/experiment/"
            )
            print(f"  Dim8 verður sleppt (NaN); aðrar víddir halda áfram.\n")
            _DIM8_WARNED = True
        _DIM8_CACHE = {}
        return _DIM8_CACHE

    cache: dict[str, float] = {}
    with open(DIM8_SUMMARY_CSV, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fname = row.get('filename', '').strip()
            val_str = row.get('in_bin_ratio', '').strip()
            if not fname or not val_str:
                continue
            try:
                cache[fname] = float(val_str)
            except ValueError:
                # Skemmd lína — sleppt með viðvörun
                print(
                    f"  AÐVÖRUN: Gat ekki þáttað in_bin_ratio='{val_str}' "
                    f"fyrir {fname} í {DIM8_SUMMARY_CSV}"
                )

    _DIM8_CACHE = cache
    return _DIM8_CACHE


def lookup_dim8_value(file_path: Path) -> float:
    """Fletta upp dim8 gildi fyrir skrá eftir skráarheiti.

    Args:
        file_path: Slóð á hráa textaskrá (.txt). Aðeins
            skráarheitið (file_path.name) er notað fyrir uppflettingu.

    Returns:
        in_bin_ratio sem float, eða float('nan') ef skráarheitið
        er ekki í cache (eða CSV vantar).
    """
    cache = _load_dim8_cache()
    return cache.get(file_path.name, float('nan'))


# ============================================================
# MÆLIHJÁLPARFÖLL / MEASUREMENT HELPERS
# ============================================================

def extract_value(result, key) -> float:
    """Draga aðalgildi (v) úr niðurstöðu víddarmælingar.

    Dim1–3 skila tuple þar sem v er fyrsta stakið (index 0).
    Dim4–7, dim9, dim10 skila dict þar sem v er undir ákveðnum lykli.

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


def measure_raw_stripped(dim: dict, prompt_path: Path) -> float:
    """Mæla hrátextavídd á promptskrá eftir að leiðbeiningarlína er fjarlægð.

    Hrátextavíddir (dim6 = orðalengd, dim10 = LIX) lesa .txt beint.
    Promptskrár byrja á leiðbeiningarlínu sem er EKKI hluti af
    mannlega textanum og þarf að fjarlægja áður en mælt er.

    Notar tímabundna skrá (tempfile) þar sem mælifallið tekur Path,
    ekki streng.

    Args:
        dim: Víddarskrá-dict úr DIMENSIONS (input='raw').
        prompt_path: Slóð á hráa promptskrá (.txt).

    Returns:
        Aðalgildi víddarinnar sem float (dim['key'] úr niðurstöðu).
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
        return measure_file(dim, tmp_path)
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
    r'(?P<register>academic|blog|news|unseen)_(?:prompt|ref)_(?P<number>\d+)'
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

    # --- 1. ÞÁTTUÐ MENNSK GÖGN / PARSED HUMAN DATA ---

    # Prompt-tré (.psd)
    if PARSED_PROMPTS_DIR.exists():
        for f in sorted(PARSED_PROMPTS_DIR.glob('*_parsed.psd')):
            sid = extract_sample_id(f.name)
            if sid:
                samples.setdefault(sid, {})['prompt_parsed'] = f

    # Viðmiðunartré (.psd)
    if PARSED_HUMAN_REF_DIR.exists():
        for f in sorted(PARSED_HUMAN_REF_DIR.glob('*_parsed.psd')):
            sid = extract_sample_id(f.name)
            if sid:
                samples.setdefault(sid, {})['ref_parsed'] = f

    # --- 2. HRÁR MENNSKUR TEXTI / RAW HUMAN TEXT (fyrir dim6) ---

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
    # ATH: MODEL_ALIASES beitt á möppuheiti svo aliased líkön (t.d.
    # le_chat_fast + le_chat_balanced → le_chat_free) safnast saman
    # í eina línu í niðurstöðum. Möppuheiti í data/ eru ÓBREYTT.
    if PARSED_LLM_DIR.exists():
        for model_dir in sorted(PARSED_LLM_DIR.iterdir()):
            if not model_dir.is_dir():
                continue
            model_name = MODEL_ALIASES.get(model_dir.name, model_dir.name)
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
            model_name = MODEL_ALIASES.get(model_dir.name, model_dir.name)
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
    """Mæla allar víddir (dim1–dim11) á einni skrá og skila aðalgildum.

    Dim1–5, dim7 og dim9 nota þáttuð tré (.psd).
    Dim6 (orðalengd) og dim10 (LIX) nota hrátexta (.txt).
    Dim8 les forútreiknaða CSV eftir skráarheiti (hrátexta-slóðarinnar).
    Ef skrá vantar fyrir ákveðna vídd er NaN skilað.

    Args:
        file_paths: Dict með lyklum eins og 'prompt_parsed',
            'ref_parsed', 'llm_parsed', 'prompt_raw', 'ref_raw',
            'llm_raw' — slóðir á viðeigandi skrár.
        is_prompt: Ef True, þetta eru promptgögn og hrátextavíddir
            (dim6, dim10) þurfa að fjarlægja leiðbeiningarlínu áður
            en mælt er. Dim8
            sér um leiðbeiningarlínu sjálft við forútreikning.

    Returns:
        Dict {dim_id: v_value} t.d. {'dim1': 0.42, 'dim2': 0.31, ...,
            'dim8': 0.96}.
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
            # Hrátextavíddir (dim6, dim10): nota hrátexta (.txt)
            raw_path = (
                file_paths.get('prompt_raw')
                or file_paths.get('ref_raw')
                or file_paths.get('llm_raw')
            )
            if raw_path and raw_path.exists():
                try:
                    if is_prompt:
                        # Fjarlægja leiðbeiningarlínu úr promptskrá
                        values[dim_id] = measure_raw_stripped(
                            dim, raw_path
                        )
                    else:
                        values[dim_id] = measure_file(dim, raw_path)
                except Exception as e:
                    print(f"  VILLA í {dim_id} á {raw_path.name}: {e}")
                    values[dim_id] = float('nan')
            else:
                values[dim_id] = float('nan')

        elif dim['input'] == 'precomputed_csv':
            # Dim8: fletta upp úr forútreiknaðri CSV eftir skráarheiti.
            # Notum sömu hráu textaskrá og dim6 — skráarheitið gildir yfir
            # prompt/ref/llm. Dim8 sjálft fjarlægir leiðbeiningarlínu við
            # forútreikning, svo is_prompt fáninn þarf ekki að hafa áhrif.
            raw_path = (
                file_paths.get('prompt_raw')
                or file_paths.get('ref_raw')
                or file_paths.get('llm_raw')
            )
            if raw_path is None:
                values[dim_id] = float('nan')
            else:
                values[dim_id] = lookup_dim8_value(raw_path)

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
            # Hrátextavíddir (dim6, dim10): finna hráa textaskrá
            raw_path = None
            for key in ('ref_raw', 'prompt_raw', 'llm_raw'):
                p = paths.get(key)
                if p and p.exists():
                    raw_path = p
                    break

            if raw_path:
                try:
                    if is_prompt:
                        values[dim_id] = measure_raw_stripped(
                            dim, raw_path
                        )
                    else:
                        values[dim_id] = measure_file(dim, raw_path)
                except Exception as e:
                    print(f"  VILLA í {dim_id} á {raw_path.name}: {e}")
                    values[dim_id] = float('nan')
            else:
                values[dim_id] = float('nan')

        elif dim['input'] == 'precomputed_csv':
            # Dim8: fletta upp í cache eftir hrátexta-skráarheiti.
            # Cache er keyrð á nafn, svo .exists() ekki krafist.
            raw_path = (
                paths.get('ref_raw')
                or paths.get('prompt_raw')
                or paths.get('llm_raw')
            )
            if raw_path is None:
                values[dim_id] = float('nan')
            else:
                values[dim_id] = lookup_dim8_value(raw_path)

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

def run_benchmark(
    output_csv: Path | None = None,
    plot: bool = False,
    figure_dir: Path | None = None,
) -> None:
    """Keyra Milička-viðmið á öllum textum og prenta niðurstöður.

    Args:
        output_csv: Ef gefin, vista niðurstöður í CSV-skrá.
        plot: Ef True, búa til dreifirit og súlurit.
        figure_dir: Mappa fyrir myndir (sjálfgefið output/figures/).
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

    # ── NaN-LOGGING / SUMMARY REPORT BÓKHALD ──
    # Til að skila summary-skýrslu eftir keyrslu (sjá ákvörðun 028):
    #   nan_log: hver (model, register, number) með NaN per dimens.
    #   sample_dim_counts: heildarfjöldi gildra vídda per (m, r, n).
    nan_log: list[dict] = []
    sample_dim_counts: dict[tuple[str, str, str], int] = {}
    n_total_dims = len(DIMENSIONS)

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

                # Bókhald fyrir NaN-summary: byrja við 0 og hækka per
                # gilda vídd. Málsýni sleppt (engin gild vídd) er
                # skráð sérstaklega neðar.
                sample_dim_counts[(model_name, register, num)] = 0

                # Reikna per vídd
                for dim in DIMENSIONS:
                    dim_id = dim['id']
                    vh = v_human.get(dim_id, float('nan'))
                    vm = v_model_vals.get(dim_id, float('nan'))

                    # Skrá NaN-tilvik í log fyrir summary-skýrslu.
                    # NaN getur komið frá víddinni sjálfri (t.d.
                    # dim7 á skrá án tengiorða) eða frá vantandi skrá.
                    if math.isnan(vh) or math.isnan(vm):
                        which = []
                        if math.isnan(vh):
                            which.append('human')
                        if math.isnan(vm):
                            which.append('llm')
                        nan_log.append({
                            'model': model_name,
                            'register': register,
                            'number': num,
                            'dim_id': dim_id,
                            'reason': '+'.join(which) + ' NaN',
                        })
                        continue

                    sample_dim_counts[(model_name, register, num)] += 1

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
            # `b_d_per_dim` inniheldur AÐEINS víddir með ≥1 gild Δv-pör.
            # Víddir án gildra para eru útilokaðar úr RMS-nefnaranum (sjá
            # ákvörðun 028) — að telja þær sem 0 myndi bjaga B niður.
            b_d_per_dim: dict[str, float] = {}

            print(f"\n    {'Vídd':<14} {'v̄_hum':>8} {'v̄_llm':>8} "
                  f"{'Δv':>8} {'SE':>8} {'b_d':>8} {'Stig':>6}")
            print(f"    {'─'*14} {'─'*8} {'─'*8} {'─'*8} {'─'*8} "
                  f"{'─'*8} {'─'*6}")

            for dim in DIMENSIONS:
                dim_id = dim['id']
                deltas = delta_v_sums[dim_id]

                if not deltas:
                    # Engin gild Δv per þessa vídd í þessari (líkan,
                    # textategund) klefa — vídd sleppt úr B-útreikningi.
                    print(f"    {dim['label']:<14} {'—':>8} {'—':>8} "
                          f"{'—':>8} {'—':>8} {'—':>8} {'—':>6}")
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

            # FORMÚLA 4 (aðlöguð): B = sqrt(mean(b_d²))   [RMS-form]
            # AÐLÖGUN frá Milička (2025) sem skilgreinir B = ‖b‖ =
            # sqrt(Σ b_d²). RMS-formið heldur sambærilegri skala þvert á
            # málsýni þar sem víddafjöldi er breytilegur (t.d. þegar
            # vídd 7 skilar NaN fyrir tiltekið málsýni). Þegar allar n
            # víddir eru gildar gildir
            #     sqrt(mean(b_d²)) = ‖b‖ / sqrt(n)
            # — sama sem Milička upp að fastri skalabreytingu sqrt(n).
            # Röðun líkana er óbreytt þegar n er fast; aðeins algild
            # B-gildi minnka um þátt sqrt(n)≈3.16 fyrir n=10.
            # Sjá ákvörðun 028 fyrir röksemdir og skjalfestingu.
            b_d_list = list(b_d_per_dim.values())
            n_valid_dims = len(b_d_list)

            if n_valid_dims == 0:
                # Engin gild vídd í þessum (líkan, textategund) klefa.
                # Mjög ólíklegt í reynd; skráum sem NaN og prentum aðvörun.
                print(
                    f"    AÐVÖRUN: engin gild vídd fyrir "
                    f"{model_name}/{register} — B sett sem NaN.",
                    file=sys.stderr,
                )
                B = float('nan')
            elif any(b == float('inf') for b in b_d_list):
                B = float('inf')
            else:
                B = math.sqrt(
                    sum(b ** 2 for b in b_d_list) / n_valid_dims
                )

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

    # ── SUMMARY-SKÝRSLA UM GILDAR VÍDDIR / VALID DIMENSIONS REPORT ──
    # Samantekt yfir fjölda gildra vídda per málsýni (sjá ákvörðun 028).
    # Sample = (líkan, textategund, númer). Við birtum fjölda málsýna
    # per víddafjölda, og lista yfir málsýni sem misstu víddir.
    print(f"\n{'=' * 80}")
    print("SUMMARY — GILDAR VÍDDIR PER MÁLSÝNI / VALID DIMENSIONS PER SAMPLE")
    print("=" * 80)

    if sample_dim_counts:
        n_samples_total = len(sample_dim_counts)
        # Safna dreifingu: hve mörg málsýni fengu k gildar víddir?
        count_distribution: dict[int, int] = {}
        for count in sample_dim_counts.values():
            count_distribution[count] = count_distribution.get(count, 0) + 1

        print(f"  Heildarfjöldi málsýna: {n_samples_total}")
        print(f"  Heildarfjöldi vídda í pípu: {n_total_dims}")
        print()
        # Prenta frá fullu setti og niður
        for k in sorted(count_distribution.keys(), reverse=True):
            n = count_distribution[k]
            if k == n_total_dims:
                label = f"allar {n_total_dims} víddir"
            elif k == 0:
                label = "engin gild vídd (sleppt)"
            else:
                label = f"{k} víddir"
            print(f"    {n}/{n_samples_total} málsýni á {label}")
    else:
        print("  (Engin málsýni með mælingar — ekkert að sýna.)")

    # Ef einhverjir NaN-atburðir komu fram, birta lista
    if nan_log:
        print()
        print(f"  Málsýni með víddir sem vantar ({len(nan_log)} NaN-atburðir):")
        # Röðuð lýsing per málsýni
        per_sample_nans: dict[tuple[str, str, str], list[str]] = {}
        for entry in nan_log:
            key = (entry['model'], entry['register'], entry['number'])
            per_sample_nans.setdefault(key, []).append(
                f"{entry['dim_id']} ({entry['reason']})"
            )
        for (model_name, reg, num) in sorted(per_sample_nans):
            sid = f"{reg}_{num}"
            dims_str = ', '.join(per_sample_nans[(model_name, reg, num)])
            print(f"    {model_name}/{sid}: {dims_str}")
    else:
        print()
        print("  Engin NaN-tilvik — allar víddir gildar fyrir öll málsýni.")

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
    print("  B   = √(meðaltal(b_d²))  (RMS-form, sjá ákvörðun 028)")
    print("        Aðlögun frá Milička B = ‖b‖. Sambærilegur skali")
    print("        þvert á málsýni með ólíkan fjölda gildra vídda.")
    print("        Algild B-gildi eru sqrt(n)≈3.16× minni en hjá")
    print("        Milička þegar allar 10 víddir eru gildar.")
    print("        B < ~0.3: mjög nálægt mannlegum texta")
    print("        B < ~0.7: viðunandi")
    print("        B > ~1.5: verulegur munur")
    print()
    print("  Stig = 0-100 einkunn per vídd")
    print("        100 = fullkomið samræmi")
    print("          0 = ekkert samræmi")
    print("=" * 80)

    # ── VISTA CSV / SAVE CSV ──
    if output_csv:
        save_csv(all_rows, output_csv)

    # ── TEIKNA MYNDIR / GENERATE PLOTS ──
    if plot:
        if figure_dir is None:
            figure_dir = PROJECT_ROOT / "output" / "figures"
        print(f"\n{'=' * 80}")
        print("TEIKNA MYNDIR / GENERATING PLOTS")
        print(f"  Mappa: {figure_dir}")
        print("=" * 80)
        generate_plots(all_rows, B_values, figure_dir)


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
# LÍNURIT / PLOTTING
# ============================================================
# Búa til Milička-stíls dreifirit (scatterplots) og
# súlurit yfir B-gildi. Matplotlib er aðeins flutt inn
# þegar --plot er gefið svo það sé ekki nauðsynleg forsenda
# fyrir þá sem vilja aðeins tölulegar niðurstöður.
#
# Generate Milička-style scatterplots and a B-score bar chart.
# matplotlib is imported lazily so it is not a hard dependency
# for users who only want the numerical output.
# ============================================================

# Litapaletta per textategund — litblinduvæn.
# Register colour palette — colourblind-friendly.
REGISTER_COLOURS: dict[str, str] = {
    'academic': '#4477AA',   # blátt / blue
    'blog':     '#EE6677',   # appelsínugult / coral-orange
    'news':     '#228833',   # grænt / green
    'unseen':   '#AA3377',   # fjólublátt / purple
}

# Sjálfgefinn litur ef textategund er ekki þekkt.
# Fallback colour for unknown registers.
_DEFAULT_COLOUR = '#BBBBBB'


def _pretty_model_name(raw: str) -> str:
    """Snoturra líkansheiti til birtingar / Prettify model name for display."""
    return raw.replace('_', ' ').title()


def generate_plots(
    all_rows: list[dict],
    B_values: dict[str, dict[str, float]],
    figure_dir: Path,
) -> None:
    """Búa til dreifirit og súlurit og vista í möppu.

    Create per-dimension scatterplots and an aggregate B-score
    bar chart and save to *figure_dir*.

    Args:
        all_rows: Listi af per-sample dict (frá run_benchmark).
        B_values: {model: {register: B}} (frá run_benchmark).
        figure_dir: Slóð á möppu þar sem myndir eru vistaðar.
    """
    # Seinkað innflutningur / Lazy import
    import matplotlib
    matplotlib.use('Agg')  # Bakendi án glugga / non-interactive backend
    import matplotlib.pyplot as plt

    figure_dir.mkdir(parents=True, exist_ok=True)

    # --- Finna allar textategundir og líkön í gögnunum ---
    # --- Discover all registers and models in the data ---
    registers_in_data: list[str] = sorted(
        {row['register'] for row in all_rows}
    )
    models_in_data: list[str] = sorted(
        {row['model'] for row in all_rows}
    )

    if not all_rows:
        print("  Engar niðurstöður til að teikna — sleppi myndum.")
        return

    # ==========================================================
    # MYND 1: Dreifirit per vídd / Per-dimension scatterplots
    # ==========================================================

    for dim in DIMENSIONS:
        dim_id = dim['id']
        dim_rows = [r for r in all_rows if r['dim_id'] == dim_id]
        if not dim_rows:
            continue

        n_models = len(models_in_data)
        fig, axes = plt.subplots(
            1, n_models,
            figsize=(5 * n_models, 4.8),
            squeeze=False,
            sharey=True,
        )

        # Finna ás-mörk / determine axis limits
        all_v = (
            [r['v_human'] for r in dim_rows]
            + [r['v_model'] for r in dim_rows]
        )
        v_min = min(all_v)
        v_max = max(all_v)
        margin = (v_max - v_min) * 0.08 if v_max > v_min else 0.1
        lo = v_min - margin
        hi = v_max + margin

        for col_idx, model_name in enumerate(models_in_data):
            ax = axes[0, col_idx]
            model_rows = [r for r in dim_rows if r['model'] == model_name]

            # Teikna hornalínu / diagonal y=x
            ax.plot([lo, hi], [lo, hi], ls='--', color='#888888',
                    lw=1, zorder=1)

            # Teikna punkta per textategund / scatter by register
            for reg in registers_in_data:
                reg_rows = [r for r in model_rows if r['register'] == reg]
                if not reg_rows:
                    continue
                xs = [r['v_human'] for r in reg_rows]
                ys = [r['v_model'] for r in reg_rows]
                colour = REGISTER_COLOURS.get(reg, _DEFAULT_COLOUR)
                ax.scatter(
                    xs, ys,
                    c=colour, label=reg.capitalize(),
                    s=36, alpha=0.8, edgecolors='white', linewidths=0.4,
                    zorder=2,
                )

            ax.set_xlim(lo, hi)
            ax.set_ylim(lo, hi)
            ax.set_aspect('equal', adjustable='box')
            ax.set_title(_pretty_model_name(model_name), fontsize=11)

            if col_idx == 0:
                ax.set_ylabel('v (LLM)', fontsize=10)
            ax.set_xlabel('v (mannlegt / human)', fontsize=10)
            ax.tick_params(labelsize=9)

        # Sameiginlegur titill og skýring / shared title and legend
        fig_title = f"{dim['name']} ({dim['label']})"
        fig.suptitle(fig_title, fontsize=13, fontweight='bold', y=1.02)

        # Einn legend fyrir alla — setja undir / shared legend below
        handles, labels = axes[0, 0].get_legend_handles_labels()
        if handles:
            fig.legend(
                handles, labels,
                loc='lower center',
                ncol=len(registers_in_data),
                fontsize=9,
                frameon=False,
                bbox_to_anchor=(0.5, -0.04),
            )

        fig.tight_layout()
        out_path = figure_dir / f"scatter_{dim_id}.png"
        fig.savefig(out_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"  Vistað: {out_path}")

    # ==========================================================
    # MYND 2: B-gildi súlurit / B-score grouped bar chart
    # ==========================================================

    if not B_values:
        return

    # Finna textategundir sem eru til í B_values
    b_registers = sorted(
        {reg for mv in B_values.values() for reg in mv}
    )
    b_models = sorted(B_values)
    n_reg = len(b_registers)
    n_mod = len(b_models)

    if n_mod == 0 or n_reg == 0:
        return

    import numpy as np
    x = np.arange(n_mod)
    bar_width = 0.8 / n_reg

    fig, ax = plt.subplots(figsize=(max(6, 2 * n_mod), 5))

    for i, reg in enumerate(b_registers):
        vals = []
        for model_name in b_models:
            b = B_values[model_name].get(reg, 0.0)
            # Takmarka inf gildi við sýnilegt hámark / cap inf for display
            vals.append(b if not math.isinf(b) else float('nan'))
        colour = REGISTER_COLOURS.get(reg, _DEFAULT_COLOUR)
        offset = (i - n_reg / 2 + 0.5) * bar_width
        ax.bar(
            x + offset, vals, bar_width,
            label=reg.capitalize(), color=colour,
            edgecolor='white', linewidth=0.5,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(
        [_pretty_model_name(m) for m in b_models],
        fontsize=10,
    )
    ax.set_ylabel('B-gildi (heildarskor / aggregate score)', fontsize=10)
    ax.set_title(
        'Milička B-gildi per líkan og textategund',
        fontsize=12, fontweight='bold',
    )

    # Viðmiðslínur / reference lines
    ax.axhline(y=1, ls=':', color='#888888', lw=0.8, label='B = 1')
    ax.axhline(y=2, ls=':', color='#BBBBBB', lw=0.8, label='B = 2')

    ax.legend(fontsize=9, frameon=False)
    ax.tick_params(labelsize=9)
    fig.tight_layout()

    out_path = figure_dir / "B_scores.png"
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Vistað: {out_path}")


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

  # Keyra og búa til myndir:
  python scripts/run_milicka.py --plot

  # Keyra allt — CSV og myndir í sérstaka möppu:
  python scripts/run_milicka.py --output-csv output/milicka_results.csv --plot --figure-dir output/figures
        """
    )
    parser.add_argument(
        '--output-csv',
        type=Path,
        default=None,
        help="Slóð á CSV-skrá til að vista nákvæmar niðurstöður "
             "(ein lína per líkan × textategund × úrtak × vídd)."
    )
    parser.add_argument(
        '--plot',
        action='store_true',
        default=False,
        help="Búa til Milička-stíls dreifirit og B-gildi súlurit "
             "(krefst matplotlib)."
    )
    parser.add_argument(
        '--figure-dir',
        type=Path,
        default=None,
        help="Mappa til að vista myndir (sjálfgefið: output/figures/)."
    )

    args = parser.parse_args()
    run_benchmark(
        output_csv=args.output_csv,
        plot=args.plot,
        figure_dir=args.figure_dir,
    )


if __name__ == "__main__":
    main()
