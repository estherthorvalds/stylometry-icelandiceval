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
│   │   │   └── ...                     # 15 per textategund × 4 (academic/blog/news/unseen) = 60 skrár
│   │   │
│   │   ├── human_texts/                # Seinni helmingur mannlegra texta (ekki á GitHub)
│   │   │   ├── academic_ref_001.txt
│   │   │   ├── blog_ref_001.txt
│   │   │   ├── news_ref_001.txt
│   │   │   ├── unseen_ref_001.txt
│   │   │   └── ...                     # 60 viðmiðsskrár (academic/blog/news/unseen)
│   │   │
│   │   ├── llm_continuations/          # Framhald LLM-líkana — hvert líkan í sinni möppu
│   │   │   ├── claude_sonnet46/        # Anthropic Claude Sonnet 4.6 (gegnum Anthropic API)
│   │   │   │   ├── academic/
│   │   │   │   ├── blog/
│   │   │   │   ├── news/
│   │   │   │   └── unseen/
│   │   │   ├── deepseek_V32_expert/    # DeepSeek V3.2 Expert
│   │   │   ├── gemini_3_thinking/      # Google Gemini 2.5 Pro (Thinking)
│   │   │   ├── gpt_5/                  # OpenAI GPT-5
│   │   │   ├── le_chat_balanced/       # Mistral Le Chat (free / balanced) — sjá MODEL_ALIASES
│   │   │   ├── le_chat_fast/           # Mistral Le Chat (free / fast, lagt niður) — sjá MODEL_ALIASES
│   │   │   └── le_chat_thinking/       # Mistral Le Chat (thinking)
│   │   │
│   │   ├── llm_continuations_clean/    # Forunnin LLM-framhöld (eftir preprocess_llm_output.py)
│   │   │   ├── claude_sonnet46/
│   │   │   ├── deepseek_V32_expert/
│   │   │   ├── gemini_3_thinking/
│   │   │   ├── gpt_5/
│   │   │   ├── le_chat_balanced/
│   │   │   ├── le_chat_fast/
│   │   │   └── le_chat_thinking/
│   │   │
│   │   └── excluded_from_pipeline/     # Skrár sem féllu á heilleikaskoðun
│   │       └── unseen_lechat_failures/ # Le Chat unseen-keyrslur sem voru útilokaðar
│   │
│   ├── unseen_authored_texts/          # Óséð höfundatextar (.txt og .rtf) — ekki á GitHub
│   │                                   # 15 bókmenntatextar til viðbótartilraunar
│   │
│   ├── experiment_unseen/              # Tilraunagögn óséðra texta — ekki á GitHub
│   │   ├── selected_samples.csv        # Upplýsingar um öll úrtök og klippistöðu
│   │   ├── prompts/                    # Fyrri helmingur (unseen_prompt_001.txt, ...)
│   │   ├── human_reference/            # Seinni helmingur (unseen_ref_001.txt, ...)
│   │   └── llm_continuations/          # Tómar möppur fyrir LLM-úttak
│   │       ├── claude_sonnet46/
│   │       ├── deepseek_V32_expert/
│   │       ├── gemini_3_thinking/
│   │       ├── gpt_5/
│   │       ├── le_chat_balanced/
│   │       ├── le_chat_fast/
│   │       └── le_chat_thinking/
│   │
│   ├── raw/                            # Hrá XML-gögn úr RMH (ekki á GitHub)
│   └── figures/                        # Myndir til skýrslunnar (tókunarsamanburður RÚV, Claude-endurtekning)
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
│   ├── generate_claude_continuations.py # Sækja LLM-framhöld gegnum Anthropic API
│   │                                   # Notar prompts/ + leiðbeiningarlínu úr run_milicka.py
│   │                                   # Vistar í data/experiment/llm_continuations/claude_sonnet46/
│   │                                   # Hæði: anthropic SDK, ANTHROPIC_API_KEY
│   │
│   ├── preprocess_llm_output.py        # Hreinsa LLM-framhöld: markdown, meta, samskeyti, endurtekningar
│   │                                   # Sama forvinnsla og extract_samples.py
│   │                                   # Samskeytaaðgreining með BÍN-staðfestingu (ákvörðun 029)
│   │                                   # Endurtekningargreining gegn prompt-texta (--prompt-dir)
│   │                                   # Inntak: llm_continuations/  Úttak: llm_continuations_clean/
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
│   │   # Þáttuð tré (.psd): dim1–5, dim7, dim9
│   │   # Hrár texti (.txt): dim6, dim8, dim10, dim11
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
│   ├── dim8_bin_ratio.py               # VÍDD 8: BÍN-þekja (BÍN vocabulary coverage)
│   │                                   # Les HRÁTEXTA, flettir tókum upp í BÍN með `islenska`-safninu
│   │                                   # 4-flokka staða: exact | compound | proper_name | oov
│   │                                   # Compound-greining: bmynd hefur FLEIRI bandstrik en inntak
│   │                                   # Samheiti/nöfn: hluti ∈ {ism, föð, móð, örn, göt, fyr, erm, bibl, lönd, þor}
│   │                                   # Reikna-einu-sinni: skrifar output/dim8_bin_summary.csv + dim8_bin_detail.csv
│   │                                   # run_milicka.py les CSV-ið beint; keyrir aldrei Bin() aftur
│   │                                   # `islenska` er valkvætt hæði (krefst python3-dev/libffi-dev á Linux)
│   │
│   ├── dim9_tree_depth.py              # VÍDD 9: Setningaþyngd — dýpt setningatrjáa (syntactic complexity)
│   │                                   # Les ÞÁTTUÐ TRÉ (.psd). 
│   │                                   # Mælir hámarksdýpt liðgerðartrjáa per setningu 
│   │                                   # rót = dýpt 0, flókin = dýpt ≥ 3
│   │                                   # meðaldýpt hreiðraðra (nested) aukasetninga IP-SUB
│   │                                   # Kallast á við dim2 (TÍÐNI aukasetninga vs. DÝPT innfelldra liða).
│   │                                   # Aðal-v: `mean_tree_depth`.
│   │
│   ├── dim10_lix.py                    # VÍDD 10: LIX-læsileikaskor (Läsbarhetsindex)
│   │                                   # Les upprunalega texta. 
│   │                                   # LIX = (orð/setn) + (löng_orð/orð × 100)
│   │                                   # „Löng orð“ = lengd > 6 stafir (hægt að breyta)
│   │                                   # Kallast á við dim6 ≥ 8 orðalengd
│   │                                   # Setningagreining: `tokenizer`-pakki Miðeindar
│   │                                   # Hæði: `tokenizer>=3.4`
│   │
│   ├── dim11_mtld.py                   # VÍDD 11: Orðaforðafjölbreytni (MTLD)
│   │                                   # McCarthy & Jarvis (2010) — lengdarstöðugt TTR.
│   │                                   # Les upprunalega texta.
│   │                                   # Rúllandi TTR, faktor lokaður þegar TTR < 0.72;
│   │                                   # hlutafaktor í lok: (1 - TTR_end) / (1 - 0.72).
│   │                                   # final_mtld = mean(forward, reverse)
│   │                                   # Wordforms (ekki lemma) — íslensk beyging getur
│   │                                   # blásið upp fjölbreytni (skjalfest takmörkun).
│   │                                   # Samnýtir dim6-tókunarreglur (PUNCT_TO_STRIP/HAS_LETTER).
│   │                                   # Engar nýjar háðir (notar staðal-Python + dim6-fallið).
│   │
│   │   # --- SAMEINING OG MAT / AGGREGATION AND SCORING ---
│   │
│   ├── run_milicka.py                  # AÐALSKRIFTA: Keyrir allar víddir, safnar b_d gildum
│   │                                   # Reiknar B = √(mean(b_d²))  — RMS-form (sjá ákvörðun 028)
│   │                                   # MODEL_ALIASES: le_chat_fast + le_chat_balanced → le_chat_free
│   │                                   # --plot: Milička-stíls dreifirit og B-gildi súlurit
│   │                                   # --output-csv: Vista niðurstöður sem CSV
│   │                                   # Úttak mynda: output/figures/
│   │
│   ├── style_score.py                  # Hjálparfall: Reiknar 0-100 stig úr v_human og v_model
│   │
│   ├── validation_harness.py           # Sannprófunartól: Slembiúrtak þáttunar til handvirkrar yfirferðar
│   │
│   └── archive/                        # Eldri tilraunaskriftur (fréttafyrirsagnatilraun + fyrstu prófanir)
│       ├── compare_headlines_v1.py     # Fyrsta tilraun á fyrirsögnum
│       ├── compare_headlines_v2.py     # Önnur útgáfa
│       ├── extract_headlines.py        # Sækja fyrirsagnir (RÚV)
│       ├── extract_headline_texts.py   # Sækja meginmál fyrirsagna
│       ├── merge_batches.py            # Sameina API-keyrslubunkur
│       ├── milicka_formulas.py         # Fyrsta Claude-prófun á formúlum
│       ├── milicka_headlines.py        # Sonnet POS-merking (proof of concept)
│       ├── milicka_headlines_ingunnparser.py # IceConParse-tilraun (proof of concept)
│       └── testing_stanza_parser.py    # Stanza-uppsetningarprófun
│
├── tests/
│   └── test_split_concatenated_tokens.py # 13 einingaprófanir á samskeyta-aðgreiningu (ákvörðun 029)
│
├── output/                             # Niðurstöður og myndir
│   ├── parsed/                         # Þáttuð tré (.psd skrár)
│   │   ├── prompts/                    # Þáttuð skipanagögn (bæði aðaltilraun og óséð)
│   │   ├── human_texts/                # Þáttuð viðmiðsgögn (bæði aðaltilraun og óséð)
│   │   └── llm_continuations_clean/    # Þáttaðir gervigreindartextar (framhald)
│   ├── figures/                        # Dreifirit og súlurit (frá run_milicka.py --plot)
│   │   ├── scatter_dim1.png ... scatter_dim11.png  (11 dreifirit, eitt per vídd)
│   │   └── B_scores.png
│   ├── integrity_report.txt            # Skýrsla frá integrity_check.py
│   ├── dim6_word_length.csv            # Per-skrá orðalengdarmælingar (cache)
│   ├── dim8_bin_summary.csv            # Ein lína per skrá — heildartölur (frá dim8_bin_ratio.py)
│   ├── dim8_bin_detail.csv             # Ein lína per tóka — tóki, staða, orðflokkur, lemma, oov_guess
│   ├── dim8_bin_summary_{prompts,human,llm}.csv  # Per-hluta keyrslur dim8 (sumarþyngra cache)
│   ├── dim8_bin_detail_{prompts,human,llm}.csv   # Per-hluta keyrslur dim8 (detail)
│   ├── dim9_tree_depth.csv             # Per-skrá trédýptamælingar (cache)
│   ├── dim10_lix.csv                   # Per-skrá LIX-skor (cache)
│   ├── milicka_results.csv             # CSV-niðurstöður (frá run_milicka.py --output-csv)
│   └── milicka_results_*.csv           # Eldri keyrslur (post_dim7fix, post_dim8fix, 4models)
│
├── archive/                            # Eldri JSON-úttak og útilokuð gögn
│   ├── excluded/                       # Snemma útilokaðar Le Chat keyrslur
│   ├── json_outputs_for_sonnet/        # Eldri JSON-gögn frá Sonnet POS-tilraun
│   └── original_repetition_report.txt  # Upprunaleg endurtekningarskýrsla (proof of concept)
│
├── audit_nan_handling.md               # Skoðun á NaN-áhættu allra vídda (ákvörðun 028)
├── style_score_leaderboard.py          # Stigatafla úr milicka_results CSV (notar pandas)
├── test_api_anthropic.py               # Lítið prófdæmi fyrir Anthropic API
└── rename_lechat.sh                    # Einnota nafnabreytingaskrift (le_chat_* staðlað)
```

## Flæði gagna / Data Flow

### Aðaltilraun / Main Experiment (RMH-gögn)

```
RMH XML-gögn           Hrein úrtök            Pöruð gögn              Þáttuð tré           Mælingar per vídd
──────────────── → extract_samples.py → prepare_paired_experiment.py → parse_texts.py → dim1–dim11 → run_milicka.py
data/raw/              data/human_texts/       data/experiment/         output/parsed/     dim6, dim10, dim11 (hrátexti)  ↓
                                               ├── prompts/                                dim8 (hrátexti, cache)  Stigatafla + B-gildi
                                               ├── human_texts/                                                   + dreifirit (--plot)
                                               └── llm_continuations/
                                                     ↓
                                               preprocess_llm_output.py → llm_continuations_clean/
                                                     ↓
                                               integrity_check.py  (viðvörunarskýrsla)
                                                     ↓
                                               parse_texts.py → dim1–dim5, dim7, dim9
                                                     +
                                               dim6_word_length.py, dim10_lix.py, dim11_mtld.py
                                                 (hrátexti — reiknað í run_milicka)
                                                     +
                                               dim8_bin_ratio.py → output/dim8_bin_summary.csv
                                                                 → output/dim8_bin_detail.csv
                                                                   (reikna-einu-sinni; run_milicka les CSV)
