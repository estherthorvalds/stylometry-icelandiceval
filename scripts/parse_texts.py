#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
parse_texts.py — SKREF 1: Þáttar alla texta með IceConParse
=============================================================

TILGANGUR / PURPOSE:
    Þetta skrifta hleður IceConParse liðgerðarþáttarann (constituency parser)
    og þáttar alla texta í tilrauninni — mennska viðmiðstexta (prompt og
    reference) og LLM-framhöld.

    This script loads the IceConParse constituency parser and parses all
    experiment texts — human baselines (prompts and references) and
    LLM continuations.

HVERS VEGNA / WHY:
    Milička-formúlurnar þurfa liðgerðartré (constituency parse trees) til að
    mæla setningagerð. Þáttarinn er dýr í keyrslu (~20 sek uppsetning +
    mínútur per skrá), svo við keyrum hann EINU SINNI og vistum niðurstöðurnar.

    Milička's formulas need constituency parse trees to measure sentence structure.
    The parser is expensive to run, so we run it ONCE and save the results.

ÞRJÁR UPPSPRETTUR / THREE SOURCES:

    1. PROMPT-TEXTAR (fyrri helmingur mannlegra texta):
       Slóð: data/experiment/prompts/
       Skrár: academic_prompt_001.txt, blog_prompt_001.txt, news_prompt_001.txt, ...
       MIKILVÆGT: Hver skrá byrjar á leiðbeiningarlínu:
           "Haltu áfram með textann á sama hátt og í sama stíl og sjáðu til
            þess að hann innihaldi að minnsta kosti tvö þúsund orð. Textinn
            þarf ekki að innihalda réttar staðreyndir en gættu þess að hann
            passi við stílinn:"
       Þessi lína er FJARLÆGÐ áður en þáttun hefst — aðeins raunverulegur
       texti er þáttaður.

    2. VIÐMIÐSTEXTAR (seinni helmingur mannlegra texta):
       Slóð: data/experiment/human_reference/
       Skrár: academic_ref_001.txt, blog_ref_001.txt, news_ref_001.txt, ...
       Þáttað eins og er, engin forvinnsla þörf.

    3. LLM-FRAMHÖLD (forunnin):
       Slóð: data/experiment/llm_continuations_preprocessed/
       Undirmöppur per líkan: gemini_3_thinking/, gpt_5/, le_chat_fast/,
       le_chat_thinking/ — hvert með academic/, blog/, news/.
       Þáttað eins og er — preprocess_llm_output.py hefur þegar hreinsað
       markdown, metaumfjöllun og endurtekningar.

ÚTTAK / OUTPUT:
    output/parsed/
    ├── prompts/                              # Þáttuð prompt-gögn
    │   ├── academic_prompt_001_parsed.psd
    │   ├── blog_prompt_001_parsed.psd
    │   └── ...
    ├── human_reference/                      # Þáttuð viðmiðsgögn
    │   ├── academic_ref_001_parsed.psd
    │   ├── blog_ref_001_parsed.psd
    │   └── ...
    └── llm_continuations_preprocessed/       # Þáttuð LLM-framhöld
        ├── gemini_3_thinking/
        │   ├── academic/
        │   │   └── gemini_academic_prompt_010_parsed.psd
        │   ├── blog/
        │   └── news/
        ├── gpt_5/...
        ├── le_chat_fast/...
        └── le_chat_thinking/...

    Hvert tré er ein lína í .psd skrá. Stjörnur (*) í þáttunartréum eru
    skiptar út fyrir bandstrik (-) til samræmis við IcePaHC-skemað.

ÞÁTTARI / PARSER:
    IceConParse eftir Ingunn Jóhönnu Kristjánsdóttur (2024)
    - Stanza-þáttunarpípa með IceBERT orðgreypingum
    - Þjálfað á IcePaHC trjábankanum
    - F-mæling: 90,38%

