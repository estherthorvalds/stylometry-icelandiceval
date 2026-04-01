#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
extract_samples.py — Draga út hreina textaúrtök úr RMH (Risamálheildinni)
===========================================================================

TILGANGUR / PURPOSE:
    Þetta skrifta les TEI XML skrár frá RMH (Risamálheildinni / Icelandic
    Gigaword Corpus), tekur inn texta, og skiptir honum í ~2.000 orða 
    úrtök (samples) til notkunar í stílmælingaverkefninu.

    This script reads TEI XML files from RMH (the Icelandic Gigaword Corpus),
    extracts clean text, and splits it into ~2,000-word samples for use in
    the stylometry benchmark.

HVERS VEGNA 2.000 ORÐ?
    Milička-formúlurnar eru hannaðar til að bera saman textaúrtök af
    svipaðri stærð. Brown-málheildin (sem Milička notar) og Koditex
    nota ~2.000 orða búta sem staðlað stærðarmark. Þetta tryggir að
    tölfræðilegar mælingar séu samanburðarhæfar á milli textategunda.

XML-SNIÐ / XML FORMATS:
    RMH notar tvö XML-snið:

    1. .ana.xml skrár (t.d. IGC-News1-ruv_*.ana.xml):
       Orð eru í <w> merkjum innan <s> (setning) innan <p> (málsgrein).
       Sérstakt: join="right" á <w> merkjum þýðir að næsta orð á að vera
       fast við þetta orð (greinarmerki, t.d. komma eða punktur).

       Dæmi:
       <p><s>
         <w pos="nken">Rekstrarkostnaður</w>
         <w pos="nkeo">sjóðsins</w>
         <w pos="sfg3en">var</w>
         <w pos="ta" join="right">1,2</w>
         <c>%</c>
       </s></p>

    2. .xml skrár (t.d. IGC-Journals-*.xml, IGC-Social2-*.xml):
       Texti er beint í <p> merkjum, án <w> eða <s> merkja.

       Dæmi:
       <p>Þetta er setning. Og önnur setning.</p>

INNTAK / INPUT:
    Mappa með RMH XML skrám (annaðhvort .ana.xml eða .xml).

ÚTTAK / OUTPUT:
    Hrein .txt skrár, ein per úrtak, í tilgreindri úttaksmöppu.
    Skráarheiti: {category}_{001..n}.txt

KEYRSLA / USAGE:
    python3 /Users/esther/Documents/GitHub/stylometry-icelandiceval/scripts/extract_samples.py --input-dir /Users/esther/Documents/GitHub/stylometry-icelandiceval/data/raw/IGC-News1_22.10/IGC-News1-22.10.ana/ruv --output-dir data/human_texts/news/ --target-words 2000
    python3 /Users/esther/Documents/GitHub/stylometry-icelandiceval/scripts/extract_samples.py --input-dir /Users/esther/Documents/GitHub/stylometry-icelandiceval/data/raw/IGC-Journals-22.10.TEI/lb/ --output-dir data/human_texts/academic/ --target-words 2000
    python3 /Users/esther/Documents/GitHub/stylometry-icelandiceval/scripts/extract_samples.py --input-dir /Users/esther/Documents/GitHub/stylometry-icelandiceval/data/raw/IGC-Social-22.10.TEI/Blog/jonas/ --output-dir data/human_texts/blog/ --target-words 2000
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


# ============================================================
# XML NAFNARÝMI / XML NAMESPACE
# TEI XML skrár nota nafnarými (namespace) sem þarf að taka
# tillit til þegar leitað er í trénu.
# ============================================================

# TEI nafnarýmið — allar TEI XML skrár nota þetta
TEI_NS = '{http://www.tei-c.org/ns/1.0}'


