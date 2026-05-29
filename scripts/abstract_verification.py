"""Verify empirical claims considered for the conference abstract.

Reads milicka_results_post_dim8fix.csv and checks four claims:
  1. Structural overshoot on dim5 (third-person pronouns) and dim3 (mean NP length).
  2. Lexical inversion on dim11 (MTLD).
  3. Robustness of the dim11 inversion after excluding the loop-prone model
     (le_chat_free, per paper section 6.2).
  4. Tracing the section 5.2 mean |b| discrepancy via three aggregation variants.

Writes analysis/abstract_verification_summary.csv and prints results to stdout.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO_ROOT / "output" / "milicka_results_post_dim8fix.csv"
OUT_DIR = REPO_ROOT / "analysis"
OUT_CSV = OUT_DIR / "abstract_verification_summary.csv"

REGISTERS = ("academic", "blog", "news", "unseen")
DIM_ORDER = [f"dim{i}" for i in range(1, 12)]

# Published mean |b_d| values from section 5.2.
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
PUBLISHED_TOLERANCE = 0.05

LOOP_PRONE_MODEL = "le_chat_free"


# ---------- helpers ----------

def human_means_per_register(df: pd.DataFrame, dim: str) -> pd.Series:
    """Mean v_human per register for one dim (dedup across model rows)."""
    sub = (
        df[df["dim_id"] == dim][["register", "number", "v_human"]]
        .drop_duplicates(subset=["register", "number"])
    )
    means = sub.groupby("register")["v_human"].mean()
    return means.reindex(list(REGISTERS))


def model_means_per_register(df: pd.DataFrame, dim: str) -> pd.DataFrame:
    """Rows = model, cols = register, values = mean v_model for one dim."""
    sub = df[df["dim_id"] == dim]
    wide = (
        sub.groupby(["model", "register"])["v_model"].mean().unstack("register")
    )
    return wide[list(REGISTERS)].sort_index()


def ordering_by_magnitude(series: pd.Series) -> list[str]:
    """Return register names sorted by abs(value) descending."""
    return list(series.abs().sort_values(ascending=False).index)


def ordering_signed_desc(series: pd.Series) -> list[str]:
    """Return register names sorted by raw value descending."""
    return list(series.sort_values(ascending=False).index)


# ---------- claim 1 ----------

def claim1_for_dim(df: pd.DataFrame, dim: str, rows: list[dict], lines: list[str]) -> None:
    lines.append(f"\n--- {dim} ---")
    h = human_means_per_register(df, dim)
    lines.append("Human mean v_human per register:")
    for reg in REGISTERS:
        lines.append(f"  {reg:<9} {h[reg]:+.4f}")
    h_order_mag = ordering_by_magnitude(h)
    lines.append(f"Human ordering by |v_human| (desc): {h_order_mag}")
    rows.append({
        "claim": "claim1",
        "sub_item": f"{dim}_human_ordering_by_magnitude",
        "value": " > ".join(h_order_mag),
        "supports_abstract_claim": "",
    })

    # human-highest register by absolute magnitude
    peak_reg = h_order_mag[0]
    h_peak_val = h[peak_reg]

    m_wide = model_means_per_register(df, dim)
    lines.append("\nPer-model mean v_model per register, and ordering by |v_model|:")
    matches = 0
    for model in m_wide.index:
        row = m_wide.loc[model]
        order = ordering_by_magnitude(row)
        match = order == h_order_mag
        matches += int(match)
        diff = ""
        if not match:
            # find first index where they differ
            for i, (a, b) in enumerate(zip(order, h_order_mag)):
                if a != b:
                    diff = f"  (diverges at position {i+1}: model={a}, human={b})"
                    break
        lines.append(
            f"  {model:<20} "
            + " ".join(f"{reg}={row[reg]:+.4f}" for reg in REGISTERS)
            + f"  order={order}  match={'yes' if match else 'no'}{diff}"
        )
        rows.append({
            "claim": "claim1",
            "sub_item": f"{dim}_{model}_ordering_matches_human",
            "value": "yes" if match else f"no; model={order}",
            "supports_abstract_claim": bool(match),
        })

    lines.append(f"\n{matches}/6 models match the human ordering exactly on {dim}.")
    rows.append({
        "claim": "claim1",
        "sub_item": f"{dim}_count_models_matching_human_ordering",
        "value": f"{matches}/6",
        "supports_abstract_claim": matches == 6,
    })

    # overshoot on the human-highest register
    lines.append(
        f"\nOvershoot on human-peak register '{peak_reg}' "
        f"(human mean = {h_peak_val:+.4f}):"
    )
    all_overshoot = True
    for model in m_wide.index:
        m_val = m_wide.loc[model, peak_reg]
        # overshoot ratio in the direction of the human value
        if h_peak_val == 0 or not np.isfinite(h_peak_val):
            pct = float("nan")
        else:
            pct = 100.0 * (m_val - h_peak_val) / h_peak_val
        same_sign = (m_val >= 0) == (h_peak_val >= 0)
        # "overshoot" = model magnitude exceeds human magnitude in same direction
        is_overshoot = same_sign and abs(m_val) > abs(h_peak_val)
        if not is_overshoot:
            all_overshoot = False
        lines.append(
            f"  {model:<20} v_model={m_val:+.4f}  overshoot_ratio={pct:+.1f}%  "
            f"overshoot={'yes' if is_overshoot else 'no'}"
        )
        rows.append({
            "claim": "claim1",
            "sub_item": f"{dim}_{model}_overshoot_pct_on_{peak_reg}",
            "value": f"{pct:+.1f}%",
            "supports_abstract_claim": bool(is_overshoot),
        })
    rows.append({
        "claim": "claim1",
        "sub_item": f"{dim}_all_models_overshoot_on_{peak_reg}",
        "value": "yes" if all_overshoot else "no",
        "supports_abstract_claim": all_overshoot,
    })


def claim1(df: pd.DataFrame, rows: list[dict]) -> str:
    lines: list[str] = []
    lines.append("=" * 78)
    lines.append("CLAIM 1 — Structural overshoot on dim5 (and dim3 sanity check)")
    lines.append("=" * 78)
    claim1_for_dim(df, "dim5", rows, lines)
    claim1_for_dim(df, "dim3", rows, lines)
    return "\n".join(lines)


# ---------- claim 2 ----------

def _peak_register(series: pd.Series) -> str:
    return series.idxmax()


def _trough_register(series: pd.Series) -> str:
    return series.idxmin()


def claim2(df: pd.DataFrame, rows: list[dict], models_subset: list[str] | None = None,
           tag: str = "claim2") -> tuple[str, dict]:
    lines: list[str] = []
    lines.append("=" * 78)
    if tag == "claim2":
        lines.append("CLAIM 2 — Lexical inversion on dim11 (MTLD), all 6 models")
    else:
        lines.append("CLAIM 3 — Lexical inversion robustness (exclude le_chat_free)")
    lines.append("=" * 78)

    sub = df[df["dim_id"] == "dim11"]
    if models_subset is not None:
        sub = sub[sub["model"].isin(models_subset)]

    h = human_means_per_register(sub, "dim11")
    lines.append("Human mean v_human per register on dim11:")
    for reg in REGISTERS:
        lines.append(f"  {reg:<9} {h[reg]:+.4f}")
    human_peak = _peak_register(h)
    human_trough = _trough_register(h)
    lines.append(f"Human peak: {human_peak}    Human trough: {human_trough}")

    rows.append({
        "claim": tag,
        "sub_item": "dim11_human_peak_register",
        "value": human_peak,
        "supports_abstract_claim": "",
    })

    m_wide = model_means_per_register(sub, "dim11")
    n_models = len(m_wide.index)
    lines.append(f"\nPer-model mean v_model per register on dim11 (n_models={n_models}):")
    peak_matches = 0
    blog_lowest_count = 0
    blog_lowest_models: list[str] = []
    peak_locations: dict[str, str] = {}
    for model in m_wide.index:
        row = m_wide.loc[model]
        model_peak = _peak_register(row)
        model_trough = _trough_register(row)
        peak_locations[model] = model_peak
        matches_peak = model_peak == human_peak
        peak_matches += int(matches_peak)
        if model_trough == "blog":
            blog_lowest_count += 1
            blog_lowest_models.append(model)
        lines.append(
            f"  {model:<20} "
            + " ".join(f"{reg}={row[reg]:+.4f}" for reg in REGISTERS)
            + f"  peak={model_peak}  trough={model_trough}"
        )
        rows.append({
            "claim": tag,
            "sub_item": f"dim11_{model}_peak_matches_human",
            "value": f"{model_peak} (human peak={human_peak})",
            "supports_abstract_claim": bool(matches_peak),
        })

    elsewhere = n_models - peak_matches
    lines.append(
        f"\n{peak_matches}/{n_models} models peak on human-peak register '{human_peak}'."
    )
    lines.append(
        f"{elsewhere}/{n_models} models peak elsewhere; locations: "
        + ", ".join(f"{m}->{r}" for m, r in peak_locations.items() if r != human_peak)
    )
    rows.append({
        "claim": tag,
        "sub_item": "dim11_count_models_peak_matches_human",
        "value": f"{peak_matches}/{n_models}",
        "supports_abstract_claim": peak_matches == n_models,
    })

    # "five of six invert on blog" — count models whose lowest v_model is blog,
    # given that humans have blog as their highest.
    human_peak_is_blog = human_peak == "blog"
    lines.append(
        f"\nInversion test ('blog is human's peak, model's trough'):"
        f"  human_peak_is_blog={human_peak_is_blog}"
    )
    lines.append(
        f"  {blog_lowest_count}/{n_models} models have blog as their LOWEST register:"
    )
    for m in blog_lowest_models:
        lines.append(f"    - {m}")
    rows.append({
        "claim": tag,
        "sub_item": "dim11_count_models_with_blog_as_lowest",
        "value": f"{blog_lowest_count}/{n_models}; models=" + ",".join(blog_lowest_models),
        "supports_abstract_claim": (
            human_peak_is_blog and blog_lowest_count >= max(1, n_models - 1)
        ),
    })

    summary = {
        "n_models": n_models,
        "human_peak": human_peak,
        "peak_matches": peak_matches,
        "blog_lowest_count": blog_lowest_count,
        "blog_lowest_models": blog_lowest_models,
        "m_wide": m_wide,
    }
    return "\n".join(lines), summary


def claim3_extra(df: pd.DataFrame, rows: list[dict]) -> str:
    """Identify the model with the highest overall mean v_model on dim11
    (across all registers) and ask whether it also inverts."""
    lines: list[str] = []
    sub = df[df["dim_id"] == "dim11"]
    overall = sub.groupby("model")["v_model"].mean().sort_values(ascending=False)
    top_model = overall.index[0]
    top_val = overall.iloc[0]
    lines.append("\nPer-model overall mean v_model on dim11 (across all registers):")
    for m, v in overall.items():
        lines.append(f"  {m:<20} {v:+.4f}")
    lines.append(f"\nHighest overall: {top_model} (mean = {top_val:+.4f})")

    # does it invert? (peak elsewhere than blog, where blog is the human peak)
    h = human_means_per_register(sub, "dim11")
    human_peak = _peak_register(h)
    m_wide = model_means_per_register(sub, "dim11")
    top_peak = _peak_register(m_wide.loc[top_model])
    top_trough = _trough_register(m_wide.loc[top_model])
    inverts = (human_peak == "blog") and (top_trough == "blog")
    lines.append(
        f"  human_peak={human_peak}, {top_model} peak={top_peak}, trough={top_trough}"
    )
    lines.append(
        f"  Does the highest-overall model also invert (blog as trough given "
        f"human blog peak)? {'yes' if inverts else 'no'}"
    )

    rows.append({
        "claim": "claim3",
        "sub_item": "dim11_highest_overall_model",
        "value": f"{top_model} (mean={top_val:+.4f})",
        "supports_abstract_claim": "",
    })
    rows.append({
        "claim": "claim3",
        "sub_item": "dim11_highest_overall_model_inverts",
        "value": (
            f"peak={top_peak}, trough={top_trough}, human_peak={human_peak} -> "
            f"{'inverts' if inverts else 'does not invert'}"
        ),
        "supports_abstract_claim": bool(inverts),
    })
    return "\n".join(lines)


# ---------- claim 4 ----------

def claim4(df: pd.DataFrame, rows: list[dict]) -> str:
    lines: list[str] = []
    lines.append("=" * 78)
    lines.append("CLAIM 4 — Trace section 5.2 mean |b| discrepancy")
    lines.append("=" * 78)

    # Variant A: mean of |b_d| across all rows per dimension.
    var_a = (
        df.assign(abs_b=df["b_d"].abs())
        .groupby("dim_id")["abs_b"].mean()
        .reindex(DIM_ORDER)
    )

    # Variant B: per (model, register, dim_id) cell, mean of |b_d| across
    # samples; then mean across the 24 cells per dim.
    cell_abs = (
        df.assign(abs_b=df["b_d"].abs())
        .groupby(["dim_id", "model", "register"])["abs_b"].mean()
        .reset_index()
    )
    var_b = cell_abs.groupby("dim_id")["abs_b"].mean().reindex(DIM_ORDER)

    # Variant C: per (model, register, dim_id) cell, mean of signed b_d across
    # samples; take absolute value; then mean across the 24 cells per dim.
    cell_signed = (
        df.groupby(["dim_id", "model", "register"])["b_d"].mean().abs()
        .reset_index()
    )
    var_c = cell_signed.groupby("dim_id")["b_d"].mean().reindex(DIM_ORDER)

    pub = pd.Series(PUBLISHED_MEAN_ABS_B).reindex(DIM_ORDER)

    table = pd.DataFrame({
        "published": pub,
        "variant_A_mean_abs_b_all_rows": var_a,
        "variant_B_mean_abs_b_per_cell_then_mean": var_b,
        "variant_C_mean_signed_per_cell_then_abs_then_mean": var_c,
    })
    table["A_diff"] = table["variant_A_mean_abs_b_all_rows"] - table["published"]
    table["B_diff"] = table["variant_B_mean_abs_b_per_cell_then_mean"] - table["published"]
    table["C_diff"] = table["variant_C_mean_signed_per_cell_then_abs_then_mean"] - table["published"]

    with pd.option_context("display.width", 140, "display.float_format", lambda x: f"{x:8.4f}"):
        lines.append(table.to_string())

    # Per-variant reproduction check
    for var_name, col, diff_col in [
        ("A", "variant_A_mean_abs_b_all_rows", "A_diff"),
        ("B", "variant_B_mean_abs_b_per_cell_then_mean", "B_diff"),
        ("C", "variant_C_mean_signed_per_cell_then_abs_then_mean", "C_diff"),
    ]:
        ok = table[diff_col].abs().max() <= PUBLISHED_TOLERANCE
        worst_dim = table[diff_col].abs().idxmax()
        worst = table.loc[worst_dim, diff_col]
        lines.append(
            f"\nVariant {var_name}: max |diff| = {abs(worst):.4f} at {worst_dim} "
            f"(diff={worst:+.4f})  reproduces_within_{PUBLISHED_TOLERANCE}={ok}"
        )
        # per-dim rows
        for dim in DIM_ORDER:
            rows.append({
                "claim": "claim4",
                "sub_item": f"variant_{var_name}_{dim}",
                "value": f"{table.loc[dim, col]:.4f} (pub={pub[dim]:.2f}, diff={table.loc[dim, diff_col]:+.4f})",
                "supports_abstract_claim": "",
            })
        rows.append({
            "claim": "claim4",
            "sub_item": f"variant_{var_name}_reproduces_published_within_{PUBLISHED_TOLERANCE}",
            "value": f"max|diff|={abs(worst):.4f} at {worst_dim}",
            "supports_abstract_claim": bool(ok),
        })

    return "\n".join(lines)


# ---------- verdicts ----------

def write_verdicts(claim1_state: dict, claim2_state: dict, claim3_state: dict,
                   claim4_state: dict) -> str:
    lines = ["", "=" * 78, "VERDICTS", "=" * 78]

    # Claim 1 — structural overshoot
    dim5 = claim1_state["dim5"]
    dim3 = claim1_state["dim3"]
    parts = []
    parts.append(
        f"On dim5, {dim5['matches']}/6 models match the human register ordering "
        f"exactly and {dim5['overshoot_count']}/6 overshoot the human-peak "
        f"register '{dim5['peak_reg']}'."
    )
    parts.append(
        f"On dim3, {dim3['matches']}/6 models match the human ordering and "
        f"{dim3['overshoot_count']}/6 overshoot '{dim3['peak_reg']}'."
    )
    if dim5["overshoot_count"] == 6 and dim3["overshoot_count"] == 6:
        verdict1 = "supported"
    elif dim5["overshoot_count"] == 6 or dim3["overshoot_count"] == 6:
        verdict1 = "partially supported"
    else:
        verdict1 = "not supported"
    lines.append(
        f"\nClaim 1 — structural overshoot (dim5 & dim3): {verdict1.upper()}. "
        + " ".join(parts)
    )

    # Claim 2 — lexical inversion on dim11
    c2 = claim2_state
    if c2["human_peak"] == "blog":
        if c2["blog_lowest_count"] >= 5:
            verdict2 = "supported"
        elif c2["blog_lowest_count"] >= 3:
            verdict2 = "partially supported"
        else:
            verdict2 = "not supported"
    else:
        verdict2 = "not supported"
    lines.append(
        f"\nClaim 2 — lexical inversion on dim11 (MTLD): {verdict2.upper()}. "
        f"Human peak on dim11 is '{c2['human_peak']}'. "
        f"{c2['peak_matches']}/6 models peak there; "
        f"{c2['blog_lowest_count']}/6 models have blog as their lowest "
        f"v_model register."
    )

    # Claim 3 — robustness
    c3 = claim3_state
    base = c2["blog_lowest_count"]
    after = c3["blog_lowest_count"]
    if c3["human_peak"] == "blog" and after >= 4 and after / 5 >= base / 6:
        verdict3 = "supported"
    elif c3["human_peak"] == "blog" and after >= 3:
        verdict3 = "partially supported"
    else:
        verdict3 = "not supported"
    lines.append(
        f"\nClaim 3 — lexical inversion robustness (drop {LOOP_PRONE_MODEL}): "
        f"{verdict3.upper()}. After exclusion, {after}/5 models have blog as "
        f"their lowest v_model register on dim11 (was {base}/6 before)."
    )

    # Claim 4 — variant that reproduces published
    c4 = claim4_state
    matches = [v for v, ok in c4.items() if ok]
    if matches:
        verdict4 = "supported"
        which = ", ".join(matches)
    else:
        verdict4 = "not supported"
        which = "none"
    lines.append(
        f"\nClaim 4 — section 5.2 mean |b| discrepancy: {verdict4.upper()}. "
        f"Variant(s) reproducing published values within {PUBLISHED_TOLERANCE}: {which}."
    )

    return "\n".join(lines)


# ---------- driver ----------

def main() -> None:
    df = pd.read_csv(DEFAULT_CSV)

    rows: list[dict] = []
    out_lines: list[str] = []

    out_lines.append(f"Source: {DEFAULT_CSV.relative_to(REPO_ROOT)}")
    out_lines.append(f"Rows: {len(df)}, models: {df['model'].nunique()}, "
                     f"registers: {df['register'].nunique()}, dims: {df['dim_id'].nunique()}")

    # --- Claim 1 ---
    out_lines.append(claim1(df, rows))

    # Recompute small summaries for verdict block (count overshoots from rows).
    def _claim1_summary(dim: str) -> dict:
        h = human_means_per_register(df, dim)
        peak_reg = ordering_by_magnitude(h)[0]
        m_wide = model_means_per_register(df, dim)
        h_peak_val = h[peak_reg]
        matches = 0
        overshoot_count = 0
        for model in m_wide.index:
            row = m_wide.loc[model]
            if ordering_by_magnitude(row) == ordering_by_magnitude(h):
                matches += 1
            m_val = row[peak_reg]
            same_sign = (m_val >= 0) == (h_peak_val >= 0)
            if same_sign and abs(m_val) > abs(h_peak_val):
                overshoot_count += 1
        return {"peak_reg": peak_reg, "matches": matches, "overshoot_count": overshoot_count}

    claim1_state = {"dim5": _claim1_summary("dim5"), "dim3": _claim1_summary("dim3")}

    # --- Claim 2 ---
    txt2, claim2_state = claim2(df, rows, models_subset=None, tag="claim2")
    out_lines.append(txt2)

    # --- Claim 3 ---
    other_models = [m for m in sorted(df["model"].unique()) if m != LOOP_PRONE_MODEL]
    out_lines.append(
        f"\nExcluded loop-prone model: {LOOP_PRONE_MODEL}. "
        f"Remaining models ({len(other_models)}): {other_models}"
    )
    txt3, claim3_state = claim2(df, rows, models_subset=other_models, tag="claim3")
    out_lines.append(txt3)
    out_lines.append(claim3_extra(df, rows))

    # --- Claim 4 ---
    out_lines.append(claim4(df, rows))

    # capture per-variant pass/fail for the verdict
    claim4_state = {}
    for r in rows:
        if r["claim"] == "claim4" and r["sub_item"].endswith(
            f"_reproduces_published_within_{PUBLISHED_TOLERANCE}"
        ):
            # sub_item is "variant_X_reproduces_published_within_0.05"
            var_letter = r["sub_item"].split("_")[1]
            claim4_state[var_letter] = bool(r["supports_abstract_claim"])

    out_lines.append(write_verdicts(claim1_state, claim2_state, claim3_state, claim4_state))

    # write CSV
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT_CSV, index=False)
    out_lines.append(f"\nWrote summary CSV: {OUT_CSV.relative_to(REPO_ROOT)}")

    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
