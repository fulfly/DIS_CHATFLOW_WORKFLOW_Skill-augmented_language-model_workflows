#!/usr/bin/env python
"""Generate revised Fig. 5a K4M fraction plot from real formulation data."""

from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ncfigs.io import ensure_dir, load_table, require_columns, save_source_copy, save_table
from ncfigs.plotting import bar_with_points, present_order
from ncfigs.stats import group_summary, one_way_test
from ncfigs.style import add_panel_label, format_axis, save_figure, set_nature_style


PREFERRED_ORDER = ["Standard", "GPT-5.4", "Qwen", "Gemini 2.5 Flash"]
MODEL_BAR_ORDER = ["GPT-5.4", "Qwen", "Gemini 2.5 Flash"]

COOL_BAR_COLORS = {
    "Standard": "#7A8DA3",
    "GPT-5.4": "#3F7FBF",
    "Qwen": "#2A9DA8",
    "Gemini 2.5 Flash": "#6B5DBB",
}


def standardize_fig5a_group(value: object) -> str:
    text = "" if pd.isna(value) else str(value).strip()
    key = text.lower().replace("_", "-").replace(" ", "-")
    if key in {"standard", "reference", "std"}:
        return "Standard"
    if key in {"gpt-5.4", "gpt5.4", "gpt-5-4", "gpt"}:
        return "GPT-5.4"
    if "qwen" in key:
        return "Qwen"
    if "gemini" in key:
        return "Gemini 2.5 Flash"
    return text


def choose_ymax(values: pd.Series) -> float:
    max_value = float(pd.to_numeric(values, errors="coerce").max())
    if max_value <= 0.6:
        return 0.6
    if max_value <= 0.8:
        return 0.8
    return min(1.0, np.ceil(max_value * 10) / 10 + 0.05)


def prepare_fig5a(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = ["formulation_group", "replicate_id", "k4m_amount", "k100lv_amount"]
    require_columns(df, required, "Fig. 5a formulation-ratio table")
    out = df.copy()
    out["source_formulation_group"] = out["formulation_group"]
    out["formulation_group"] = out["formulation_group"].map(standardize_fig5a_group)
    out["k4m_amount"] = pd.to_numeric(out["k4m_amount"], errors="coerce")
    out["k100lv_amount"] = pd.to_numeric(out["k100lv_amount"], errors="coerce")
    denominator = out["k4m_amount"] + out["k100lv_amount"]
    out["relative_k4m_fraction"] = out["k4m_amount"] / denominator
    out["relative_k4m_fraction_formula"] = "K4M / (K4M + K100LV)"
    out["denominator_k4m_plus_k100lv"] = denominator

    if "k4m_k100lv_ratio" in out.columns:
        out["provided_k4m_k100lv_ratio"] = pd.to_numeric(out["k4m_k100lv_ratio"], errors="coerce")
        out["provided_ratio_matches_fraction"] = np.isclose(
            out["provided_k4m_k100lv_ratio"],
            out["relative_k4m_fraction"],
            rtol=1e-6,
            atol=1e-9,
            equal_nan=False,
        )
    else:
        out["provided_k4m_k100lv_ratio"] = np.nan
        out["provided_ratio_matches_fraction"] = False

    qc = (
        out.groupby(["source_formulation_group", "formulation_group"], observed=False)
        .agg(
            n_rows=("replicate_id", "count"),
            n_replicates=("replicate_id", "nunique"),
            missing_k4m=("k4m_amount", lambda x: int(x.isna().sum())),
            missing_k100lv=("k100lv_amount", lambda x: int(x.isna().sum())),
            missing_relative_fraction=("relative_k4m_fraction", lambda x: int(x.isna().sum())),
            mean_relative_k4m_fraction=("relative_k4m_fraction", "mean"),
            sd_relative_k4m_fraction=("relative_k4m_fraction", lambda x: x.std(ddof=1)),
        )
        .reset_index()
        .sort_values(["formulation_group", "source_formulation_group"])
    )
    qc["group_standardization_note"] = np.where(
        qc["source_formulation_group"] != qc["formulation_group"],
        "source group standardized for Fig. 5a display",
        "",
    )
    return out, qc


def plot_fig5a(processed: pd.DataFrame, order: list[str], ymax: float, outbase: Path) -> pd.DataFrame:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(3.8, 2.35))
    summary = bar_with_points(
        ax,
        processed,
        group_col="formulation_group",
        value_col="relative_k4m_fraction",
        order=order,
        palette=COOL_BAR_COLORS,
        y_label="Relative K4M fraction\nK4M / (K4M + K100LV)",
        ylim=(0, ymax),
    )
    ax.set_xlabel("")
    ax.set_title("K4M fraction")
    add_panel_label(ax, "a")
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return summary


