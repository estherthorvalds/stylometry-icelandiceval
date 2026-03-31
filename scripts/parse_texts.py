# parse_texts.py

"""
parse_texts.py — loads IceConParse, parses all texts, saves parse trees to files
dim1_frumlagsfall.py — reads parsed files, measures frumlagsnafnliðarleysi
dim2_aukasetningar.py — reads parsed files, measures subordination ratio
dim3_nafnlidalengd.py — reads parsed files, measures mean NP length
run_milicka.py — executes all dimensions, collects b_d scores, calculates overall benchmark

"""

import stanza

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
# CLAUDE CODE - SEPARATE THESE TWO FUNCTIONS THAT ARE WITHIN THE SAME FUNCION, THIS ONE SHOULD ONLY PARSE, NOT DETERMINE IF A SENTENCE HAS A NOUN SUBJECT. 
# THIS COULD SHOULD RETURN A NEW TEXT AND SAVE IT
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
