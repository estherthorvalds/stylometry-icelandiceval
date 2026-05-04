# stylometry-icelandiceval

Stílmælingar á íslensku — mælipróf til að meta getu risamállíkana til að meðhöndla stíl á íslensku.

A research project developing a stylometric evaluation benchmark for the [Icelandic LLM Leaderboard](https://huggingface.co/spaces/mideind/icelandic-llm-leaderboard) maintained by Miðeind, following the methodology of Milička et al. (2025).

## Method / Aðferð

The benchmark uses a **paired continuation design** from Milička et al. (2025):
1. Extract ~2,000-word samples from the Icelandic Gigaword Corpus (RMH) across three registers: academic (Læknablaðið), news (RÚV), blog (Jonas.is)
2. Split each sample in half — the first half becomes a **prompt**, the second half becomes a **human reference**
3. LLM models receive the prompt and generate a continuation
4. Measure stylometric dimensions (dim1–dim11) on both human reference and LLM continuation
5. Compute deviation scores (Δv, b_d, B) to quantify stylistic similarity

### Models tested

Continuations were collected from 7 model endpoints. Le Chat Fast (deprecated mid-collection) and Le Chat Balanced are aggregated as a single `le_chat_free` row in result tables (see decision 030), so 6 model rows appear in the leaderboard:

- Anthropic Claude Sonnet 4.6
- DeepSeek V3.2 Expert
- Google Gemini 2.5 Pro (Thinking)
- OpenAI GPT-5
- Mistral Le Chat (free) — combined Fast + Balanced
- Mistral Le Chat (thinking)

Per-directory data is preserved unchanged under `data/experiment/llm_continuations/{model}/`. Aggregation is applied at read time in `run_milicka.py` via `MODEL_ALIASES`.

### Stylometric dimensions / Mælivíddir

| Dim | Script | Feature | Input |
|-----|--------|---------|-------|
| 1 | `dim1_frumlagsnafnfall.py` | Subject drop rate | Parsed |
| 2 | `dim2_aukasetningar.py` | Subordination ratio (IP-SUB / IP-MAT) | Parsed |
| 3 | `dim3_nafnlidalengd.py` | Mean NP length | Parsed |
| 4 | `dim4_past_tense.py` | Past tense verb ratio | Parsed |
| 5 | `dim5_thirdperson_pronouns.py` | Third person pronoun ratio | Parsed |
| 6 | `dim6_word_length.py` | Mean word length (chars) | Raw text |
| 7 | `dim7_complementizers.py` | Complementizer frequency (sem/að) | Parsed |
| 8 | `dim8_bin_ratio.py` | BÍN vocabulary coverage (in_bin_ratio) | Raw text |
| 9 | `dim9_tree_depth.py` | Mean constituency tree depth (syntactic complexity) | Parsed |
| 10 | `dim10_lix.py` | LIX readability score (Läsbarhetsindex) | Raw text |
| 11 | `dim11_mtld.py` | Lexical diversity (MTLD) | Raw text |

Dim 8 requires the [`islenska`](https://pypi.org/project/islenska/) package (Miðeind's BinPackage) for BÍN lookups. Install with `pip install islenska>=1.0`. On Linux, building `islenska` may require `python3-dev` and `libffi-dev`. The package is optional — the pipeline runs without it, but dim8 will be skipped.

Dim 10 requires the [`tokenizer`](https://pypi.org/project/tokenizer/) package (Miðeind) for Icelandic-aware sentence splitting (handles abbreviations such as `þ.e.`, `o.s.frv.`, `t.d.`). Install with `pip install tokenizer>=3.4`. LIX is kept as a parallel candidate to dim6 — one, both, or neither may carry forward to the MA-thesis dimension set. Its Swedish-calibrated thresholds are used here only as rough indicators; Icelandic baselines need to be established empirically.

Dim 11 implements MTLD (Measure of Textual Lexical Diversity, McCarthy & Jarvis 2010) — a length-robust successor to type/token ratio. It is a Biber-motivated extension rather than a Miličkadimension; the Miličkabenchmark does not include any lexical-diversity measure. Implementation is pure-Python (no external MTLD package); tokenization reuses dim6's rules for cross-dimension comparability. Wordforms only (not lemmas) — Icelandic inflection can inflate diversity relative to less-inflected languages, which is documented as a known limitation. See decision #027 for algorithm details (threshold 0.72, strict "<" direction, partial-factor formula `(1 - TTR) / (1 - 0.72)`, forward+reverse averaging).

## Project structure

```
stylometry-icelandiceval/
├── README.md
├── ARCHITECTURE.md                   # Ítarleg skipulagslýsing (sjá þar)
├── research_log.md                   # Rannsóknardagbók
├── decisions_log.md                  # Skrá yfir ákvarðanir
├── reference_tracker.csv             # Heimildaskrá
├── audit_nan_handling.md             # Skoðun á NaN-áhættu allra vídda (ákvörðun 028)
├── style_score_leaderboard.py        # Stigatafla úr milicka_results CSV (notar pandas)
├── test_api_anthropic.py             # Lítið prófdæmi fyrir Anthropic API
├── rename_lechat.sh                  # Einnota nafnabreytingaskrift (le_chat_* staðlað)
│
├── data/
│   ├── human_texts/                  # 36k úrtök úr RMH (ekki á GitHub — sjá Data & Licensing)
│   ├── experiment/                   # Tilraunagögn (sjá ARCHITECTURE.md)
│   │   ├── prompts/                  # Fyrri helmingar (60 skrár, ekki á GitHub)
│   │   ├── human_texts/              # Seinni helmingar (60 skrár, ekki á GitHub)
│   │   ├── llm_continuations/        # Hrá LLM-framhöld, ein mappa per líkan (7 möppur)
│   │   ├── llm_continuations_clean/  # Forunnin LLM-framhöld
│   │   └── excluded_from_pipeline/   # Skrár sem féllu á heilleikaskoðun (Le Chat unseen)
│   ├── experiment_unseen/            # Pöruð gögn óséðra höfundatexta (ekki á GitHub)
│   ├── unseen_authored_texts/        # Bókmenntatextar fyrir óséða tilraun (ekki á GitHub)
│   ├── figures/                      # Tókunarsamanburðarmyndir (RÚV, Claude-endurtekning)
│   └── raw/                          # Hrá RMH XML-gögn (ekki á GitHub)
│
├── scripts/
│   ├── extract_samples.py                # Draga úrtök úr RMH TEI XML
│   ├── prepare_paired_experiment.py      # Klippa texta og búa til pöruð gögn (RMH)
│   ├── prepare_unseen_authored_texts.py  # Pöruð gögn óséðra höfundatexta
│   ├── generate_claude_continuations.py  # Sækja LLM-framhöld gegnum Anthropic API
│   ├── preprocess_llm_output.py          # Hreinsa LLM-úttak (markdown, meta, endurtekning, samskeyti)
│   ├── parse_texts.py                    # Þátta texta með IceConParse
│   ├── integrity_check.py                # Finnur villur og svindl (keyra fyrir þáttun)
│   ├── dim1_frumlagsnafnfall.py          # Vídd 1: Frumlagsnafnliðarleysi
│   ├── dim2_aukasetningar.py             # Vídd 2: Aukasetningahlutfall
│   ├── dim3_nafnlidalengd.py             # Vídd 3: Meðallengd nafnliða
│   ├── dim4_past_tense.py                # Vídd 4: Þátíðarhlutfall
│   ├── dim5_thirdperson_pronouns.py      # Vídd 5: Þriðjupersónufornöfn
│   ├── dim6_word_length.py               # Vídd 6: Meðalorðalengd
│   ├── dim7_complementizers.py           # Vídd 7: Tengiorðatíðni
│   ├── dim8_bin_ratio.py                 # Vídd 8: BÍN-þekja (reikna-einu-sinni → output/dim8_bin_*.csv)
│   ├── dim9_tree_depth.py                # Vídd 9: Trédýpt (úr IcePaHC-trjám)
│   ├── dim10_lix.py                      # Vídd 10: LIX-læsilegskor
│   ├── dim11_mtld.py                     # Vídd 11: Orðaforðafjölbreytni (MTLD)
│   ├── run_milicka.py                    # Safna b_d, reikna B (RMS-form, sjá ákvörðun 028)
│   ├── style_score.py                    # Hjálparfall: 0-100 stig
│   ├── validation_harness.py             # Sannprófunartól: handvirk yfirferð
│   └── archive/                          # Eldri tilraunaskriftur (fréttafyrirsagnir, fyrstu prófanir)
│
├── tests/
│   └── test_split_concatenated_tokens.py # Einingaprófanir á samskeyta-aðgreiningu (ákvörðun 029)
│
├── output/                               # Niðurstöður (CSV, myndir — sjá ARCHITECTURE.md)
├── models/                               # IceConParse þáttunarlíkan (ekki á GitHub)
└── archive/                              # Eldri JSON-úttak og útilokuð gögn
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed data flow and IcePaHC tag reference.

## Áfangar verkefnis / Project phases

1. **Rannsókn / Literature survey** — Map existing generation/style evaluation benchmarks across languages, with focus on low-resource languages
2. **Hönnun mæliprófs / Benchmark design** — Design an Icelandic stylometry benchmark with well-defined correctness criteria
3. **Keyrsla og greining / Evaluation** — Run the benchmark on selected models and analyze results

## Ráðgjafar / Advisors

- [Miðeind](https://mideind.is/)
- [Háskóli Íslands](https://hi.is/)

## Context

This project addresses a known gap on the Icelandic LLM Leaderboard: the absence of a benchmark that systematically evaluates language generation quality and style.

## Parser

IceConParse by Ingunn Jóhanna Kristjánsdóttir (2024) — a Stanza-based constituency parser trained on the IcePaHC treebank with IceBERT embeddings (F-score: 90.38%).

## Data & Licensing

Human baseline texts in this benchmark are extracted from **RMH (Risamálheild / Icelandic Gigaword Corpus)** and are **not included in this repository** due to the RMH license terms. This applies to:

- `data/human_texts/` — 36,310 extracted ~2,000-word samples
- `data/experiment/prompts/` — 60 prompt files (first halves: 15 per × academic, blog, news, unseen)
- `data/experiment/human_texts/` — 60 reference files (second halves)
- `data/experiment/selected_samples.csv` — metadata mapping source files to pairs
- `data/unseen_authored_texts/` and `data/experiment_unseen/` — 15 literary works for the unseen-author add-on experiment

> **Git history rewrite (2026-04-13):** These files were purged from all git history using `git filter-repo`. If you cloned this repository before this date, you should **delete your local clone and re-clone** to avoid retaining the removed data in your local packfile.

To reproduce the full dataset locally:
1. Obtain RMH 22.10 from https://repository.clarin.is/repository/xmlui/handle/20.500.12537/89
2. Place XML files into `data/raw/`
3. Run `python scripts/extract_samples.py` to extract ~2,000-word samples into `data/human_texts/`
4. Run `python scripts/prepare_paired_experiment.py` to create the 45 paired prompts and references for academic/blog/news (RMH-based)
5. Provide the 15 unseen literary works under `data/unseen_authored_texts/` and run `python scripts/prepare_unseen_authored_texts.py` for the additional 15 unseen pairs

RMH access requires accepting the CLARIN license terms. The LLM-generated continuations (`data/experiment/llm_continuations/`, `data/experiment/llm_continuations_clean/`) and all derived outputs (parse trees, dimension scores) **are** included in the repository.

### Unseen-author experiment

In addition to the RMH-based main experiment, a parallel run is performed on 15 literary works (Icelandic novels and book chapters) under the `unseen` register. The pipeline is identical — paired prompt/reference design, same dimensions, same B-score — but the source texts are not from RMH and are kept under separate licensing. Failed Le Chat runs on the unseen set are kept in `data/experiment/excluded_from_pipeline/unseen_lechat_failures/` for reference but are excluded from results.