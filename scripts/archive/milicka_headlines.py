"""
Örpróf með reikniformúlu Milička — Hlutfall fréttafyrirsagna án frumlagsnafnliðar
================================================================================

HVAÐ GERIR ÞETTA FORRIT?
Forritið mælir hversu oft risamállíkön búa til fyrirsagnir án frumlagsnafnliðar
í íslenskum fréttafyrirsögnum og ber saman við mennska fréttatexta.

Fyrirsögn án frumlagsnafnliðar = fyrirsögn hefur sögn í persónuhætti en ekkert frumlag.
Dæmi: "Fengu vel búnar verkfærakistur að gjöf" — hver fékk? Þetta er klassískt stíleinkenni íslenskra fréttafyrirsagna.

HVERNIG VIRKAR ÞAÐ?
1. Les POS-merktar fyrirsagnir (frá manneskjum og risamállíkönum) úr JSON skrám
2. Flokkar fyrirsagnir: hefur hún sögn? Hefur hún frumlag? Er hún í boðhætti?
3. Reiknar hlutfall fyrirsagna án frumlagsnafnliðar hjá mönnum og hverju líkani
4. Notar formúlu Milička (2025) til að bera saman (aðlagað: ópöruð gögn og bootstrap SE)

FORMÚLUR MILIČKA:
Formúla 2: i = v_orig2 - v_orig1   (mennsk frávik - grunnlína)
Formúla 1: Δv = v_orig2 - v_model  (frávik risamállíkansins)
Formúla 3: b_d = Δv̄_d / SE(I_d)   (staðlað frávik)

MIKILVÆG ATHUGASEMD:
Milička notaði pöruð gögn (framhald skrifað af manneskju annarsvegar og risamállíkani hinsvegar).
Hér eru gögnin ópöruð (aðskildar fyrirsagnir) og bootstrap notað til að
meta SE. Þetta er proof of concept, ekki fullkomin útfærsla.
"""

import json
import random
import sys


# ============================================================
# PATH Á GÖGNIN - HÆGT AÐ SKIPTA ÞESSU ÚT
# ============================================================

HUMAN_PATH = "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/human_texts/520_headlines_pos_tagged.json"

LLM_PATHS = {
    "Gemini_3_Thinking": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/Gemini_3_Thinking/520_Gemini_3_Thinking.json",
    "Le_Chat_Fast": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/Le_Chat_Fast/520_Le_Chat_Fast.json",
    "GPT_5": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/GPT_5/merged_GPT_5.json",
    "Le_Chat_Thinking": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/Le_Chat_Thinking/Le_Chat_merged.json",
}


# ============================================================
# POS-MERKJALESTUR
# Þessar föll lesa POS-merki samkvæmt IFD-tagsetinu og greina
# hvort orð sé í ákveðnum málfræðiflokki.
# ============================================================

def is_nominative_nominal(pos):
    """Athugar hvort POS-merking bendi til nafnliðar í nefnifalli.
    
    IFD-tagsetið kóðar upplýsingar í POS staðnum:
    - Nafnorð (n):       n + kyn + tala + fall + greinir
      Dæmi: nken = nafnorð, karlkyn, eintala, nefnifall
    - Lýsingarorð (l):   l + kyn + tala + fall + ...
    - Fornafn (f):        f + tegund + ... + fall (lengra tag)
    - Greinir (g):        g + kyn + tala + fall
    """
    if not pos or len(pos) < 4:         # Of stutt tag — getur ekki verið nafnliður
        return False
    wc = pos[0]                         # Fyrsti stafur = orðflokkur
    if wc == 'n' and len(pos) >= 4:     # Nafnorð: fall í stöðu 3
        return pos[3] == 'n'            # 'n' = nefnifall
    if wc == 'l' and len(pos) >= 4:     # Lýsingarorð: fall í stöðu 3
        return pos[3] == 'n'
    if wc == 'f' and len(pos) >= 5:     # Fornafn: fall í stöðu 4 (lengra tag)
        return pos[4] == 'n'
    if wc == 'g' and len(pos) >= 4:     # Greinir: fall í stöðu 3
        return pos[3] == 'n'
    return False                        # Ekkert passaði — ekki nafnliður í nefnifalli


