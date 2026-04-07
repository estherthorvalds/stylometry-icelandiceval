#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
preprocess_llm_output.py — Forvinnsla á LLM-útttökum til stílmælinga
=====================================================================

TILGANGUR / PURPOSE:
    Þetta skrifta hreinsar texta sem risamállíkön (LLMs) framleiddu, svo
    þeir fái NÁKVÆMLEGA sömu forvinnslu og mannlegu textarnir í
    extract_samples.py.

    This script cleans LLM-generated text continuations so they receive
    the EXACT SAME preprocessing treatment as the human texts from
    extract_samples.py.

HVERS VEGNA ÞETTA SKIPTIR MÁLI / WHY THIS MATTERS:
    Viðmiðið (benchmark) ber saman mannlegan texta við LLM-texta með
    þáttaratengdum mælingum. Ef mannlegur texti var hreinsaður (XML
    fjarlægt, punktur bættur við fyrirsagnir) en LLM-texti er ekki
    hreinsaður (enn með markdown-sniði, hausum o.s.frv.), myndum við
    mæla sniðsmun frekar en raunverulegan stílmun.

    SAMA FORVINNSLA = SANNGJARN SAMANBURÐUR.

FORVINNSLA SEM extract_samples.py BeitIR / PREPROCESSING FROM extract_samples.py:
    1. ensure_sentence_ending() — bætir punkti (.) við texta sem endar
       ekki á . ? !  (fyrirsagnir, stuttar línur)
    2. Hvítbilsnormun (whitespace normalization) — re.sub(r'\\s+', ' ')
       — sameinkar mörg bil í eitt
    3. Ekkert stafaumbrot eða kóðunarlagfæring umfram þetta
    4. Engin sérstök meðhöndlun á gæsalappir/tilvitnunarmerkjum

LLM-SÉRSTÖK HREINSUN / LLM-SPECIFIC CLEANING:
    Ofan á sömu forvinnslu og extract_samples.py framkvæmir, þurfum við
    einnig að fjarlægja LLM-sérstaka hluti:
    - Markdown-snið: # hausar, **feitletrað**, *skáletrað**, - bullets
    - Metaumfjöllun (meta-commentary): "Hér er framhaldið:", "Að lokum"
    - Lárétt strikin (---, ***)

ENDURTEKNINGARGREINING / REPETITION DETECTION:
    Sum LLM-líkön afrita orðrétt textabúta úr promptinu (fyrri helmingi
    mannlega textans) inn í framhaldið. Þetta blæs upp stílmælingar á
    tilbúinn hátt. Þegar --prompt-dir er gefið, leitar skriftan að 10+
    orða samfelldum runum úr promptinu sem birtast í framhaldinu og
    skrifar skýrslu (repetition_report.txt). Endurtekningar eru EKKI
    fjarlægðar sjálfkrafa — nemandinn ákveður per skrá.

KEYRSLA / USAGE:
    # Hreinsa öll LLM-úttök án endurtekningargreiningar
    python scripts/preprocess_llm_output.py \\
        --input-dir data/experiment/llm_continuations/ \\
        --output-dir data/experiment/llm_continuations_clean/

    # Með endurtekningargreiningu
    python scripts/preprocess_llm_output.py \\
        --input-dir data/experiment/llm_continuations/ \\
        --output-dir data/experiment/llm_continuations_clean/ \\
        --prompt-dir data/experiment/prompts/

    # Hreinsa eitt líkan
    python scripts/preprocess_llm_output.py \\
        --input-dir data/experiment/llm_continuations/gemini_3_thinking/ \\
        --output-dir data/experiment/llm_continuations_clean/gemini_3_thinking/
