#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
dim8_bin_ratio.py — VÍDD 8: BÍN-orðaforðadekkun (BÍN vocabulary coverage)
==========================================================================

TILGANGUR / PURPOSE:
    Þessi skrifta mælir hlutfall tóka í textaskrá sem finnast í BÍN
    (Beygingarlýsingu íslensks nútímamáls). Mælingin grípur bæði stílbreytileika
    (fræðitextar með mikið af íðorðum, fréttir með mörg sérnöfn, blogg með
    óformlegt mál) OG gæðavandamál mállíkana (íslenskuleg orð sem eru ekki til,
    þ.e. skynvilluorð / hallucinations).

    This script measures the ratio of tokens in a text file that are found in
    BÍN (Database of Icelandic Morphology). The measurement captures BOTH
    stylistic variation (academic texts heavy in technical compounds, news
    with proper names, blogs with informal spellings) AND LLM quality failures
    (Icelandic-looking but non-existent words — hallucinations).

MÁLVÍSINDI / LINGUISTICS:
    BÍN (Beygingarlýsing íslensks nútímamáls) er staðlað beygingarlíkan fyrir
    íslensku, gefið út af Stofnun Árna Magnússonar. Það inniheldur um 300.000
    uppflettiorð (lemmur) með öllum beygingarmyndum. `islenska` pakkinn
    (Miðeind) veitir flettiaðgang og býður einnig upp á samsetningargreiningu
    fyrir samsett orð sem ekki eru í grunnskrá.

    FJÖGURRA ÞREPA FLOKKUN / FOUR-WAY CLASSIFICATION:
        exact       — fannst í BÍN (en ekki sérnafn)
        compound    — leyst með samsetningarreikniriti BÍN (bmynd inniheldur
                      bandstrik sem inntakið hefur ekki)
        proper_name — sérnöfn (hluti ∈ {ism, föð, móð, örn, göt, fyr, erm,
                      bibl, lönd, þor})
        oov         — fannst ekki í BÍN (out-of-vocabulary)

    OOV ÁGISKANIR / OOV GUESSES (í detail CSV):
        foreign              — inniheldur c/q/w (aldrei staðlaðir í íslensku)
        archaic_icelandic    — inniheldur z OG nútímamynd (z→s) finnst í BÍN.
                               Ráðgjöf: staðfest forn-íslensk stafsetning fyrir
                               1973–74 réttritunarbreytinguna (sbr. Íslenska
                               réttritunarorðabókin; Ritreglur 1929). Dæmi:
                               „verzlun“ → „verslun“ (sem er í BÍN).
        archaic_z_unverified — inniheldur z EN nútímamynd (z→s) er ekki
                               í BÍN. Líklega erlent sérnafn (Zoëga, Sarkozy)
                               eða tökuorð. Ekki staðfest íslensk fornleikur.
        likely_proper_name   — hástafur í miðri setningu
        unknown              — ekki hægt að ágiska

    HVERS VEGNA 4-ÞREPA FLOKKUN EN EKKI BARA TVEGGJA:
        Hlutfall orða sem finnast í BÍN er ekki einhlít vísbending. Mannlegur
        fræðitexti getur haft 5% „oov“ orð sem eru lögmæt íðorð, og fréttir
        geta haft 10% sérnöfn sem skekkja hrátt „in_bin_ratio“. Með því að
        greina á milli tegunda fáum við að sjá HVERS VEGNA hlutfall er eins og
        það er — og getum greint á milli stílbreytileika og gæðavandamála.

    EFTIRVÆNTAR MYNSTUR / EXPECTED PATTERNS:
        Fræðitextar (Læknablaðið): MIÐLUNGS-HÁTT compound_ratio (íðorð eru
            lögmæt samsett orð — BÍN leysir þau með samsetningarreiknirit)
        Fréttir (RÚV): HÆSTA proper_name_ratio (mannanöfn, staðir)
        Blogg (Jonas.is): HÆSTA oov_ratio (óformleg ritun, slettur, slangur)
        Ransakhugsuð LLM-úttak: HÁTT oov_ratio, LÁGT proper_name_ratio

AÐFERÐ / METHOD:
    1. Lesa texta úr .txt skrám
    2. Tóka á sama hátt og dim6 (skipta á bili/whitespace, 
       fjarlægja greinarmerki í köntum,
       sleppa tókum án bókstafs)
    3. Fletta hverjum tóka fyrir sig upp í BÍN 
       (reyna upprunalega stafsetningu, þá lágstaf)
    4. Flokka tókann sem exact/compound/proper_name/oov
    5. Vista samantekt (ein lína per skrá) og nákvæma tákn-fyrir-tákn skrá
       (ein lína per tóka)

TÓKASKIPTING / TOKENIZATION:
    Notum `PUNCT_TO_STRIP` og `HAS_LETTER` úr `dim6_word_length` — sama
    tóki = sama orð. Þetta tryggir að BÍN-dekkun og meðalorðalengd séu reiknuð
    á nákvæmlega sama úrtaki orða.

ARKITEKTÚR — ÞÁTTA-EINU-SINNI / PARSE-ONCE CACHING:
    BÍN-flettun er ekki dýr (~150k flettiuppsláttir á nokkrum sekúndum), en það 
    tekur tíma fyrir 'islenska'-pakkann hlaðast í minnið. Þessi skrifta keyrir allar
    flettingar EINU SINNI og skrifar niðurstöður í CSV. run_milicka.py les
    CSV-skrána beint og flettir ekki neinu — þannig þarf ekki að nota 'islenska'-
    pakkann ef búið er að forvinna textann, það er aðeins nauðsynleg þegar dim8 er keyrt.