# ============================================================
# FLOKKUNARFÖLL
# Þessi föll greina fyrirsagnir sem þarf að útiloka úr mælingunni
# vegna þess að þær eru ekki dæmi um fyrirsagnir án frumlagsnafnliðar.
# ============================================================

def has_imperative_verb(tokens):
    """Athugar hvort fyrirsögn innihaldi sögn í boðhætti.
    
    Boðháttur (t.d. "Vertu á verði") hefur ekki frumlag —
    þetta er málfræðiregla, ekki stíll fréttafólks.
    IFD-tag: sb... (s=sögn, b=boðháttur)
    """
    for token in tokens:
        pos = token.get("pos", "")
        if len(pos) >= 2 and pos[0] == 's' and pos[1] == 'b':
            return True                 # Fann boðhátt
    return False                        # Enginn boðháttur


def has_dummy_subject(tokens):
    """Athugar hvort fyrirsögn byrji á gervifrumlaginu 'það' + sögn.
    
    Dæmi: "Það verður að koma á aðhaldi á hinu opinbera"
    Gervifrumlag er ekki frumlagsnafnliðarleysi — setningin hefur frumlag,
    það er bara merkingarlaust. Þetta mynstur er ekki sértækt
    fyrir fréttafyrirsagnir og ætti því ekki að teljast með.
    
    Aðferð: Athuga hvort fyrsta orðið sé "það" merkt sem fornafn (f...)
    og annað orðið sé sögn í persónuhátt (sf...).
    """
    if len(tokens) < 2:                 # Þarf að minnsta kosti tvö orð
        return False
    first = tokens[0]                   # Fyrsta orðið
    second = tokens[1]                  # Annað orðið
    if (first.get("text", "").lower() == "það"          # Fyrsta orð er "það"
        and first.get("pos", "")[0:1] == "f"            # Merkt sem fornafn
        and len(second.get("pos", "")) >= 2             # Annað orð hefur POS-tag sem er a.m.k. 2 stafir
        and second["pos"][0] == "s"                     # Annað orð er sögn
        and second["pos"][1] == "f"):                   # Í persónuhátt
        return True                     # Þetta er gervifrumlag
    return False                        # Ekki gervifrumlag


# ============================================================
# AÐALMÆLING
# Þetta fall er hjarta forritsins. Það fer í gegnum fyrirsagnir
# og flokkar þær í tvo hópa: án frumlagsnafnliðar vs. full setning.
# ============================================================

def subject_drop_rate(headlines):
    """Mæla hlutfall fyrirsagna án frumlagsnafnliðar meðal fyrirsagna sem eru setningar.
    
    AÐFERÐ:
    Aðeins fyrirsagnir með sögn í persónuhætti eru skoðaðar.
    Þrjár gerðir fyrirsagna eru undanskildar:
    - Boðháttur (t.d. "Vertu á verði") — málfræðiregla, ekki stílval
    - Gervifrumlag (t.d. "Það verður að...") — ekki fréttastíleinkenni
    - Nafnliðarfyrirsagnir án sagnar (t.d. "Al-Anon á Blönduósi") — ekki setning
    
    SKILAGILDI:
    - rate: hlutfall fyrirsagna án frumlagsnafnliðar (0.0 til 1.0)
    - dropped: listi af fyrirsögnum án frumlagsnafnliðar (sögn en ekkert frumlag)
    - kept: listi af fyrirsögnum með frumlagi (bæði sögn og frumlag)
    """
    if not headlines:                   # Ef engar fyrirsagnir
        return 0.0, [], []              # Skila tómu
    dropped = []                        # Hér safnast fyrirsagnir ÁN frumlagsnafnliðar
    kept = []                           # Hér safnast fyrirsagnir MEÐ frumlagsnafnliði
    for h in headlines:                 # Fara í gegnum hverja fyrirsögn fyrir sig
        tokens = h.get("tokens", [])    # Sækja orðin í fyrirsögninni

        # --- ÚTILOKANIR ---
        if has_imperative_verb(tokens):
            continue                    # Boðháttur — sleppa
        if has_dummy_subject(tokens):
            continue                    # Gervifrumlag — sleppa

        # --- GREINING ---
        has_nom = any(is_nominative_nominal(t.get("pos", "")) for t in tokens)
                                        # Er nafnliður í nefnifalli í fyrirsögninni?
        has_verb = any(
            len(t.get("pos", "")) >= 2
            and t["pos"][0] == 's'       # 's' = sögn
            and t["pos"][1] == 'f'       # 'f' = persónuháttur (finite)
            for t in tokens
        )                               # Er sögn í persónuhætti í fyrirsögninni?

        # --- NAFNLIÐARFYRIRSAGNIR ---
        if not has_verb:
            continue                    # Engin sögn = nafnliðarfyrirsögn, sleppa

        # --- FLOKKUN ---
        if not has_nom:
            dropped.append(h)           # Sögn EN ekkert frumlag = ÁN FRUMLAGSNAFNLIÐAR
        else:
            kept.append(h)              # Sögn OG frumlag = full setning

    counted = len(dropped) + len(kept)  # Heildarfjöldi fyrirsagna sem voru skoðaðar
    rate = len(dropped) / counted if counted > 0 else 0.0
                                        # Hlutfall: af setningafyrirsögnum, hversu
                                        # margar eru án frumlagsnafnliðar?
    return rate, dropped, kept          # Skila hlutfalli og báðum listum