```

### Óséð höfundatextar / Unseen Authored Texts

```
Bókmenntatextar (.txt/.rtf)      Pöruð gögn                    Þáttuð tré
──────────────────────────── → prepare_unseen_authored_texts.py → parse_texts.py → dim1–dim5, dim7, dim9 + dim6/dim8/dim10/dim11 (hrátexti)
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
4. Bera saman stíleinkenni framhalds (dim1–dim11) við viðmið mannsins

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
| `data/experiment/human_texts/` | Seinni helmingar RMH-texta |
| `data/experiment/prompts/unseen/` | Promp-skrár óséðra texta (þegar þær eru í undirmöppu) |
| `data/experiment/llm_continuations/*/unseen/` | LLM-framhöld óséðra texta (þegar þau eru í undirmöppu) |
| `data/unseen_authored_texts/` | Óséð höfundatextar (leyfisskyld) |
| `data/experiment_unseen/` | Öll óséð tilraunagögn (eldri möppulagning) |
| `output/parsed/prompts/unseen_*` | Þáttuð tré óséðra prompt-texta |
| `output/parsed/human_reference/unseen_*` | Þáttuð tré óséðra viðmiðstexta (eldri heiti) |
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
| IP-SUB | Aukasetning (subordinate clause) | dim2, dim7, dim9 |
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
Formúla 4 (aðlöguð): B = √(mean(b_d²))  (RMS-form — sjá ákvörðun 028)
```

Upphafleg formúla 4 hjá Milička (2025) er `B = ‖b‖ = √(Σ b_d²)` — evklíðskt
norm. Hér er notað RMS-form til að halda B-skori sambærilegu þvert á
málsýni þegar einstakar víddir skila NaN. Þegar allar n víddir eru gildar
gildir `√(mean(b_d²)) = ‖b‖ / √n` — sama röðun, fastur kvarðamunur √n.

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

## Beygingarlýsing / BÍN (dim8)

`dim8_bin_ratio.py` flettir tókum upp í Beygingarlýsingu íslensks nútímamáls (BÍN)
í gegnum `islenska`-safnið (BinPackage) frá Miðeind.

- Pakki: https://pypi.org/project/islenska/
- Háð: valkvæð — verkefnið keyrir án `islenska`, en dim8 verður sleppt
- Á Linux krefst uppsetning oft `python3-dev` og `libffi-dev`
- Útgáfa í `requirements.txt`: `islenska>=1.0`

### Reikna-einu-sinni (parse-once caching)

Uppfletting í BÍN er hæg miðað við aðrar víddir. Til að halda `run_milicka.py`
hraðvirku og með færri háðsemdir fylgir dim8 sér pípu:

1. `python scripts/dim8_bin_ratio.py --text-dir data/experiment/human_texts`
   (o.s.frv. fyrir hverja möppu) → skrifar tvö CSV í `output/`
2. `run_milicka.py` les `output/dim8_bin_summary.csv` beint og flettir upp
   `in_bin_ratio` per skrárnafni. Kallar ALDREI á `Bin()` sjálft.
3. Ef summary-CSV vantar birtir `run_milicka` eina viðvörun og sleppir dim8
   (fær NaN í b-gildi) — aðrar víddir haldast óbreyttar.

Þetta þýðir að `islenska` þarf aðeins að vera uppsett á þeirri vél sem
reiknar dim8. Aðrir samstarfsmenn geta sótt CSV-ið úr útgáfustjórn og keyrt
`run_milicka` án þess að setja upp pakkann.

### Úttak dim8

| Skrá | Línur | Hlutverk |
|------|-------|----------|
| `output/dim8_bin_summary.csv` | 1 per skrá | Heildartölur og hlutföll (`in_bin_ratio`, `exact_ratio`, `compound_ratio`, `proper_name_ratio`, `oov_ratio`, `archaic_icelandic_ratio`, `archaic_z_unverified_ratio`) |
| `output/dim8_bin_detail.csv`  | 1 per tóka | `tóki`, `staða`, `orðflokkur`, `lemma`, `oov_guess` (fyrir villuleit) |

`run_milicka` notar aðeins summary-skrána. `--no-detail` flagg sleppir
detail-skránni ef aðeins heildartölur eru nauðsynlegar.

`oov_guess` ∈ {`foreign` (c/q/w), `archaic_icelandic` (z OG z→s mynd í BÍN — staðfest fornleg stafsetning fyrir 1973–74), `archaic_z_unverified` (z EN z→s mynd ekki í BÍN — líklega erlent sérnafn eða tökuorð), `likely_proper_name` (hástafur í miðri setningu), `unknown`}. Sjá ákvörðun 025 fyrir upphaflega aðgreiningu og ákvörðun 026 fyrir BÍN-staðfestingarþrepið.

### Stöðuflokkar (status)

| Staða | Skilgreining |
|-------|--------------|
| `exact` | Tóki finnst í BÍN sem sjálfstætt orð |
| `compound` | BÍN skilar samsetningu með fleiri bandstrikum en inntakið (t.d. `heilbrigðisþjónusta` → `heilbrigðis-þjónusta`) |
| `proper_name` | `hluti` ∈ {ism, föð, móð, örn, göt, fyr, erm, bibl, lönd, þor} (eiginheiti) |
| `oov` | Ekki í BÍN (tölur, erlent, nýyrði, stafsetningarvillur, fornt mál) |

Aðal-v fyrir Milička: `in_bin_ratio = (exact + compound + proper_name) / total`.

## Setningarþyngd — trédýpt (dim9)

`dim9_tree_depth.py` mælir setningaflækjustig með trédýpt á IcePaHC
liðgerðartrjám. Aðlagað úr „sentence weight“ fyrirlestri Steinþórs
Steingrímssonar sem byggði á Universal Dependencies-háðartrjám; hér er
sama hugmynd yfirfærð á liðgerðartré.

### Tengsl við dim2 — orthogonal merki / orthogonal signals

- **dim2 (Aukasetningar):** mælir TÍÐNI aukasetninga — hversu oft
  aukasetning kemur fyrir sem hlutfall af öllum setningum
  (IP-SUB / (IP-MAT + IP-SUB)).
- **dim9 (Trédýpt):** mælir DÝPT innfelldra liða — hversu langt er
  milli rótar og dýpsta laufa í liðgerðartré.

Textinn getur því verið:
- dim2 hátt, dim9 lágt — margar aukasetningar hver fyrir sig á grunnri dýpt
- dim2 miðlungs, dim9 hátt — færri en djúpt hreiðraðar aukasetningar
- bæði há — formlegur fræðitexti með margar djúpt innfelldar aukasetningar

### Þrjár undirmælingar

| Dálkur | Skilgreining |
|--------|--------------|
| `total_sentences` | Fjöldi trjáa í skrá (eftir síun tómra trjáa) |
| `mean_tree_depth` | Meðal-hámarksdýpt per tré. Rót = dýpt 0. **Aðal-v.** |
| `std_tree_depth` | Staðalfrávik trédýpta (population std) |
| `pct_complex_trees` | Hlutfall trjáa með dýpt ≥ 3 |
| `total_ip_sub` | Heildarfjöldi IP-SUB-hnúta í skránni |
| `mean_ip_sub_nesting` | Meðal-hreiðslustig IP-SUB (fjöldi IP-SUB forfeðra) |

### Þröskuldur „flókið tré“ (≥ 3)

Sami þröskuldur og í fyrirlestri Steinþórs (UD-byggt). IcePaHC
liðgerðartré eru KERFISBUNDIÐ DÝPRI en UD-háðartré vegna POS-hnúta
sem vefja utan um orð, svo `pct_complex_trees` verður hátt (~99%)
á flestum textategundum. Þröskuldurinn er AÐFERÐAFRÆÐILEG HLIÐSTÆÐA,
ekki kvarðaður sérstaklega fyrir IcePaHC. Fyrir MA-verkefnið mætti
kalibrera þröskuldinn út frá empirískri dreifingu trédýpta í
benchmark-gögnunum sjálfum.

### Aðferð

1. Hlaða þáttuðum trjám úr .psd skrá (eitt tré per línu).
2. Fyrir hvert tré: einfaldur staf-fyrir-staf svigatalning →
   hámarksfjöldi opnaðra sviga í einni stöðu. Dýpt = hámark - 1
   (ROOT sjálft er á dýpt 0).
3. Fyrir hvert tré: staflugönguferli sem heldur opnuðum merkjum.
   Fyrir hvern IP-SUB sem er pushaður, talin fjöldi IP-SUB sem
   fyrir eru í staflanum = fjöldi IP-SUB forfeðra.
4. Sleppa tómum trjám og trjám með hámarks-svigadýpt < 2 (líklega
   þáttunarvillur eða stakstæðir tókar).

### Háð / Dependencies

Engin ytri söfn — notar aðeins staðlað Python. Endurnýtir `mean` og
`stdev` úr `dim6_word_length` til að halda tölfræði samræmdum milli
vídda.

Aðal-v fyrir Milička: `mean_tree_depth`.

## LIX-læsilegskor (dim10)

`dim10_lix.py` reiknar LIX-læsilegskor (Läsbarhetsindex, Björnsson 1968),
klassískan sænskan læsilegsstuðul sem sameinar orðalengd og setningalengd:

```
LIX = (words / sentences) + (long_words / words × 100)
```

þar sem `long_words` = orð með FLEIRI EN 6 stafi (LIX-staðall — ÖÐRUVÍSI
en dim6 sem notar ≥ 8 stafi).

### Tvíþætt hlutverk / Dual purpose

1. **Klassísk læsilegsmæling** í sjálfu sér: birtir hversu „þungur“
   textinn er á sömu formúlu og víða er notuð fyrir norrænar tungur.
2. **Hliðstæð mæling við dim6** (meðalorðalengd). Bæði mæla orðaþyngd,
   en dim10 bætir setningalengd við. Í greiningarkafla verður borin
   saman: er fylgni dim6↔dim10 svo há að ein vídd gegnir hlutverki
   beggja? Niðurstaðan ákveður hvort báðar haldist áfram í
   MA-lokaverkefnis-víddarsetti eða aðeins önnur.

### Kvörðunarfyrirvari / Calibration caveat

LIX var kvörðuð fyrir sænsku. Staðlaðir þröskuldar
(< 30 mjög auðvelt, 30–40 auðvelt, 40–50 miðlungs, 50–60 erfitt,
> 60 mjög erfitt) endurspegla sænska texta. Íslenska hefur virkara
samsetningarkerfi (fleiri löng orð) og oft lengri setningar, svo
hrávirði er kerfisbundið hærra — ekki vegna þess að textinn sé
ólæsari. Í greininni birtast þröskuldarnir aðeins sem grófir vísar;
íslenskir kvörðunarþröskuldar þurfa að byggjast á reynslugögnum úr
mæliprófinu sjálfu.

### Tokenization

`dim10` endurnýtir `PUNCT_TO_STRIP` og `HAS_LETTER` úr dim6 — engin
samhliða skilgreining, svo dim6 og dim10 telja NÁKVÆMLEGA sömu orð.
Setningaskilming notar `tokenizer.split_into_sentences` frá Miðeind,
sem kann íslenskar skammstafanir (þ.e., o.s.frv., t.d., m.a., o.fl.)
og tugabrot („3,14“, „1.000“) — barefn `.!?`-regex gerir það ekki og
myndi ofmæla setningar.

### Sub-measures í úttaki

| Dálkur | Skilgreining |
|--------|--------------|
| `total_words` | Fjöldi gildra orða (dim6-reglur) |
| `total_sentences` | Fjöldi setninga (tokenizer-pakki) |
| `mean_sentence_length` | orð / setningar |
| `pct_long_words` | Hlutfall orða með > 6 stafi (LIX-skilgreining) |
| `lix_score` | Aðal-v fyrir Milička |

Aðal-v fyrir Milička: `lix_score`.

### Háð / Dependency

`tokenizer>=3.4` (Miðeind): `pip install tokenizer`. Pakkinn er hreinn
Python, ekkert C-háð; þarf ekki sérstaka uppsetningu á Linux.

## Orðaforðafjölbreytni — MTLD (dim11)

`dim11_mtld.py` reiknar MTLD (Measure of Textual Lexical Diversity,
McCarthy & Jarvis 2010) — lengdarstöðugan arftaka TTR (type/token
ratio). Barefnt TTR minnkar kerfisbundið með lengd texta af
stærðfræðilegum ástæðum, svo það er ósamanburðarhæft milli texta af
ólíkri lengd (t.d. LLM-framhalda og mannlegra viðmiðstexta). MTLD
leysir þetta með faktor-talningu.

### Tengsl við Milička- og Biber-ramma

- **Milička-ramminn (2025):** Engin víddanna 6 (enska) eða 8 (tékkneska)
  inniheldur MTLD, TTR, vocd-D eða HD-D. Dim11 er því EKKI hliðstæða
  Milička-vídda.
- **Biber-ramminn (1988):** TTR var einn af eiginleikum
  „Informational Production“-víddarinnar. Dim11 er framlenging á þeirri
  hugmynd í lengdarstöðugu formi.

Sjá ákvörðun 027 fyrir forathugun og hönnunarrökstuðning.

### Reikniritið (McCarthy & Jarvis 2010)

1. Halda rúllandi TTR (cumulative_types / cumulative_tokens).
2. Þegar TTR fer UNDIR þröskuld 0.72 (strictly less than, „<“), loka
   faktor: `factor_count += 1`; endurstilla báða talara.
3. Í lok tókaraðar, ef óklárður faktor er eftir: bæta við hluta
   `(1 - TTR_end) / (1 - 0.72)`.
4. `forward_mtld = total_tokens / factor_count`.
5. Endurtaka á tókaröðinni SNÚINNI → `reverse_mtld`.
6. `final_mtld = (forward_mtld + reverse_mtld) / 2`.

Þröskuldur 0.72 er staðlaður (McCarthy & Jarvis könnuðu [0.660, 0.750];
koRpus, lexical-diversity og allar síðari útfærslur nota 0.72).

### Tókunin

Nákvæmlega sömu reglur og dim6/dim10 (`PUNCT_TO_STRIP`, `HAS_LETTER` úr
dim6) — tryggir að orðaforðafjölbreytni er mæld yfir sömu tókamengi og
orðalengd/LIX. Tókar eru lágstafraðir áður en talningar hefjast;
wordform-MTLD krefst þess að „Kötturinn“ og „kötturinn“ teljist sem
sama gerð.

### Takmörk

- **Wordforms, ekki lemma:** Íslensk beyging („hestur“, „hests“,
  „hesti“, „hesta“) blæs upp fjölbreytni miðað við lemma-MTLD.
  Wordform-talning er þó staðallinn í McCarthy & Jarvis og
  stílfræðibókmenntum; lemma-MTLD getur verið bætt við sem
  viðbótarsamanburður í MA-verkefni.
- **Sample-lengd:** MTLD er óáreiðanlegt undir ~100 tókum; aðvörun
  prentuð ef svo fáir tókar eru í skrá. Úrtökin í þessu verkefni eru
  ~200–500 tókar eftir hreinsun — vel yfir mörkunum.
- **Endurtekningarmynstur í LLM-úttaki:** Dim11 greinir EKKI
  endurtekningar beint, en þær LÆKKA MTLD sem hliðarverkun. Það er
  jákvæð verkun: texti sem festist í sama frásamynstri fær lægra skor.
- **Umorðun / merking:** MTLD er blindur á merkingu — texti sem
  endurtekur sömu hugmynd með MISMUNANDI orðmyndum skorar hærra en
  sama hugmynd með sömu orðmyndum.

### Sub-measures í úttaki

| Dálkur | Skilgreining |
|--------|--------------|
| `total_tokens` | Heildarfjöldi gildra tóka (dim6-reglur, lágstafraðir) |
| `total_types` | Fjöldi einstakra orðmynda (type count) |
| `forward_mtld` | MTLD í fram-göngu |
| `reverse_mtld` | MTLD í afturábak-göngu |
| `final_mtld` | Meðaltal (aðal-v) |
| `factor_count_forward` | Fjöldi faktora (með hluta) fram |
| `factor_count_reverse` | Fjöldi faktora (með hluta) aftur |

Aðal-v fyrir Milička: `final_mtld`.

### Hæði / Dependencies

Engin ytri söfn. Endurnýtir `PUNCT_TO_STRIP`, `HAS_LETTER` og `mean` úr
`dim6_word_length`. Reikniritið er ~50 línur af staðal-Python og er
skjalfest að fullu í docstring skriftunnar.

### Heimild

McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: A
validation study of sophisticated approaches to lexical diversity
assessment. *Behavior Research Methods*, 42(2), 381–392. DOI:
[10.3758/BRM.42.2.381](https://doi.org/10.3758/BRM.42.2.381).
