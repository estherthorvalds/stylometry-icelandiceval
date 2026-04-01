#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
parse_texts.py — SKREF 1: Þáttar alla texta með IceConParse
=============================================================

TILGANGUR / PURPOSE:
    Þetta skrifta hleður IceConParse liðgerðarþáttarann (constituency parser)
    og þáttar alla texta — bæði mannlega og LLM-framleidda.

    This script loads the IceConParse constituency parser and parses all texts
    — both human and LLM-generated.

HVERS VEGNA / WHY:
    Milička-formúlurnar þurfa liðgerðartré (constituency parse trees) til að
    mæla setningagerð. Þáttarinn er dýr í keyrslu (~20 sek uppsetning +
    mínútur per skrá), svo við keyrum hann EINU SINNI og vistum niðurstöðurnar.

    Milička's formulas need constituency parse trees to measure sentence structure.
    The parser is expensive to run, so we run it ONCE and save the results.

INNTAK / INPUT:
    - data/human_texts/*.txt  — mannlegir textar, ein setning per línu
    - data/llm_texts/*.txt    — LLM-framleiddir textar, sama snið

ÚTTAK / OUTPUT:
    - data/parsed/human/*_parsed.txt  — eitt þáttunartré per línu
    - data/parsed/llm/*_parsed.txt    — eitt þáttunartré per línu
    Stjörnur (*) í þáttunartréum eru skiptar út fyrir bandstrik (-) til að
    forðast ruggling í lyklum IcePaHC-skemans.

ÞÁTTARI / PARSER:
    IceConParse eftir Ingunn Jóhönnu Kristjánsdóttur (2024)
    - Stanza-þáttunarpípa með IceBERT orðgreypingum
    - Þjálfað á IcePaHC trjábankanum
    - F-mæling: 90,38%

KEYRSLA / USAGE:
    python scripts/parse_texts.py
    python scripts/parse_texts.py --model-path models/is_icepahc_transformer_finetuned_constituency.pt
    python scripts/parse_texts.py --human-dir data/human_texts --llm-dir data/llm_texts
"""

import argparse
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

# Inntak: möppur með hreinum textaskrám (ein setning per línu)
DEFAULT_HUMAN_DIR = PROJECT_ROOT / "data" / "human_texts"
DEFAULT_LLM_DIR = PROJECT_ROOT / "data" / "llm_texts"

# Úttak: möppur þar sem þáttuð tré verða vistuð
DEFAULT_PARSED_HUMAN_DIR = PROJECT_ROOT / "data" / "parsed" / "human"
DEFAULT_PARSED_LLM_DIR = PROJECT_ROOT / "data" / "parsed" / "llm"


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
# LESA SETNINGAR ÚR TEXTASKRÁ / READ SENTENCES FROM TEXT FILE
# Hvert inntak er textaskrá þar sem ein setning er á hverri línu.
# Tómar línur eru hundsaðar.
# ============================================================

def load_sentences(path: Path) -> list[str]:
    """Lesa setningar úr textaskrá. Ein setning per línu.

    Args:
        path: Slóð á textaskrá (.txt) með einni setningu per línu.

    Returns:
        Listi af strengjum (setningar). Tómar línur eru undanskildar.

    Raises:
        FileNotFoundError: Ef textaskráin finnst ekki.
    """
    if not path.exists():
        raise FileNotFoundError(f"Textaskrá fannst ekki: {path}")

    # encoding='utf-8' er mikilvægt fyrir íslensku — sértákn eins og
    # þ, ð, æ, ö þurfa UTF-8 umritun til að lesast rétt.
    with open(path, 'r', encoding='utf-8') as f:
        # line.strip() fjarlægir bil og línuskipti frá byrjun og enda línunnar.
        # Skilyrðið `if line.strip()` útilokar tómar línur.
        sentences = [line.strip() for line in f if line.strip()]

    return sentences


# ============================================================
# ÞÁTTA SETNINGAR / PARSE SENTENCES
# Þessi fall tekur lista af setningum og skilar lista af
# þáttunartréum (constituency trees) sem strengjum.
# Stjörnur (*) eru skiptar út fyrir bandstrik (-) vegna þess
# að IcePaHC-skemað notar bandstrik í lyklum (t.d. NP-SBJ).
# ============================================================

def parse_sentences(nlp: stanza.Pipeline, sentences: list[str]) -> list[str]:
    """Þátta lista af setningum og skila liðgerðartréum sem strengjum.

    Hvert tré verður ein lína í úttaksskránni.
    Stjörnur (*) eru skiptar út fyrir bandstrik (-) til samræmis
    við IcePaHC-merkingaskemað.

    Args:
        nlp: Stanza-þáttunarpípa (úttakið úr load_parser).
        sentences: Listi af setningum til að þátta.

    Returns:
        Listi af strengjum — hvert tré er einn strengur í svigaformi,
        t.d. "(ROOT (IP-MAT (NP-SBJ (NPR-N KPMG)) (VBPI opnar) ...))".
    """
    trees = []

    for idx, sentence in enumerate(sentences):
        # Stanza.Pipeline tekur streng og skilar Doc hlut.
        # doc.sentences er listi af setningum sem Stanza greindi —
        # við notum fyrstu setninguna (index 0) vegna þess að inntak
        # okkar er ein setning í einu.
        doc = nlp(sentence)

        # doc.sentences[0].constituency er Tree hlutur.
        # str() breytir honum í svigastreng (bracketed string).
        tree_str = str(doc.sentences[0].constituency)

        # Skipta stjörnum (*) út fyrir bandstrik (-).
        # Þáttarinn notar stundum stjörnur í merkingarlyklum (t.d. NP-SBJ*),
        # en það getur ruglað saman við aðra reikninga okkar.
        tree_str = tree_str.replace('*', '-')

        trees.append(tree_str)

        # Sýna framvindu á hverri 50. setningu svo notandinn sjái
        # að þáttunin gangi sem skyldi og sé ekki föst.
        if (idx + 1) % 50 == 0:
            print(f"  Þáttað {idx + 1}/{len(sentences)} setningar...")

    return trees


# ============================================================
# VISTA ÞÁTTUÐ TRÉ Í SKRÁ / SAVE PARSED TREES TO FILE
# Hvert tré er ein lína. Þetta er einfalt snið sem önnur
# skriftu (dim1, dim2, dim3) geta lesið auðveldlega.
# ============================================================

def save_trees(trees: list[str], output_path: Path) -> None:
    """Vista lista af þáttunartréum í textaskrá (eitt tré per línu).

    Args:
        trees: Listi af strengjum — hvert tré í svigaformi.
        output_path: Slóð á úttaksskrá (.txt).
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
# ÞÁTTA ALLAR SKRÁR Í MÖPPU / PARSE ALL FILES IN DIRECTORY
# Fer í gegnum allar .txt skrár í inntaksmöppu, þáttar þær,
# og vistar niðurstöðurnar í úttaksmöppu.
# ============================================================

def parse_directory(nlp: stanza.Pipeline, input_dir: Path, output_dir: Path) -> None:
    """Þátta allar .txt skrár í möppu og vista niðurstöður.

    Inntaksskrá:  input_dir/foo.txt
    Úttaksskrá:   output_dir/foo_parsed.txt

    Skráarheitið fær viðskeytið '_parsed' til að auðkenna þáttaðar skrár.

    Args:
        nlp: Stanza-þáttunarpípa.
        input_dir: Mappa með .txt skrám til þáttunar.
        output_dir: Mappa þar sem þáttuð tré verða vistuð.
    """
    if not input_dir.exists():
        print(f"AÐVÖRUN: Inntaksmappa finnst ekki: {input_dir}")
        return

    # sorted() raðar skráarnöfnum í stafrófsröð svo úttakið sé fyrirsjáanlegt.
    # .glob('*.txt') finnur allar .txt skrár í möppunni (ekki í undirmöppum).
    txt_files = sorted(input_dir.glob('*.txt'))

    if not txt_files:
        print(f"AÐVÖRUN: Engar .txt skrár fundust í {input_dir}")
        return

    print(f"\nFann {len(txt_files)} textaskrár í {input_dir.name}/")
    print("=" * 60)

    for txt_file in txt_files:
        print(f"\nÞátta: {txt_file.name}")

        # Lesa setningar úr skránni
        sentences = load_sentences(txt_file)
        print(f"  {len(sentences)} setningar")

        if not sentences:
            print(f"  AÐVÖRUN: Tóm skrá, sleppi")
            continue

        # Þátta allar setningar
        trees = parse_sentences(nlp, sentences)

        # Búa til úttaksskráarheiti: foo.txt → foo_parsed.txt
        # .stem er skráarheitið án endingar, t.d. "news_ruv"
        output_name = f"{txt_file.stem}_parsed.txt"
        output_path = output_dir / output_name

        # Vista þáttuð tré
        save_trees(trees, output_path)

    print("\nÞáttun lokið!")


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
  python scripts/parse_texts.py
  python scripts/parse_texts.py --model-path models/is_icepahc_transformer_finetuned_constituency.pt
  python scripts/parse_texts.py --human-dir data/human_texts --llm-dir data/llm_texts
        """
    )

    parser.add_argument(
        '--model-path',
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help=f"Slóð á IceConParse .pt líkan (sjálfgefið: {DEFAULT_MODEL_PATH})"
    )
    parser.add_argument(
        '--human-dir',
        type=Path,
        default=DEFAULT_HUMAN_DIR,
        help=f"Mappa með mannlegum textaskrám (sjálfgefið: {DEFAULT_HUMAN_DIR})"
    )
    parser.add_argument(
        '--llm-dir',
        type=Path,
        default=DEFAULT_LLM_DIR,
        help=f"Mappa með LLM-framleiddun textaskrám (sjálfgefið: {DEFAULT_LLM_DIR})"
    )
    parser.add_argument(
        '--parsed-human-dir',
        type=Path,
        default=DEFAULT_PARSED_HUMAN_DIR,
        help=f"Úttaksmappa fyrir þáttuð mannleg tré (sjálfgefið: {DEFAULT_PARSED_HUMAN_DIR})"
    )
    parser.add_argument(
        '--parsed-llm-dir',
        type=Path,
        default=DEFAULT_PARSED_LLM_DIR,
        help=f"Úttaksmappa fyrir þáttuð LLM tré (sjálfgefið: {DEFAULT_PARSED_LLM_DIR})"
    )

    return parser.parse_args()


# ============================================================
# MAIN — AÐALFLÆÐI / MAIN FLOW
# 1. Hlaða þáttara
# 2. Þátta mennsku gögnin
# 3. Þátta LLM gögnin
# ============================================================

def main() -> None:
    """Aðalfall: Hlaða þáttara og þátta öll gögn."""
    args = parse_args()

    # --- SKREF 1: Hlaða þáttara ---
    nlp = load_parser(args.model_path)

    # --- SKREF 2: Þátta mannlega texta ---
    print("\n" + "=" * 60)
    print("ÞÁTTUN MANNLEGRA TEXTA")
    print("=" * 60)
    parse_directory(nlp, args.human_dir, args.parsed_human_dir)

    # --- SKREF 3: Þátta LLM texta ---
    print("\n" + "=" * 60)
    print("ÞÁTTUN LLM TEXTA")
    print("=" * 60)
    parse_directory(nlp, args.llm_dir, args.parsed_llm_dir)

    print("\n" + "=" * 60)
    print("ÖLLUM ÞÁTTUN LOKIÐ")
    print("=" * 60)


if __name__ == "__main__":
    main()
