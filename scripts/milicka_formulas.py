"""
Skrifta búin til af Claude Opus 4.6 - Óbreytt 19.03.2026. 
Verður notuð sem grunnur til að prófa mismunandi aðferðir síðar meir. 

Milička (2025) MDA Benchmark Formulas - Proof of Concept
=========================================================
This script implements the statistical formulas from Section 3.2
of "Benchmark of stylistic variation in LLM-generated texts."

SETUP:
- Paste original text into orig_text
- The script splits it in half: orig1 (prompt) and orig2 (human continuation)
- Paste the LLM-generated continuation into model_text
- The script computes simple feature counts as a stand-in for MDA dimensions

NOTE: This uses basic feature proxies, not a full MDA pipeline.
The point is to understand the formulas, not to produce real results.
"""

import re
import math
import numpy as np


# ============================================================
# PASTE YOUR TEXTS HERE
# ============================================================

# The original human-written text (will be split in half)
orig_text = """
Veðrið var hvasst þennan dag. Sjómennirnir höfðu siglt frá Ísafirði snemma morguns
og stefndu á Hornstrandir. Skipstjórinn sagði við hásetana að þeir skyldu búa sig
undir erfiða ferð. Vindurinn jókst eftir hádegi og bylgjurnar urðu hærri. Enginn
kvartaði þó. Þeir höfðu allir séð verra veður. Að kvöldi dags náðu þeir landi
og drógu bátinn á fjöruna. Eldurinn í kofa var kærkomin sjón eftir langan dag á sjó.
"""

# The LLM-generated continuation (given orig1 as prompt)
model_text = """
Skipstjórinn horfði út um gluggann og sá að veðrið var að batna. Hann ákvað að
halda áfram ferðinni næsta morgun. Hásetarnir voru þakklátir fyrir hvíldina og
settust niður við eldinn. Þeir ræddu um ferðalagið og deildu sögum af fyrri
úthöldum. Nóttin var rólega og allir sofnuðu vel.
"""


# ============================================================
# FEATURE EXTRACTION (simple proxies for MDA dimensions)
# ============================================================

def extract_features(text):
    """
    Extract simple linguistic features as proxies for MDA dimensions.
    
    Returns a dict of feature scores. These are NOT real Biber dimensions — 
    they're simple countable features to demonstrate the formulas.
    A real implementation would need a full Icelandic NLP pipeline (e.g. Greynir).
    """
    text = text.strip()
    
    # Tokenize simply
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = re.findall(r'\b\w+\b', text.lower())
    
    num_sentences = len(sentences) if sentences else 1
    num_words = len(words) if words else 1
    
    # Feature 1: Average sentence length (proxy for information density)
    avg_sentence_length = num_words / num_sentences
    
    # Feature 2: Past tense ratio (proxy for narrativity)
    # In Icelandic, common past tense endings include -ði, -ti, -aði, -uðu, -du
    past_tense_patterns = r'\b\w+(aði|uðu|ði|ti|du|ðu)\b'
    past_tense_count = len(re.findall(past_tense_patterns, text.lower()))
    past_tense_ratio = past_tense_count / num_words
    
    # Feature 3: Pronoun density (proxy for involved vs informational)
    # Common Icelandic pronouns
    pronouns = {'hann', 'hún', 'það', 'þeir', 'þær', 'þau', 'ég', 'við',
                'þú', 'þið', 'sig', 'sér', 'sín', 'hans', 'hennar', 'þeirra',
                'honum', 'henni', 'þeim', 'mér', 'okkur', 'þér', 'ykkur'}
    pronoun_count = sum(1 for w in words if w in pronouns)
    pronoun_ratio = pronoun_count / num_words
    
    # Feature 4: Long word ratio (proxy for formality/complexity)
    long_words = sum(1 for w in words if len(w) > 8)
    long_word_ratio = long_words / num_words
    
    # Feature 5: Conjunction density (proxy for textual cohesion)
    conjunctions = {'og', 'en', 'eða', 'því', 'þó', 'þar', 'sem', 'að',
                    'heldur', 'enda', 'svo', 'eftir', 'áður', 'þegar', 'meðan'}
    conjunction_count = sum(1 for w in words if w in conjunctions)
    conjunction_ratio = conjunction_count / num_words
    
    return {
        'avg_sentence_length': avg_sentence_length,
        'past_tense_ratio': past_tense_ratio,
        'pronoun_ratio': pronoun_ratio,
        'long_word_ratio': long_word_ratio,
        'conjunction_ratio': conjunction_ratio,
    }


