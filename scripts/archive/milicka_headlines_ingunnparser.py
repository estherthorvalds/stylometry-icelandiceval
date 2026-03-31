"""
Örpróf með reikniformúlu Milička — Hlutfall fréttafyrirsagna án frumlagsnafnliðar
================================================================================

HVER GERÐI ÞETTA FORRIT?
Nemandi: Esther Ýr Þorvaldsdóttir
Með aðstoð: Claude Opus 4.6
Námskeið: TÖL025, Háskóli Íslands

HVAÐ GERIR ÞETTA FORRIT?
Forritið mælir hversu oft risamállíkön búa til fyrirsagnir án frumlagsnafnliðar
í íslenskum fréttafyrirsögnum og ber saman við mennska fréttatexta.

Fyrirsögn án frumlagsnafnliðar = fyrirsögn hefur sögn í persónuhætti en ekkert frumlag.
Dæmi: "Fengu vel búnar verkfærakistur að gjöf" — hver fékk? Þetta er klassískt
stíleinkenni íslenskra fréttafyrirsagna.

ÞÁTTARI:
Notaður er íslenskur taugaþáttari eftir Ingunn Jóhönnu Kristjánsdóttur (2024)
sem þjálfaður er á IcePaHC trjábankanum og tilheyrir Stanza-þáttunarpípunni.
Þáttarinn skilar liðgerðartrjám þar sem NP-SBJ merkir frumlagsnafnlið.
F-mæling þáttarans: 90,38%.

HVERNIG VIRKAR ÞAÐ?
1. Les fyrirsagnir úr textaskrám (ein fyrirsögn í hverri línu)
2. Þáttar hverja fyrirsögn með Stanza-taugaþáttaranum
3. Athugar hvort liðgerðartréð innihaldi NP-SBJ (frumlagsnafnlið)
4. Reiknar hlutfall fyrirsagna án frumlagsnafnliðar
5. Notar formúlu Milička (2025) til að bera saman (aðlagað: ópöruð gögn og bootstrap SE)

FORMÚLUR MILIČKA:
Formúla 2: i = v_orig2 - v_orig1   (mennsk frávik - grunnlína)
Formúla 1: Δv = v_orig2 - v_model  (frávik risamállíkansins)
Formúla 3: b_d = Δv̄_d / SE(I_d)   (staðlað frávik)

Milička notaði pöruð gögn (framhald skrifað af manneskju annarsvegar og
risamállíkani hinsvegar). Hér eru gögnin ópöruð (aðskildar fyrirsagnir)
og bootstrap notað til að meta SE. Þetta er proof of concept, ekki fullkomin útfærsla.

Formúla fyrir mælingar: b_d = Δv / SE(I_d)
b : Meðaltal.
d : Vídd, hugtakið kemur frá Biber og hér mætti tala um það sem stíleinkenni. 
b_d : Markmið líkans ætti að vera að reyna að vera eins nálægt 0 og hægt er. Þá er það innan mennska fráviksins. 
v : Niðurstaða af mælingum frá víddinni. 
Δ : Mismunur, hér er verið að skoða mismuninn á niðurstöðum gervigreindartexta og mannlegs texta á sama prófi. 
i : Náttúrulegt staðalfrávik fundið út frá mismuninum á upprunatexta (fyrri helmingur mannlega textans) og prófunartexta (seinni helmingur mannlega textans).
SE : Staðalfrávik, það er metið með handahófsúrtakanálgun (mennsku gögnunum raðað upp á nýjan hátt 1000 sinnum).

"""

import random
import sys
import stanza
import re


# ============================================================
# SLÓÐIR Í TÖLVUNNI
# ============================================================

# Slóð á IceConParse
MODEL_PATH = "/Users/esther/Documents/GitHub/stylometry-icelandiceval/models/is_icepahc_transformer_finetuned_constituency.pt"

# Fyrirsagnir í textaskrám — ein fyrirsögn í hverri línu
HUMAN_PATH = "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/human_texts/520_Headlines_Human.txt"

LLM_PATHS = {
    "Gemini_3_Thinking": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/Gemini_3_Thinking/520_Headlines_Gemini_3_Thinking.txt",
    "Le_Chat_Fast": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/Le_Chat_Fast/520_Headlines_Le_Chat_Fast.txt",
    "GPT_5": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/GPT_5/520_Headlines_GPT_5.txt",
    "Le_Chat_Thinking": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/Le_Chat_Thinking/520_Headlines_Le_Chat_Thinking.txt",
}


