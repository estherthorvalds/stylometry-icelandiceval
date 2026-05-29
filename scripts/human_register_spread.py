"""Cross-register human variability vs. model error per dimension.

Question: do the dimensions where models struggle most (high mean |b_d|
across all model x register cells) coincide with the dimensions where
human writers vary most across registers?

For each of the 11 dimensions:
  1. Mean v_human per register (academic, blog, news, unseen) and the
     coefficient of variation across those four register means.
  2. Mean |b_d| across all rows (reproduces the paper's section 5.2 table).

Then Spearman (primary) and Pearson (reference) correlations between the
two across the 11 dimensions, plus a scatter plot.
"""
from __future__ import annotations

from pathlib import Path
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO_ROOT / "output" / "milicka_results_post_dim8fix.csv"
OUT_DIR = REPO_ROOT / "analysis"
OUT_CSV = OUT_DIR / "human_register_spread.csv"
OUT_PNG = OUT_DIR / "human_register_spread.png"

REGISTERS = ("academic", "blog", "news", "unseen")
DIM_ORDER = [f"dim{i}" for i in range(1, 12)]

# Published mean |b_d| values from section 5.2 of the paper.
PUBLISHED_MEAN_ABS_B = {
    "dim1": 1.62,
    "dim2": 4.44,
    "dim3": 2.60,
    "dim4": 1.71,
    "dim5": 2.90,
    "dim6": 4.09,
    "dim7": 3.26,
    "dim8": 1.89,
    "dim9": 3.21,
    "dim10": 2.88,
    "dim11": 7.14,
}
PUBLISHED_TOLERANCE = 0.1


def compute_table(df: pd.DataFrame) -> pd.DataFrame:
    """One row per dimension with per-register human means, spread, and mean |b|."""
    # v_human is a property of the (register, number, dim_id) human sample
    # and is duplicated across the six model rows. Deduplicate before
    # averaging so each human sample contributes once.
    human = (
        df[["register", "number", "dim_id", "dim_label", "v_human"]]
        .drop_duplicates(subset=["register", "number", "dim_id"])
    )

    per_cell = (
        human.groupby(["dim_id", "register"], as_index=False)["v_human"].mean()
    )
    wide = per_cell.pivot(index="dim_id", columns="register", values="v_human")
    wide = wide[list(REGISTERS)]

    register_means = wide.to_numpy()
    means_of_means = register_means.mean(axis=1)
    stds = register_means.std(axis=1, ddof=0)
    # Population std (ddof=0) across the four register means is the natural
    # choice here: we have the full population of registers, not a sample.
    with np.errstate(divide="ignore", invalid="ignore"):
        cvs = np.where(np.abs(means_of_means) > 1e-12, stds / np.abs(means_of_means), np.nan)

    mean_abs_b = (
        df.assign(abs_b=df["b_d"].abs())
        .groupby("dim_id")["abs_b"].mean()
    )

    labels = df[["dim_id", "dim_label"]].drop_duplicates().set_index("dim_id")["dim_label"]

    out = pd.DataFrame({
        "dim_id": wide.index,
        "dim_label": labels.reindex(wide.index).to_numpy(),
        "mean_v_human_academic": wide["academic"].to_numpy(),
        "mean_v_human_blog": wide["blog"].to_numpy(),
        "mean_v_human_news": wide["news"].to_numpy(),
        "mean_v_human_unseen": wide["unseen"].to_numpy(),
        "between_register_std": stds,
        "between_register_CV": cvs,
        "mean_abs_b": mean_abs_b.reindex(wide.index).to_numpy(),
    })

    out["_dim_n"] = out["dim_id"].str.extract(r"(\d+)").astype(int)
    out = out.sort_values("between_register_CV", ascending=False).drop(columns="_dim_n")
    return out.reset_index(drop=True)


def check_against_published(table: pd.DataFrame) -> None:
    for _, row in table.iterrows():
        dim = row["dim_id"]
        observed = row["mean_abs_b"]
        published = PUBLISHED_MEAN_ABS_B.get(dim)
        if published is None:
            continue
        if abs(observed - published) > PUBLISHED_TOLERANCE:
            warnings.warn(
                f"{dim} mean|b_d|={observed:.3f} differs from published "
                f"{published:.2f} by more than {PUBLISHED_TOLERANCE}",
                stacklevel=2,
            )


def make_scatter(table: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    x = table["between_register_CV"].to_numpy()
    y = table["mean_abs_b"].to_numpy()
    ax.scatter(x, y, s=50, color="steelblue", edgecolor="black", zorder=3)
    for _, row in table.iterrows():
        ax.annotate(
            row["dim_id"],
            (row["between_register_CV"], row["mean_abs_b"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
        )
    ax.set_xlabel("Between-register CV of mean v_human")
    ax.set_ylabel("Mean |b_d| across all rows")
    ax.set_title("Human cross-register spread vs. model error per dimension")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(DEFAULT_CSV)
    table = compute_table(df)
    check_against_published(table)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_CSV, index=False)
    make_scatter(table, OUT_PNG)

    # Drop dims with undefined CV before correlating.
    valid = table.dropna(subset=["between_register_CV", "mean_abs_b"])
    spearman = stats.spearmanr(valid["between_register_CV"], valid["mean_abs_b"])
    pearson = stats.pearsonr(valid["between_register_CV"], valid["mean_abs_b"])

    with pd.option_context(
        "display.max_rows", None,
        "display.width", 140,
        "display.float_format", lambda x: f"{x:8.4f}",
    ):
        print(f"Source: {DEFAULT_CSV.relative_to(REPO_ROOT)}")
        print(f"Rows: {len(df)}, dims: {table['dim_id'].nunique()}")
        print()
        print("Per-dimension table (sorted by between_register_CV desc):")
        print(table.to_string(index=False))
        print()
        print(f"Spearman rho (primary): {spearman.statistic:+.4f}  p = {spearman.pvalue:.4f}  n = {len(valid)}")
        print(f"Pearson  r  (reference): {pearson.statistic:+.4f}  p = {pearson.pvalue:.4f}  n = {len(valid)}")
        print()
        print(f"Wrote table: {OUT_CSV.relative_to(REPO_ROOT)}")
        print(f"Wrote plot:  {OUT_PNG.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