INNTAK / INPUT:
    Textaskrár (.txt) — t.d. úr:
        data/human_texts/
        data/experiment/human_reference/
        data/experiment/llm_continuations_clean/

ÚTTAK / OUTPUT:
    1. Samantekt: output/dim8_bin_summary.csv
         Ein lína per skrá — með talningum og hlutföllum.
         Aðaldálkur fyrir Milička: in_bin_ratio.
         Viðbótardálkar:
           archaic_icelandic_count / archaic_icelandic_ratio
             (staðfest forn-íslensk z-stafsetning — z→s mynd í BÍN)
           archaic_z_unverified_count / archaic_z_unverified_ratio
             (z-tóki án staðfestingar — líklega erlent sérnafn/tökuorð)
    2. Ítargögn: output/dim8_bin_detail.csv
         Ein lína per tóka — filename, token_index, token, cleaned,
         status, word_class, lemma, oov_guess.
         Stór skrá (~hundruð þúsunda lína) en ómetanleg fyrir villugreiningu,
         sérstaklega við að finna ranghugsuð orð í gervigreindarúttaki.
         oov_guess ∈ {foreign, archaic_icelandic, archaic_z_unverified,
                      likely_proper_name, unknown}.

KEYRSLA / USAGE:
    python scripts/dim8_bin_ratio.py --text-dir data/experiment/human_reference/
    python scripts/dim8_bin_ratio.py --text-dir data/experiment/llm_continuations_clean/gpt_5/
    python scripts/dim8_bin_ratio.py --files file1.txt file2.txt
    python scripts/dim8_bin_ratio.py --text-dir ... --dry-run
    python scripts/dim8_bin_ratio.py --text-dir ... --debug
    python scripts/dim8_bin_ratio.py --text-dir ... --no-detail

    # Sem innflutt eining:
    from dim8_bin_ratio import measure_bin_coverage
    result = measure_bin_coverage(Path("data/experiment/human_reference/news_ref_001.txt"))
