# Skipulag skrifta / Script Architecture
## stylometry-icelandiceval

```
stylometry-icelandiceval/
│
├── README.md
├── ARCHITECTURE.md
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
│   ├── human_texts/                    # Hrá RMH-gögn, skipulögð eftir textategund (ekki á GitHub)
│   │   ├── academic/                   # Fræðitextar (Læknablaðið, úr RMH)
│   │   ├── blog/                       # Blogg (Jonas.is, úr RMH)
│   │   └── news/                       # Fréttir (RÚV, úr RMH)
│   │
│   ├── experiment/                     # Tilraunagögn — pöruð hönnun eftir Milička o.fl. (2025)
│   │   ├── selected_samples.csv        # Skrá yfir valin úrtök og klippistöðu
│   │   ├── prompts/                    # Fyrri helmingur mannlegra texta (ekki á GitHub)
│   │   │   ├── academic_prompt_001.txt
│   │   │   ├── blog_prompt_001.txt
│   │   │   ├── news_prompt_001.txt
│   │   │   └── ...                     # 15 per textategund = 45 prompt-skrár
│   │   │
│   │   ├── human_reference/            # Seinni helmingur mannlegra texta (ekki á GitHub)
│   │   │   ├── academic_ref_001.txt
│   │   │   ├── blog_ref_001.txt
│   │   │   ├── news_ref_001.txt
│   │   │   └── ...                     # 15 per textategund = 45 viðmiðsskrár
│   │   │
│   │   ├── llm_continuations/          # Framhald LLM-líkana — hvert líkan í sinni möppu
│   │   │   ├── gemini_3_thinking/      # Google Gemini 2.5 Pro (Thinking)
│   │   │   │   ├── academic/
│   │   │   │   ├── blog/
│   │   │   │   └── news/
│   │   │   ├── gpt_5/                  # OpenAI GPT-5
│   │   │   ├── le_chat_fast/           # Mistral Le Chat (fast)
│   │   │   └── le_chat_thinking/       # Mistral Le Chat (thinking)
│   │   │
│   │   └── llm_continuations_preprocessed/  # Forunnin LLM-framhöld (eftir preprocess_llm_output.py)
│   │       ├── gemini_3_thinking/
│   │       ├── gpt_5/
│   │       ├── le_chat_fast/
│   │       └── le_chat_thinking/
│   │
│   ├── unseen_authored_texts/          # Óséð höfundatextar (.txt og .rtf) — ekki á GitHub
│   │                                   # 15 bókmenntatextar til viðbótartilraunar
│   │
│   ├── experiment_unseen/              # Tilraunagögn óséðra texta — ekki á GitHub
│   │   ├── selected_samples.csv        # Upplýsingar um öll úrtök og klippistöðu
│   │   ├── prompts/                    # Fyrri helmingur (unseen_prompt_001.txt, ...)
│   │   ├── human_reference/            # Seinni helmingur (unseen_ref_001.txt, ...)
│   │   └── llm_continuations/          # Tómar möppur fyrir LLM-úttak
│   │       ├── gemini_3_thinking/
│   │       ├── gpt_5/
│   │       ├── le_chat_thinking/
│   │       └── le_chat_fast/
│   │
│   ├── raw/                            # Hrá XML-gögn úr RMH (ekki á GitHub)
│   └── figures/                        # Myndir til skýrslunnar
│
├── scripts/
│   │
│   │   # --- GAGNAUNDIRBÚNINGUR / DATA PREPARATION ---
│   │
│   ├── extract_samples.py              # Draga ~2.000 orða úrtök úr RMH TEI XML skrám
│   │                                   # Les .ana.xml og .xml snið, hreinsar, staðlar
│   │                                   # Inntak: data/raw/   Úttak: data/human_texts/
│   │
│   ├── prepare_paired_experiment.py    # Búa til pöruð gögn: klippa texta í tvennt
│   │                                   # Fyrri helmingur → prompts/, seinni → human_reference/
│   │                                   # Fylgir Milička o.fl. (2025) aðferð
│   │
│   ├── prepare_unseen_authored_texts.py # Undirbúa óséð höfundatexta fyrir Milička-tilraun
│   │                                   # Les .txt og .rtf skrár úr data/unseen_authored_texts/
│   │                                   # Klippir við setningamörk nálægt miðju
│   │                                   # SKRIF-meðhöndlun fyrir HUSVORDURINN (kafli/skrif-skipulag)
│   │                                   # Úttak: data/experiment_unseen/
│   │
│   ├── preprocess_llm_output.py        # Hreinsa LLM-framhöld: fjarlægja markdown, meta-athugasemdir
│   │                                   # Sama forvinnsla og extract_samples.py
│   │                                   # Endurtekningargreining gegn prompt-texta (--prompt-dir)
│   │                                   # Inntak: llm_continuations/  Úttak: llm_continuations_preprocessed/
│   │
│   ├── parse_texts.py                  # Þáttar alla texta með IceConParse
│   │                                   # Hvert tré er ein lína, stjörnur (*) skipt út fyrir bandstrik (-)
│   │                                   # Keyra EINU SINNI — þáttun er dýr
│   │                                   # Þáttar bæði aðaltilraun og óséða höfundatexta
│   │
│   ├── integrity_check.py              # Heilleikaskoðun á LLM-framhöldum (keyra FYRIR þáttun)
│   │                                   # 7 athuganir: tvítekin efni, prompt-leki, lágmarkslengd,
│   │                                   # möppu/heitamisræmi, vantar pör, tungumál, NaN-hlutfall
│   │                                   # Viðvarar en stöðvar ekki pípuna
│   │                                   # Úttak: output/integrity_report.txt
│   │
│   │   # --- MÆLIVÍDDIR / MEASUREMENT DIMENSIONS ---
│   │   # Allar lesa þáttuð tré nema dim6 (les hrátexta)
│   │
│   ├── dim1_frumlagsnafnfall.py        # VÍDD 1: Frumlagsnafnliðarleysi (subject drop rate)
│   │                                   # Telur hlutfall setninga með sögn en án NP-SBJ
│   │
│   ├── dim2_aukasetningar.py           # VÍDD 2: Hlutfall aukasetninga (subordination ratio)
│   │                                   # Telur IP-SUB vs IP-MAT
│   │
│   ├── dim3_nafnlidalengd.py           # VÍDD 3: Meðallengd nafnliða (mean NP length)
│   │                                   # Telur tóka innan NP-liða
│   │
│   ├── dim4_past_tense.py              # VÍDD 4: Hlutfall þátíðarsagna (past tense ratio)
│   │                                   # Telur D-tíðarmerki í sagnhnútum (VB|BE|MD|DO|HV|RD)D(I|S)
│   │
│   ├── dim5_thirdperson_pronouns.py    # VÍDD 5: Þriðjupersónufornöfn (third person pronouns)
│   │                                   # Ber saman PRO-* orðform við lokaða mengi 18 forma
│   │
│   ├── dim6_word_length.py             # VÍDD 6: Meðalorðalengd (mean word length)
│   │                                   # Les HRÁTEXTA (ekki þáttuð tré)
│   │                                   # Mælir meðal/miðgildi/staðalfrávik/hlutfall 8+ stafa orða
│   │
│   ├── dim7_complementizers.py         # VÍDD 7: Tíðni tengiorða (complementizer frequency)
│   │                                   # Telur (C sem) og (C að) í þáttuðum trjám
│   │                                   # Mælir sem/að hlutfall og tíðni per 1.000 orð
│   │
│   │   # --- SAMEINING OG MAT / AGGREGATION AND SCORING ---
│   │
│   ├── run_milicka.py                  # AÐALSKRIFTA: Keyrir allar víddir, safnar b_d gildum
│   │                                   # Reiknar heildarfrávik B = ‖b‖ (formúla 4 Milička)
│   │                                   # --plot: Milička-stíls dreifirit og B-gildi súlurit
│   │                                   # --output-csv: Vista niðurstöður sem CSV
│   │                                   # Úttak mynda: output/figures/
│   │
│   ├── style_score.py                  # Hjálparfall: Reiknar 0-100 stig úr v_human og v_model
│   │
│   └── validation_harness.py           # Sannprófunartól: Slembiúrtak þáttunar til handvirkrar yfirferðar
│
├── output/                             # Niðurstöður og myndir
│   ├── parsed/                         # Þáttuð tré (.psd skrár)
│   │   ├── prompts/                    # Þáttuð prompt-gögn (bæði aðaltilraun og óséð)
│   │   ├── human_reference/            # Þáttuð viðmiðsgögn (bæði aðaltilraun og óséð)
│   │   └── llm_continuations_preprocessed/  # Þáttuð LLM-framhöld
│   ├── figures/                        # Dreifirit og súlurit (frá run_milicka.py --plot)
│   │   ├── scatter_dim1.png ... scatter_dim7.png
│   │   └── B_scores.png
│   ├── integrity_report.txt            # Skýrsla frá integrity_check.py
│   └── milicka_results.csv             # CSV-niðurstöður (frá run_milicka.py --output-csv)
│
└── archive/                            # Eldri skriftur og gögn sem ekki eru lengur í notkun
    ├── milicka_headlines_final.py       # Fyrsta útgáfa með Sonnet POS-merkingum
    ├── milicka_headlines_ingunnparser.py # Önnur útgáfa með IceConParse (proof of concept)
    └── json/                           # Eldri JSON-gögn frá Sonnet þáttun
```