def features_to_vector(features):
    """Convert feature dict to numpy array (consistent ordering)."""
    keys = sorted(features.keys())
    return np.array([features[k] for k in keys]), keys


# ============================================================
# MILIČKA'S FORMULAS
# ============================================================

def split_text_in_half(text):
    """Split text roughly in half by sentences."""
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]
    mid = len(sentences) // 2
    first_half = ' '.join(sentences[:mid])
    second_half = ' '.join(sentences[mid:])
    return first_half, second_half


def compute_benchmark(orig_text, model_text):
    """
    Compute Milička's benchmark metrics.
    
    Formula 1: Δv = v_orig2 - v_model        (stylistic shift per dimension)
    Formula 2: i = v_orig2 - v_orig1          (natural human variation)
    Formula 3: b_d = Δv̄_d / SE(I_d)          (normalized benchmark score)
    Formula 4: B = ||b||                       (single overall score)
    """
    
    # Split original text in half
    orig1, orig2 = split_text_in_half(orig_text)
    
    print("=" * 60)
    print("TEXTS")
    print("=" * 60)
    print(f"\norig1 (prompt given to LLM):\n  '{orig1[:100]}...'\n")
    print(f"orig2 (what the human actually wrote):\n  '{orig2[:100]}...'\n")
    print(f"model (what the LLM generated):\n  '{model_text.strip()[:100]}...'\n")
    
    # Extract features
    f_orig1 = extract_features(orig1)
    f_orig2 = extract_features(orig2)
    f_model = extract_features(model_text)
    
    v_orig1, keys = features_to_vector(f_orig1)
    v_orig2, _ = features_to_vector(f_orig2)
    v_model, _ = features_to_vector(f_model)
    
    # Formula 1: Δv = v_orig2 - v_model (shift between human and LLM)
    delta_v = v_orig2 - v_model
    
    # Formula 2: i = v_orig2 - v_orig1 (natural variation within human text)
    i = v_orig2 - v_orig1
    
    print("=" * 60)
    print("FEATURE SCORES PER TEXT")
    print("=" * 60)
    for idx, key in enumerate(keys):
        print(f"\n  {key}:")
        print(f"    orig1 (first half):    {v_orig1[idx]:.4f}")
        print(f"    orig2 (second half):   {v_orig2[idx]:.4f}")
        print(f"    model (LLM):           {v_model[idx]:.4f}")
        print(f"    Δv (formula 1):        {delta_v[idx]:.4f}  (orig2 - model)")
        print(f"    i  (formula 2):        {i[idx]:.4f}  (orig2 - orig1)")
    
    print("\n" + "=" * 60)
    print("BENCHMARK SCORES (formulas 3 and 4)")
    print("=" * 60)
    print("""
    NOTE: Formulas 3 and 4 are designed to work with MANY text pairs,
    averaging across them. With a single text pair (like this demo),
    we can only show the per-text differences. To compute b_d properly,
    you would need multiple text pairs and calculate:
    
        b_d = mean(Δv across all texts) / SE(i across all texts)
    
    With one text pair, we show the raw values instead.
    """)
    
    print("  Per-dimension results:")
    print(f"  {'Dimension':<25} {'Δv (shift)':<12} {'i (natural)':<12} {'|Δv| > |i|?'}")
    print(f"  {'-'*25} {'-'*12} {'-'*12} {'-'*12}")
    
    b_values = []
    for idx, key in enumerate(keys):
        shift = delta_v[idx]
        natural = i[idx]
        worse = "← MODEL DEVIATES MORE" if abs(shift) > abs(natural) else ""
        print(f"  {key:<25} {shift:<12.4f} {natural:<12.4f} {worse}")
        
        # For single text: use |i| as rough SE proxy (not statistically valid)
        if abs(natural) > 0.0001:
            b_d = shift / abs(natural)
        else:
            b_d = float('inf') if abs(shift) > 0.0001 else 0.0
        b_values.append(b_d)
    
    # Formula 4: B = ||b|| (Euclidean length)
    b_array = np.array([b for b in b_values if b != float('inf')])
    B = np.linalg.norm(b_array)
    
    print(f"\n  Formula 4 — B (overall distance): {B:.4f}")
    print(f"  (Lower = model is closer to human stylistic norms)")
    
    return delta_v, i, keys


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    compute_benchmark(orig_text, model_text)