# ============================================================
# TRYGGJA SETNINGARENDAMERKI / ENSURE SENTENCE-FINAL PUNCTUATION
# Fyrirsagnir og undirfyrirsagnir enda oft ekki á punkti (. ? !).
# Þetta er vandamál fyrir IceConParse þáttarann, sem reiknar með
# að hvert inntak sé setning sem endar á greinarmerki.
#
# FORVINNSLUÁKVÖRÐUN (preprocessing decision):
#   Við bætum punkti við texta sem endar ekki á setningarendamerki.
#   Þetta er EKKI breyting á málvísindagögnunum sjálfum — þetta er
#   forvinnsla til að þáttarinn virki rétt. Fyrirsagnir eins og
#   „Aukast um innan við 200 milljónir" verða „Aukast um innan við
#   200 milljónir." svo þáttarinn viðurkenni þær sem fullgerar setningar.
#   Án þessa gæti þáttarinn sameint textablokkir yfir setningamörk.
# ============================================================

def ensure_sentence_ending(text: str) -> str:
    """Bæta punkti við texta sem endar ekki á setningarendamerki.

    Ef textinn endar á . ? eða ! gerum við ekkert.
    Annars bætum við punkti (.) við endann.

    Þetta er forvinnsla (preprocessing) til að hjálpa þáttaranum —
    ekki breyting á efni textans sjálfs.

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
# DRAGA ÚT TEXTA ÚR .ana.xml SKRÁ / EXTRACT TEXT FROM .ana.xml
# Þessar skrár hafa orð í <w> merkjum og greinarmerki í <c> merkjum.
# join="right" þýðir: engin bil á undan næsta orði (greinarmerki).
# ============================================================

def extract_text_from_ana_xml(filepath: Path) -> list[str]:
    """Draga út setningar úr .ana.xml skrá.

    .ana.xml skrár hafa orð í <w> merkjum og greinarmerki í <pc> merkjum,
    skipulögð í <s> (setning) og <p> (málsgrein) merkjum.

    MIKILVÆGT UM GREINARMERKI:
        RMH notar <pc> (punctuation character) merki fyrir greinarmerki,
        EKKI <c> (sem eldri TEI-útgáfur notuðu). Við meðhöndlum bæði til
        öryggis.

    MIKILVÆGT UM join="right":
        Ef <w> merki hefur join="right", þýðir það „næsta merki (token)
        á að tengjast beint á eftir mér, án bils". Þetta er venjulega
        notað fyrir orð á undan greinarmerki:
            <w join="right">Gunnarsdóttir</w>  →  „Gunnarsdóttir,"
            <pc>,</pc>
        Ef <pc> merkið er EKKI meðhöndlað, hverfur kommið og næsta
        orð klistrist fast við fyrra: „Gunnarsdóttirfyrrverandi".

    Args:
        filepath: Slóð á .ana.xml skrá.

    Returns:
        Listi af strengjum — hver strengur er ein málsgrein (setningar
        innan málsgreinar sameinaðar með bilum). Fyrirsagnir og
        efnismálsgreinar eru aðskildar sem sjálfstæð stök.
        Forvinnsla: Sérhver málsgrein er tryggð að enda á setningarendamerki.
    """
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        print(f"  AÐVÖRUN: XML-villa í {filepath.name}: {e}")
        return []

    root = tree.getroot()

    # Finna <body> merkið — texti er inni í <text><body><div><p><s><w>
    body = root.find(f'.//{TEI_NS}body')
    if body is None:
        return []

    # Safna setningum per málsgrein (<p>).
    # Þetta varðveitir málsgreinaskil — mikilvægt til að halda
    # fyrirsögnum og efnismálsgreinum aðskildum.
    paragraph_groups = []  # Listi af listum: [[sent1, sent2], [sent3], ...]

    for p_elem in body.iter(f'{TEI_NS}p'):
        para_sentences = []  # Setningar í þessari málsgrein

        # Finna allar setningar (<s> merki) undir þessari málsgrein
        for s_elem in p_elem.findall(f'{TEI_NS}s'):
            tokens = []
            join_next = False  # Flagg: næsta tóki á að vera fast við fyrra

            # Fara í gegnum öll börn <s> merksins
            for child in s_elem:
                # Fjarlægja nafnarými úr merki til samanburðar
                tag = child.tag.replace(TEI_NS, '')

                # <w> = orð (word), <pc> = greinarmerki (punctuation character).
                # <c> er einnig meðhöndlað (eldri TEI-snið) til öryggis.
                if tag in ('w', 'pc', 'c'):
                    text = child.text or ''
                    text = text.strip()

                    if not text:
                        continue

                    if join_next:
                        # Fast við fyrra orð (engin bil á milli).
                        # Þetta gerist þegar fyrra merki hafði join="right",
                        # t.d. orð á undan kommu: „Gunnarsdóttir" + „," → „Gunnarsdóttir,"
                        if tokens:
                            tokens[-1] = tokens[-1] + text
                        else:
                            tokens.append(text)
                        join_next = False
                    else:
                        tokens.append(text)

                    # Athuga hvort join="right" sé á ÞESSU merki.
                    # Ef svo, á NÆSTA merki (token) að vera fast við þetta merki.
                    if child.get('join') == 'right':
                        join_next = True

            # Sameina orð í eina setningu
            if tokens:
                sentence = ' '.join(tokens)
                # Hreinsa tvöföld bil ef einhver slæddust inn
                sentence = re.sub(r'\s+', ' ', sentence).strip()
                if sentence:
                    para_sentences.append(sentence)

        # Bæta setningum þessarar málsgreinar við paragraph_groups
        if para_sentences:
            paragraph_groups.append(para_sentences)

    # --- SAMSETNING Á MÁLSGREINUM / ASSEMBLE PARAGRAPHS ---
    # Hverri málsgrein (para) skilar við sem einn streng, með
    # setningum aðskildum með bilum.
    # Ef fyrsta málsgreinin (para 0) er stutt og endar ekki á
    # greinarmerki, gæti hún verið fyrirsögn — við tryggjum
    # setningarendamerki á henni.
    paragraphs = []
    for para_idx, para_sents in enumerate(paragraph_groups):
        if not para_sents:
            continue

        # Forvinnsla (preprocessing):
        # Tryggja setningarendamerki á hverri setningu.
        # Fyrirsagnir og stutt undirfyrirsagnir enda oft án punkts,
        # sem getur ruglað þáttarann. Sjá athugasemd um
        # ensure_sentence_ending() hér að ofan.
        processed = [ensure_sentence_ending(s) for s in para_sents]

        # Sameina setningar málsgreinarinnar í einn streng
        para_text = ' '.join(processed)
        paragraphs.append(para_text)

    return paragraphs


# ============================================================
# DRAGA ÚT TEXTA ÚR .xml SKRÁ (PLAIN TEI) / EXTRACT FROM PLAIN TEI
# Þessar skrár hafa texta beint í <p> merkjum — mun einfaldara.
# ============================================================

def extract_text_from_plain_xml(filepath: Path) -> list[str]:
    """Draga út málsgreinar úr venjulegri TEI XML skrá.

    Venjulegar TEI XML skrár hafa texta beint í <p> merkjum,
    án <w> eða <s> undirmerkja.

    MIKILVÆGT: Sumar <p> merkingar í TEI-haus (teiHeader) innihalda
    lýsigögn (metadata), ekki texta. Við tökum AÐEINS <p> merki sem
    eru undir <body>.

    Args:
        filepath: Slóð á .xml skrá.

    Returns:
        Listi af strengjum — hver strengur er ein málsgrein.
        Forvinnsla: Sérhver málsgrein er tryggð að enda á setningarendamerki.
    """
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        print(f"  AÐVÖRUN: XML-villa í {filepath.name}: {e}")
        return []

    root = tree.getroot()

    # Finna <body> merkið
    body = root.find(f'.//{TEI_NS}body')
    if body is None:
        return []

    paragraphs = []

    # Finna allar málsgreinar (<p> merki) undir <body>
    for p_elem in body.iter(f'{TEI_NS}p'):
        # itertext() sækir allan texta undir merkinu, þ.m.t. texta
        # innan undirmerkja (t.d. <ref>, <hi>). Þetta fjarlægir allar
        # XML merkingar og skilar hreinum texta.
        text = ''.join(p_elem.itertext()).strip()

        if text:
            # Hreinsa tvöföld bil
            text = re.sub(r'\s+', ' ', text)

            # Forvinnsla: Tryggja setningarendamerki.
            # Sjá athugasemd um ensure_sentence_ending() hér að ofan.
            text = ensure_sentence_ending(text)

            paragraphs.append(text)

    return paragraphs


# ============================================================
# GREINA SKRÁARGERÐ / DETECT FILE TYPE
# Athuga hvort skráin sé .ana.xml eða venjuleg .xml
# ============================================================

def is_ana_xml(filepath: Path) -> bool:
    """Athuga hvort skrá sé .ana.xml (annotated) eða venjuleg .xml.

    .ana.xml skrár hafa orð í <w> merkjum, venjulegar .xml skrár hafa
    texta beint í <p> merkjum.

    Args:
        filepath: Slóð á XML skrá.

    Returns:
        True ef skráin er .ana.xml, False annars.
    """
    return filepath.name.endswith('.ana.xml')


# ============================================================
# LESA ÖLLUM XML SKRÁR Í MÖPPU / READ ALL XML FILES FROM DIRECTORY
# Fer endurkvæmt (recursively) í gegnum möppuna og les alla texta.
# ============================================================

def read_all_texts(input_dir: Path) -> list[str]:
    """Lesa texta úr öllum XML skrám í möppu (endurkvæmt).

    Þetta fall finnur allar .xml og .ana.xml skrár í möppunni og
    öllum undirmöppum, dregur út texta úr hverri, og skilar einum
    sameinuðum lista af setningum/málsgreinum.

    Args:
        input_dir: Mappa sem inniheldur XML skrár.

    Returns:
        Listi af strengjum — hvert stak er ein setning eða málsgrein.
    """
    all_texts = []

    # Finna allar .xml skrár endurkvæmt.
    # rglob('*.xml') finnur alla .xml skrár í möppu og undirmöppum.
    # Þetta nær einnig yfir .ana.xml skrár (þær enda á .xml).
    xml_files = sorted(input_dir.rglob('*.xml'))

    if not xml_files:
        print(f"VILLA: Engar XML skrár fundust í {input_dir}")
        return []

    # Sía burtu stóru heildarskrárnar (aggregate / index files) og
    # lýsigagnaskrár (README). Heildarskrárnar eru samansteypur allra
    # texta í undirmöppunum og enda á sniðinu:
    #   IGC-News1-22.10.ana.xml
    #   IGC-Journals-22.10.xml
    #   IGC-Social-22.10.xml  /  IGC-Social2-22.10.xml
    # Einstakar skrár hafa ID-númer eða heimildarheiti, t.d.:
    #   IGC-News1-ruv_4208820.ana.xml     (2 bandstrik — einstök skrá)
    #   IGC-Journals-44-7567188.xml       (3 bandstrik — einstök skrá)
    #   IGC-Social2-silfuregils_5753180.xml
    #
    # Við síum út heildarskrárnar með reglulegri segð sem passar við
    # „IGC-<flokkur>-<útgáfunúmer>" munstur (þ.e. engin undirstrik eða
    # löng ID-númer eftir flokkunum).
    AGGREGATE_PATTERN = re.compile(
        r'^IGC-[A-Za-z0-9]+-\d+\.\d+(?:\.ana)?\.xml$'
    )
    xml_files = [
        f for f in xml_files
        if not AGGREGATE_PATTERN.match(f.name)
    ]

    # Sía einnig burtu README og lýsigagnaskrár
    xml_files = [f for f in xml_files if 'readme' not in f.name.lower()]

    print(f"  Fann {len(xml_files)} XML skrár í {input_dir.name}/")

    n_processed = 0
    for filepath in xml_files:
        if is_ana_xml(filepath):
            # .ana.xml: orð í <w> merkjum → lista af setningum
            sentences = extract_text_from_ana_xml(filepath)
            all_texts.extend(sentences)
        else:
            # Venjuleg .xml: texti í <p> merkjum → lista af málsgreinum
            paragraphs = extract_text_from_plain_xml(filepath)
            all_texts.extend(paragraphs)

        n_processed += 1
        if n_processed % 100 == 0:
            print(f"    Unnið {n_processed}/{len(xml_files)} skrár...")

    print(f"  Samtals: {len(all_texts)} setningar/málsgreinar")

    return all_texts


# ============================================================
# SKIPTA Í SETNINGAR / SPLIT INTO SENTENCES
# Málsgreinar úr plain .xml skrám geta innihaldið margar setningar.
# Þetta fall skiptir málsgreinum í einstakar setningar.
# ============================================================

def split_into_sentences(texts: list[str]) -> list[str]:
    """Skipta málsgreinum í einstakar setningar.

    Notar einfalda reglu: setning endar á punkti (.), spurningarmerki (?),
    eða upphrópunarmerki (!), ef næsti stafur er stór (upphafsstafur).

    Þetta er ekki fullkomin setningaskipting, en virkar vel fyrir
    flesta íslensku texta í RMH.

    ATHUGASEMD: .ana.xml skrár hafa þegar setningar í <s> merkjum,
    svo þessi aðferð er aðallega fyrir plain .xml skrár.

    Args:
        texts: Listi af strengjum (málsgreinar eða setningar).

    Returns:
        Listi af strengjum — ein setning per stak.
    """
    sentences = []

    for text in texts:
        # Skipta á stöðum þar sem setningarendamerki er fylgt af stafabili
        # og upphafsstaf.
        # Regluleg segð:
        #   ([.?!])  = setningarendamerki (hópur 1)
        #   \s+      = eitt eða fleiri bil
        #   (?=[A-ZÁÉÍÓÚÝÞÆÖÐ])  = lookahead: næsti stafur er stór
        #                           (íslenskir og enskir upphafsstafir)
        # re.split skilar bæði texta og endamerkinu, svo við þurfum
        # að sameina þau aftur.
        parts = re.split(r'([.?!])\s+(?=[A-ZÁÉÍÓÚÝÞÆÖÐ])', text)

        # Sameina endamerki aftur við setninguna
        # parts verður t.d. ['Hún fór', '.', 'Hann kom', '.', '']
        i = 0
        while i < len(parts):
            sentence = parts[i].strip()
            # Ef næsta stak er endamerki, bæta því við
            if i + 1 < len(parts) and parts[i + 1] in '.?!':
                sentence += parts[i + 1]
                i += 2
            else:
                i += 1

            if sentence:
                sentences.append(sentence)

    return sentences


# ============================================================
# BÚA TIL ÚRTÖK / CREATE SAMPLES
# Skiptir lista af setningum í ~2.000 orða búta.
# Aldrei klippt í miðri setningu.
# ============================================================

def create_samples(
    sentences: list[str],
    target_words: int = 2000,
    tolerance: float = 0.10,
) -> list[str]:
    """Skipta setningalista í úrtök af ~target_words stærð.

    REGLUR:
        1. Aldrei klippa í miðri setningu — hvert úrtak byrjar og endar
           á setningamörkum.
        2. Stefna á target_words ± tolerance.
        3. Ef setning myndi fara yfir target_words × (1 + tolerance),
           byrja nýtt úrtak.
        4. Ef lokaúrtak er of stutt (< target_words × 0.5), sameina
           það við fyrra úrtak.

    Args:
        sentences: Listi af setningum.
        target_words: Markmiðsorðafjöldi per úrtak (sjálfgefið 2000).
        tolerance: Leyfilegt frávik sem hlutfall (sjálfgefið 0.10 = 10%).

    Returns:
        Listi af strengjum — hvert úrtak er einn samfelldur texti.
    """
    if not sentences:
        return []

    samples = []
    current_sentences = []  # Setningar í núverandi úrtaki
    current_words = 0       # Orðafjöldi í núverandi úrtaki

    # Hámarksfjöldi orða áður en nýtt úrtak byrjar
    max_words = int(target_words * (1 + tolerance))

    for sentence in sentences:
        # Telja orð í þessari setningu
        word_count = len(sentence.split())

        # Ef þessi setning myndi fara yfir hámark OG við höfum nú þegar
        # eitthvað í úrtakinu, byrja nýtt úrtak
        if current_words + word_count > max_words and current_sentences:
            # Vista núverandi úrtak
            sample_text = ' '.join(current_sentences)
            samples.append(sample_text)
            current_sentences = []
            current_words = 0

        # Bæta setningu við núverandi úrtak
        current_sentences.append(sentence)
        current_words += word_count

    # Vista síðasta úrtak
    if current_sentences:
        sample_text = ' '.join(current_sentences)
        last_word_count = len(sample_text.split())

        # Ef síðasta úrtakið er of stutt (< 50% af markmiði),
        # sameina við fyrra úrtak ef til er
        if last_word_count < target_words * 0.5 and samples:
            samples[-1] = samples[-1] + ' ' + sample_text
        else:
            samples.append(sample_text)

    return samples


# ============================================================
# VISTA ÚRTÖK / SAVE SAMPLES
# Skrifa hvert úrtak í sína .txt skrá.
# ============================================================

def save_samples(
    samples: list[str],
    output_dir: Path,
    category: str,
) -> list[dict]:
    """Vista úrtök sem einstakar .txt skrár.

    Skráarheiti: {category}_001.txt, {category}_002.txt, o.s.frv.

    Args:
        samples: Listi af textaúrtökum (strengir).
        output_dir: Mappa til að vista í.
        category: Textategund (t.d. "news", "academic", "blog").

    Returns:
        Listi af dict með upplýsingum um hvert úrtak:
            - filename: skráarheiti
            - words: orðafjöldi
    """
    # Búa til úttaksmöppu ef hún er ekki til
    output_dir.mkdir(parents=True, exist_ok=True)

    sample_info = []

    for i, sample_text in enumerate(samples, start=1):
        # Skráarheiti: category_001.txt, category_002.txt, ...
        filename = f"{category}_{i:03d}.txt"
        filepath = output_dir / filename

        # Skrifa texta í skrá
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sample_text + '\n')

        word_count = len(sample_text.split())
        sample_info.append({
            'filename': filename,
            'words': word_count,
        })

    return sample_info


# ============================================================
# PRENTA SAMANTEKT / PRINT SUMMARY
# ============================================================

def print_summary(sample_info: list[dict], category: str) -> None:
    """Prenta samantekt um úrtökin.

    Args:
        sample_info: Listi af dict frá save_samples.
        category: Textategund.
    """
    if not sample_info:
        print(f"  AÐVÖRUN: Engin úrtök búin til fyrir {category}")
        return

    word_counts = [s['words'] for s in sample_info]
    total = sum(word_counts)
    mean_wc = total / len(word_counts)
    min_wc = min(word_counts)
    max_wc = max(word_counts)

    print(f"\n  SAMANTEKT: {category}")
    print(f"  {'─' * 40}")
    print(f"  Fjöldi úrtaka: {len(sample_info)}")
    print(f"  Heildarorðafjöldi: {total:,}")
    print(f"  Meðalfjöldi orða: {mean_wc:.0f}")
    print(f"  Lágmark: {min_wc}")
    print(f"  Hámark: {max_wc}")
    print()

    # Sýna hvert úrtak
    for s in sample_info:
        print(f"    {s['filename']}: {s['words']:,} orð")


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Aðalfall: Draga út og skipta texta úr RMH XML skrám."""
    parser = argparse.ArgumentParser(
        description="Draga út textaúrtök úr RMH TEI XML skrám.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi um keyrslu:
  # Fréttir (RÚV) — .ana.xml snið
  python scripts/extract_samples.py \\
      --input-dir data/raw/IGC-News1_22.10/IGC-News1-22.10.ana/ruv/ \\
      --output-dir data/human_texts/news/ \\
      --category news \\
      --target-words 2000

  # Fræðitímarit (Læknablaðið) — plain .xml snið
  python scripts/extract_samples.py \\
      --input-dir data/raw/IGC-Journals-22.10.TEI/lb/ \\
      --output-dir data/human_texts/academic/ \\
      --category academic \\
      --target-words 2000

  # Blogg (Jonas.is) — plain .xml snið
  python scripts/extract_samples.py \\
      --input-dir data/raw/IGC-Social-22.10.TEI/Blog/jonas/ \\
      --output-dir data/human_texts/blog/ \\
      --category blog \\
      --target-words 2000
        """
    )
    parser.add_argument(
        '--input-dir',
        type=Path,
        required=True,
        help="Mappa með RMH XML skrám (leit er endurkvæm)"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        required=True,
        help="Mappa til að vista hrein textaúrtök í"
    )
    parser.add_argument(
        '--category',
        type=str,
        default=None,
        help="Textategund til skráarheita (t.d. 'news', 'academic', 'blog'). "
             "Ef ekki tilgreind, leidd af úttaksmöppu."
    )
    parser.add_argument(
        '--target-words',
        type=int,
        default=2000,
        help="Markmiðsorðafjöldi per úrtak (sjálfgefið: 2000)"
    )
    parser.add_argument(
        '--tolerance',
        type=float,
        default=0.10,
        help="Leyfilegt frávik frá markmiði sem hlutfall (sjálfgefið: 0.10 = 10%%)"
    )

    args = parser.parse_args()

    # Ákvarða textategund
    category = args.category or args.output_dir.name

    print("=" * 60)
    print(f"TEXTAÚTDRÁTTUR ÚR RMH / RMH TEXT EXTRACTION")
    print("=" * 60)
    print(f"  Inntak: {args.input_dir}")
    print(f"  Úttak: {args.output_dir}")
    print(f"  Textategund: {category}")
    print(f"  Markmiðsorðafjöldi: {args.target_words}")
    print(f"  Vikmörk: ±{args.tolerance:.0%}")
    print()

    # --- SKREF 1: Lesa alla texta úr XML ---
    print("SKREF 1: Les texta úr XML skrám...")
    texts = read_all_texts(args.input_dir)

    if not texts:
        print("VILLA: Enginn texti fannst. Athugaðu slóðina.")
        sys.exit(1)

    # --- SKREF 2: Skipta í setningar ---
    print("\nSKREF 2: Skipti í setningar...")
    sentences = split_into_sentences(texts)
    total_words = sum(len(s.split()) for s in sentences)
    print(f"  {len(sentences)} setningar, {total_words:,} orð alls")

    # --- SKREF 3: Búa til úrtök ---
    print(f"\nSKREF 3: Bý til ~{args.target_words} orða úrtök...")
    samples = create_samples(
        sentences,
        target_words=args.target_words,
        tolerance=args.tolerance,
    )
    print(f"  {len(samples)} úrtök búin til")

    # --- SKREF 4: Vista ---
    print(f"\nSKREF 4: Vista í {args.output_dir}/...")
    sample_info = save_samples(samples, args.output_dir, category)

    # --- SKREF 5: Samantekt ---
    print_summary(sample_info, category)

    print(f"\n{'=' * 60}")
    print("LOKIÐ!")
    print("=" * 60)


if __name__ == "__main__":
    main()
