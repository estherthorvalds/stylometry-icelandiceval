"""
Subject Drop Comparison — Human vs LLM Headlines
==================================================
Compares subject drop rates in POS-tagged Icelandic news headlines.

Subject drop = headline has no nominative noun or pronoun (no overt subject).
Based on the Icelandic POS tagset where:
  - Nouns (n): position 3 = case (n=nom, o=acc, þ=dat, e=gen)
  - Pronouns (f): case position varies by subtype
  - Verbs (s): identified by tag starting with 's'

Usage:
  python3 compare_headlines.py
  
  Update the file paths below to point to your JSON files.
"""

import json
import math
import sys


# ============================================================
# FILE PATHS — UPDATE THESE
# ============================================================

HUMAN_PATH = "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/human_texts/520_headlines_pos_tagged.json"

LLM_PATHS = {
    "Le_Chat_Fast": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/Le_Chat_Fast/520_Le_Chat_Fast.json",
    "Gemini_3_Thinking": "/Users/esther/Documents/GitHub/stylometry-icelandiceval/output/news_headlines/LLM_tagged_generated_texts/Gemini_3_Thinking/520_Gemini_3_Thinking.json",
}


# ============================================================
# POS TAG HELPERS
# ============================================================

def is_nominative_noun(pos):
    """Check if POS tag is a noun in nominative case.
    Icelandic noun tags: n + gender + case + number + article
    e.g. nkfn = noun, masculine, nominative, plural
         nhen = noun, neuter, nominative, singular
    Position 0: 'n' (noun)
    Position 1: gender (k=masc, v=fem, h=neut)
    Position 2: case (n=nom, o=acc, þ=dat, e=gen)
    Position 3: number (e=sing, f=plur)
    """
    if len(pos) >= 3 and pos[0] == 'n' and pos[2] == 'n':
        return True
    return False


def is_nominative_pronoun(pos):
    """Check if POS tag is a pronoun in nominative case.
    Pronoun tags start with 'f' and vary by subtype.
    Common patterns:
      fp1en = personal pronoun, 1st person, singular, nominative
      fp3kn = personal pronoun, 3rd person, masculine, nominative
      fa... = demonstrative pronoun
    The nominative marker 'n' appears at different positions
    depending on pronoun subtype, but generally:
    - Personal pronouns (fp): pos[4] or pos[3] = 'n' for nominative
    - Other pronouns: check if 'n' appears in case position
    
    Simplified approach: pronoun tag starts with 'f' and contains 
    'n' in positions 3-4 (after the subtype markers).
    """
    if len(pos) < 3 or pos[0] != 'f':
        return False
    # Check common nominative positions for pronouns
    if len(pos) >= 4 and pos[3] == 'n':
        return True
    if len(pos) >= 5 and pos[4] == 'n':
        return True
    return False


def is_finite_verb(pos):
    """Check if POS tag is a finite verb.
    Verb tags start with 's' followed by form markers.
    'sf' prefix = finite verb (sfg3en = finite, indicative, 3rd, singular, present)
    'sþ' prefix = past participle (not finite)
    'sn' prefix = infinitive (not finite)
    """
    if len(pos) >= 2 and pos[0] == 's' and pos[1] == 'f':
        return True
    return False


def has_nominative(tokens):
    """Check if headline has any nominative noun or pronoun (overt subject)."""
    for token in tokens:
        pos = token.get("pos", "")
        if is_nominative_noun(pos) or is_nominative_pronoun(pos):
            return True
    return False


def has_finite_verb(tokens):
    """Check if headline has a finite verb."""
    for token in tokens:
        pos = token.get("pos", "")
        if is_finite_verb(pos):
            return True
    return False


# ============================================================
# ANALYSIS
# ============================================================

def analyze_headlines(headlines):
    """Analyze a list of POS-tagged headlines.
    
    Returns dict with:
    - total: number of headlines
    - subject_drops: headlines with no nominative nominal
    - drop_rate: proportion of subject drops
    - has_verb_no_subject: headlines with finite verb but no subject
    - avg_tokens: average token count
    - avg_nominatives: average nominative count per headline
    - nom_per_token: nominative density
    """
    total = len(headlines)
    subject_drops = 0
    verb_no_subject = 0
    total_tokens = 0
    total_nominatives = 0
    
    for headline in headlines:
        tokens = headline.get("tokens", [])
        total_tokens += len(tokens)
        
        nom_count = sum(1 for t in tokens 
                       if is_nominative_noun(t.get("pos", "")) 
                       or is_nominative_pronoun(t.get("pos", "")))
        total_nominatives += nom_count
        
        has_nom = nom_count > 0
        has_verb = has_finite_verb(tokens)
        
        if not has_nom:
            subject_drops += 1
        
        if has_verb and not has_nom:
            verb_no_subject += 1
    
    return {
        "total": total,
        "subject_drops": subject_drops,
        "drop_rate": subject_drops / total if total > 0 else 0,
        "verb_no_subject": verb_no_subject,
        "avg_tokens": total_tokens / total if total > 0 else 0,
        "avg_nominatives": total_nominatives / total if total > 0 else 0,
        "nom_per_token": total_nominatives / total_tokens if total_tokens > 0 else 0,
    }