KEYRSLA / USAGE:
    # Þátta öll tilraunagögn (sjálfgefið):
    python scripts/parse_texts.py

    # Þátta aðeins ákveðna möppu:
    python scripts/parse_texts.py --input-dirs data/experiment/human_reference

    # Nota annað líkan:
    python scripts/parse_texts.py --model-path models/is_icepahc_transformer_finetuned_constituency.pt
"""

import argparse
import re
import sys
from pathlib import Path

# We need stanza for the IceConParse parser pipeline.
# stanza is a neural NLP library from Stanford that IceConParse builds on.
import stanza


# ============================================================
# SJÁLFGEFNAR SLÓÐIR / DEFAULT PATHS
# Þessar slóðir miðast við að skriftið sé keyrt úr rótarmöppu
# verkefnisins (stylometry-icelandiceval/).
# ============================================================

# Rótarmappa verkefnisins — fundin sjálfkrafa út frá staðsetningu þessa skrifts.
# __file__ er slóðin á þetta Python-skrifta, .resolve() gerir hana fulla (absolute),
# og .parent.parent fer tvo möppuþrep upp (scripts/ → verkefnisrót).
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Slóð á IceConParse-líkanið (constituency parser model).
# Þetta er Stanza-líkan sem Ingunn Jóhanna Kristjánsdóttir þjálfaði á IcePaHC.
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "is_icepahc_transformer_finetuned_constituency.pt"

# Inntak: þrjár möppur sem innihalda textaskrár til þáttunar.
#
# 1. prompts/ — fyrri helmingur mannlegra texta (notaður sem human baseline).
#    MIKILVÆGT: Leiðbeiningarlína fremst í hverri skrá er fjarlægð fyrir þáttun.
#
# 2. human_reference/ — seinni helmingur mannlegra texta (viðmið).
#    Þáttað eins og er.
#
# 3. llm_continuations_preprocessed/ — LLM-framhöld eftir forvinnslu.
#    Hvert líkan í sinni undirmöppu (gemini_3_thinking/, gpt_5/, o.s.frv.),
#    með academic/, blog/, news/ undir hverju.
DEFAULT_INPUT_DIRS = [
    PROJECT_ROOT / "data" / "experiment" / "prompts",
    PROJECT_ROOT / "data" / "experiment" / "human_reference",
    PROJECT_ROOT / "data" / "experiment" / "llm_continuations_preprocessed",
]

# Úttak: rótarmappa þar sem þáttuð tré verða vistuð.
# Möppustrúktúr inntaksins er varðveittur undir þessari rót.
# Dæmi: data/experiment/prompts/academic_prompt_001.txt
#      → output/parsed/prompts/academic_prompt_001_parsed.psd
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output" / "parsed"

# Möppur sem á að hundsá (sleppa) við endurkvæma leit.
# „excluded" inniheldur skrár sem voru fjarlægðar úr tilrauninni
# (t.d. LLM-framhöld sem voru of mikil endurtekning á prompt-texta).
EXCLUDED_DIR_NAMES = {'excluded'}

# ============================================================
# LEIÐBEININGARLÍNA Í PROMPTSKRÁM / PROMPT INSTRUCTION LINE
# ============================================================
# prepare_paired_experiment.py setur þessa föstu leiðbeiningu
# fremst í hverja promptskrá. Hún er EKKI hluti af mannlega
# textanum og VERÐUR að vera fjarlægð áður en þáttun hefst,
# annars fær þáttarinn setningu sem er ekki hluti textans.
#
# Leiðbeiningin er alltaf EIN lína, fylgt af tómri línu, og
# síðan kemur raunverulegur texti.
# ============================================================
PROMPT_INSTRUCTION = (
    "Haltu áfram með textann á sama hátt og í sama stíl og sjáðu til þess "
    "að hann innihaldi að minnsta kosti tvö þúsund orð. Textinn þarf ekki "
    "að innihalda réttar staðreyndir en gættu þess að hann passi við stílinn:"
)


# ============================================================
# HLAÐA ÞÁTTARA / LOAD PARSER
# IceConParse notar Stanza-pípu (pipeline) með þremur þáttum:
#   1. tokenize — skipta texta í setningar og orð
#   2. pos — orðflokkamerkja (part-of-speech tagging)
#   3. constituency — liðgerðarþáttun (constituency parsing)
# Uppsetning tekur ~20 sekúndur vegna IceBERT-líkansins,
# en eftir það er þáttun hverrar setningar hröð.
# ============================================================

def load_parser(model_path: Path) -> stanza.Pipeline:
    """Hlaða Stanza-þáttunarpípunni með íslenska liðgerðarþáttaranum.

    Args:
        model_path: Slóð á .pt líkansskrá IceConParse.

    Returns:
        stanza.Pipeline tilbúin til þáttunar.

    Raises:
        FileNotFoundError: Ef líkansskráin finnst ekki.
    """
    # Athuga hvort líkansskráin sé til áður en við reynum að hlaða henni.
    # Þetta gefur skýrari villuboð en Stanza sjálft myndi gefa.
    if not model_path.exists():
        raise FileNotFoundError(
            f"IceConParse-líkan fannst ekki: {model_path}\n"
            f"Sæktu líkanið og settu það í models/ möppuna."
        )

    print(f"Hleð þáttara frá {model_path.name} ...")

    # Búa til Stanza-þáttunarpípu.
    # lang='is' segir Stanza að nota íslenskt tungumálalíkan.
    # processors='tokenize,pos,constituency' segir hvaða þáttunarlyklum á að beita.
    # constituency_model_path bendir á sérsniðið þáttunarlíkan (IceConParse).
    nlp = stanza.Pipeline(
        lang='is',
        processors='tokenize,pos,constituency',
        constituency_model_path=str(model_path),
    )

    print("Þáttari tilbúinn.\n")
    return nlp


# ============================================================
# LESA TEXTA ÚR SKRÁ / READ TEXT FROM FILE
# Textaskrárnar geta verið á ýmsu sniði:
#   - Ein löng lína (~1.000 orð á einni línu) — algengast í human_reference/
#   - Margar línur (ein setning per línu, eða málsgreinar) — algengast í LLM-úttaki
# Stanza sér um setningarskiptingu (sentence segmentation) svo
# við lesum allan texta sem einn streng og látum Stanza skipta.
# ============================================================

def load_text(path: Path, strip_prompt_instruction: bool = False) -> str:
    """Lesa allan texta úr skrá sem einn streng.

    Stanza sér sjálft um setningarskiptingu (tokenize processor),
    svo inntak þarf EKKI að vera ein setning per línu.

    Args:
        path: Slóð á textaskrá (.txt).
        strip_prompt_instruction: Ef True, fjarlægja leiðbeiningarlínu
            fremst í skránni (notað fyrir promptskrár). Leiðbeiningin
            er ekki hluti af mannlega textanum og á ekki að þáttast.

    Returns:
        Strengur með textainnihaldi skráarinnar (styttur á endum).

    Raises:
        FileNotFoundError: Ef textaskráin finnst ekki.
    """
    if not path.exists():
        raise FileNotFoundError(f"Textaskrá fannst ekki: {path}")

    # encoding='utf-8' er mikilvægt fyrir íslensku — sértákn eins og
    # þ, ð, æ, ö þurfa UTF-8 umritun til að lesast rétt.
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    # --- FJARLÆGJA LEIÐBEININGARLÍNU ÚR PROMPTSKRÁM ---
    # Promptskrár byrja á fastri leiðbeiningarlínu frá
    # prepare_paired_experiment.py. Þessi lína á EKKI að þáttast —
    # hún er skipun til LLM-líkansins, ekki hluti af mannlega textanum.
    #
    # Snið skráarinnar:
    #   <leiðbeiningarlína>\n\n<raunverulegur texti>
    #
    # Við leitum að leiðbeiningunni og fjarlægjum hana ásamt tómu línunni
    # á eftir. Ef leiðbeiningin finnst ekki (óvænt snið) er viðvörun
    # prentuð og allur textinn notaður.
    if strip_prompt_instruction:
        if text.startswith(PROMPT_INSTRUCTION):
            text = text[len(PROMPT_INSTRUCTION):].lstrip()
        else:
            print(f"  AÐVÖRUN: Leiðbeiningarlína fannst ekki fremst í "
                  f"{path.name} — þátta allan texta")

    return text


# ============================================================
# ÞÁTTA TEXTA / PARSE TEXT
# Gefur Stanza ALLAN texta skráarinnar í einu. Stanza skiptir
# textanum í setningar (tokenize) og þáttar hverja setningu
# (constituency). Við söfnum öllum þáttunartréum.
#
# ELDRA VANDAMÁL (LEIÐRÉTT):
#   Áður var gert ráð fyrir að inntak væri ein setning per línu
#   og aðeins doc.sentences[0] var notað. Þetta þýddi að ef
#   allur textinn var á einni línu (~2.000 orð) var aðeins
#   FYRSTA setningin þáttuð og allar hinar glataðar.
#   Nú er allur textinn gefinn Stanza og ALLAR setningar notaðar.
#
# Stjörnur (*) eru skiptar út fyrir bandstrik (-) vegna þess
# að IcePaHC-skemað notar bandstrik í lyklum (t.d. NP-SBJ).
# ============================================================

def parse_text(nlp: stanza.Pipeline, text: str) -> list[str]:
    """Þátta texta og skila liðgerðartréum sem strengjum.

    Stanza sér um setningarskiptingu — textinn þarf EKKI að vera
    forskiptur í setningar. Hvert tré verður ein lína í úttaksskránni.
    Stjörnur (*) eru skiptar út fyrir bandstrik (-) til samræmis
    við IcePaHC-merkingaskemað.

    Args:
        nlp: Stanza-þáttunarpípa (úttakið úr load_parser).
        text: Allur texti skráarinnar sem einn strengur.

    Returns:
        Listi af strengjum — hvert tré er einn strengur í svigaformi,
        t.d. "(ROOT (IP-MAT (NP-SBJ (NPR-N KPMG)) (VBPI opnar) ...))".
    """
    # Stanza.Pipeline tekur streng og skilar Doc hlut.
    # doc.sentences er listi af ÖLLUM setningum sem Stanza greindi
    # — Stanza skiptir textanum sjálft í setningar.
    doc = nlp(text)

    trees = []
    n_sentences = len(doc.sentences)

    for idx, sentence in enumerate(doc.sentences):
        # sentence.constituency er Tree hlutur.
        # str() breytir honum í svigastreng (bracketed string).
        tree_str = str(sentence.constituency)

        # Skipta stjörnum (*) út fyrir bandstrik (-).
        # Þáttarinn notar stundum stjörnur í merkingarlyklum (t.d. NP-SBJ*),
        # en það getur ruglað saman við aðra reikninga okkar.
        tree_str = tree_str.replace('*', '-')

        trees.append(tree_str)

        # Sýna framvindu á hverri 50. setningu svo notandinn sjái
        # að þáttunin gangi sem skyldi og sé ekki föst.
        if (idx + 1) % 50 == 0:
            print(f"  Þáttað {idx + 1}/{n_sentences} setningar...")

    return trees


# ============================================================
# VISTA ÞÁTTUÐ TRÉ Í SKRÁ / SAVE PARSED TREES TO FILE
# Hvert tré er ein lína. Þetta er einfalt snið sem önnur
# skriftu (dim1, dim2, dim3, ...) geta lesið auðveldlega.
# Skráarendingin er .psd (parsed) til aðgreiningar frá .txt.
# ============================================================

def save_trees(trees: list[str], output_path: Path) -> None:
    """Vista lista af þáttunartréum í skrá (eitt tré per línu).

    Args:
        trees: Listi af strengjum — hvert tré í svigaformi.
        output_path: Slóð á úttaksskrá (.psd).
    """
    # Búa til möppukeðjuna ef hún er ekki til.
    # parents=True býr til allar yfirmöppur, exist_ok=True kvartar ekki
    # ef mappan er nú þegar til.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        for tree in trees:
            f.write(tree + '\n')

    print(f"  Vistað: {output_path} ({len(trees)} tré)")


# ============================================================
# FINNA ALLAR TEXTASKRÁR / FIND ALL TEXT FILES
# Finnur .txt skrár ENDURKVÆMT (recursive) í inntaksmöppu.
# Hundsár möppur sem heita „excluded".
# ============================================================

def find_text_files(input_dir: Path) -> list[Path]:
    """Finna allar .txt skrár í möppu og undirmöppum hennar.

    Sleppur möppum sem heita „excluded" (sjá EXCLUDED_DIR_NAMES).
    Raðar skrám í stafrófsröð til endurtekjanlegrar keyrslu.

    Args:
        input_dir: Rótarmappa til að leita í.

    Returns:
        Raðaður listi af Path-hlutum.
    """
    if not input_dir.exists():
        print(f"AÐVÖRUN: Inntaksmappa finnst ekki: {input_dir}")
        return []

    # rglob('*.txt') finnur allar .txt skrár endurkvæmt (recursive).
    # Síðan sláum við út allar skrár sem eru í „excluded" möppum.
    txt_files = []
    for f in input_dir.rglob('*.txt'):
        # Athuga hvort einhver hluti af slóðinni sé í EXCLUDED_DIR_NAMES.
        # Dæmi: le_chat_fast/excluded/foo.txt → „excluded" er í parts → sleppa.
        if any(part in EXCLUDED_DIR_NAMES for part in f.relative_to(input_dir).parts):
            continue
        txt_files.append(f)

    return sorted(txt_files)


# ============================================================
# REIKNA ÚTTAKSSLÓÐ / COMPUTE OUTPUT PATH
# Varðveitir möppustrúktúr: inntak-slóðin hlutfallslega við
# inntaksmöppuna er notuð sem undirmappa í úttakinu.
#
# Dæmi:
#   input_dir  = data/experiment/llm_continuations_preprocessed
#   txt_file   = data/experiment/llm_continuations_preprocessed/gpt_5/news/foo.txt
#   output_dir = output/parsed
#   → output/parsed/llm_continuations_preprocessed/gpt_5/news/foo_parsed.psd
#
#   input_dir  = data/experiment/prompts
#   txt_file   = data/experiment/prompts/academic_prompt_001.txt
#   output_dir = output/parsed
#   → output/parsed/prompts/academic_prompt_001_parsed.psd
# ============================================================

def compute_output_path(
    txt_file: Path,
    input_dir: Path,
    output_dir: Path,
) -> Path:
    """Reikna úttaksslóð sem varðveitir möppustrúktúr.

    Args:
        txt_file: Slóð á inntaksskrá.
        input_dir: Rótarmappa inntaksins (notað til að reikna hlutfallslega slóð).
        output_dir: Rótarmappa úttaksins.

    Returns:
        Slóð á úttaksskrá (.psd), t.d.
        output/parsed/prompts/academic_prompt_001_parsed.psd
    """
    # Hlutfallsleg slóð: t.d. academic_prompt_001.txt (frá input_dir)
    # eða gpt_5/news/gpt5_news_prompt_001.txt
    relative = txt_file.relative_to(input_dir)

    # Úttaksskráarheiti: foo.txt → foo_parsed.psd
    output_name = f"{txt_file.stem}_parsed.psd"

    # Sameina: output_dir / nafn rótarmöppu / möppuskipulag / nýtt skráarheiti
    # input_dir.name er nafn rótarmöppunnar (t.d. prompts, human_reference,
    # llm_continuations_preprocessed)
    # relative.parent er möppuhlutinn (t.d. . eða gpt_5/news/)
    return output_dir / input_dir.name / relative.parent / output_name


# ============================================================
# ATHUGA HVORT MAPPA ER PROMPTMAPPA / CHECK IF DIR IS PROMPTS
# Promptmöppan þarf sérstaka meðhöndlun: leiðbeiningarlína
# fremst í hverri skrá er fjarlægð áður en þáttun hefst.
# ============================================================

def is_prompt_dir(input_dir: Path) -> bool:
    """Athuga hvort inntaksmappa sé promptmappa sem þarfnast strippingar.

    Promptmappan heitir „prompts" og inniheldur skrár sem byrja á
    leiðbeiningarlínu frá prepare_paired_experiment.py.

    Args:
        input_dir: Rótarmappa inntaksins.

    Returns:
        True ef þetta er promptmappan.
    """
    return input_dir.name == "prompts"


# ============================================================
# ÞÁTTA ALLAR SKRÁR Í MÖPPU / PARSE ALL FILES IN DIRECTORY
# Fer endurkvæmt í gegnum allar .txt skrár í inntaksmöppu
# og undirmöppum, þáttar þær, og vistar niðurstöðurnar
# í úttaksmöppu með varðveittum möppustrúktúr.
# ============================================================

def parse_directory(
    nlp: stanza.Pipeline,
    input_dir: Path,
    output_dir: Path,
) -> int:
    """Þátta allar .txt skrár í möppu (endurkvæmt) og vista niðurstöður.

    Varðveitir möppustrúktúr í úttaki:
        input_dir/sub/foo.txt → output_dir/input_dir.name/sub/foo_parsed.psd

    Sleppur skrám sem þegar eru þáttaðar (úttaksskrá til staðar).

    Ef input_dir er promptmappan (heitir „prompts"), er leiðbeiningarlína
    fjarlægð úr hverri skrá áður en þáttun hefst.

    Args:
        nlp: Stanza-þáttunarpípa.
        input_dir: Mappa með .txt skrám til þáttunar (leitað endurkvæmt).
        output_dir: Rótarmappa þar sem þáttuð tré verða vistuð.

    Returns:
        Fjöldi skráa sem voru þáttaðar.
    """
    txt_files = find_text_files(input_dir)

    if not txt_files:
        print(f"AÐVÖRUN: Engar .txt skrár fundust í {input_dir}")
        return 0

    # Athuga hvort þetta er promptmappan — ef svo, þarf að fjarlægja
    # leiðbeiningarlínu úr skránum áður en þáttun hefst.
    strip_instruction = is_prompt_dir(input_dir)

    if strip_instruction:
        print(f"\nFann {len(txt_files)} promptskrár í {input_dir.name}/")
        print("  (leiðbeiningarlína verður fjarlægð úr hverri skrá)")
    else:
        print(f"\nFann {len(txt_files)} textaskrár í {input_dir.name}/")
    print("=" * 60)

    n_parsed = 0
    n_skipped = 0

    for txt_file in txt_files:
        # Reikna úttaksslóð
        output_path = compute_output_path(txt_file, input_dir, output_dir)

        # Sleppa ef þáttuð skrá er þegar til (til að geta endurræst eftir bilun)
        if output_path.exists():
            n_skipped += 1
            continue

        # Sýna hlutfallslega slóð til styttingar
        rel_path = txt_file.relative_to(input_dir)
        print(f"\nÞátta: {rel_path}")

        # Lesa texta úr skránni.
        # Ef þetta er promptskrá, er leiðbeiningarlína fjarlægð sjálfkrafa.
        text = load_text(txt_file, strip_prompt_instruction=strip_instruction)

        if not text:
            print(f"  AÐVÖRUN: Tóm skrá, sleppi")
            continue

        # Þátta texta — Stanza skiptir sjálft í setningar
        trees = parse_text(nlp, text)
        print(f"  {len(trees)} setningar þáttaðar")

        # Vista þáttuð tré
        save_trees(trees, output_path)
        n_parsed += 1

    if n_skipped > 0:
        print(f"\n  Sleppt {n_skipped} skrám (þegar þáttaðar)")
    print(f"  Þáttað {n_parsed} nýjar skrár")

    return n_parsed


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# argparse gerir okkur kleift að breyta stillingum án þess
# að breyta kóðanum sjálfum.
# ============================================================

def parse_args() -> argparse.Namespace:
    """Lesa skipanalínubreytur (command-line arguments).

    Returns:
        argparse.Namespace með öllum stillingum.
    """
    parser = argparse.ArgumentParser(
        description="Þátta texta með IceConParse og vista liðgerðartré.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi um keyrslu:
  # Þátta öll tilraunagögn (sjálfgefið: prompts, human_reference,
  # llm_continuations_preprocessed):
  python scripts/parse_texts.py

  # Þátta aðeins ákveðnar möppur:
  python scripts/parse_texts.py --input-dirs data/experiment/human_reference

  # Þátta fleiri en eina möppu:
  python scripts/parse_texts.py --input-dirs data/experiment/prompts data/experiment/human_reference

  # Nota annað líkan eða aðra úttaksmöppu:
  python scripts/parse_texts.py --model-path models/other.pt --output-dir output/parsed_v2
        """
    )

    parser.add_argument(
        '--model-path',
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help=f"Slóð á IceConParse .pt líkan (sjálfgefið: {DEFAULT_MODEL_PATH.relative_to(PROJECT_ROOT)})"
    )
    parser.add_argument(
        '--input-dirs',
        type=Path,
        nargs='+',
        default=None,
        help="Ein eða fleiri möppur með textaskrám til þáttunar. "
             "Leitað er endurkvæmt í undirmöppum. "
             "Sjálfgefið: prompts, human_reference, llm_continuations_preprocessed."
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Rótarmappa fyrir þáttuð tré (sjálfgefið: {DEFAULT_OUTPUT_DIR.relative_to(PROJECT_ROOT)})"
    )

    return parser.parse_args()