## Flæði gagna / Data Flow

### Aðaltilraun / Main Experiment (RMH-gögn)

```
RMH XML-gögn           Hrein úrtök            Pöruð gögn              Þáttuð tré           Mælingar per vídd
──────────────── → extract_samples.py → prepare_paired_experiment.py → parse_texts.py → dim1–dim7 → run_milicka.py
data/raw/              data/human_texts/       data/experiment/         output/parsed/            ↓
                                               ├── prompts/                                  Stigatafla + B-gildi
                                               ├── human_reference/                          + dreifirit (--plot)
                                               └── llm_continuations/
                                                     ↓
                                               preprocess_llm_output.py → llm_continuations_preprocessed/
                                                     ↓
                                               integrity_check.py  (viðvörunarskýrsla)
                                                     ↓
                                               parse_texts.py → dim1–dim7
```

### Óséð höfundatextar / Unseen Authored Texts

```
Bókmenntatextar (.txt/.rtf)      Pöruð gögn                    Þáttuð tré
──────────────────────────── → prepare_unseen_authored_texts.py → parse_texts.py → dim1–dim7
data/unseen_authored_texts/      data/experiment_unseen/          output/parsed/
                                 ├── prompts/                     ├── prompts/unseen_*
                                 ├── human_reference/             └── human_reference/unseen_*
                                 └── llm_continuations/
```