# ============================================================
# ICECONPARSE-ÞÁTTARINN
# Þáttarinn er hlaðinn einu sinni og notaður á allar fyrirsagnir.
# Fyrsta keyrslan tekur ~20 sek vegna IceBERT, en eftir það er
# þáttun hverrar fyrirsagnar hröð.
# ============================================================

def load_parser(model_path):
    """Hlaða Stanza-þáttunarpípunni með íslenska liðgerðarþáttaranum."""
    print("Hleð þáttara ...")
    nlp = stanza.Pipeline(
        lang='is',
        processors='tokenize, pos, constituency',
        constituency_model_path=model_path,
    )
    print("Þáttari tilbúinn.\n")
    return nlp


# ============================================================
# LESA FYRIRSAGNIR ÚR TEXTASKRÁ
# Ein fyrirsögn í hverri línu. Sleppir tómum línum.
# ============================================================

def load_headlines(path):
    """Lesa fyrirsagnir úr textaskrá. Skilar lista af strengjum."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"VILLA: Skrá fannst ekki: {path}")
        return []


# ============================================================
# ÞÁTTUN OG GREINING
# Þáttar fyrirsagnir og athugar hvort NP-SBJ sé í trénu.
# ============================================================

def parse_headlines(nlp, headlines):
    """Þáttar lista af fyrirsögnum og skilar lista af niðurstöðum.

    Hvert stak í listanum er dict með:
        - text: upprunalegi strengurinn
        - tree: liðgerðartréð sem strengur
        - has_subject: True ef NP-SBJ finnst í trénu
        - has_verb: True ef sögn (VB/BE/DO/HV/MD/RD) finnst í trénu
        - is_imperative: True ef sagnliður er boðháttur
    """
    results = []
    for idx, headline in enumerate(headlines):
        doc = nlp(headline)
        tree_str = str(doc.sentences[0].constituency).replace('*', '-')

        # Athuga hvort NP-SBJ sé í trénu
        has_subject = 'NP-SBJ' in tree_str

        # Athuga hvort persónubeygð sögn sé í trénu
        # IcePaHC merkir persónubeygðar sagnir með I (framsöguháttur) eða S (viðtengingarh.)
        # t.d. VBPI, VBDI, VBPS, VBDS, BEPI, BEDI, DOPI, HVPI, MDPI, RDPI...
        # VB eitt og sér er nafnháttur, VBN/VAN er lýsingarháttur — ekki telja
        
        # Athuga hvort sagnliður sé í boðhætti
        is_imperative = 'IP-IMP' in tree_str
        
        # Athuga hvort persónubeygð sögn sé í aðalsetningu (ekki í aukasetningum)
        # Fjarlægja aukasetningar úr trénu áður en leitað er að sögn

        #main_clause = re.sub(r'\(CP-[A-Z]+\s.*?\)\)', '', tree_str) # TODO: fínstilla til að útiloka sagnir í aukasetningum
        has_verb = bool(re.search(r'\b(VB|BE|DO|HV|MD|RD)[PD][IS]\b', tree_str))

        results.append({
            'text': headline,
            'tree': tree_str,
            'has_subject': has_subject,
            'has_verb': has_verb,
            'is_imperative': is_imperative,
            'index': idx,
        })

        # Sýna framvindu á hverri 50. fyrirsögn til að athuga hvort allt sé að virka sem skyldi
        if (idx + 1) % 50 == 0:
            print(f"  Þáttað {idx + 1}/{len(headlines)} fyrirsagnir...")

    return results


# ============================================================
# AÐALMÆLING
# Reiknar hlutfall fyrirsagna án frumlagsnafnliðar.
# Þáttarinn sér um greiningu (einfaldara en með JSON-fæla frá Sonnet 4.6)
# ============================================================

def subject_drop_rate(parsed_headlines):
    """Mæla hlutfall fyrirsagna án frumlagsnafnliðar.

    Aðeins fyrirsagnir sem innihalda sögn eru skoðaðar.
    Fyrirsagnir án sagnar (nafnliðarfyrirsagnir) eru undanskildar.

    SKILAGILDI:
    - rate: hlutfall fyrirsagna án frumlagsnafnliðar (0.0 til 1.0)
    - dropped: listi af fyrirsögnum án frumlagsnafnliðar
    - kept: listi af fyrirsögnum með frumlagi
    """
    if not parsed_headlines:
        return 0.0, [], []

    dropped = []    # Fyrirsagnir ÁN frumlagsnafnliðar
    kept = []       # Fyrirsagnir MEÐ frumlagsnafnlið

    for h in parsed_headlines:
        if not h['has_verb']:
            continue
        if h.get('is_imperative', False):
            continue

        if not h['has_subject']:
            dropped.append(h)
        else:
            kept.append(h)

    counted = len(dropped) + len(kept)
    rate = len(dropped) / counted if counted > 0 else 0.0
    return rate, dropped, kept


# ============================================================
# MILIČKA FORMÚLURNAR
# ============================================================

def run_milicka(parsed_human, nlp):
    """Reikna Milička-formúlur og bera saman við risamállíkön.

    SKREF:
    1. Skipta mennskum gögnum í tvennt (upprunabunki og prófunarbunki)
    2. Mæla fyrirsagnir án frumlagsnafnliðar í hvorum bunka
    3. Finna náttúrulegt frávik (formúla 2)
    4. Nota bootstrap til að meta SE (staðalskekkju)
    5. Mæla frávik hvers líkans og staðla með SE (formúla 3)
    """
    n = len(parsed_human)
    mid = n // 2

    half1 = parsed_human[:mid]
    half2 = parsed_human[mid:]

    # --- MÆLA HLUTFALL Í HVORUM BUNKA ---
    v_half1, _, _ = subject_drop_rate(half1)
    v_half2, _, _ = subject_drop_rate(half2)
    v_full, dropped_full, kept_full = subject_drop_rate(parsed_human)

    # --- FORMÚLA 2: NÁTTÚRULEGT FRÁVIK ---
    i = v_half2 - v_half1

    # --- PRENTA GRUNNLÍNU ---
    print("=" * 80)
    print("FORMÚLUR MILIČKA — FYRIRSAGNIR ÁN FRUMLAGSNAFNLIÐAR")
    print("Þáttari: Ingunn J. Kristjánsdóttir (2024), Stanza + IceBERT")
    print("=" * 80)
    print()
    print("GRUNNLÍNA (MENNSKT FRÁVIK)")
    print("-" * 80)
    print(f"  Heildargögn ({n} fyrirsagnir):     án frumlagsnafnliðar = {v_full:.3f} ({v_full:.1%})")
    print(f"  Upprunabunki ({len(half1)} fyrirsagnir):    án frumlagsnafnliðar = {v_half1:.3f} ({v_half1:.1%})")
    print(f"  Prófunarbunki ({len(half2)} fyrirsagnir):   án frumlagsnafnliðar = {v_half2:.3f} ({v_half2:.1%})")
    print(f"  Formúla 2: i = {v_half2:.3f} - {v_half1:.3f} = {i:+.3f}")
    print(f"  |i| (náttúrulegt frávik):     {abs(i):.3f}")
    print()

    # --- BOOTSTRAP: GERVIFRÁVIK (SE) ---
    random.seed(42)
    num_resamples = 1000
    i_values = []

    indices = list(range(n))
    for _ in range(num_resamples):
        random.shuffle(indices)
        resample_half1 = [parsed_human[j] for j in indices[:mid]]
        resample_half2 = [parsed_human[j] for j in indices[mid:]]
        r1, _, _ = subject_drop_rate(resample_half1)
        r2, _, _ = subject_drop_rate(resample_half2)
        i_values.append(r2 - r1)

    mean_i = sum(i_values) / len(i_values)
    se_i = (sum((x - mean_i)**2 for x in i_values) / (len(i_values) - 1)) ** 0.5

    print("BOOTSTRAP SE (1000 endurúrtök)")
    print("-" * 70)
    print(f"  Meðaltal i gildis:      {mean_i:+.4f}")
    print(f"  SE(I_d) frá bootstrap:  {se_i:.4f}")
    print()

    # --- SAMANBURÐUR VIÐ RISAMÁLLÍKÖN ---
    print("SAMANBURÐUR VIÐ RISAMÁLLÍKÖN")
    print("-" * 70)
    print()
    print(f"  {'Líkan':<25} {'Hlutfall':<10} {'Δv':<10} {'b_d':<10} {'Stig':<10}")
    print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")

    for name, path in LLM_PATHS.items():
        # Lesa og þátta gögn líkansins
        llm_headlines = load_headlines(path)
        if not llm_headlines:
            print(f"  {name:<25} VANTAR SKRÁ: {path}")
            continue

        print(f"\n  Þátta {name} ({len(llm_headlines)} fyrirsagnir)...")
        parsed_llm = parse_headlines(nlp, llm_headlines)

        # Mæla fyrirsagnir án frumlagsnafnliðar
        v_llm, _, _ = subject_drop_rate(parsed_llm)

        # FORMÚLA 1: Δv
        delta_v = v_full - v_llm

        # FORMÚLA 3: b_d
        if se_i > 0.0001:
            b_d = delta_v / se_i
        else:
            b_d = float('inf') if abs(delta_v) > 0.0001 else 0.0

        # Stigatöflueinkunn
        score = style_score(v_full, v_llm)

        print(f"  {name:<25} {v_llm:>9.1%} {delta_v:>+9.3f} {b_d:>+10.2f} {score:>8.1f}")

    # --- LEIÐBEININGAR ---
    print()
    print("-" * 70)
    print()
    print("HVERNIG Á AÐ TÚLKA NIÐURSTÖÐURNAR:")
    print("  Δv  = mennskt hlutfall mínus hlutfall líkans")
    print("        Jákvætt = líkanið sleppir frumlagsnafnlið sjaldnar en fréttafólk")
    print("        Neikvætt = líkanið sleppir frumlagsnafnlið oftar en fréttafólk")
    print("  b_d = Δv staðlað með SE (náttúrulegri sveiflu í mennskum gögnum)")
    print("        b_d nálægt 0 = líkanið hegðar sér eins og mennskir fréttamenn")
    print("        |b_d| > 2 = verulegt frávik frá mennsku stíleinkenni")
    print("  Stig = 0-100 stigatöflueinkunn (100 = fullkomið, 0 = ekkert af stíleinkenninu)")
    print("=" * 70)

    return v_full, dropped_full, kept_full


# ============================================================
# STIGATÖFLUEINKUNN
# ============================================================

def style_score(v_human, v_model):
    """Reikna skor á kvarðanum 0-100 fyrir stílhermu.

    100 = líkan framleiðir nákvæmlega sama hlutfall og fréttafólk.
    0 = líkan framleiðir ekkert af stíleinkenninu (eða meira en tvöfalt).

    Formúla: score = 100 × (1 - |v_human - v_model| / v_human)
    """
    if v_human == 0:
        return 100.0 if v_model == 0 else 0.0
    raw = 100.0 * (1.0 - abs(v_human - v_model) / v_human)
    return max(0.0, raw)


# ============================================================
# MAIN
# ============================================================

def main():
    # --- HLAÐA ÞÁTTARA ---
    nlp = load_parser(MODEL_PATH)

    # --- LESA OG ÞÁTTA MENNSKU GÖGNIN ---
    human_headlines = load_headlines(HUMAN_PATH)
    if not human_headlines:
        print(f"VILLA: Mennsku gögnin fundust ekki: {HUMAN_PATH}")
        sys.exit(1)

    print(f"Fann {len(human_headlines)} fyrirsagnir í mennskum gögnum.")
    print(f"Þátta mennsku fyrirsagnirnar...")
    parsed_human = parse_headlines(nlp, human_headlines)

    # --- KEYRA MILIČKA FORMÚLUR ---
    v_full, dropped_full, kept_full = run_milicka(parsed_human, nlp)

    # --- SÝNA DÆMI ÚR ÞÁTTUN ---
    print("\n" + "=" * 70)
    print(f"DÆMI UM FYRIRSAGNIR ÁN FRUMLAGSNAFNLIÐAR ({len(dropped_full)}):")
    print("=" * 70)
    for h in dropped_full[:10]:
        print(f"\n  [{h['index']:>3}] {h['text']}")
        print(f"        {h['tree']}")
    if len(dropped_full) > 10:
        print(f"\n  ... og {len(dropped_full) - 10} í viðbót")

    print("\n" + "=" * 70)
    print(f"DÆMI UM FYRIRSAGNIR MEÐ FRUMLAGI ({len(kept_full)}):")
    print("=" * 70)
    for h in kept_full[:10]:
        print(f"\n  [{h['index']:>3}] {h['text']}")
        print(f"        {h['tree']}")
    if len(kept_full) > 10:
        print(f"\n  ... og {len(kept_full) - 10} í viðbót")


if __name__ == "__main__":
    main()