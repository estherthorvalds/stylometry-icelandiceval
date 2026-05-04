"""Style-score leaderboard from per-sample Milička scores.

Reads `output/milicka_results_post_dim8fix.csv` and produces a leaderboard
of models ranked by style score (0–100, higher = closer to human style).

Three-stage balanced mean (see decisions_log.md for methodology):
    1. mean(score) per (model, register, dim_id) — collapses samples
    2. weighted mean across dim_ids per (model, register) — collapses dims
    3. mean across registers per model — collapses registers

`compute_leaderboard()` is the entry point used by other scripts (e.g. the
planned Gradio leaderboard). The CLI is a thin wrapper that prints the
default leaderboard.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

DEFAULT_CSV = Path(__file__).parent / "output" / "milicka_results_post_dim8fix.csv"
REGISTERS = ("academic", "blog", "news", "unseen")


def compute_leaderboard(
    weights: dict[str, float] | None = None,
    register_filter: str | None = None,
    csv_path: str | Path = DEFAULT_CSV,
) -> pd.DataFrame:
    """Compute the leaderboard via a three-stage balanced mean.

    Stage 1: average raw per-sample scores within each
    (model, register, dim_id) cell so unequal sample counts don't bias.
    Stage 2: weighted mean across dim_ids gives a per-(model, register)
    score; weight=0 drops a dimension, unset dims default to 1.0
    (equivalent to an unweighted mean).
    Stage 3: unweighted mean across the four registers gives the final
    style score. Skipped when `register_filter` selects a single register.

    Args:
        weights: dim_id -> weight. Defaults to 1.0 per dim. weight=0 excludes.
        register_filter: one of 'academic', 'blog', 'news', 'unseen', or None
            for all four. When set, the returned frame has only `style_score`
            (that register's score) and no per-register columns.
        csv_path: path to the per-sample results CSV.

    Returns:
        DataFrame sorted by style_score desc with columns
        [rank, model, style_score, <register>...].
    """
    df = pd.read_csv(csv_path)
    if register_filter is not None:
        df = df[df["register"] == register_filter]

    # Stage 1 — collapse samples within each cell.
    cell = df.groupby(["model", "register", "dim_id"], as_index=False)["score"].mean()

    # Apply per-dimension weights (default 1.0 for any unset dim).
    w = weights or {}
    cell["weight"] = cell["dim_id"].map(w).fillna(1.0)
    cell = cell[cell["weight"] > 0]

    # Stage 2 — weighted mean across dim_ids.
    cell["wscore"] = cell["score"] * cell["weight"]
    by_reg = cell.groupby(["model", "register"], as_index=False).agg(
        wsum=("wscore", "sum"),
        wtot=("weight", "sum"),
    )
    by_reg["score"] = by_reg["wsum"] / by_reg["wtot"]
    by_reg = by_reg[["model", "register", "score"]]

    if register_filter is not None:
        out = by_reg.rename(columns={"score": "style_score"})[["model", "style_score"]]
        out = out.sort_values("style_score", ascending=False).reset_index(drop=True)
        out.insert(0, "rank", range(1, len(out) + 1))
        return out

    # Stage 3 — mean across registers.
    pivot = by_reg.pivot(index="model", columns="register", values="score")
    pivot["style_score"] = pivot[list(REGISTERS)].mean(axis=1)
    pivot = pivot.sort_values("style_score", ascending=False).reset_index()
    pivot.insert(0, "rank", range(1, len(pivot) + 1))
    cols = ["rank", "model", "style_score", *[r for r in REGISTERS if r in pivot.columns]]
    return pivot[cols]


def _parse_weights(spec: str) -> dict[str, float]:
    out: dict[str, float] = {}
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        key, value = part.split("=", 1)
        out[key.strip()] = float(value)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--register", choices=list(REGISTERS), default=None)
    parser.add_argument(
        "--weights",
        type=_parse_weights,
        default=None,
        help="e.g. dim1=1.5,dim2=0,dim11=2.0 (unset dims default to 1.0)",
    )
    parser.add_argument("--csv", default=str(DEFAULT_CSV))
    args = parser.parse_args()

    leaderboard = compute_leaderboard(
        weights=args.weights,
        register_filter=args.register,
        csv_path=args.csv,
    )

    with pd.option_context(
        "display.max_rows", None,
        "display.width", 120,
        "display.float_format", lambda x: f"{x:6.2f}",
    ):
        print(leaderboard.to_string(index=False))


if __name__ == "__main__":
    main()