# ============================================================
# MILIČKA FORMÚLURNAR
# Hér er formúlum Milička beitt á gögnin. Gögnin eru ópöruð
# svo bootstrap er notað til að meta SE (staðalskekkju).
# ============================================================

def run_milicka(human_headlines):
    """Reikna Milička-formúlur og bera saman við risamállíkön.
    
    SKREF:
    1. Skipta mennskum gögnum í tvennt (upprunabunki og prófunarbunki)
    2. Mæla fyrirsagnir án frumlagsnafnliðar í hvorum bunka
    3. Finna náttúrulegt frávik (formúla 2)
    4. Nota bootstrap til að meta SE (staðalskekkju)
    5. Mæla frávik hvers líkans og staðla með SE (formúla 3)
    
    SKILAGILDI:
    - v_full: heildarhlutfall fyrirsagna án frumlagsnafnliðar hjá mönnum
    - dropped_full: listi af mennskum fyrirsögnum án frumlagsnafnliðar
    - kept_full: listi af mennskum fyrirsögnum með frumlagi
    """

    n = len(human_headlines)            # Fjöldi fyrirsagna í mennskum gögnum
    mid = n // 2                        # Miðja — skipta í tvennt

    half1 = human_headlines[:mid]       # Fyrri helmingur (upprunabunki)
    half2 = human_headlines[mid:]       # Seinni helmingur (prófunarbunki)

    # --- MÆLA HLUTFALL Í HVORUM BUNKA ---
    v_half1, _, _ = subject_drop_rate(half1)        # Hlutfall í upprunabunka
    v_half2, _, _ = subject_drop_rate(half2)        # Hlutfall í prófunarbunka
    v_full, dropped_full, kept_full = subject_drop_rate(human_headlines)
                                                    # Hlutfall í öllum gögnum

    # --- FORMÚLA 2: NÁTTÚRULEGT FRÁVIK ---
    # Þetta segir okkur: hversu mikið sveiflast mælingin bara
    # vegna þess að við erum að skoða mismunandi texta?
    i = v_half2 - v_half1

    # --- PRENTA GRUNNLÍNU ---
    print("=" * 80)
    print("FORMÚLUR MILIČKA PRÓFAÐAR — FYRIRSAGNIR ÁN FRUMLAGSNAFNLIÐAR")
    print("=" * 80)
    print()
    print("GRUNNLÍNA (MENNSKT FRÁVIK)")
    print("-" * 80)
    print(f"  Heildargögn ({n} fyrirsagnir):     án frumlagsnafnliðar = {v_full:.3f} ({v_full:.1%})")
    print(f"  Upprunabunki ({len(half1)} fyrirsagnir):     án frumlagsnafnliðar = {v_half1:.3f} ({v_half1:.1%})")
    print(f"  Prófunarbunki ({len(half2)} fyrirsagnir):     án frumlagsnafnliðar = {v_half2:.3f} ({v_half2:.1%})")
    print(f"  Formúla 2: i = {v_half2:.3f} - {v_half1:.3f} = {i:+.3f}")
    print(f"  |i| (náttúrulegt frávik):     {abs(i):.3f}")
    print()

    # --- BOOTSTRAP: META SE ---
    # Vandamál: Við höfum aðeins eitt gagnasafn og skiptum því í tvennt.
    # Ein skipting gefur eitt i-gildi, en við þurfum að vita hversu mikið
    # i-gildið sveiflast almennt. Lausn: stokka gögnin 1000 sinnum,
    # skipta í hvert sinn, og mæla i. Staðalfrávik þessara 1000 i-gilda
    # er SE (staðalskekkjan) — hversu mikla sveiflu má búast við af tilviljun.
    random.seed(42)                     # Fast fræ (seed) svo niðurstöður endurtaki sig

    num_resamples = 1000                # Fjöldi endurúrtaka
    i_values = []                       # Hér safnast öll i-gildin

    indices = list(range(n))            # Vísitölur allra fyrirsagna [0, 1, 2, ..., 519]
    for _ in range(num_resamples):      # Endurtaka 1000 sinnum
        random.shuffle(indices)         # Stokka vísitölurnar
        resample_half1 = [human_headlines[j] for j in indices[:mid]]
                                        # Fyrri helmingur úr stokkuðum gögnum
        resample_half2 = [human_headlines[j] for j in indices[mid:]]
                                        # Seinni helmingur úr stokkuðum gögnum
        r1, _, _ = subject_drop_rate(resample_half1)    # Mæla hlutfall
        r2, _, _ = subject_drop_rate(resample_half2)    # Mæla hlutfall
        i_values.append(r2 - r1)        # Vista muninn (formúla 2 á þessu úrtaki)

    # Reikna SE: staðalfrávik allra i-gilda
    mean_i = sum(i_values) / len(i_values)              # Meðaltal i-gilda
    se_i = (sum((x - mean_i)**2 for x in i_values) / (len(i_values) - 1)) ** 0.5
                                        # SE = staðalfrávik = √(Σ(x-meðaltal)² / (n-1))

    print("BOOTSTRAP SE (1000 endurúrtök)")
    print("-" * 70)
    print(f"  Meðaltal i gildis:      {mean_i:+.4f}")
    print(f"  SE(I_d) frá bootstrap:  {se_i:.4f}")
    print()

    # --- SAMANBURÐUR VIÐ RISAMÁLLÍKÖN ---
    # Fyrir hvert líkan: lesa gögn, mæla hlutfall, reikna frávik og b_d
    print("SAMANBURÐUR VIÐ RISAMÁLLÍKÖN")
    print("-" * 70)
    print()
    print(f"  {'Líkan':<25} {'Hlutfall':<10} {'Δv':<10} {'b_d':<10} {'Stig':<10}")
    print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")

    for name, path in LLM_PATHS.items():
        # Lesa gögn líkansins
        try:
            with open(path, 'r', encoding='utf-8') as f:
                llm_data = json.load(f)
        except FileNotFoundError:
            print(f"  {name:<25} VANTAR SKRÁ: {path}")
            continue

        # Mæla fyrirsagnir án frumlagsnafnliðar hjá líkaninu
        v_llm, _, _ = subject_drop_rate(llm_data)

        # FORMÚLA 1: Δv = mennskt hlutfall - hlutfall líkansins
        # Jákvætt Δv = líkanið sleppir frumlagsnafnlið sjaldnar en manneskjur (of formlegt)
        # Neikvætt Δv = líkanið sleppir frumlagsnafnlið oftar en manneskjur (of þjappað)
        delta_v = v_full - v_llm

        # FORMÚLA 3: b_d = Δv / SE
        # Staðlar frávikið miðað við náttúrulega sveiflu í mennskum gögnum.
        # b_d nálægt 0 = líkanið er innan mennskra marka
        # |b_d| > 2 = líkanið víkur verulega frá mennsku stíleinkenni
        if se_i > 0.0001:              # Forðast deilingu með 0
            b_d = delta_v / se_i
        else:
            b_d = float('inf') if abs(delta_v) > 0.0001 else 0.0
        
        # Stigatöflueinkunn reiknuð
        score = style_score(v_full, v_llm)

        # Prenta niðurstöður
        print(f"  {name:<25} {v_llm:>9.1%} {delta_v:>+9.3f} {b_d:>+10.2f} {score:>8.1f}")
        

    # --- LEIÐBEININGAR ---
    print()
    print("-" * 70)
    print()
    print("HVERNIG Á AÐ TÚLKA NIÐURSTÖÐURNAR:")
    print("  Δv  = mennskt hlutfall mínus hlutfall líkans")
    print("        Jákvætt = líkanið fellir frumlag sjaldnar en menn")
    print("        Neikvætt = líkanið fellir frumlag oftar en menn")
    print("  b_d = Δv staðlað með SE (náttúrulegri sveiflu í mennskum gögnum)")
    print("        b_d nálægt 0 = líkanið hegðar sér eins og mennskir fréttamenn")
    print("        |b_d| > 2 = verulegt frávik frá mennsku stíleinkenni")
    print("=" * 70)

    return v_full, dropped_full, kept_full

