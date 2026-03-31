# Skipulag skrifta / Script Architecture
## stylometry-icelandiceval

```
stylometry-icelandiceval/
│
├── README.md
├── research_log.md
├── decisions_log.md
├── reference_tracker.csv
│
├── models/
│   └── is_icepahc_transformer_finetuned_constituency.pt   # IceConParse þáttunarlíkan (Ingunn J.K., 2024)
│                                                           # Stanza + IceBERT, 90.38% F-score
│                                                           # Ekki á GitHub (of stórt), hlaða niður sérstaklega
│
├── data/
│   ├── human_texts/                    # Mannlegir textar — hreinn texti, ein setning/fyrirsögn per línu
│   │   ├── news_ruv.txt                # RÚV fréttir (úr RMH)
│   │   ├── news_huni.txt               # Húnahornið fréttafyrirsagnir (úr RMH)
│   │   ├── journals_islmal.txt         # Íslenskt mál og almenn málfræði (úr RMH)
│   │   ├── journals_laeknabladid.txt   # Læknablaðið (úr RMH)
│   │   ├── blogs_jonas.txt             # Jonas.is (úr RMH)
│   │   └── blogs_silfur.txt            # Silfur Egils (úr RMH)
│   │
│   ├── llm_texts/                      # Textar búnir til af risamállíkönum — sama snið
│   │   ├── news_ruv_gemini.txt
│   │   ├── news_ruv_gpt5.txt
│   │   ├── news_ruv_lechat.txt
│   │   ├── journals_islmal_gemini.txt
│   │   ├── blogs_jonas_gemini.txt
│   │   └── ...                         # Eitt per líkan × textategund
│   │
│   └── parsed/                         # Þáttuð tré — úttak úr parse_texts.py
│       ├── human/                      # Eitt tré per línu, sama röð og hreini textinn
│       │   ├── news_ruv_parsed.txt
│       │   ├── news_huni_parsed.txt
│       │   ├── journals_islmal_parsed.txt
│       │   ├── journals_laeknabladid_parsed.txt
│       │   ├── blogs_jonas_parsed.txt
│       │   └── blogs_silfur_parsed.txt
│       │
│       └── llm/
│           ├── news_ruv_gemini_parsed.txt
│           ├── news_ruv_gpt5_parsed.txt
│           └── ...
│
├── scripts/
│   │
│   ├── parse_texts.py                  # SKREF 1: Þáttar alla texta með IceConParse
│   │                                   # Inntak: data/human_texts/*.txt og data/llm_texts/*.txt
│   │                                   # Úttak: data/parsed/human/*.txt og data/parsed/llm/*.txt
│   │                                   # Hvert tré er ein lína, stjörnur (*) skipt út fyrir bandstrik (-)
│   │                                   # Keyra EINU SINNI — þáttun er dýr (~20 sek uppsetning + mínútur per skrá)
│   │
│   ├── dim1_frumlagsnafnfall.py        # VÍDD 1: Fyrirsagnir án frumlagsnafnliðar
│   │                                   # Les þáttuð tré, athugar NP-SBJ í trénu
│   │                                   # Telur hlutfall fyrirsagna/setninga sem hafa sögn en ekkert NP-SBJ
│   │                                   # Reiknar b_d og stig per líkan
│   │
│   ├── dim2_aukasetningar.py           # VÍDD 2: Hlutfall aukasetninga (subordination ratio)
│   │                                   # Les þáttuð tré, telur IP-SUB vs IP-MAT
│   │                                   # Hátt hlutfall = flóknari setningagerð (fræðitextar)
│   │                                   # Lágt hlutfall = einfaldari setningagerð (blogg, fréttir)
│   │
│   ├── dim3_nafnlidalengd.py           # VÍDD 3: Meðallengd nafnliða (mean NP length)
│   │                                   # Les þáttuð tré, telur tóka innan hvers NP-liðar
│   │                                   # Lengri nafnliðir = þéttari, upplýsingameiri texti
│   │
│   ├── run_milicka.py                  # AÐALSKRIFTA: Keyrir allar víddir, safnar b_d gildum
│   │                                   # Reiknar heildarfrávik B = ‖b‖ (formúla 4 Milička)
│   │                                   # Prentar stigatöflu og niðurstöður
│   │
│   └── style_score.py                  # Hjálparfall: Reiknar 0-100 stig úr v_human og v_model
│                                       # Formúla: stig = 100 × (1 - |v_human - v_model| / v_human)
│
├── output/                             # Niðurstöður og myndir
│   └── ...
│
└── archive/                            # Eldri skriftur og gögn sem ekki eru lengur í notkun
    ├── milicka_headlines_final.py       # Fyrsta útgáfa með Sonnet POS-merkingum
    ├── milicka_headlines_ingunnparser.py # Önnur útgáfa með IceConParse (proof of concept)
    └── json/                           # Eldri JSON-gögn frá Sonnet þáttun
```