"""

import argparse
import csv
import re
import sys
from pathlib import Path

# Endurnýtum tókaskiptingarreglur úr dim6 svo þær séu nákvæmlega eins
# Reuse tokenization rules from dim6 so they are identical across dims
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dim6_word_length import PUNCT_TO_STRIP, HAS_LETTER


# ============================================================
# LEIÐBEININGARLÍNA Í SKIPANASKRÁM / PROMPT INSTRUCTION LINE
# ============================================================
# Sömu leiðbeiningar og í run_milicka.py og parse_texts.py. Þessi lína
# er ekki hluti mannlegs texta og þarf að fjarlægja áður en BÍN-dekkun
# er mæld á skipanaskrám. Annars bjagast in_bin_ratio upp á móti fyrir
# skipun en ekki mennski viðmiðunartextinn — sem skekkir SE-útreikning.
#
# AF HVERJU HÉR OG EKKI BARA Í run_milicka.py?
#   dim8 er „parse-once“ skrifta — hún er keyrð einu sinni og CSV er
#   cachað. run_milicka les bara úr CSV og getur ekki lengur strippað.
#   Því verður dim8 sjálft að fjarlægja leiðbeininguna áður en mælt er.
#   Þetta er EINA dim-skriftan sem þarf að vita um þessa línu.
# ============================================================

PROMPT_INSTRUCTION = (
    "Haltu áfram með textann á sama hátt og í sama stíl og sjáðu til þess "
    "að hann innihaldi að minnsta kosti tvö þúsund orð. Textinn þarf ekki "
    "að innihalda réttar staðreyndir en gættu þess að hann passi við stílinn:"
)


# ============================================================
# BÍN-FLOKKAR FYRIR SÉRNÖFN / BIN PROPER-NAME CATEGORIES
# ============================================================
# Í BÍN eru sérnöfn auðkennd með „hluti“-reitnum. Eftirfarandi
# flokkar eru sérnöfn:
#   ism  — íslensk mannanöfn (eiginnöfn: Jón, Guðrún)
#   föð  — föðurnöfn (Jónsson, Guðmundsdóttir)
#   móð  — móðurnöfn (Katrínardóttir, Steinuson)
#   örn  — örnefni (staðanöfn innan sveitar: Þingvellir)
#   göt  — götunöfn (Laugavegur, Skólavörðustígur)
#   fyr  — fyrirtækjanöfn (Landsbankinn)
#   erm  — erlend mannanöfn (Barack, Angela)
#   bibl — biblíunöfn (Móses, María)
#   lönd — landaheiti (Ísland, Þýskaland)
#   þor  — þorpa- og bæjarnöfn (Reykjavík, Akureyri)
#
# „alm“ (almennt) og „sérn“ eru ekki flokkuð í þennan flokk.
# ============================================================

PROPER_NAME_HLUTI = frozenset({
    'ism', 'föð', 'móð', 'örn', 'göt',
    'fyr', 'erm', 'bibl', 'lönd', 'þor',
})


# Tóka-staða / Token status values
STATUS_EXACT = 'exact'
STATUS_COMPOUND = 'compound'
STATUS_PROPER_NAME = 'proper_name'
STATUS_OOV = 'oov'


# c, q, w eru aldrei staðlaðir íslenskir stafir — nærvera bendir til
# tökuorða eða erlendra sérnafna.
# c, q, w are never native Icelandic letters. Presence suggests loanwords
# or foreign proper names.
NON_ICELANDIC_LETTERS = re.compile(r'[cqwCQW]')

# z var staðlað íslenskt ritmál fram að réttritunarbreytingunni 1973–74.
# Nærvera í OOV-tóka bendir til fornleiks eða hefðarhyggju í stafsetningu.
# ATHUGIÐ: z-orð sem héldu sér í notkun eftir breytinguna (t.d. „verzlun“)
# eru í BÍN og flokkast sem `exact` — þessi heuristic sér þau aldrei.
# z was standard Icelandic orthography until the 1973–74 spelling reform.
# Presence in an OOV token suggests archaic/traditionalist spelling.
# NOTE: z-words that remained in use after the reform (e.g. `verzlun`) are
# in BÍN and classified as `exact` — they never reach this heuristic.
ARCHAIC_Z = re.compile(r'[zZ]')


# ============================================================
# BIN-SINGLETON / BIN-SINGLETON
# Hlöðum 'islenska' aðeins EINU SINNI og endurnotum fyrir allar
# flettingar. islenska.Bin() er erfitt í upphafi en auðvelt í notkun.
# ============================================================

_BIN_INSTANCE = None


def _get_bin():
    """Skila staka BÍN-hlut (lazy-initialized).

    Við hlaðum islenska aðeins þegar þörf er á — tryggir að
    innflutningur dim8_bin_ratio.py sé ódýr og að villuskilaboð
    birtist aðeins ef notandi keyrir í raun á BÍN-flettingu.
    """
    global _BIN_INSTANCE
    if _BIN_INSTANCE is None:
        try:
            from islenska import Bin
        except ImportError as e:
            raise ImportError(
                "islenska pakkinn er nauðsynlegur fyrir dim8. "
                "Settu upp með: pip install islenska"
            ) from e
        _BIN_INSTANCE = Bin()
    return _BIN_INSTANCE


# ============================================================
# TÓKASKIPTING / TOKENIZATION
# Endurtökum dim6-aðferð: split, strip, filter. Skilum báðum
# (raw, cleaned) svo ítarskráin geti sýnt hvort tveggja.
# ============================================================

def tokenize(text: str) -> list[tuple[str, str]]:
    """Skipta texta í (hrátt_tóki, hreinsaður_tóki) pör.

    NOTAR sömu reglur og dim6_word_length.tokenize_and_measure:
      1. Skipta á hvítbili
      2. Fjarlægja kantamerki með PUNCT_TO_STRIP
      3. Sleppa tómum strengjum og tókum án bókstafs (HAS_LETTER)

    Args:
        text: Hráður texti.

    Returns:
        Listi af (raw, cleaned) pörum fyrir gild orð.
    """
    pairs: list[tuple[str, str]] = []
    for raw in text.split():
        cleaned = raw.strip(PUNCT_TO_STRIP)
        if not cleaned:
            continue
        if not HAS_LETTER.search(cleaned):
            continue
        pairs.append((raw, cleaned))
    return pairs


# ============================================================
# BÍN-FLETTING / BIN LOOKUP
# ============================================================

def _lookup_bin(token: str, bin_obj) -> tuple[list, str]:
    """Fletta tóka upp í BÍN með tveimur tilraunum.

    REGLUR:
        1. Prófa upprunalega stafsetningu fyrst (varðveitir hástaf — BÍN
           greinir á milli sérnafna og samnafna með stórum/litlum staf).
        2. Ef tómt, prófa lágstaf (nær þá almennum orðum sem voru
           hástafaður, t.d. í byrjun setningar).

    Args:
        token: Hreinsaður tóki (eftir kantamerki-fjarlægingu).
        bin_obj: islenska.Bin hlutur.

    Returns:
        Tuple (meanings, used_form) — listi af BinEntry og hvaða form
        gaf smell (upprunalegt eða lágstaf). Ef tómt, meanings er [].
    """
    _, meanings = bin_obj.lookup(token)
    if meanings:
        return meanings, token

    # Reyna lágstaf — BÍN getur hafnað hástafaða útgáfu ef orðið er í
    # raun almennt nafnorð í byrjun setningar.
    lower = token.lower()
    if lower != token:
        _, meanings = bin_obj.lookup(lower)
        if meanings:
            return meanings, lower

    return [], token


def classify_token(
    token: str,
    bin_obj,
) -> tuple[str, str, str]:
    """Flokka einn tóka í eina af fjórum stöðum.

    FLOKKUNARREGLUR:
        1. Engin meanings → STATUS_OOV
        2. First meaning's hluti er í PROPER_NAME_HLUTI → STATUS_PROPER_NAME
        3. Samsetningargreining greind (fleiri „-“ í bmynd en í inntaki)
           → STATUS_COMPOUND
        4. Annars → STATUS_EXACT

    AÐGERÐ VIÐ MARGRÆÐNI:
        BÍN getur skilað mörgum merkingum fyrir sama orð (mismunandi föll,
        kyn, o.fl.). Við notum fyrstu merkinguna til flokkunar, sem er
        venjulega NEFNIFALL EINTALA (NFET) eða önnur „grunnmynd“. Í
        flestum tilfellum er öll meanings-listinn með sömu `hluti` (sama
        orð), svo þetta er ekki áhyggjuefni. Undantekning: orð sem eru
        bæði mannanafn og almennt orð (t.d. „Björn“ sem nafn og samnafn
        fyrir bjarndýr) — hér getur meanings-listinn blandast. Við veljum
        fyrstu merkinguna sem BÍN skilar, sem í reynd er algengasta/
        líklegasta.

    Args:
        token: Hreinsaður tóki.
        bin_obj: islenska.Bin hlutur.

    Returns:
        Tuple (status, word_class, lemma)
            status: Ein af 'exact', 'compound', 'proper_name', 'oov'
            word_class: BÍN-orðflokkur (no, so, lo, ism, ...) eða tómt
            lemma: ord-reitur (uppflettiform) eða hrátt tóki fyrir oov
    """
    meanings, used_form = _lookup_bin(token, bin_obj)

    if not meanings:
        return STATUS_OOV, '', token

    first = meanings[0]
    hluti = first.hluti
    ofl = first.ofl
    bmynd = first.bmynd
    ord_ = first.ord

    # Orðflokkur sem birtist í detail CSV er samsett af (ofl, hluti):
    # venjulega tökum við ofl („no“, „so“, „lo“) en fyrir sérnöfn er
    # hluti upplýsandara („ism“ etc). Notum hluti fyrir sérnöfn,
    # ofl annars.
    if hluti in PROPER_NAME_HLUTI:
        return STATUS_PROPER_NAME, hluti, ord_

    # Samsetningargreining: BÍN setur bandstrik í bmynd til að sýna
    # samsetningargrein. Ef bmynd hefur FLEIRI bandstrik en inntakið
    # hafði, þá var orðið leyst með samsetningarreiknirit.
    # Dæmi: inntak „heilbrigðisþjónustukerfi“ (0 strik) →
    #        bmynd „heilbrigðis-þjónustukerfi“ (1 strik)
    # Dæmi: inntak „Nýju-Delí“ (1 strik) →
    #        bmynd „Nýju-Delí“ (1 strik) — EKKI compound, strikið
    #        var í inntakinu.
    bmynd_hyphens = bmynd.count('-')
    input_hyphens = used_form.count('-')
    if bmynd_hyphens > input_hyphens:
        return STATUS_COMPOUND, ofl, ord_.replace('-', '')

    return STATUS_EXACT, ofl, ord_


# ============================================================
# OOV ÁGISKUNAR-HEURISTICS / OOV GUESS HEURISTICS
# Fyrir orð sem ekki finnast í BÍN — ágiskun um tegund sem getur
# hjálpað við villugreiningu. Aðeins ráðgjafargildi, ekki vísindaleg
# flokkun. Birtist í detail CSV.
# ============================================================

def verify_archaic_z(token: str, bin_obj) -> tuple[bool, str]:
    """Prófa hvort z-tóki sé staðfestur forn-íslensk stafsetning.

    AÐFERÐ:
        1. Skipta z→s og Z→S í tókanum (varðveita hástaf). Þetta er
           heildarreglan fyrir 1973–74 réttritunarbreytinguna: z var
           skipt út fyrir s hvar sem hún kom fyrir. Engin etymólógísk
           endurgerð (ts/ds/ðs) var gerð í staðlinum — bein strengbreyting
           er rétta módelið.
        2. Fletta nútímamyndinni upp í BÍN með sömu upp/lágstafs-fallback
           og aðalflettingin.
        3. Ef BÍN skilar niðurstöðum → staðfest forn-mynd (z→s er raunverulegt
           íslenskt orð). Annars → líklega erlent sérnafn eða tökuorð.

    Args:
        token: Hreinsaður tóki (með z/Z).
        bin_obj: islenska.Bin hlutur (endurnýtt staka-tilvik).

    Returns:
        Tuple (verified, modernized_form)
            verified: True ef nútímamyndin er í BÍN.
            modernized_form: z→s formaðið (til villuleitar/sýnishorns).
    """
    modernized = token.replace('z', 's').replace('Z', 'S')
    meanings, _ = _lookup_bin(modernized, bin_obj)
    return bool(meanings), modernized


def guess_oov_class(
    raw_token: str,
    cleaned: str,
    token_index: int,
    bin_obj,
) -> str:
    """Ágiska flokk fyrir OOV-tóka.

    FORGANGSREGLA / PRIORITY:
        1. Inniheldur c/q/w (aldrei-íslenskir stafir) → „foreign“
        2. Inniheldur z OG z→s mynd er í BÍN → „archaic_icelandic“
        3. Inniheldur z EN z→s mynd er EKKI í BÍN → „archaic_z_unverified“
        4. Byrjar á hástaf og er EKKI fyrsti tóki → „likely_proper_name“
        5. Annars → „unknown“

    RÖKSTUÐNINGUR FORGANGS:
        Tóki sem inniheldur BÆÐI z og c (ólíklegt en mögulegt í erlendum
        umritunum) skal merkjast „foreign“, ekki „archaic“. c/q/w eru
        afdráttarlausari merki um ekki-íslenskt uppruna en z.

        Staðfesting (þrep 2 vs 3): z→s prófunin er einföld en áreiðanleg.
        Raunverulegur fornleikur (t.d. „verzlun“, „þjóðhátíð hafizt“)
        breytist í nútímamynd sem er í BÍN. Erlend sérnöfn (Zoëga, Sarkozy)
        gera það ekki. Þetta eyðir helsta falsjákvæða mynstri — erlendum
        nöfnum sem slumpast á z-ið í stafsetningu.

    Args:
        raw_token: Hrár tóki (með kantamerki).
        cleaned: Hreinsaður tóki.
        token_index: Staðsetning tóka í skjali (0-byggt).
        bin_obj: islenska.Bin hlutur (fyrir z→s staðfestingu).

    Returns:
        Strengur með ágiskun.
    """
    if NON_ICELANDIC_LETTERS.search(cleaned):
        return 'foreign'

    # z í OOV-tóka: staðfesta með z→s flettiuppfærslu. Ef nútímamyndin
    # er í BÍN þá er þetta sannarlega fornleg íslensk stafsetning. Annars
    # er þetta líklega erlent sérnafn eða tökuorð með z.
    if ARCHAIC_Z.search(cleaned):
        verified, _ = verify_archaic_z(cleaned, bin_obj)
        if verified:
            return 'archaic_icelandic'
        return 'archaic_z_unverified'

    # Hástafi-í-miðri-setningu: ef orðið byrjar á hástaf en er ekki
    # allra-fyrsti tókinn, þá er það líklega sérnafn sem BÍN þekkir
    # ekki.
    if token_index > 0 and cleaned[0].isupper():
        return 'likely_proper_name'

    return 'unknown'


# ============================================================
# AÐALMÆLING / MAIN MEASUREMENT
# ============================================================

def measure_bin_coverage(
    text_file: Path,
    collect_detail: bool = True,
    debug: bool = False,
) -> tuple[dict, list[dict]]:
    """Mæla BÍN-orðaforðaþekju í einni textaskrá.

    MÆLINGAR:
        - total_words: Heildarfjöldi gildra tóka
        - exact_count, compound_count, proper_name_count, oov_count
        - in_bin_ratio: (exact + compound + proper_name) / total
        - exact_ratio, compound_ratio, proper_name_ratio, oov_ratio
        - archaic_icelandic_count: OOV-tókar með z OG z→s mynd í BÍN
          (staðfest forn-íslensk stafsetning — stílvísir)
        - archaic_icelandic_ratio: archaic_icelandic_count / total_words
        - archaic_z_unverified_count: OOV-tókar með z EN z→s mynd ekki
          í BÍN (líklega erlent sérnafn/tökuorð)
        - archaic_z_unverified_ratio: archaic_z_unverified_count / total_words

    ATH: báðir z-flokkar eru UNDIRMENGI oov — tökin teljast áfram sem oov.
    in_bin_ratio breytist EKKI. archaic_icelandic_ratio er stílvísir, ekki
    gæðavandamál. archaic_z_unverified_ratio bendir oftast á erlend
    sérnöfn í textanum.

    Args:
        text_file: Slóð á .txt skrá.
        collect_detail: Ef True, skilar líka lista af detail-röðum
            (ein per tóki). Ef False, detail-listinn er tómur.
        debug: Prenta villuleitarupplýsingar og fyrstu 20 OOV-tóka.

    Returns:
        Tuple (summary_dict, detail_rows)
            summary_dict: Aðalmælingar.
            detail_rows: Listi af dict með lyklum filename, token_index,
                token, cleaned, status, word_class, lemma, oov_guess.
    """
    if not text_file.exists():
        raise FileNotFoundError(f"Textaskrá fannst ekki: {text_file}")

    text = text_file.read_text(encoding='utf-8').lstrip()

    # Fjarlægja leiðbeiningarlínu ef þetta er skipanaskrá. Sama hegðun
    # og í dim6 gegnum run_milicka.measure_word_length_stripped, nema
    # hér inni í dim8 svo cache-lögun (parse-once) virki fyrir skipanir.
    if text.startswith(PROMPT_INSTRUCTION):
        text = text[len(PROMPT_INSTRUCTION):].lstrip()

    pairs = tokenize(text)

    bin_obj = _get_bin()

    # Teljarar fyrir samantekt
    n_exact = 0
    n_compound = 0
    n_proper = 0
    n_oov = 0
    n_archaic_ice = 0  # undirmengi oov: staðfest forn-íslensk z
    n_archaic_unv = 0  # undirmengi oov: z án BÍN-staðfestingar

    detail_rows: list[dict] = []
    oov_examples: list[str] = []  # Fyrir --debug
    # Dæmi til debug-útskrifta. Fyrir staðfest geymum við líka nútímamyndina
    # (z→s) til að sýna notanda hver staðfestingarmyndin var.
    archaic_ice_examples: list[tuple[str, str]] = []  # (tóki, z→s mynd)
    archaic_unv_examples: list[str] = []

    for idx, (raw, cleaned) in enumerate(pairs):
        status, word_class, lemma = classify_token(cleaned, bin_obj)

        if status == STATUS_EXACT:
            n_exact += 1
            oov_guess = ''
        elif status == STATUS_COMPOUND:
            n_compound += 1
            oov_guess = ''
        elif status == STATUS_PROPER_NAME:
            n_proper += 1
            oov_guess = ''
        else:  # OOV
            n_oov += 1
            oov_guess = guess_oov_class(raw, cleaned, idx, bin_obj)
            if oov_guess == 'archaic_icelandic':
                n_archaic_ice += 1
                # Endurreikna nútímamyndina fyrir debug-sýnishorn. Þetta
                # er ódýrt (ein strengbreyting) og forðast að skila auka-
                # gildi út úr guess_oov_class.
                _, modernized = verify_archaic_z(cleaned, bin_obj)
                archaic_ice_examples.append((cleaned, modernized))
            elif oov_guess == 'archaic_z_unverified':
                n_archaic_unv += 1
                archaic_unv_examples.append(cleaned)
            if len(oov_examples) < 20:
                oov_examples.append(f"{cleaned} ({oov_guess})")

        if collect_detail:
            detail_rows.append({
                'filename': text_file.name,
                'token_index': idx,
                'token': raw,
                'cleaned': cleaned,
                'status': status,
                'word_class': word_class,
                'lemma': lemma,
                'oov_guess': oov_guess,
            })

    total = len(pairs)

    # --- REIKNA HLUTFÖLL ---
    if total > 0:
        exact_ratio = n_exact / total
        compound_ratio = n_compound / total
        proper_ratio = n_proper / total
        oov_ratio = n_oov / total
        in_bin_ratio = (n_exact + n_compound + n_proper) / total
        archaic_ice_ratio = n_archaic_ice / total
        archaic_unv_ratio = n_archaic_unv / total
    else:
        exact_ratio = compound_ratio = proper_ratio = oov_ratio = 0.0
        in_bin_ratio = 0.0
        archaic_ice_ratio = 0.0
        archaic_unv_ratio = 0.0

    # Stutt-skráar viðvörun (spec: total_words < 50)
    if 0 < total < 50:
        print(
            f"  AÐVÖRUN: {text_file.name} hefur aðeins {total} orð — "
            f"niðurstöður óáreiðanlegar fyrir stutta texta."
        )

    if debug:
        print(f"\n  [DEBUG] Skrá: {text_file.name}")
        print(f"  [DEBUG] Heildarfjöldi tóka: {total}")
        print(
            f"  [DEBUG] exact={n_exact} ({exact_ratio:.1%}), "
            f"compound={n_compound} ({compound_ratio:.1%}), "
            f"proper_name={n_proper} ({proper_ratio:.1%}), "
            f"oov={n_oov} ({oov_ratio:.1%})"
        )
        print(f"  [DEBUG] in_bin_ratio = {in_bin_ratio:.4f}")
        if oov_examples:
            print(f"  [DEBUG] Fyrstu {len(oov_examples)} OOV-tókar:")
            for ex in oov_examples:
                print(f"  [DEBUG]   • {ex}")

    summary = {
        'filename': text_file.name,
        'total_words': total,
        'exact_count': n_exact,
        'compound_count': n_compound,
        'proper_name_count': n_proper,
        'oov_count': n_oov,
        'archaic_icelandic_count': n_archaic_ice,
        'archaic_z_unverified_count': n_archaic_unv,
        'in_bin_ratio': in_bin_ratio,
        'exact_ratio': exact_ratio,
        'compound_ratio': compound_ratio,
        'proper_name_ratio': proper_ratio,
        'oov_ratio': oov_ratio,
        'archaic_icelandic_ratio': archaic_ice_ratio,
        'archaic_z_unverified_ratio': archaic_unv_ratio,
        # Undirstrik-lyklar: sleppa við CSV-DictWriter vegna
        # extrasaction='ignore'. Notað í main() til að prenta
        # debug-sýnishorn þvert á skrár.
        '_archaic_ice_examples': archaic_ice_examples,
        '_archaic_unv_examples': archaic_unv_examples,
    }

    return summary, detail_rows


# ============================================================
# VISTA NIÐURSTÖÐUR SEM CSV / SAVE RESULTS AS CSV
# ============================================================

SUMMARY_FIELDS = [
    'filename',
    'total_words',
    'exact_count',
    'compound_count',
    'proper_name_count',
    'oov_count',
    'archaic_icelandic_count',
    'archaic_z_unverified_count',
    'in_bin_ratio',
    'exact_ratio',
    'compound_ratio',
    'proper_name_ratio',
    'oov_ratio',
    'archaic_icelandic_ratio',
    'archaic_z_unverified_ratio',
]

DETAIL_FIELDS = [
    'filename',
    'token_index',
    'token',
    'cleaned',
    'status',
    'word_class',
    'lemma',
    'oov_guess',
]


def save_summary_csv(
    results: list[dict],
    output_path: Path,
) -> None:
    """Vista samantektarniðurstöður (ein lína per skrá).

    Args:
        results: Listi af summary-dict frá measure_bin_coverage.
        output_path: Slóð á CSV-skrá.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        # extrasaction='ignore' — sleppir undirstriksveitum eins og
        # `_archaic_ice_examples` sem aðeins eru notaðir fyrir debug í main().
        writer = csv.DictWriter(
            f, fieldnames=SUMMARY_FIELDS, extrasaction='ignore'
        )
        writer.writeheader()
        for row in results:
            row_out = dict(row)
            # Slétta hlutföll til 6 aukastafa
            for key in (
                'in_bin_ratio', 'exact_ratio', 'compound_ratio',
                'proper_name_ratio', 'oov_ratio',
                'archaic_icelandic_ratio', 'archaic_z_unverified_ratio',
            ):
                row_out[key] = f"{row[key]:.6f}"
            writer.writerow(row_out)


