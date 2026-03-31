# dim1_frumlagsnafnfall.py


import random
import sys
import re


# ============================================================
# GREINING
# CLAUDE CODE, THIS SCRIPT SHOULD OPEN THE ALREADY PARSED TEXTS, RUN THE FUNCTION AND FIND THEIR SCORE AND RETURN THE SCORE TO BE CALCULATED BY RUN_MILICKA.PY
# CLAUDE CODE, WE'RE NO LONGER ONLY WORKING WITH HEADLINES, REPLACE VARIABLE NAME WITH SENTENCES
# Athugar hvort NP-SBJ sé í trénu.
# ============================================================

def parse_headlines(nlp, headlines):
    """
    REMOVE THE PARSINS, USE ALREADY PARSED TEXTS. 
    Þáttar lista af fyrirsögnum og skilar lista af niðurstöðum.

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