"""

import argparse
import re
import sys
from pathlib import Path


# ============================================================
# TRYGGJA SETNINGARENDAMERKI / ENSURE SENTENCE-FINAL PUNCTUATION
# SAMA fall og í extract_samples.py — endurnotum nákvæmlega sömu
# rökfræðina svo mannlegir og LLM-textar fái sömu meðhöndlun.
#
# Fyrirsagnir og undirfyrirsagnir enda oft ekki á punkti (. ? !).
# IceConParse reiknar með setningarendamerki, svo við bætum punkti
# við línur sem vantar hann.
# ============================================================

def ensure_sentence_ending(text: str) -> str:
    """Bæta punkti við texta sem endar ekki á setningarendamerki.

    Ef textinn endar á . ? eða ! gerum við ekkert.
    Annars bætum við punkti (.) við endann.

    NÁKVÆMLEGA sama rökfræði og í extract_samples.py — þetta tryggir
    að LLM-texti og mannlegur texti fái sömu meðhöndlun.

    Args:
        text: Textastrengur (setning, fyrirsögn, eða málsgrein).

    Returns:
        Textinn, mögulega með punkti bættum við enda.
    """
    stripped = text.rstrip()
    if stripped and stripped[-1] not in '.?!':
        return stripped + '.'
    return stripped


# ============================================================
# MARKDOWN-HREINSUN / MARKDOWN STRIPPING
# LLM-líkön framleiða oft markdown-snið í textanum sínum.
# Við þurfum að fjarlægja ALLT markdown en halda textanum.
#
# Mikilvægt: Við fjarlægjum aðeins sniðmerkingar, EKKI textann sjálfan.
# "## Niðurstöður" verður "Niðurstöður" (ekki eytt).
# "**mikilvægt**" verður "mikilvægt" (ekki eytt).
# ============================================================

def strip_markdown(text: str) -> tuple[str, dict[str, int]]:
    """Fjarlægja markdown-sniðmerkingar úr texta.

    Hreinsar:
    - Hausamerkingar (# ## ### o.s.frv.)
    - Feitletrað (**texti** eða __texti__)
    - Skáletrað (*texti* eða _texti_)
    - Punktalistar (- , * , + í upphafi línu)
    - Númeraðir listar (1. , 2. , o.s.frv.)
    - Lárétt strik (---, ***, ___)
    - Kóðamerki (`texti`)
    - Blokkartilvitnun (> í upphafi línu)

    Args:
        text: Hráður texti frá LLM.

    Returns:
        Tuple af (hreinsaður texti, tölfræði um hvað var fjarlægt).
        Tölfræðin er dict með lyklum eins og 'headings', 'bold', o.s.frv.
    """
    stats = {
        'headings': 0,       # Fjöldi hausa sem fjarlægðir voru
        'bold': 0,           # Fjöldi feitletraðra merkinga
        'italic': 0,         # Fjöldi skáletraðra merkinga
        'bullets': 0,        # Fjöldi punktalista
        'numbered_lists': 0, # Fjöldi númeraðra lista
        'horizontal_rules': 0,  # Fjöldi láréttra strika
        'blockquotes': 0,    # Fjöldi blokkartilvitnana
        'code_spans': 0,     # Fjöldi kóðamerkinga
    }

    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        original = line

        # --- LÁRÉTT STRIK / HORIZONTAL RULES ---
        # Línur sem eru AÐEINS --- eða *** eða ___ (3+ tákn).
        # Þessar línur eru ekki texti og eru eyddar alveg.
        if re.match(r'^\s*[-*_]{3,}\s*$', line):
            stats['horizontal_rules'] += 1
            continue  # Sleppa þessari línu alveg

        # --- BLOKKARTILVITNUN / BLOCKQUOTE ---
        # > í upphafi línu. Fjarlægja > en halda textanum.
        if re.match(r'^\s*>\s*', line):
            line = re.sub(r'^\s*>\s*', '', line)
            stats['blockquotes'] += 1

        # --- HAUSAR / HEADINGS ---
        # Eitt eða fleiri # í upphafi línu, fylgt af bili.
        # "## Niðurstöður" → "Niðurstöður"
        heading_match = re.match(r'^(#{1,6})\s+(.*)$', line)
        if heading_match:
            line = heading_match.group(2)
            stats['headings'] += 1

        # --- NÚMERAÐIR LISTAR / NUMBERED LISTS ---
        # "1. Texti" → "Texti", "12. Texti" → "Texti"
        # Athugasemd: Aðeins í upphafi línu til að forðast
        # rangt samsvörun í miðjum setningum (t.d. "þann 5. mars").
        numbered_match = re.match(r'^(\s*)\d+\.\s+(.*)$', line)
        if numbered_match:
            # Halda inndraginni ef einhver var
            indent = numbered_match.group(1)
            line = indent + numbered_match.group(2)
            stats['numbered_lists'] += 1

        # --- PUNKTALISTAR / BULLET POINTS ---
        # "- Texti" → "Texti", "* Texti" → "Texti", "+ Texti" → "Texti"
        # Athugasemd: * í upphafi línu fylgt af bili er bullet,
        # EKKI skáletrun (skáletrun er *texti*).
        bullet_match = re.match(r'^(\s*)[-*+]\s+(.*)$', line)
        if bullet_match:
            indent = bullet_match.group(1)
            line = indent + bullet_match.group(2)
            stats['bullets'] += 1

        # --- KÓÐAMERKI / CODE SPANS ---
        # `texti` → texti (fjarlægja backticks)
        code_count = len(re.findall(r'`[^`]+`', line))
        if code_count > 0:
            line = re.sub(r'`([^`]+)`', r'\1', line)
            stats['code_spans'] += code_count

        # --- FEITLETRAÐ / BOLD ---
        # **texti** → texti og __texti__ → texti
        # Athugasemd: Þarf að gera feitletrað ÁÐUR en skáletrað,
        # annars myndi *texti* samsvara hluta af **texti**.
        bold_count = len(re.findall(r'\*\*[^*]+\*\*', line))
        bold_count += len(re.findall(r'__[^_]+__', line))
        if bold_count > 0:
            line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            line = re.sub(r'__([^_]+)__', r'\1', line)
            stats['bold'] += bold_count

        # --- SKÁLETRAÐ / ITALIC ---
        # *texti* → texti og _texti_ → texti
        # Athugasemd: Forðumst að fjarlægja _ í orðum eins og
        # "orð_með_undirstrikum" — aðeins _texti_ (bil eða
        # strengjaupphaf/-endi utan við _)
        italic_count = len(re.findall(r'(?<!\w)\*([^*]+)\*(?!\w)', line))
        italic_count += len(re.findall(r'(?<!\w)_([^_]+)_(?!\w)', line))
        if italic_count > 0:
            line = re.sub(r'(?<!\w)\*([^*]+)\*(?!\w)', r'\1', line)
            line = re.sub(r'(?<!\w)_([^_]+)_(?!\w)', r'\1', line)
            stats['italic'] += italic_count

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines), stats


# ============================================================
# METAUMFJÖLLUN / META-COMMENTARY STRIPPING
# LLM-líkön bæta stundum við upphafsorðum eða lokaorðum sem
# eru EKKI hluti af textaframhaldinu, heldur viðbrögð við
# beiðninni (prompt).
#
# Dæmi: "Hér er framhaldið:", "Ég held áfram:", "Vonandi nýttist þetta."
#
# VARÚÐ: Við erum ÍHALDSSÖM (conservative) hér. Við fjarlægjum
# AÐEINS línur sem eru augljóslega metaumfjöllun, ekki efni
# textans sjálfs. Ef vafamál, HÖLDUM við línunni.
# ============================================================

# Mynstur (patterns) fyrir íslenska metaumfjöllun sem LLM-líkön
# setja gjarnan framan á eða aftan á textaframhald.
#
# Þessi eru AÐEINS notuð á fyrstu/síðustu línur til öryggis.
# Hver regex passar við heila línu.
META_PATTERNS_START = [
    # "Hér er framhaldið:" eða "Hér er framhald textans:"
    re.compile(r'^Hér\s+er\s+framhald', re.IGNORECASE),
    # "Ég held áfram:" eða "Ég held áfram með textanum:"
    re.compile(r'^Ég\s+held\s+áfram', re.IGNORECASE),
    # "Samkvæmt beiðni:" eða "Samkvæmt fyrirmælum:"
    re.compile(r'^Samkvæmt\s+(beiðni|fyrirmælum)', re.IGNORECASE),
    # "Framhald textans:" eða "Framhald:"
    re.compile(r'^Framhald(?:\s+textans)?\s*:', re.IGNORECASE),
    # "Framhald sögunnar" (án tvípunkts — séð í Le Chat Fast)
    re.compile(r'^Framhald\s+sögunnar\s*$', re.IGNORECASE),
    # "Textinn heldur áfram:" eða svipaðar lýsingar
    re.compile(r'^Textinn\s+heldur\s+áfram', re.IGNORECASE),
    # "Hér fyrir neðan er framhaldið:"
    re.compile(r'^Hér\s+fyrir\s+neðan', re.IGNORECASE),
    # "Sure, here is the continuation:" (ef LLM svarar á ensku)
    re.compile(r'^Sure,?\s+here\s+is', re.IGNORECASE),
    # "Here is the continuation:" (ef LLM svarar á ensku)
    re.compile(r'^Here\s+is\s+the\s+continuation', re.IGNORECASE),
    # "Certainly" eða "Of course" (enskt preamble)
    re.compile(r'^(Certainly|Of\s+course)[,!.]', re.IGNORECASE),
]

META_PATTERNS_END = [
    # "Vonandi nýttist þetta." eða "Vonandi hjálpar þetta."
    re.compile(r'^Vonandi\s+(nýttist|hjálpar|gagnast)', re.IGNORECASE),
    # "Ég vona að þetta nýtist." eða svipað
    re.compile(r'^Ég\s+vona\s+að\s+þetta', re.IGNORECASE),
    # "Láttu mig vita ef..." (LLM-lokasetning)
    re.compile(r'^Láttu\s+mig\s+vita', re.IGNORECASE),
    # "Ef þú vilt að ég haldi áfram..."
    re.compile(r'^Ef\s+þú\s+vilt\s+að\s+ég', re.IGNORECASE),
    # "Endilega láttu mig vita" eða "Ekki hika við"
    re.compile(r'^(Endilega|Ekki\s+hika)', re.IGNORECASE),
    # "Let me know if..." (enskt)
    re.compile(r'^Let\s+me\s+know', re.IGNORECASE),
    # "I hope this helps" (enskt)
    re.compile(r'^I\s+hope\s+this\s+helps', re.IGNORECASE),
    # "Að loknu textanum" (séð í Le Chat Fast)
    re.compile(r'^Að\s+loknu\s+textanum\s*$', re.IGNORECASE),

    # ====================================================
    # VIÐBÆTUR (added) — sjálfsvísandi LLM-lokasetningar
    # SELF-REFERENTIAL CLOSING PATTERNS observed in real
    # LLM outputs (sérstaklega Le Chat Thinking).
    #
    # Þessar línur eru þegar líkanið brýtur úr karakter
    # og talar beint við notandann um eigin úttak.
    # The model breaks character to address the user
    # directly about its own output.
    # ====================================================

    # Bein vísun í verkefnið / direct reference to the task:
    # "Þessi texti er ekki sannleikur, en hann er í stíl við þann
    #  sem þú gafst mér."
    # Hugmynd: Líkanið vísar til textans sem það fékk sem prompt.
    re.compile(r'stíl\s+við\s+þann\s+sem\s+þú\s+gafst', re.IGNORECASE),
    re.compile(r'í\s+stíl\s+við\s+(þann|texta(nn)?)\s+sem', re.IGNORECASE),
    # "Þessi texti er ekki sannleikur" / "ekki efnislega réttur"
    # — líkanið viðurkennir að efnið sé tilbúningur.
    re.compile(r'^Þessi\s+texti\s+er\s+(ekki|tilbúin)', re.IGNORECASE),
    re.compile(r'er\s+ekki\s+sannleikur', re.IGNORECASE),
    re.compile(r'er\s+ekki\s+efnislega\s+rétt', re.IGNORECASE),

    # Bein spurning til notandans / direct question to the user:
    # "Ertu ánægð með þessum stíli, eða viltu að ég breyti einhverju?"
    re.compile(r'^Ertu\s+(ánægð|ánægður|sátt|sáttur)', re.IGNORECASE),
    re.compile(r'viltu\s+að\s+ég\s+(breyti|haldi|skrifi|geri)', re.IGNORECASE),
    re.compile(r'^Á\s+ég\s+að\s+halda\s+áfram', re.IGNORECASE),
    re.compile(r'^Vilt\s+þú\s+að\s+ég', re.IGNORECASE),
    # "Hvað finnst þér?" — bein spurning sem er aldrei hluti
    # af raunverulegum texta í þessum gögnum.
    re.compile(r'^Hvað\s+finnst\s+þér\s*\?*$', re.IGNORECASE),

    # Sjálfsvísandi orðalag um eigin skrif:
    # "Ég hef reynt að halda þeim stíl..."
    re.compile(r'^Ég\s+hef\s+reynt\s+að\s+(halda|skrifa|líkja)', re.IGNORECASE),
    re.compile(r'^Ég\s+reyndi\s+að\s+(halda|skrifa|líkja)', re.IGNORECASE),
    # "Ég vona að þér líki" / "Ég vona að þetta sé í samræmi"
    re.compile(r'^Ég\s+vona\s+að\s+þér\s+líki', re.IGNORECASE),
    re.compile(r'^Ég\s+vona\s+að\s+þetta\s+sé', re.IGNORECASE),
    # "(Athugasemd: ...)" — meta-athugasemd í sviga
    re.compile(r'^\(?Athugasemd\s*[:.]', re.IGNORECASE),
    # "(Note:" eða "Note:" — enskt
    re.compile(r'^\(?Note\s*:', re.IGNORECASE),
    # "Þetta er framhald á textanum" / "Þetta er tilraun til..."
    re.compile(r'^Þetta\s+er\s+(framhald|tilraun|dæmi)', re.IGNORECASE),
]


def strip_meta_commentary(text: str) -> tuple[str, list[str]]:
    """Fjarlægja metaumfjöllun frá LLM úr upphafi og enda texta.

    Aðeins athugað á fyrstu og síðustu línunum — ALDREI í miðju
    textanum, þar sem hluti af efninu gæti passað við mynstur
    óviljandi.

    VARÚÐ / CAUTION:
        Þetta er ÍHALDSSAMT. Ef lína passar ekki við eitthvert
        þekkt mynstur, er henni HALDIÐ. Betra að halda einni
        óþarfa línu en eyða raunverulegum texta.

    LÍNUR SEM SKOÐAÐAR ERU / LINES INSPECTED:
        - Upphaf: fyrstu 3 línurnar (sjaldgæft að meta sé djúpt)
        - Endi: síðustu 6 línurnar (LLM-líkön setja oft margar
          metasetningar saman í lokamálsgrein, t.d. "Þessi texti er
          ekki sannleikur..." + "Ertu ánægð..." + tóm lína)

    Args:
        text: Texti sem gæti haft metaumfjöllun.

    Returns:
        Tuple af (hreinsaður texti, listi af línum sem voru fjarlægðar).
        Listinn er notaður til skráningar svo nemandinn geti
        sannreynt að engin raunveruleg textalína hafi verið eytt.
    """
    lines = text.split('\n')
    stripped_lines: list[str] = []  # Allar línur sem voru fjarlægðar (til skráningar)

    # --- ATHUGA UPPHAF / CHECK START ---
    # Skoða fyrstu 3 línurnar (LLM getur sett meta á fyrstu 1-2 línur
    # og jafnvel sleppt einni auðri línu á milli).
    # Fjarlægjum línur frá toppi á meðan þær eru annaðhvort tómar
    # eða passa við meta-mynstur.
    lines_to_check = min(3, len(lines))
    start_idx = 0

    for i in range(lines_to_check):
        line_stripped = lines[i].strip()

        # Tómar línur í upphafi — sleppa þeim (ekki telja sem meta)
        if not line_stripped:
            start_idx = i + 1
            continue

        # Athuga hvort línan passi við upphafsmynstur
        is_meta = False
        for pattern in META_PATTERNS_START:
            if pattern.search(line_stripped):
                is_meta = True
                break

        if is_meta:
            start_idx = i + 1
            stripped_lines.append(f"[START] {line_stripped}")
        else:
            # Fyrsta lína sem er ekki tóm og ekki meta → hætta
            break

    # --- ATHUGA ENDA / CHECK END ---
    # Skoða síðustu 6 línurnar á sama hátt.
    # AUKINN GLUGGI: 6 í stað 3, þar sem Le Chat Thinking framleiðir
    # oft 2-3 metasetningar í röð í lokamálsgrein, og þær geta verið
    # aðskildar með auðum línum eða blandaðar saman.
    end_idx = len(lines)
    end_window = min(6, len(lines) - start_idx)

    # Vinnum frá aftasta í áttina að upphafi
    # Lækkum end_idx fyrir hverja línu sem er meta eða tóm.
    lower_bound = max(start_idx, len(lines) - end_window)

    i = len(lines) - 1
    while i >= lower_bound:
        line_stripped = lines[i].strip()

        # Tómar línur í enda — sleppa þeim
        if not line_stripped:
            end_idx = i
            i -= 1
            continue

        # Athuga hvort línan passi við lokamynstur
        is_meta = False
        for pattern in META_PATTERNS_END:
            if pattern.search(line_stripped):
                is_meta = True
                break

        if is_meta:
            end_idx = i
            stripped_lines.append(f"[END] {line_stripped}")
            i -= 1
        else:
            # Fyrsta lína (frá enda séð) sem er ekki meta → hætta
            break

    # Skera textann niður í aðeins efnislínur
    result_lines = lines[start_idx:end_idx]
    return '\n'.join(result_lines), stripped_lines


# ============================================================
# HVÍTBILSNORMUN / WHITESPACE NORMALIZATION
# SAMA rökfræði og í extract_samples.py:
#   re.sub(r'\s+', ' ', text).strip()
#
# extract_samples.py vinnur á EINNI MÁLSGREIN Í SENN og sameinkar
# setningar með bilum. LLM-texti kemur hins vegar sem heill texti
# með línuskilum sem málsgreinaskil.
#
# Aðferð: Við vinnum á hverri málsgrein (paragraph) sér, nákvæmlega
# eins og extract_samples.py gerir.
# ============================================================

def normalize_whitespace(text: str) -> str:
    """Norma hvítbil í texta — sama og extract_samples.py.

    Skiptir textanum í málsgreinar (á auðum línum), hreinsar hverja
    málsgrein sér (sameinkar mörg bil í eitt), og sameinar svo
    málsgreinarnar aftur.

    HVERS VEGNA MÁLSGREINAUPPBYGGING?
        extract_samples.py vinnur á málsgreinum (úr XML <p> merkjum)
        og hreinsar hverja sér. Í LLM-texta eru málsgreinar aðskildar
        með auðum línum. Við endurgerum þá sömu uppbyggingu.

    Args:
        text: Texti sem gæti haft óreglulegt hvítbil.

    Returns:
        Texti þar sem hvert hvítbilsruna er eitt bil,
        og málsgreinaskil eru varðveitt sem eitt línuskil.
    """
    # Skipta í málsgreinar á auðum línum
    # (Ein eða fleiri auðar línur = málsgreinaskil)
    paragraphs = re.split(r'\n\s*\n', text)

    cleaned_paragraphs = []
    for para in paragraphs:
        # Hreinsa hverja málsgrein:
        # 1. Skipta allt hvítbil (línuskil, fleirum bil) í eitt bil
        # 2. Fjarlægja bil framan og aftan
        # Þetta er NÁKVÆMLEGA re.sub(r'\s+', ' ', text).strip()
        # eins og extract_samples.py gerir á hverri málsgrein.
        cleaned = re.sub(r'\s+', ' ', para).strip()
        if cleaned:
            cleaned_paragraphs.append(cleaned)

    # Sameina málsgreinar aftur — ein ný lína á milli
    return '\n'.join(cleaned_paragraphs)


# ============================================================
# FYRIRSAGNAGREINING / HEADLINE DETECTION
# Eftir markdown-hreinsun geta sumar línur verið fyrirsagnir
# (stuttar línur sem enda ekki á . ? !).
#
# extract_samples.py beitir ensure_sentence_ending() á allar
# málsgreinar. Við gerum nákvæmlega það sama.
#
# ATHUGASEMD: Þetta er forvinnsla til að hjálpa þáttaranum,
# nákvæmlega eins og í extract_samples.py.
# ============================================================

def apply_sentence_endings(text: str) -> str:
    """Tryggja setningarendamerki á öllum málsgreinum.

    NÁKVÆMLEGA sama rökfræði og í extract_samples.py, þar sem
    ensure_sentence_ending() er beitt á hverja málsgrein.

    Args:
        text: Texti skipt í málsgreinar (ein per línu).

    Returns:
        Texti þar sem öll málsgrein endar á . ? eða !
    """
    lines = text.split('\n')
    processed = [ensure_sentence_ending(line) for line in lines if line.strip()]
    return '\n'.join(processed)


# ============================================================
# ENDURTEKNINGARGREINING / REPETITION DETECTION
# ============================================================
# Sum LLM-líkön afrita orðrétt textabúta úr promptinu (fyrri
# helmingi mannlega textans) inn í framhaldið. Þetta sást
# sérstaklega í Le Chat Thinking úttökum.
#
# HVERS VEGNA ÞETTA ER VANDAMÁL:
#     Ef líkanið afritar 50 orð beint úr promptinu inn í eigin
#     framhald, þá lítur framhaldið út fyrir að vera mjög svipað
#     mannlegum stíl — en það er bara afritun, ekki raunverulegur
#     stíleftirherma. Þetta blæs upp stílmælingar á tilbúinn hátt.
#
# AÐFERÐ / METHOD:
#     Við notum n-gram samsvörun (n-gram matching). Tökum hvert
#     10-orða bút úr framhaldinu og athugum hvort það birtist í
#     promptinu. Þegar samsvörun finnst, lengjum við hana eins langt
#     og hægt er, og hoppum svo yfir samsvörunina til að forðast
#     tvíteljun.
#
# AÐ TAKA ÁKVÖRÐUN / NOT AUTOMATIC REMOVAL:
#     Við FJARLÆGJUM EKKI sjálfkrafa endurtekna búta. Þetta er
#     aðferðafræðileg ákvörðun sem nemandinn þarf að taka per skrá.
#     Skriftan skrifar AÐEINS skýrslu — nemandinn ákveður hvað á
#     að gera við hverja samsvörun.
# ============================================================

# Lágmarkslengd samsvörunar (orð) til að teljast endurtekning.
# 10 orð er nógu langt til að útiloka tilviljanir í íslensku
# (algeng orð eins og "það er", "að vera" o.s.frv.) en stutt
# nóg til að ná raunverulegum afritunum.
MIN_REPEAT_WORDS = 10


def normalize_for_matching(text: str) -> list[str]:
    """Tókenisera texta fyrir endurtekningarsamanburð.

    Lágstafa allt og fjarlægja greinarmerki frá köntum tókna,
    svo "Þetta," og "þetta" passi saman. Halda þó orðakjarnanum
    eins og hann er — engin stefnufræðileg (lemmatization).

    Hugmynd: Við viljum að "Sjá einnig töflu V." og "sjá einnig
    töflu V" passi saman, jafnvel þótt punktur sé á einum.

    Args:
        text: Hráður texti.

    Returns:
        Listi af tóknum (lágstöfuðum, hreinsuðum).
    """
    # Skipta í orð á hvítbili
    raw_tokens = text.split()
    cleaned = []
    for tok in raw_tokens:
        # Lágstafa
        tok = tok.lower()
        # Fjarlægja algeng greinarmerki frá köntum
        # (en halda í miðju, t.d. "TAVI-aðgerð")
        tok = tok.strip('.,;:!?„"""()[]{}«»')
        if tok:
            cleaned.append(tok)
    return cleaned


def find_repeated_passages(
    continuation_text: str,
    prompt_text: str,
    min_words: int = MIN_REPEAT_WORDS,
) -> list[dict]:
    """Finna samfelldar orðaraðir úr framhaldi sem birtast í prompti.

    Notar n-gram samsvörun: byggjum upp orðaröð úr promptinu og
    leitum að 10+ orða samfelldum runum úr framhaldinu sem passa
    nákvæmlega við einhverja runu í promptinu.

    REIKNIRIT (algorithm):
        1. Tókenisera bæði promptið og framhaldið (lágstafað).
        2. Búa til samsetta strengi: prompt = "orð1 orð2 orð3 ..."
        3. Fyrir hvern stað i í framhaldinu, prófaðu 10-orða bút.
        4. Ef búturinn finnst í promptstrengnum, lengdu hann eins
           langt og hann passar (greedy extension).
        5. Skráðu samsvörunina og hoppaðu yfir hana (i += match_len)
           til að forðast að telja sama bút margfalt.

    KOSTUR / ADVANTAGE:
        Innbyggt strengjaleit í Python er hraðvirkt (C-útfært),
        svo þetta er nógu hratt fyrir 2.000 orða skrár.

    Args:
        continuation_text: Texti frá LLM (framhald).
        prompt_text: Texti sem var sendur sem prompt (mannlegi
            fyrri helmingurinn).
        min_words: Lágmarksfjöldi orða í samfellu til að teljast
            endurtekning. Sjálfgefið 10.

    Returns:
        Listi af dict, eitt per samsvörun:
            - cont_word_start: Byrjunarvísir (orðanúmer) í framhaldi
            - cont_word_end: Endavísir (eftir síðasta orðið)
            - length: Fjöldi orða í samsvöruninni
            - cont_text: Hin samsvaraða runa, eins og hún birtist í
              framhaldinu (upprunaleg orð, ekki lágstafað)
            - prompt_match: Sama runa eins og hún birtist í promptinu
              (gæti haft annað hástafsnotkun eða greinarmerki)
    """
    # --- TÓKENISERING ---
    # Höldum bæði "upprunalegu" orðunum (til sýningar) og lágstöfuðu
    # útgáfunni (til samsvörunar).
    cont_tokens_orig = continuation_text.split()
    cont_tokens_norm = normalize_for_matching(continuation_text)
    prompt_tokens_orig = prompt_text.split()
    prompt_tokens_norm = normalize_for_matching(prompt_text)

    # Athugasemd: normalize_for_matching getur sleppt tómum tóknum,
    # svo lengdir gætu verið mismunandi. Við vinnum á normalize-listanum
    # en sækjum upprunalega texta út frá hlutfallslegri stöðu.
    #
    # Til einföldunar notum við áfram cont_tokens_orig.split() lengd,
    # sem ætti að vera sú sama og len(cont_tokens_norm) þar sem
    # split() skilar engum tómum tóknum og normalize sleppir aðeins
    # alveg-tómum tóknum. Það er nógu nákvæmt fyrir okkar þarfir.

    # Ef framhaldið eða promptið er of stutt, skilja engar samsvaranir.
    if len(cont_tokens_norm) < min_words or len(prompt_tokens_norm) < min_words:
        return []

    # --- BYGGJA UPP STRENG TIL LEITAR ---
    # Sameina tóknin í einn streng með bilmilli, svo við getum
    # notað innbyggða strengjaleit (Python `in` virki) hraðvirkt.
    SEP = ' '
    prompt_joined = SEP.join(prompt_tokens_norm)

    matches = []
    i = 0
    n = len(cont_tokens_norm)

    while i <= n - min_words:
        # Prófa fyrsta 10-orða bút frá stöðu i
        ngram = SEP.join(cont_tokens_norm[i:i + min_words])

        if ngram in prompt_joined:
            # SAMSVÖRUN! Reyndu að lengja hana.
            # Greedy extension: bæta einu orði í einu og athuga.
            length = min_words
            while i + length < n:
                extended = SEP.join(cont_tokens_norm[i:i + length + 1])
                if extended in prompt_joined:
                    length += 1
                else:
                    break

            # Skrá samsvörunina
            # Sækja upprunalegu textaútgáfuna (með upprunalegri
            # hástafsnotkun og greinarmerki).
            # Athugasemd: i og length eiga við lágstöfuðu listana,
            # en cont_tokens_orig á að vera samsvarandi (split() vs
            # normalize() ættu að gefa sama fjölda í þessum gögnum).
            cont_orig_slice = ' '.join(cont_tokens_orig[i:i + length])

            # Finna samsvarandi stað í promptinu (til sýningar)
            match_in_prompt = SEP.join(cont_tokens_norm[i:i + length])
            prompt_match_idx = prompt_joined.find(match_in_prompt)
            # Telja hve mörg orð koma á undan í promptinu
            # (til að finna byrjunarstaðinn í upprunalega listanum)
            words_before = prompt_joined[:prompt_match_idx].count(SEP)
            if prompt_match_idx > 0:
                # Bæta einu við ef við erum ekki á byrjun (því SEP
                # eftir síðasta orðsins fyrir framan).
                pass
            prompt_orig_slice = ' '.join(
                prompt_tokens_orig[words_before:words_before + length]
            )

            matches.append({
                'cont_word_start': i,
                'cont_word_end': i + length,
                'length': length,
                'cont_text': cont_orig_slice,
                'prompt_match': prompt_orig_slice,
            })

            # Hoppa yfir samsvörunina til að forðast tvíteljun
            i += length
        else:
            i += 1

    return matches


def find_prompt_for_continuation(
    cont_filename: str,
    prompt_dir: Path,
) -> Path | None:
    """Finna promptskrá sem passar við LLM-úttaksskrá.

    Skráarheitamynstur:
        Framhald:  <model>_<category>_prompt_<NNN>.txt
                   (t.d. "gemini_academic_prompt_010.txt",
                         "lechat_thinking_blog_prompt_002.txt")
        Prompt:    <category>_prompt_<NNN>.txt
                   (t.d. "academic_prompt_010.txt",
                         "blog_prompt_002.txt")

    AÐFERÐ:
        Drögum út „<category>_prompt_<NNN>.txt" hluta úr
        framhaldsskráarheiti með reglulegri segð, og bætum því
        við promptmöppuna.

    Args:
        cont_filename: Skráarheiti framhaldsskrár.
        prompt_dir: Mappa með promptskrám.

    Returns:
        Slóð á promptskrá ef hún finnst, annars None.
    """
    # Reglulega segðin: leita að "<orð>_prompt_<tölur>.txt" í
    # endanum á skráarheitinu. <orð> er flokkurinn (news, blog,
    # academic). Þetta nær yfir öll þekkt nafnamynstur:
    #   gemini_academic_prompt_010.txt    → academic_prompt_010.txt
    #   lechat_thinking_blog_prompt_002.txt → blog_prompt_002.txt
    #   gpt5_academic_prompt_001.txt      → academic_prompt_001.txt
    match = re.search(
        r'(news|blog|academic)_prompt_\d+\.txt$',
        cont_filename,
    )
    if not match:
        return None

    prompt_name = match.group(0)
    prompt_path = prompt_dir / prompt_name

    if prompt_path.exists():
        return prompt_path
    return None


def strip_prompt_instruction(prompt_text: str) -> str:
    """Fjarlægja íslensku leiðbeininguna úr promptinu.

    prepare_paired_experiment.py setur fasta leiðbeiningu fremst í
    hverja promptskrá:
        "Vinsamlegast haltu áfram með textann á sama hátt og í sama
         stíl. ... Haltu áfram þar sem textinn hættir:"

    Þessi leiðbeining er EKKI hluti af mannlega textanum, svo við
    fjarlægjum hana áður en við berum saman við framhaldið.

    Args:
        prompt_text: Heill textinn úr promptskrá.

    Returns:
        Promptið án leiðbeiningarinnar fremst.
    """
    # Þekkjum lokaorð leiðbeiningarinnar: "Haltu áfram þar sem textinn
    # hættir:" — eftir tvípunktinn kemur raunverulegi mannlegi textinn.
    marker = "Haltu áfram þar sem textinn hættir:"
    idx = prompt_text.find(marker)
    if idx >= 0:
        return prompt_text[idx + len(marker):].strip()
    # Ef leiðbeiningin er ekki til staðar (t.d. annað snið), skila öllu
    return prompt_text


# ============================================================
# AÐALHREINSUNARFALL / MAIN CLEANING FUNCTION
# Keðja allra hreinsunaraðgerða í réttri röð.
# ============================================================

def clean_llm_text(text: str) -> tuple[str, dict]:
    """Hreinsa LLM-texta svo hann fái sömu forvinnslu og mannlegir textar.

    Hreinsunarröð (cleaning pipeline):
        1. Fjarlægja metaumfjöllun (upphaf/endi)
        2. Fjarlægja markdown-sniðmerkingar
        3. Norma hvítbil (eins og extract_samples.py)
        4. Tryggja setningarendamerki (eins og extract_samples.py)

    HVERS VEGNA ÞESSI RÖÐ?
        - Meta-commentary fyrst, þar sem hún getur innihaldið markdown
          sem myndi ruglast við efni ef markdown-hreinsun gerð fyrst.
        - Markdown næst, þar sem það fjarlægir # og * merki sem myndu
          trufla hvítbilsnormun.
        - Hvítbilsnormun þriðja, til að fá hreinar línur.
        - Setningarendamerki síðast, þar sem þau þurfa hreinar línur
          til að virka rétt.

    Args:
        text: Hráður texti frá LLM.

    Returns:
        Tuple af (hreinsaður texti, tölfræðidict).
    """
    all_stats = {}

    # SKREF 1: Fjarlægja metaumfjöllun
    # Skilar bæði tölu og lista af línum sem voru fjarlægðar
    # — listinn er notaður til skráningar svo nemandinn geti
    # staðfest að engin raunveruleg textalína hafi verið eytt.
    text, stripped_meta_lines = strip_meta_commentary(text)
    all_stats['meta_lines_removed'] = len(stripped_meta_lines)
    all_stats['meta_lines'] = stripped_meta_lines  # Listi til skráningar

    # SKREF 2: Fjarlægja markdown
    text, md_stats = strip_markdown(text)
    all_stats.update(md_stats)

    # SKREF 3: Norma hvítbil — eins og extract_samples.py
    text = normalize_whitespace(text)

    # SKREF 4: Tryggja setningarendamerki — eins og extract_samples.py
    text = apply_sentence_endings(text)

    return text, all_stats


# ============================================================
# VINNA EINA SKRÁ / PROCESS SINGLE FILE
# ============================================================

def process_file(
    input_path: Path,
    output_path: Path,
    prompt_path: Path | None = None,
    save: bool = True,
) -> dict:
    """Hreinsa eina LLM-úttaksskrá og vista niðurstöðu.

    Args:
        input_path: Slóð á inntaksskrá (.txt frá LLM).
        output_path: Slóð á úttaksskrá (hreinsuð útgáfa).
        prompt_path: Slóð á promptskrá (valkvætt). Ef gefið, er
            endurtekningargreining keyrð á móti promptinu.
        save: Ef False, ekki skrifa úttaksskrá (notað fyrir --dry-run).

    Returns:
        Dict með tölfræði um hreinsunina:
            - filename: skráarheiti
            - input_words: orðafjöldi í inntaki
            - output_words: orðafjöldi í úttaki
            - stats: dict frá clean_llm_text
            - repetitions: listi af samsvörunum við prompt (eða [])
    """
    # Lesa inntaksskrá
    raw_text = input_path.read_text(encoding='utf-8')

    # Telja orð í inntaki
    input_words = len(raw_text.split())

    # Hreinsa textann
    cleaned_text, stats = clean_llm_text(raw_text)

    # Telja orð í úttaki
    output_words = len(cleaned_text.split())

    # --- ENDURTEKNINGARGREINING / REPETITION DETECTION ---
    # Ef promptskrá var gefin, leita að orðréttum endurtekningum.
    # ATHUGASEMD: Við keyrum þetta á HREINSAÐA textanum, ekki hráu,
    # svo við berum saman „raunverulega" textann við promptið.
    repetitions: list[dict] = []
    if prompt_path is not None and prompt_path.exists():
        prompt_raw = prompt_path.read_text(encoding='utf-8')
        # Fjarlægja leiðbeiningarstrenginn úr fremst í promptinu
        prompt_human = strip_prompt_instruction(prompt_raw)
        repetitions = find_repeated_passages(cleaned_text, prompt_human)

    # Vista hreinsaðan texta (nema í dry-run)
    if save:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(cleaned_text + '\n', encoding='utf-8')

    return {
        'filename': input_path.name,
        'input_words': input_words,
        'output_words': output_words,
        'stats': stats,
        'repetitions': repetitions,
    }


# ============================================================
# SKÝRSLA / REPORT
# Prenta greinargóða skýrslu um hvað var fjarlægt úr hverri skrá.
# Þetta gerir nemandanum kleift að staðfesta hreinsunina áður
# en þáttarinn er keyrður.
# ============================================================

def print_file_report(info: dict) -> None:
    """Prenta skýrslu um eina skrá.

    Args:
        info: Dict frá process_file.
    """
    stats = info['stats']

    # Safna öllum breytingum sem voru gerðar
    changes = []
    if stats.get('meta_lines_removed', 0) > 0:
        changes.append(f"metaumfjöllun: {stats['meta_lines_removed']} lín.")
    if stats.get('headings', 0) > 0:
        changes.append(f"# hausar: {stats['headings']}")
    if stats.get('bold', 0) > 0:
        changes.append(f"**feit**: {stats['bold']}")
    if stats.get('italic', 0) > 0:
        changes.append(f"*skáltr*: {stats['italic']}")
    if stats.get('bullets', 0) > 0:
        changes.append(f"bullets: {stats['bullets']}")
    if stats.get('numbered_lists', 0) > 0:
        changes.append(f"núm.listar: {stats['numbered_lists']}")
    if stats.get('horizontal_rules', 0) > 0:
        changes.append(f"hr-strik: {stats['horizontal_rules']}")
    if stats.get('blockquotes', 0) > 0:
        changes.append(f"tilvitnun: {stats['blockquotes']}")
    if stats.get('code_spans', 0) > 0:
        changes.append(f"kóði: {stats['code_spans']}")

    # Endurtekningar (ef nokkrar fundust)
    reps = info.get('repetitions', [])
    if reps:
        rep_words = sum(r['length'] for r in reps)
        rep_pct = (rep_words / info['output_words'] * 100) if info['output_words'] else 0
        changes.append(f"ENDURTEKN: {len(reps)} bút./{rep_words}orð ({rep_pct:.0f}%)")

    # Orðafjöldabreyting
    word_diff = info['input_words'] - info['output_words']

    if changes:
        changes_str = ', '.join(changes)
        print(f"    {info['filename']}: {info['input_words']} → "
              f"{info['output_words']} orð ({word_diff:+d}) | {changes_str}")
    else:
        print(f"    {info['filename']}: {info['input_words']} → "
              f"{info['output_words']} orð ({word_diff:+d}) | engar breytingar")

    # Prenta hverja stripped meta-línu á sérstaka línu (innskotið)
    # svo nemandinn geti séð nákvæmlega hvað var fjarlægt.
    for meta_line in info['stats'].get('meta_lines', []):
        print(f"        ↳ {meta_line}")


def print_summary(all_results: list[dict]) -> None:
    """Prenta heildarsamantekt um allar skrár.

    Args:
        all_results: Listi af dict frá process_file.
    """
    if not all_results:
        print("  Engar skrár unnar.")
        return

    total_input = sum(r['input_words'] for r in all_results)
    total_output = sum(r['output_words'] for r in all_results)

    # Tölvur um markdown-breytingar yfir allar skrár
    total_headings = sum(r['stats'].get('headings', 0) for r in all_results)
    total_bold = sum(r['stats'].get('bold', 0) for r in all_results)
    total_italic = sum(r['stats'].get('italic', 0) for r in all_results)
    total_bullets = sum(r['stats'].get('bullets', 0) for r in all_results)
    total_numbered = sum(r['stats'].get('numbered_lists', 0) for r in all_results)
    total_meta = sum(r['stats'].get('meta_lines_removed', 0) for r in all_results)
    total_hr = sum(r['stats'].get('horizontal_rules', 0) for r in all_results)

    print(f"\n  HEILDARSAMANTEKT / OVERALL SUMMARY")
    print(f"  {'─' * 50}")
    print(f"  Skrár unnar:           {len(all_results)}")
    print(f"  Heildarorð (inntak):   {total_input:,}")
    print(f"  Heildarorð (úttak):    {total_output:,}")
    print(f"  Orð fjarlægð:          {total_input - total_output:,}")
    print()
    print(f"  Markdown fjarlægt:")
    print(f"    Hausar (#):          {total_headings}")
    print(f"    Feitletrað (**):     {total_bold}")
    print(f"    Skáletrað (*):       {total_italic}")
    print(f"    Punktalistar (-):    {total_bullets}")
    print(f"    Númeraðir listar:    {total_numbered}")
    print(f"    Lárétt strik:        {total_hr}")
    print(f"  Metaumfjöllun:         {total_meta} línur")

    # --- ENDURTEKNINGAR PER LÍKAN / REPETITIONS PER MODEL ---
    # Ef einhver skrá hefur endurtekningar, prentum samantekt
    # flokkaða eftir líkani (efsta möppustig).
    files_with_reps = [r for r in all_results if r.get('repetitions')]
    if files_with_reps:
        print()
        print(f"  ENDURTEKNINGAR ÚR PROMPT / PROMPT REPETITIONS")
        print(f"  {'─' * 50}")

        # Flokka eftir líkani (fyrsta hluta hlutfallslegrar slóðar)
        # — við notum subdir sem var sett í 'subdir' lyklinum.
        per_model: dict[str, list[dict]] = {}
        for r in files_with_reps:
            model = r.get('model', '?')
            per_model.setdefault(model, []).append(r)

        for model in sorted(per_model.keys()):
            model_results = per_model[model]
            total_reps = sum(len(r['repetitions']) for r in model_results)
            total_rep_words = sum(
                sum(rep['length'] for rep in r['repetitions'])
                for r in model_results
            )
            print(f"    {model}: {len(model_results)} skrár með "
                  f"endurtekningar, {total_reps} bútar samtals, "
                  f"{total_rep_words} orð")


def write_repetition_report(
    all_results: list[dict],
    report_path: Path,
) -> None:
    """Skrifa ítarlega skýrslu um endurtekningar í texta.

    Skýrslan inniheldur fyrir hverja skrá sem hefur endurtekningar:
        - Skráarheiti og líkan
        - Heildartölfræði (orðafjöldi, hlutfall)
        - Hver samsvörun: lengd, samhengi, samsvarandi promptbútur

    Skýrslan er ætluð til handvirkrar yfirferðar af nemandanum.
    Hann ákveður per skrá hvort eigi að halda eða fjarlægja
    endurtekningar — þetta er aðferðafræðileg ákvörðun.

    Args:
        all_results: Listi af dict frá process_file.
        report_path: Slóð til að vista skýrsluna í.
    """
    # Sía aðeins skrár sem hafa endurtekningar
    files_with_reps = [r for r in all_results if r.get('repetitions')]

    # Búa til úttaksmöppu ef hún er ekki til
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("=" * 70)
    lines.append("ENDURTEKNINGARSKÝRSLA / PROMPT REPETITION REPORT")
    lines.append("=" * 70)
    lines.append("")
    lines.append("Þessi skýrsla sýnir orðréttar endurtekningar úr prompti")
    lines.append("(fyrri helmingi mannlega textans) sem birtast í")
    lines.append("framhaldi LLM-líkans.")
    lines.append("")
    lines.append("Lágmarkslengd samsvörunar: " + str(MIN_REPEAT_WORDS) + " orð")
    lines.append("")
    lines.append("AÐFERÐAFRÆÐILEG ATHUGASEMD:")
    lines.append("    Þessar endurtekningar eru ekki fjarlægðar sjálfkrafa.")
    lines.append("    Nemandinn ákveður per skrá hvort/hvernig á að bregðast")
    lines.append("    við þeim. Ef líkanið afritar mannlega textann orðrétt,")
    lines.append("    blæs það upp stílmælingar á tilbúinn hátt.")
    lines.append("")
    lines.append(f"Skrár með endurtekningar: {len(files_with_reps)} af "
                 f"{len(all_results)} alls")
    lines.append("")
    lines.append("=" * 70)
    lines.append("")

    if not files_with_reps:
        lines.append("Engar endurtekningar fundust í neinni skrá.")
    else:
        for r in files_with_reps:
            reps = r['repetitions']
            total_rep_words = sum(rep['length'] for rep in reps)
            pct = (total_rep_words / r['output_words'] * 100
                   if r['output_words'] else 0)

            lines.append(f"SKRÁ: {r.get('relative_path', r['filename'])}")
            lines.append(f"  Líkan: {r.get('model', '?')}")
            lines.append(f"  Orðafjöldi (hreinsaður): {r['output_words']}")
            lines.append(
                f"  {len(reps)} endurteknir bútar samtals "
                f"({total_rep_words} orð, {pct:.1f}% af framhaldi)"
            )
            lines.append("")

            for idx, rep in enumerate(reps, start=1):
                lines.append(
                    f"  [{idx}] {rep['length']} orð, "
                    f"orðastaða {rep['cont_word_start']}–{rep['cont_word_end']}"
                )
                lines.append(f"      Í framhaldi:")
                lines.append(f"        \"{rep['cont_text']}\"")
                lines.append(f"      Í prompti:")
                lines.append(f"        \"{rep['prompt_match']}\"")
                lines.append("")

            lines.append("-" * 70)
            lines.append("")

    report_path.write_text('\n'.join(lines), encoding='utf-8')


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Aðalfall: Hreinsa LLM-úttök til stílmælinga."""
    parser = argparse.ArgumentParser(
        description="Hreinsa LLM-úttök svo þau fái sömu forvinnslu og mannlegir textar.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi um keyrslu:
  # Hreinsa öll LLM-úttök (allar undirmöppur):
  python scripts/preprocess_llm_output.py \\
      --input-dir data/experiment/llm_continuations/ \\
      --output-dir data/experiment/llm_continuations_clean/

  # Hreinsa eitt líkan:
  python scripts/preprocess_llm_output.py \\
      --input-dir data/experiment/llm_continuations/gemini_3_thinking/ \\
      --output-dir data/experiment/llm_continuations_clean/gemini_3_thinking/

  # Keyra á þurrt (dry run) — engar skrár vistaðar:
  python scripts/preprocess_llm_output.py \\
      --input-dir data/experiment/llm_continuations/ \\
      --output-dir data/experiment/llm_continuations_clean/ \\
      --dry-run
        """
    )
    parser.add_argument(
        '--input-dir',
        type=Path,
        required=True,
        help="Mappa með LLM-úttökum (.txt skrám). Leit er endurkvæm."
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        required=True,
        help="Mappa til að vista hreinsuð úttök í. Möppuuppbygging "
             "speglast frá inntaksmöppu."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Sýna hvað myndi breytast án þess að vista skrár."
    )
    parser.add_argument(
        '--prompt-dir',
        type=Path,
        default=None,
        help="Mappa með promptskrám (data/experiment/prompts/). "
             "Ef gefin, er endurtekningargreining keyrð á móti hverjum "
             "prompti og skýrsla skrifuð. Samsvörun við prompt er gerð "
             "út frá skráarheitamynstri (t.d. "
             "gemini_academic_prompt_010.txt → academic_prompt_010.txt)."
    )
    parser.add_argument(
        '--repetition-report',
        type=Path,
        default=None,
        help="Slóð á endurtekningarskýrslu. Sjálfgefið: "
             "<output-dir>/../repetition_report.txt"
    )

    args = parser.parse_args()

    # Staðfesta inntaksmöppu
    if not args.input_dir.is_dir():
        print(f"VILLA: Inntaksmappa finnst ekki: {args.input_dir}")
        sys.exit(1)

    # Finna allar .txt skrár endurkvæmt
    txt_files = sorted(args.input_dir.rglob('*.txt'))

    if not txt_files:
        print(f"VILLA: Engar .txt skrár fundust í {args.input_dir}")
        sys.exit(1)

    # Staðfesta promptmöppu ef hún var gefin
    if args.prompt_dir is not None and not args.prompt_dir.is_dir():
        print(f"VILLA: Promptmappa finnst ekki: {args.prompt_dir}")
        sys.exit(1)

    print("=" * 60)
    print("LLM-FORVINNSLA / LLM OUTPUT PREPROCESSING")
    print("=" * 60)
    print(f"  Inntak:   {args.input_dir}")
    print(f"  Úttak:    {args.output_dir}")
    print(f"  Skrár:    {len(txt_files)}")
    if args.prompt_dir is not None:
        print(f"  Prompt:   {args.prompt_dir}")
        print(f"  Endurtekningargreining: VIRK (lágmark "
              f"{MIN_REPEAT_WORDS} orð)")
    else:
        print(f"  Endurtekningargreining: SLÖKKT (notaðu --prompt-dir)")
    if args.dry_run:
        print(f"  ÞURR KEYRSLA (dry run) — engar skrár vistaðar")
    print()

    # Vinna hverja skrá
    all_results = []

    # Halda utan um núverandi undirmöppu til útprentunar
    current_subdir = None

    for txt_file in txt_files:
        # Reikna hlutfallslega slóð frá inntaksmöppu
        relative_path = txt_file.relative_to(args.input_dir)
        output_path = args.output_dir / relative_path

        # Prenta undirmöppuhaus ef hún breyttist
        subdir = str(relative_path.parent) if relative_path.parent != Path('.') else '(rót)'
        if subdir != current_subdir:
            current_subdir = subdir
            print(f"\n  [{subdir}]")

        # Finna samsvarandi promptskrá ef --prompt-dir var gefið
        prompt_path = None
        if args.prompt_dir is not None:
            prompt_path = find_prompt_for_continuation(
                txt_file.name, args.prompt_dir
            )
            if prompt_path is None:
                print(f"    AÐVÖRUN: Engin promptskrá fannst fyrir "
                      f"{txt_file.name}")

        # Vinna skrána (process_file höndlar bæði keyrslur og dry-run
        # gegnum save=False flagginn).
        info = process_file(
            txt_file,
            output_path,
            prompt_path=prompt_path,
            save=not args.dry_run,
        )

        # Bæta við lýsigögnum sem print_summary og report nota
        # Líkanaheiti = fyrsta hluta hlutfallslegrar slóðar
        # (t.d. "gemini_3_thinking" úr "gemini_3_thinking/academic/...")
        rel_parts = relative_path.parts
        info['model'] = rel_parts[0] if len(rel_parts) > 1 else '(rót)'
        info['relative_path'] = str(relative_path)

        all_results.append(info)
        print_file_report(info)

    # Prenta heildarsamantekt
    print_summary(all_results)

    # --- SKRIFA ENDURTEKNINGARSKÝRSLU ---
    # Aðeins ef endurtekningargreining var virk (þ.e. --prompt-dir gefið)
    if args.prompt_dir is not None:
        # Sjálfgefin staðsetning skýrslu: við hliðina á úttaksmöppu
        if args.repetition_report is not None:
            report_path = args.repetition_report
        else:
            report_path = args.output_dir.parent / "repetition_report.txt"

        write_repetition_report(all_results, report_path)
        print(f"\n  Endurtekningarskýrsla vistuð í:")
        print(f"    {report_path}")

    if args.dry_run:
        print(f"\n  ÞURR KEYRSLA — engar skrár voru vistaðar.")
        print(f"  Keyrðu aftur án --dry-run til að vista.")

    print(f"\n{'=' * 60}")
    print("LOKIÐ!")
    print("=" * 60)


if __name__ == "__main__":
    main()