def load_json(path):
    """Load headlines from JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}")
        sys.exit(1)


def chi_squared_test(drops_a, total_a, drops_b, total_b):
    """Simple chi-squared test for comparing two proportions.
    Returns chi-squared statistic and whether p < 0.05 (df=1, critical=3.84).
    """
    nodrop_a = total_a - drops_a
    nodrop_b = total_b - drops_b
    
    total = total_a + total_b
    total_drops = drops_a + drops_b
    total_nodrops = nodrop_a + nodrop_b
    
    # Expected values
    expected = [
        [total_drops * total_a / total, total_nodrops * total_a / total],
        [total_drops * total_b / total, total_nodrops * total_b / total],
    ]
    
    observed = [
        [drops_a, nodrop_a],
        [drops_b, nodrop_b],
    ]
    
    chi2 = 0
    for i in range(2):
        for j in range(2):
            if expected[i][j] > 0:
                chi2 += (observed[i][j] - expected[i][j]) ** 2 / expected[i][j]
    
    significant = chi2 > 3.841  # p < 0.05 with df=1
    return chi2, significant


# ============================================================
# MAIN
# ============================================================

def main():
    # Load data
    human = load_json(HUMAN_PATH)
    
    llm_data = {}
    for name, path in LLM_PATHS.items():
        llm_data[name] = load_json(path)
    
    # Analyze
    human_stats = analyze_headlines(human)
    llm_stats = {name: analyze_headlines(data) for name, data in llm_data.items()}
    
    # Print results
    print("=" * 90)
    print("SUBJECT DROP COMPARISON — HUMAN vs LLM-GENERATED HEADLINES")
    print("=" * 90)
    print()
    print(f"{'Source':<25} {'Drop rate':>10} {'Drops':>7} {'V+no S':>8} "
          f"{'Total':>7} {'Avg tok':>8} {'Avg nom':>8} {'Nom/tok':>8}")
    print("-" * 90)
    
    # Human baseline
    s = human_stats
    print(f"{'Human':<25} {s['drop_rate']:>9.1%} {s['subject_drops']:>7} "
          f"{s['verb_no_subject']:>8} {s['total']:>7} {s['avg_tokens']:>8.1f} "
          f"{s['avg_nominatives']:>8.2f} {s['nom_per_token']:>8.4f}")
    
    # LLM results
    for name, s in llm_stats.items():
        print(f"{name:<25} {s['drop_rate']:>9.1%} {s['subject_drops']:>7} "
              f"{s['verb_no_subject']:>8} {s['total']:>7} {s['avg_tokens']:>8.1f} "
              f"{s['avg_nominatives']:>8.2f} {s['nom_per_token']:>8.4f}")
    
    print("-" * 90)
    print()
    print("Drop rate  = proportion of headlines with NO nominative nominal (subject drop)")
    print("V+no S     = headlines with a finite verb but no nominative (strongest subject drop)")
    print("Nom/tok    = nominative nominals per token (subject density)")
    
    # Statistical comparison
    print()
    print("=" * 90)
    print("STATISTICAL COMPARISON (chi-squared test, p < 0.05)")
    print("=" * 90)
    print()
    
    for name, s in llm_stats.items():
        chi2, sig = chi_squared_test(
            human_stats['subject_drops'], human_stats['total'],
            s['subject_drops'], s['total']
        )
        delta = s['drop_rate'] - human_stats['drop_rate']
        sig_str = "SIGNIFICANT" if sig else "not significant"
        print(f"  Human vs {name}:")
        print(f"    Delta drop rate: {delta:>+.1%}")
        print(f"    Chi-squared:     {chi2:.3f}  ({sig_str})")
        print()
    
    # Show example headlines with subject drop from human data
    print("=" * 90)
    print("EXAMPLES: Human headlines WITH subject drop (no nominative)")
    print("=" * 90)
    print()
    
    count = 0
    for h in human:
        tokens = h.get("tokens", [])
        if not has_nominative(tokens):
            text = " ".join(t["text"] for t in tokens)
            tags = " ".join(t["pos"] for t in tokens)
            print(f"  [{h['index']:>3}] {text}")
            print(f"        {tags}")
            print()
            count += 1
            if count >= 10:
                print(f"  ... and {human_stats['subject_drops'] - 10} more")
                break


if __name__ == "__main__":
    main()