# ============================================================
# MAIN — AÐALFLÆÐI / MAIN FLOW
# 1. Hlaða þáttara
# 2. Þátta allar inntaksmöppur (endurkvæmt)
# ============================================================

def main() -> None:
    """Aðalfall: Hlaða þáttara og þátta öll tilraunagögn."""
    args = parse_args()

    # Nota sjálfgefnar möppur ef engar voru tilgreindar
    input_dirs = args.input_dirs if args.input_dirs else DEFAULT_INPUT_DIRS

    # --- SKREF 1: Hlaða þáttara ---
    nlp = load_parser(args.model_path)

    # --- SKREF 2: Þátta allar möppur ---
    total_parsed = 0
    for input_dir in input_dirs:
        # Sýna hlutfallslega slóð ef mögulegt, annars fulla slóð
        try:
            display_path = input_dir.relative_to(PROJECT_ROOT)
        except ValueError:
            display_path = input_dir

        print("\n" + "=" * 60)
        print(f"ÞÁTTUN: {display_path}")
        print("=" * 60)
        n = parse_directory(nlp, input_dir, args.output_dir)
        total_parsed += n

    print("\n" + "=" * 60)
    print(f"ÖLLUM ÞÁTTUN LOKIÐ — {total_parsed} skrár þáttaðar samtals")
    print("=" * 60)


if __name__ == "__main__":
    main()