### Pöruð tilraunahönnun / Paired Experiment Design

Eftir Milička o.fl. (2025):
1. Velja ~2.000 orða mannlegan texta
2. Klippa í tvennt: fyrri helmingur = prompt, seinni helmingur = viðmið
3. LLM-líkan fær prompt + leiðbeiningar, skrifar framhald
4. Bera saman stíleinkenni framhalds (dim1–dim7) við viðmið mannsins

### Óséð tilraun / Unseen Experiment

Sama pöruð aðferð, en á óséðum bókmenntatextum (15 verk) í stað RMH-úrtaka.
SKRIF-meðhöndlun: HUSVORDURINN hefur kafli/skrif-uppbyggingu; klipping
tryggir að SKRIF-efni sé í báðum helmingum.

## Ekki á GitHub / Not on GitHub

Eftirfarandi er í `.gitignore` og er aðeins til staðar á staðbundnum vélum:

| Slóð | Ástæða |
|------|--------|
| `data/raw/` | Hrá RMH XML-gögn (leyfisskyld) |
| `data/human_texts/` | RMH-afleidd úrtök (leyfisskyld) |
| `data/experiment/prompts/` | Fyrri helmingar RMH-texta |
| `data/experiment/human_reference/` | Seinni helmingar RMH-texta |
| `data/unseen_authored_texts/` | Óséð höfundatextar (leyfisskyld) |
| `data/experiment_unseen/` | Öll óséð tilraunagögn |
| `output/parsed/prompts/unseen_*` | Þáttuð tré óséðra prompt-texta |
| `output/parsed/human_reference/unseen_*` | Þáttuð tré óséðra viðmiðstexta |
| `models/` | IceConParse líkansvæði (of stórt) |

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
| IP-MAT | Aðalsetning (matrix clause) | dim2, dim7 |
| IP-SUB | Aukasetning (subordinate clause) | dim2, dim7 |
| IP-IMP | Boðháttur (imperative) | dim1 (útilokun) |
| NP | Nafnliður (noun phrase) | dim3 |
| VB/BE/MD/DO/HV/RD + P/D + I/S | Persónubeygt sagnform (finite verb) | dim1, dim4 |
| PRO-N/A/D/G | Fornafn í falli (pronoun in case) | dim5 |
| ES | Gervifrumlag (expletive subject) | dim5 (útilokun — annað merki en PRO) |
| C | Tengiorð (complementizer: sem, að) | dim7 |
| P | Forsetning (preposition: að o.fl.) | dim7 (útilokun — ekki C) |
| TO | Nafnháttarmerki (infinitive marker: að) | dim7 (útilokun — ekki C) |
| CP-REL | sem-tilvísunaraukasetning (relative clause) | dim2, dim7 |
| CP-THT | að-fallsetning (that-clause) | dim7 |
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
| Óséð (Unseen) | 15 bókmenntatextar | — (viðbótartilraun á nýjum textum) |

## Þáttari / Parser

IceConParse eftir Ingunn Jóhönnu Kristjánsdóttur (2024)
- Stanza-þáttunarpípa með IceBERT orðgreypingum
- Þjálfað á IcePaHC trjábankanum
- F-mæling: 90,38%
- GitHub: https://github.com/ingunnjk/IceConParse
- Líkan: is_icepahc_transformer_finetuned_constituency.pt