def standard_reference_value(processed: pd.DataFrame) -> float:
    standard_values = pd.to_numeric(
        processed.loc[processed["formulation_group"] == "Standard", "relative_k4m_fraction"],
        errors="coerce",
    ).dropna()
    if standard_values.empty:
        raise ValueError("Standard formulation is required for the Fig. 5a reference line.")
    if not np.allclose(standard_values, standard_values.iloc[0], rtol=1e-7, atol=1e-9):
        warnings.warn(
            "Multiple Standard values were found; using their mean as the dashed reference line.",
            stacklevel=2,
        )
    return float(standard_values.mean())


def plot_fig5a_reference_line(
    processed: pd.DataFrame,
    model_order: list[str],
    standard_value: float,
    ymax: float,
    outbase: Path,
) -> pd.DataFrame:
    """Plot model-optimized bars with Standard as a dashed reference line."""
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(3.55, 2.35))
    model_df = processed.loc[processed["formulation_group"].isin(model_order)].copy()
    summary = group_summary(model_df, "formulation_group", "relative_k4m_fraction", order=model_order)
    x = np.arange(len(model_order))
    means = []
    sds = []
    colors = []
    for idx, group in enumerate(model_order):
        row = summary.loc[summary["formulation_group"] == group]
        means.append(float(row["mean"].iloc[0]) if not row.empty else np.nan)
        sd = float(row["sd"].iloc[0]) if not row.empty else np.nan
        sds.append(0.0 if np.isnan(sd) else sd)
        colors.append(COOL_BAR_COLORS.get(group, "#4F6D7A"))

    ax.bar(
        x,
        means,
        yerr=sds,
        width=0.58,
        color=colors,
        edgecolor="black",
        linewidth=0.5,
        error_kw={"elinewidth": 0.6, "capsize": 2, "capthick": 0.6},
        zorder=1,
    )
    rng = np.random.default_rng(17)
    for idx, group in enumerate(model_order):
        values = pd.to_numeric(
            model_df.loc[model_df["formulation_group"] == group, "relative_k4m_fraction"],
            errors="coerce",
        ).dropna()
        jitter = rng.uniform(-0.10, 0.10, size=len(values))
        ax.scatter(
            np.full(len(values), idx) + jitter,
            values,
            s=10,
            facecolor="white",
            edgecolor="black",
            linewidth=0.45,
            zorder=3,
        )

    ax.axhline(
        standard_value,
        color="#303030",
        linestyle=(0, (3, 2)),
        linewidth=0.75,
        zorder=2,
    )
    ax.set_xlim(-0.58, len(model_order) - 0.42)
    ax.set_ylim(0, ymax)
    ax.set_xticks(x)
    ax.set_xticklabels(model_order, rotation=30, ha="right")
    ax.set_xlabel("")
    ax.set_ylabel("Relative K4M fraction\nK4M / (K4M + K100LV)")
    ax.set_title("K4M fraction")
    ax.legend(
        handles=[
            Line2D(
                [0],
                [0],
                color="#303030",
                linestyle=(0, (3, 2)),
                linewidth=0.75,
                label="Standard reference",
            )
        ],
        loc="upper right",
        frameon=False,
    )
    add_panel_label(ax, "a")
    format_axis(ax)
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)

    summary["display_type"] = "model bar with individual points and mean +/- SD"
    summary["standard_reference_value"] = standard_value
    summary["standard_display_type"] = "horizontal dashed reference line; no Standard bar or error bar"
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=ROOT / "data/raw/fig5a_formulation_ratios.csv", type=Path)
    parser.add_argument("--sheet", default=None, help="Excel sheet name/index for --input.")
    parser.add_argument("--outdir", default=ROOT / "outputs", type=Path)
    parser.add_argument(
        "--output-prefix",
        default="fig5a_formulation_ratio_revised",
        help="Filename prefix for figure and output tables.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figdir = ensure_dir(args.outdir / "figures")
    processed_dir = ensure_dir(args.outdir / "processed")
    source_dir = ensure_dir(args.outdir / "source_data")
    stats_dir = ensure_dir(args.outdir / "stats")
    qc_dir = ensure_dir(args.outdir / "qc")

    raw = load_table(args.input, sheet_name=args.sheet)
    prefix = args.output_prefix
    save_source_copy(raw, source_dir / f"{prefix}_source.csv")
    processed, qc = prepare_fig5a(raw)
    order = present_order(processed["formulation_group"], PREFERRED_ORDER)
    model_order = present_order(processed.loc[processed["formulation_group"] != "Standard", "formulation_group"], MODEL_BAR_ORDER)
    standard_value = standard_reference_value(processed)
    ymax = choose_ymax(processed["relative_k4m_fraction"])

    save_table(processed, processed_dir / f"{prefix}_processed.csv")
    save_table(qc, qc_dir / f"{prefix}_qc.csv")
    if prefix.endswith("reference_line"):
        summary = plot_fig5a_reference_line(
            processed,
            model_order=model_order,
            standard_value=standard_value,
            ymax=ymax,
            outbase=figdir / prefix,
        )
    else:
        summary = plot_fig5a(
            processed,
            order=order,
            ymax=ymax,
            outbase=figdir / prefix,
        )
    summary["y_axis_min"] = 0.0
    summary["y_axis_max"] = ymax
    summary["plotted_value_formula"] = "K4M / (K4M + K100LV)"
    summary["standard_reference_value"] = standard_value
    summary["standard_plotted_as_bar"] = not prefix.endswith("reference_line")
    save_table(summary, processed_dir / f"{prefix}_summary.csv")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        stats_input = processed.loc[processed["formulation_group"].isin(model_order)].copy()
        stats_rows = [
            one_way_test(
                stats_input,
                "relative_k4m_fraction",
                "formulation_group",
                "Fig. 5a relative K4M fraction across model-optimized groups",
                order=model_order,
                preferred="kruskal",
                replicate_definition=(
                    "Each point is one formulation entry/replicate from the Fig. 5a CSV; "
                    "the plotted value is recalculated as K4M/(K4M+K100LV). "
                    "Standard is displayed as a fixed dashed reference line and excluded from this group test."
                ),
            )
        ]
    stats = pd.concat(stats_rows, ignore_index=True)
    model_summary = group_summary(stats_input, "formulation_group", "relative_k4m_fraction", order=model_order)
    for row in model_summary.itertuples(index=False):
        stats.loc[len(stats)] = {
            "analysis": "Fig. 5a descriptive difference from Standard reference",
            "value": "relative_k4m_fraction",
            "group": "formulation_group",
            "n_total": int(row.n),
            "group_ns": f"{row.formulation_group}: n={int(row.n)}; Standard reference: fixed line",
            "replicate_definition": (
                "Model bars use formulation entries/replicates from the Fig. 5a CSV. "
                "Standard is treated as a fixed dashed reference value, not a replicate group."
            ),
            "test": "not run",
            "comparison": f"{row.formulation_group} mean minus Standard reference",
            "statistic": float(row.mean - standard_value),
            "p_value": np.nan,
            "p_adjusted": np.nan,
            "correction": "none",
            "notes": (
                "No inferential comparison versus Standard was plotted because Standard is represented "
                "as a fixed reference line without an error bar."
            ),
        }
    if caught:
        warning_text = " | ".join(str(w.message) for w in caught)
        stats.loc[len(stats)] = {
            "analysis": "Fig. 5a warnings",
            "value": "relative_k4m_fraction",
            "group": "formulation_group",
            "n_total": len(processed),
            "group_ns": "",
            "replicate_definition": "",
            "test": "warning",
            "comparison": "runtime",
            "statistic": np.nan,
            "p_value": np.nan,
            "p_adjusted": np.nan,
            "correction": "",
            "notes": warning_text,
        }
    save_table(stats, stats_dir / f"{prefix}_stats.csv")

    color_table = pd.DataFrame(
        [
            {
                "formulation_group": group,
                "color_hex": COOL_BAR_COLORS.get(group, "#4F6D7A"),
                "display_type": "bar",
            }
            for group in model_order
        ]
        + [
            {
                "formulation_group": "Standard",
                "color_hex": "#303030",
                "display_type": "horizontal dashed reference line",
            }
        ]
    )
    save_table(color_table, processed_dir / f"{prefix}_colors.csv")

    print(f"input_file={args.input}")
    print("groups=" + "; ".join(order))
    print("bar_groups=" + "; ".join(model_order))
    print("standard_display=horizontal dashed reference line")
    print(f"standard_reference_value={standard_value:.10g}")
    print("formula=relative_k4m_fraction = K4M / (K4M + K100LV)")
    print("recalculated_from_k4m_and_k100lv=True")
    print(f"y_axis_range=0,{ymax}")
    print("colors=" + "; ".join(f"{row.formulation_group}: {row.color_hex}" for row in color_table.itertuples()))
    print(f"output_prefix={prefix}")
    print(f"figure=outputs/figures/{prefix}.[pdf|svg|png]")
    print(f"processed=outputs/processed/{prefix}_processed.csv")
    print(f"source=outputs/source_data/{prefix}_source.csv")
    print(f"stats=outputs/stats/{prefix}_stats.csv")
    print(f"qc=outputs/qc/{prefix}_qc.csv")


if __name__ == "__main__":
    main()
