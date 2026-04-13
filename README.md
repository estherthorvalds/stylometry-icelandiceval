# stylometry-icelandiceval

Stílmælingar á íslensku — mælipróf til að meta getu risamállíkana til að meðhöndla stíl á íslensku.

A research project developing a stylometric evaluation benchmark for the [Icelandic LLM Leaderboard](https://huggingface.co/spaces/mideind/icelandic-llm-leaderboard) maintained by Miðeind, following the methodology of Milička et al. (2025).

## Method / Aðferð

The benchmark uses a **paired continuation design** from Milička et al. (2025):
1. Extract ~2,000-word samples from the Icelandic Gigaword Corpus (RMH) across three registers: academic (Læknablaðið), news (RÚV), blog (Jonas.is)
2. Split each sample in half — the first half becomes a **prompt**, the second half becomes a **human reference**
3. LLM models receive the prompt and generate a continuation
4. Measure 7 stylometric dimensions on both human reference and LLM continuation
5. Compute deviation scores (Δv, b_d, B) to quantify stylistic similarity

### Models tested

- Google Gemini 2.5 Pro (Thinking)
- OpenAI GPT-5
- Mistral Le Chat (fast)
- Mistral Le Chat (thinking)

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

## Project structure

```
stylometry-icelandiceval/
├── README.md
├── ARCHITECTURE.md           # Ítarleg skipulagslýsing (sjá þar)
├── research_log.md           # Rannsóknardagbók
├── decisions_log.md          # Skrá yfir ákvarðanir
├── reference_tracker.csv     # Heimildaskrá
│
├── data/
│   ├── human_texts/          # Hrá úrtök úr RMH (academic/, blog/, news/)
│   ├── experiment/           # Tilraunagögn (prompts, human_reference, llm_continuations)
│   └── raw/                  # Hrá RMH XML-gögn (ekki á GitHub)
│
├── scripts/
│   ├── extract_samples.py            # Draga úrtök úr RMH TEI XML
│   ├── prepare_paired_experiment.py  # Klippa texta og búa til pöruð gögn
│   ├── preprocess_llm_output.py      # Hreinsa LLM-úttak (markdown, meta, endurtekning)
│   ├── parse_texts.py                # Þátta texta með IceConParse
│   ├── dim1_frumlagsnafnfall.py      # Vídd 1: Frumlagsnafnliðarleysi
│   ├── dim2_aukasetningar.py         # Vídd 2: Aukasetningarhlutfall
│   ├── dim3_nafnlidalengd.py         # Vídd 3: Meðallengd nafnliða
│   ├── dim4_past_tense.py            # Vídd 4: Þátíðarhlutfall
│   ├── dim5_thirdperson_pronouns.py  # Vídd 5: Þriðjupersónufornöfn
│   ├── dim6_word_length.py           # Vídd 6: Meðalorðalengd
│   ├── dim7_complementizers.py       # Vídd 7: Tengiorðatíðni
│   ├── run_milicka.py                # Safna b_d, reikna B = ‖b‖
│   ├── style_score.py                # Hjálparfall: 0-100 stig
│   └── validation_harness.py         # Sannprófunartól: handvirk yfirferð
│
├── output/                   # Niðurstöður (CSV, myndir)
├── models/                   # IceConParse þáttunarlíkan (ekki á GitHub)
└── archive/                  # Eldri skriftur
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

## Data

Raw corpus files are not included in this repo.

To reproduce:
1. Download RMH data from https://repository.clarin.is/repository/xmlui/handle/20.500.12537/89
2. Place XML files into `data/raw/`
3. Run: `python scripts/extract_samples.py` to extract ~2,000-word samples
4. Run: `python scripts/prepare_paired_experiment.py` to create paired prompts/references