def save_detail_csv(
    detail_rows: list[dict],
    output_path: Path,
) -> None:
    """Vista ítargögn (ein lína per tóka).

    Args:
        detail_rows: Samanlagður listi detail-raða úr öllum skrám.
        output_path: Slóð á CSV-skrá.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=DETAIL_FIELDS)
        writer.writeheader()
        for row in detail_rows:
            writer.writerow(row)


# ============================================================
# PRENTA TÖFLU / PRINT TABLE
# ============================================================

def _mean(values: list[float]) -> float:
    """Meðaltal — 0.0 ef listi er tómur."""
    return sum(values) / len(values) if values else 0.0


def print_results_table(results: list[dict]) -> None:
    """Prenta niðurstöður á skipanalínu sem töflu.

    Args:
        results: Listi af summary-dict frá measure_bin_coverage.
    """
    print(f"\nVÍDD 8: BÍN-orðaforðadekkun (BÍN vocabulary coverage)")
    print("=" * 120)

    # Hauslína
    print(
        f"  {'Skrá':<35} {'Orð':<7} {'in_bin%':<8} {'exact%':<8} "
        f"{'cmpnd%':<8} {'propn%':<8} {'oov%':<8} "
        f"{'arch-is%':<10} {'arch-unv%':<10}"
    )
    print(
        f"  {'-'*35} {'-'*7} {'-'*8} {'-'*8} "
        f"{'-'*8} {'-'*8} {'-'*8} {'-'*10} {'-'*10}"
    )

    for r in results:
        print(
            f"  {r['filename']:<35} "
            f"{r['total_words']:<7} "
            f"{r['in_bin_ratio']*100:<8.2f} "
            f"{r['exact_ratio']*100:<8.2f} "
            f"{r['compound_ratio']*100:<8.2f} "
            f"{r['proper_name_ratio']*100:<8.2f} "
            f"{r['oov_ratio']*100:<8.2f} "
            f"{r['archaic_icelandic_ratio']*100:<10.2f} "
            f"{r['archaic_z_unverified_ratio']*100:<10.2f}"
        )

    if results:
        avg_in_bin = _mean([r['in_bin_ratio'] for r in results]) * 100
        avg_exact = _mean([r['exact_ratio'] for r in results]) * 100
        avg_compound = _mean([r['compound_ratio'] for r in results]) * 100
        avg_proper = _mean([r['proper_name_ratio'] for r in results]) * 100
        avg_oov = _mean([r['oov_ratio'] for r in results]) * 100
        avg_arch_ice = _mean(
            [r['archaic_icelandic_ratio'] for r in results]
        ) * 100
        avg_arch_unv = _mean(
            [r['archaic_z_unverified_ratio'] for r in results]
        ) * 100

        print(
            f"  {'-'*35} {'-'*7} {'-'*8} {'-'*8} "
            f"{'-'*8} {'-'*8} {'-'*8} {'-'*10} {'-'*10}"
        )
        print(
            f"  {'MEÐALTAL':<35} {'':7} "
            f"{avg_in_bin:<8.2f} {avg_exact:<8.2f} "
            f"{avg_compound:<8.2f} {avg_proper:<8.2f} "
            f"{avg_oov:<8.2f} "
            f"{avg_arch_ice:<10.2f} {avg_arch_unv:<10.2f}"
        )

    print("=" * 120)
    print()
    print("  SKÝRING DÁLKA / COLUMN KEY:")
    print("    Orð        = Heildarfjöldi gildra tóka (sama og dim6)")
    print("    in_bin%    = (exact + compound + proper_name) / total  ← AÐALVÍDD")
    print("    exact%     = Bein BÍN-fletta, ekki sérnafn")
    print("    cmpnd%     = Leyst með samsetningarreiknirit BÍN")
    print("    propn%     = Sérnafn (mannanafn, staður, föðurnafn, o.s.frv.)")
    print("    oov%       = Fannst ekki í BÍN")
    print("    arch-is%   = Undirmengi oov: STAÐFEST forn-íslensk z (z→s mynd í BÍN)")
    print("    arch-unv%  = Undirmengi oov: z án BÍN-staðfestingar (líklega erlent sérnafn)")
    print()
    print("  TÚLKUN:")
    print("    in_bin% > 95       → staðlaður orðaforði (flest orð í BÍN)")
    print("    in_bin% 90–95      → sérhæft orðaforði eða sérnafnaþungt")
    print("    in_bin% < 90       → líklega óformlegt, fantasía, eða LLM-gæðavandamál")
    print("    Hátt oov% + lágt propn% → grunur um ranghugsuð orð (hallucinations)")
    print("    arch-is% > 0       → texti með staðfesta forna stafsetningu (fyrir 1973–74)")
    print("                          (Morgunblaðið fyrir 2000, eldri Jónas-bloggfærslur,")
    print("                          pre-1974 bókmenntir). EKKI gæðavandamál — stílvísir.")
    print("    arch-unv% > 0      → z-stafir í erlendum sérnöfnum/tökuorðum (Zoëga, Sarkozy).")
    print("                          Oft samhliða háu propn% í fréttatextum.")


# ============================================================
# FINNA ALLAR TEXTASKRÁR / FIND ALL TEXT FILES
# ============================================================

def find_text_files(text_dir: Path) -> list[Path]:
    """Finna allar .txt skrár í möppu (endurkvæmt).

    Args:
        text_dir: Mappa með textaskrám.

    Returns:
        Raðaður listi af Path-hlutum.
    """
    txt_files = sorted(text_dir.rglob('*.txt'))
    if not txt_files:
        print(f"  AÐVÖRUN: Engar .txt skrár fundust í {text_dir}")
    return txt_files


# ============================================================
# SKIPANALÍNUVIÐMÓT / COMMAND LINE INTERFACE
# ============================================================

def main() -> None:
    """Keyra dim8 á textaskrám og vista CSV."""
    parser = argparse.ArgumentParser(
        description="Vídd 8: Mæla BÍN-orðaforðaþekju (BÍN vocabulary coverage).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dæmi:
  # Á möppu:
  python scripts/dim8_bin_ratio.py \\
      --text-dir data/experiment/human_reference/

  # Á stökum skrám:
  python scripts/dim8_bin_ratio.py \\
      --files data/human_texts/news/news_001.txt

  # Með villuleit (sýnir fyrstu 20 OOV-tóka per skrá):
  python scripts/dim8_bin_ratio.py \\
      --text-dir data/experiment/human_reference/ --debug

  # Sleppa ítargögn (detail CSV) til að spara tíma/pláss:
  python scripts/dim8_bin_ratio.py \\
      --text-dir data/experiment/human_reference/ --no-detail

  # Þurrkeyrsla (dry run) — sýnir hvað yrði unnið, vistar ekki:
  python scripts/dim8_bin_ratio.py \\
      --text-dir data/experiment/human_reference/ --dry-run
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--text-dir',
        type=Path,
        help="Mappa með textaskrám (.txt). Leit er endurkvæm."
    )
    group.add_argument(
        '--files',
        type=Path,
        nargs='+',
        help="Ein eða fleiri textaskrár til að greina."
    )

    parser.add_argument(
        '--summary-csv',
        type=Path,
        default=Path('output/dim8_bin_summary.csv'),
        help="Slóð á samantekt CSV (sjálfgefið: output/dim8_bin_summary.csv)"
    )
    parser.add_argument(
        '--detail-csv',
        type=Path,
        default=Path('output/dim8_bin_detail.csv'),
        help="Slóð á ítargögn CSV (sjálfgefið: output/dim8_bin_detail.csv)"
    )
    parser.add_argument(
        '--no-detail',
        action='store_true',
        help="Sleppa ítargögn CSV — sparar tíma og pláss."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Sýna hvaða skrár yrðu unnar en vista ekkert."
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Prenta villuleitarupplýsingar, þ.m.t. fyrstu 20 OOV-tóka "
             "per skrá."
    )

    args = parser.parse_args()

    # --- FINNA SKRÁR ---
    if args.text_dir:
        if not args.text_dir.is_dir():
            print(f"VILLA: Mappa finnst ekki: {args.text_dir}")
            sys.exit(1)
        text_files = find_text_files(args.text_dir)
    else:
        text_files = args.files
        for f in text_files:
            if not f.exists():
                print(f"VILLA: Skrá finnst ekki: {f}")
                sys.exit(1)

    if not text_files:
        print("VILLA: Engar skrár til að greina.")
        sys.exit(1)

    # --- DRY RUN ---
    if args.dry_run:
        print(f"\n  [DRY RUN] Myndi greina {len(text_files)} skrá(r):")
        for f in text_files:
            print(f"  [DRY RUN]   {f}")
        print(f"  [DRY RUN] Myndi vista samantekt í: {args.summary_csv}")
        if not args.no_detail:
            print(f"  [DRY RUN] Myndi vista ítargögn í: {args.detail_csv}")
        else:
            print(f"  [DRY RUN] --no-detail virkt, sleppi ítargögnum")
        return

    print(f"\n  Greini {len(text_files)} skrá(r)...")
    if args.debug:
        print("  [DEBUG] Villuleitarhamur virkur — sýni ítarlegar upplýsingar")
    if args.no_detail:
        print("  [--no-detail] Sleppir ítargögnum (detail CSV)")

    # --- HLAÐA BÍN (lazy, en hér biðjum við um það strax svo
    #      notandi fái villuskilaboð fljótt ef islenska vantar) ---
    print("  Hleð BÍN (islenska)...")
    try:
        _get_bin()
    except ImportError as e:
        print(f"\nVILLA: {e}")
        sys.exit(1)
    print("  BÍN tilbúið.")

    # --- KEYRA MÆLINGAR ---
    summaries: list[dict] = []
    all_detail: list[dict] = []

    for tf in text_files:
        summary, detail_rows = measure_bin_coverage(
            tf,
            collect_detail=not args.no_detail,
            debug=args.debug,
        )
        summaries.append(summary)
        if not args.no_detail:
            all_detail.extend(detail_rows)

    # --- DEBUG: Fyrstu 5 archaic-z tókar í hverjum flokki þvert á skrár ---
    # Sýnir verified-flokkinn (z→s mynd í BÍN — staðfest forn-íslenska) með
    # nútímamyndinni við hliðina, og unverified-flokkinn (líklega erlend
    # sérnöfn) sér.
    if args.debug:
        # Staðfestar fornmyndir — (skrá, tóki, z→s mynd)
        ice_sample: list[tuple[str, str, str]] = []
        for s in summaries:
            for tok, modern in s.get('_archaic_ice_examples', []):
                ice_sample.append((s['filename'], tok, modern))
                if len(ice_sample) >= 5:
                    break
            if len(ice_sample) >= 5:
                break

        # Óstaðfestar z-myndir — (skrá, tóki)
        unv_sample: list[tuple[str, str]] = []
        for s in summaries:
            for tok in s.get('_archaic_unv_examples', []):
                unv_sample.append((s['filename'], tok))
                if len(unv_sample) >= 5:
                    break
            if len(unv_sample) >= 5:
                break

        print()
        if ice_sample:
            print(
                f"  [DEBUG] Fyrstu {len(ice_sample)} STAÐFEST archaic-icelandic "
                f"tókar (z-mynd → z→s mynd í BÍN):"
            )
            for fname, tok, modern in ice_sample:
                print(f"  [DEBUG]   • {tok} → {modern}  ({fname})")
        else:
            print(
                "  [DEBUG] Engir staðfestir archaic-icelandic tókar fundust."
            )

        print()
        if unv_sample:
            print(
                f"  [DEBUG] Fyrstu {len(unv_sample)} ÓSTAÐFESTIR archaic-z "
                f"tókar (z→s ekki í BÍN — líklega erlent):"
            )
            for fname, tok in unv_sample:
                print(f"  [DEBUG]   • {tok}  ({fname})")
        else:
            print("  [DEBUG] Engir óstaðfestir archaic-z tókar fundust.")

    # --- PRENTA TÖFLU ---
    print_results_table(summaries)

    # --- VISTA CSV ---
    save_summary_csv(summaries, args.summary_csv)
    print(f"\n  Samantekt vistuð: {args.summary_csv}")

    if not args.no_detail:
        save_detail_csv(all_detail, args.detail_csv)
        print(f"  Ítargögn vistuð: {args.detail_csv} "
              f"({len(all_detail):,} línur)")


if __name__ == "__main__":
    main()
