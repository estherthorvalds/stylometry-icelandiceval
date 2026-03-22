# stylometry-icelandiceval

Stílmælingar á íslensku — mælipróf til að meta getu risamállíkana til að meðhöndla stíl á íslensku.

A research project developing a stylometric evaluation benchmark for the [Icelandic LLM Leaderboard](https://huggingface.co/spaces/mideind/icelandic-llm-leaderboard) maintained by Miðeind.

## Project structure

```
stylometry-icelandiceval/
├── README.md
├── research_log.md           # Rannsóknardagbók
├── decisions_log.md          # Skrá yfir ákvarðanir
├── reference_tracker.csv     # Heimildaskrá
├── data/                     # Gögn mæliprófs (seinna)
└── scripts/                  # Keyrsluskriftur (seinna)
```

## Áfangar verkefnis / Project phases

1. **Rannsókn / Literature survey** — Map existing generation/style evaluation benchmarks across languages, with focus on low-resource languages
2. **Hönnun mæliprófs / Benchmark design** — Design an Icelandic stylometry benchmark with well-defined correctness criteria
3. **Keyrsla og greining / Evaluation** — Run the benchmark on selected models and analyze results

## Ráðgjafar / Advisors

- [Miðeind](https://mideind.is/)
- [Háskóli Íslands](https://hi.is/)

## Context

This project addresses a known gap on the Icelandic LLM Leaderboard: the absence of a benchmark that systematically evaluates language generation quality and style.

# Data

Raw corpus files are not included in this repo.

To reproduce:
1. Download IGC-News1-21.05.zip from https://repository.clarin.is/repository/xmlui/handle/20.500.12537/89
2. Unzip into data/raw/IGC-News1-21.05/
3. Run: python scripts/extract_headlines.py -i data/raw/IGC-News1-21.05/ -o output/headline_pairs.json