# ============================================================
# STIGATÖFLUEINKUNN REIKNUÐ
# ============================================================

def style_score(v_human, v_model):
    """Reikna skor á kvarðanum 0-100 fyrir stílhermu.
    
    Skorið mælir hversu nálægt hlutfall módelsins er mannlegri grunnlínu.
    100 = módel framleiðir nákvæmlega sama hlutfall og fréttafólk.
    0 = módel framleiðir enga texta með stíleinkenninu eða tvöfaldar það.
    
    Formúla: score = 100 × (1 - |v_human - v_model| / v_human)
    
    """
    if v_human == 0:        # Ef mennski textinn er 0% þá virkar þetta ekki
        return 100.0 if v_model == 0 else 0.0
    raw = 100.0 * (1.0 - abs(v_human - v_model) / v_human)
    return max(0.0, raw)

# ============================================================
# MAIN — KEYRA FORRITIÐ
# ============================================================

def main():
    # --- LESA MENNSKU GÖGNIN ---
    try:
        with open(HUMAN_PATH, 'r', encoding='utf-8') as f:
            human_data = json.load(f)
    except FileNotFoundError:
        print(f"VILLA: Mennsku gögnin fundust ekki: {HUMAN_PATH}")
        sys.exit(1)

    print(f"\nFann {len(human_data)} fyrirsagnir í mennskum gögnum: {HUMAN_PATH}")

    # --- KEYRA MILIČKA FORMÚLUR ---
    # run_milicka prentar niðurstöður OG skilar listum til að sýna dæmi
    v_full, dropped_full, kept_full = run_milicka(human_data)

    # --- SÝNA DÆMI UM FYRIRSAGNIR ÁN FRUMLAGSNAFNLIÐAR ---
    # Þessar fyrirsagnir hafa sögn í persónuhætti en ekkert frumlag.
    # Þetta er hið fréttalega stíleinkenni sem við erum að mæla.
    print("\n" + "=" * 70)
    print(f"DÆMI UM FYRIRSAGNIR ÁN FRUMLAGSNAFNLIÐAR ({len(dropped_full)}):")
    print("=" * 70)
    for h in dropped_full[:20]:         # Sýna fyrstu 20
        tokens = h.get("tokens", [])
        text = " ".join(t["text"] for t in tokens)
        tags = " ".join(t["pos"] for t in tokens)
        print(f"\n  [{h['index']:>3}] {text}")
        print(f"        {tags}")
    if len(dropped_full) > 20:          # Ef fleiri en 20, segja frá
        print(f"\n  ... og {len(dropped_full) - 20} í viðbót")

    # --- SÝNA DÆMI UM FULLAR SETNINGAR ---
    # Þessar fyrirsagnir hafa bæði sögn og frumlag.
    # Þetta er hinn helmingurinn — ekki frumlagsnafnliðarleysi.
    print("\n" + "=" * 70)
    print(f"DÆMI UM FYRIRSAGNIR MEÐ FRUMLAGI ({len(kept_full)} fyrirsagnir):")
    print("=" * 70)
    for h in kept_full[:20]:            # Sýna fyrstu 20
        tokens = h.get("tokens", [])
        text = " ".join(t["text"] for t in tokens)
        tags = " ".join(t["pos"] for t in tokens)
        print(f"\n  [{h['index']:>3}] {text}")
        print(f"        {tags}")
    if len(kept_full) > 20:             # Ef fleiri en 20, segja frá
        print(f"\n  ... og {len(kept_full) - 20} í viðbót")


if __name__ == "__main__":
    main()