## Flæði gagna / Data Flow

```
Hreinn texti (.txt)          Þáttuð tré (.txt)           Mælingar per vídd
─────────────────── → parse_texts.py → ──────────────────── → dim1/dim2/dim3 → run_milicka.py
data/human_texts/                       data/parsed/human/                      ↓
data/llm_texts/                         data/parsed/llm/                   Stigatafla + b_d
```

## Snið þáttaðra trjáa / Parsed Tree Format

Hvert tré er ein lína í textaskrá. Stjörnur (*) eru skipt út fyrir bandstrik (-).
Dæmi:

```
(ROOT (IP-MAT (NP-SBJ (NPR-N KPMG)) (VBPI opnar) (NP-OB1 (N-A skrifstofu)) (PP (P á) (NP (NPR-D Blönduósi)))))
(ROOT (IP-MAT (VBDI Fengu) (NP-OB1 (ADJP (ADV vel) (VAN búnar)) (NS-N verkfærakistur)) (PP (P að) (NP (N-D gjöf)))))
```

## Lykilmerki í IcePaHC þáttunarskema / Key Labels

| Merki | Merking | Notað í |
|-------|---------|---------|
| NP-SBJ | Frumlagsnafnliður (subject) | dim1 |
| IP-MAT | Aðalsetning (matrix clause) | dim2 |
| IP-SUB | Aukasetning (subordinate clause) | dim2 |
| IP-IMP | Boðháttur (imperative) | dim1 (útilokun) |
| NP | Nafnliður (noun phrase) | dim3 |
| VBPI/VBDI | Sögn í persónuhætti (finite verb, present/past indicative) | dim1 |
| VBPS/VBDS | Sögn í viðtengingarhætti (subjunctive) | dim1 |
| CP-REL | Tilvísunaraukasetning (relative clause) | dim2 |
| CP-ADV | Atviksorðsaukasetning (adverbial clause) | dim2 |

## Formúlur Milička / Milička's Formulas

```
Formúla 1: Δv = v_orig - v_model        (frávik líkans frá mannlegum texta)
Formúla 2: i = v_orig2 - v_orig1        (náttúrulegt frávik í mennskum gögnum)
Formúla 3: b_d = Δv / SE(I_d)           (staðlað frávik per vídd)
Formúla 4: B = ‖b‖                      (heildarskor yfir allar víddir)
```

## Textategundir / Text Categories

| Flokkur | Heimildir | Milička-hliðstæða |
|---------|-----------|-------------------|
| Fréttir (News) | RÚV, Húnahornið | Press: Reportage |
| Fræðitímarit (Journals) | Íslenskt mál og almenn málfræði, Læknablaðið | Learned |
| Blogg (Blogs) | Jonas.is, Silfur Egils | — (næst Miscellaneous / informal opinion) |

## Þáttari / Parser

IceConParse eftir Ingunn Jóhönnu Kristjánsdóttur (2024)
- Stanza-þáttunarpípa með IceBERT orðgreypingum
- Þjálfað á IcePaHC trjábankanum
- F-mæling: 90,38%
- GitHub: https://github.com/ingunnjk/IceConParse
- Líkan: is_icepahc_transformer_finetuned_constituency.pt
