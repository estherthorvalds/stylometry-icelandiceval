"""Is prompt/reference length a confound for the seen-vs-unseen B-score gap?

Hypothesis to falsify: the 'unseen' register has different prompt/reference
word counts than the seen registers (academic, blog, news), and that length
difference - not anything inherent to unseen-style text - drives the higher
B-scores models receive on unseen.

Pipeline:
  1. Word-count every prompt and reference file (whitespace tokens).
  2. Descriptive stats per register.
  3. Per (model, register, sample), B_sample = sqrt(mean(b_d^2 over dims)).
  4. Spearman(B_sample, prompt_wc) and Spearman(B_sample, ref_wc) per
     register, pooling across models.
  5. OLS:  B_sample ~ register + prompt_wc + ref_wc + C(model).
     Question: does the 'unseen' dummy stay significant once length is
     held constant?
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_DIR = REPO_ROOT / "data" / "experiment" / "prompts"
REF_DIR = REPO_ROOT / "data" / "experiment" / "human_texts"
RESULTS_CSV = REPO_ROOT / "output" / "milicka_results_post_dim8fix.csv"

OUT_DIR = REPO_ROOT / "analysis"
OUT_LENGTHS_CSV = OUT_DIR / "prompt_length_by_sample.csv"
OUT_COEFS_CSV = OUT_DIR / "length_regression_coefs.csv"

REGISTERS = ("academic", "blog", "news", "unseen")
N_SAMPLES_PER_REGISTER = 15

# Baseline category for the regression dummies. 'academic' is the baseline
# register so that 'unseen' (and 'blog', 'news') each get their own dummy
# and we can read off the unseen effect directly.
REGISTER_BASELINE = "academic"


def word_count(path: Path) -> int:
    """Whitespace-token count of a text file."""
    return len(path.read_text(encoding="utf-8").split())


def collect_lengths() -> pd.DataFrame:
    """One row per (register, sample_number) with prompt and reference wc."""
    rows = []
    for register in REGISTERS:
        for n in range(1, N_SAMPLES_PER_REGISTER + 1):
            prompt_path = PROMPT_DIR / f"{register}_prompt_{n:03d}.txt"
            ref_path = REF_DIR / f"{register}_ref_{n:03d}.txt"
            if not prompt_path.exists():
                raise FileNotFoundError(prompt_path)
            if not ref_path.exists():
                raise FileNotFoundError(ref_path)
            rows.append({
                "register": register,
                "sample_number": n,
                "prompt_word_count": word_count(prompt_path),
                "reference_word_count": word_count(ref_path),
            })
    return pd.DataFrame(rows)


def descriptive_stats(lengths: pd.DataFrame) -> pd.DataFrame:
    """Mean / median / std / min / max of prompt and ref word counts per register."""
    agg = lengths.groupby("register").agg(
        n=("sample_number", "count"),
        prompt_mean=("prompt_word_count", "mean"),
        prompt_median=("prompt_word_count", "median"),
        prompt_std=("prompt_word_count", "std"),
        prompt_min=("prompt_word_count", "min"),
        prompt_max=("prompt_word_count", "max"),
        ref_mean=("reference_word_count", "mean"),
        ref_median=("reference_word_count", "median"),
        ref_std=("reference_word_count", "std"),
        ref_min=("reference_word_count", "min"),
        ref_max=("reference_word_count", "max"),
    )
    return agg.reindex(list(REGISTERS))


def per_sample_B(df: pd.DataFrame) -> pd.DataFrame:
    """B_sample = sqrt(mean(b_d^2)) over the 11 dimensions, per (model, register, sample)."""
    b2 = df.assign(b_sq=df["b_d"] ** 2)
    grouped = b2.groupby(["model", "register", "number"], as_index=False).agg(
        b_mean_sq=("b_sq", "mean"),
        n_dims=("b_sq", "count"),
    )
    grouped["B_sample"] = np.sqrt(grouped["b_mean_sq"])
    return grouped[["model", "register", "number", "B_sample", "n_dims"]]


def spearman_per_register(merged: pd.DataFrame) -> pd.DataFrame:
    """Within each register, Spearman of B_sample with prompt_wc and ref_wc."""
    rows = []
    for register in REGISTERS:
        sub = merged[merged["register"] == register]
        n = len(sub)
        sp_prompt = stats.spearmanr(sub["B_sample"], sub["prompt_word_count"])
        sp_ref = stats.spearmanr(sub["B_sample"], sub["reference_word_count"])
        rows.append({
            "register": register,
            "n": n,
            "spearman_rho_prompt": sp_prompt.statistic,
            "p_prompt": sp_prompt.pvalue,
            "spearman_rho_ref": sp_ref.statistic,
            "p_ref": sp_ref.pvalue,
        })
    return pd.DataFrame(rows)


def build_design_matrix(merged: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    """Intercept + register dummies (baseline academic) + length covariates + model dummies."""
    n = len(merged)
    parts = [np.ones((n, 1))]
    names = ["Intercept"]

    for register in REGISTERS:
        if register == REGISTER_BASELINE:
            continue
        col = (merged["register"] == register).astype(float).to_numpy().reshape(-1, 1)
        parts.append(col)
        names.append(f"register[{register}]")

    parts.append(merged["prompt_word_count"].to_numpy().reshape(-1, 1).astype(float))
    names.append("prompt_word_count")
    parts.append(merged["reference_word_count"].to_numpy().reshape(-1, 1).astype(float))
    names.append("reference_word_count")

    models_sorted = sorted(merged["model"].unique())
    model_baseline = models_sorted[0]
    for m in models_sorted:
        if m == model_baseline:
            continue
        col = (merged["model"] == m).astype(float).to_numpy().reshape(-1, 1)
        parts.append(col)
        names.append(f"model[{m}]")

    X = np.hstack(parts)
    return X, names


def fit_ols(X: np.ndarray, y: np.ndarray, names: list[str]) -> pd.DataFrame:
    """Classical OLS with t-based 95% CIs."""
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta
    dof = n - k
    sigma2 = (resid @ resid) / dof
    var_beta = sigma2 * XtX_inv
    se = np.sqrt(np.diag(var_beta))
    t_stat = beta / se
    p_val = 2 * (1 - stats.t.cdf(np.abs(t_stat), df=dof))
    t_crit = stats.t.ppf(0.975, df=dof)
    ci_low = beta - t_crit * se
    ci_high = beta + t_crit * se

    return pd.DataFrame({
        "term": names,
        "coef": beta,
        "std_err": se,
        "t": t_stat,
        "p_value": p_val,
        "ci_low_95": ci_low,
        "ci_high_95": ci_high,
    })


def print_descriptive(stats_df: pd.DataFrame) -> None:
    print("=" * 90)
    print("Prompt and reference word counts by register")
    print("=" * 90)
    print(f"{'register':<10} {'n':>3}  "
          f"{'prompt mean':>12} {'median':>8} {'std':>8} {'min':>6} {'max':>6}   "
          f"{'ref mean':>10} {'median':>8} {'std':>8} {'min':>6} {'max':>6}")
    for register, row in stats_df.iterrows():
        print(f"{register:<10} {int(row['n']):>3}  "
              f"{row['prompt_mean']:>12.1f} {row['prompt_median']:>8.1f} {row['prompt_std']:>8.1f} "
              f"{int(row['prompt_min']):>6} {int(row['prompt_max']):>6}   "
              f"{row['ref_mean']:>10.1f} {row['ref_median']:>8.1f} {row['ref_std']:>8.1f} "
              f"{int(row['ref_min']):>6} {int(row['ref_max']):>6}")
    print()


def print_spearman(table: pd.DataFrame) -> None:
    print("=" * 90)
    print("Spearman correlation: B_sample vs. prompt/reference word count, by register")
    print("(B_sample pooled across models; n = 15 samples x 6 models = 90 per register)")
    print("=" * 90)
    print(f"{'register':<10} {'n':>4}  "
          f"{'rho(prompt)':>12} {'p(prompt)':>10}  "
          f"{'rho(ref)':>10} {'p(ref)':>10}")
    for _, row in table.iterrows():
        print(f"{row['register']:<10} {int(row['n']):>4}  "
              f"{row['spearman_rho_prompt']:>+12.4f} {row['p_prompt']:>10.4f}  "
              f"{row['spearman_rho_ref']:>+10.4f} {row['p_ref']:>10.4f}")
    print()


def print_coefs(coefs: pd.DataFrame) -> None:
    print("=" * 90)
    print("OLS: B_sample ~ register + prompt_word_count + reference_word_count + C(model)")
    print(f"     Baseline register: {REGISTER_BASELINE}")
    print("=" * 90)
    print(f"{'term':<30} {'coef':>10} {'std_err':>10} {'t':>8} {'p':>10}  "
          f"{'95% CI':>26}")
    for _, row in coefs.iterrows():
        ci = f"[{row['ci_low_95']:+.4f}, {row['ci_high_95']:+.4f}]"
        print(f"{row['term']:<30} {row['coef']:>+10.4f} {row['std_err']:>10.4f} "
              f"{row['t']:>+8.3f} {row['p_value']:>10.4f}  {ci:>26}")
    print()


def main() -> None:
    lengths = collect_lengths()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lengths.to_csv(OUT_LENGTHS_CSV, index=False)

    stats_df = descriptive_stats(lengths)
    print_descriptive(stats_df)

    results = pd.read_csv(RESULTS_CSV)
    sample_B = per_sample_B(results)
    if (sample_B["n_dims"] != 11).any():
        bad = sample_B[sample_B["n_dims"] != 11]
        raise ValueError(f"Expected 11 dims per cell, got mismatched rows:\n{bad.head()}")
    sample_B = sample_B.drop(columns="n_dims")

    merged = sample_B.merge(
        lengths.rename(columns={"sample_number": "number"}),
        on=["register", "number"],
        how="inner",
        validate="many_to_one",
    )
    expected_rows = len(sample_B)
    if len(merged) != expected_rows:
        raise ValueError(
            f"Merge dropped rows: {expected_rows} -> {len(merged)}"
        )

    sp_table = spearman_per_register(merged)
    print_spearman(sp_table)

    X, names = build_design_matrix(merged)
    y = merged["B_sample"].to_numpy()
    coefs = fit_ols(X, y, names)
    coefs.to_csv(OUT_COEFS_CSV, index=False)
    print_coefs(coefs)

    unseen_row = coefs[coefs["term"] == "register[unseen]"].iloc[0]
    verdict = "still significant" if unseen_row["p_value"] < 0.05 else "no longer significant"
    print(
        f"Unseen register effect after controlling for length and model: "
        f"coef = {unseen_row['coef']:+.4f}, p = {unseen_row['p_value']:.4f} ({verdict} at alpha=0.05)"
    )
    print()
    print(f"Wrote: {OUT_LENGTHS_CSV.relative_to(REPO_ROOT)}")
    print(f"Wrote: {OUT_COEFS_CSV.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
