#!/usr/bin/env python
"""Generate revised Fig. 5b time-course and ratio plots from processed UV data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ncfigs.io import ensure_dir, require_columns, save_table
from ncfigs.plotting import bar_with_points, present_order
from ncfigs.stats import trapezoid_auc
from ncfigs.style import add_panel_label, format_axis, save_figure, set_nature_style


PREFERRED_ORDER = [
    "Standard",
    "GPT-5-mini",
    "Qwen3.6-plus",
    "Gemini 2.5 Flash",
    "GLM-4.6V",
    "Kimi-K2.5",
]

COOL_GROUP_COLORS = {
    "Standard": "#6E7F92",  # neutral gray-blue
    "GPT-5-mini": "#0072B2",  # clear blue
    "Qwen3.6-plus": "#009E9E",  # teal / blue-green
    "Gemini 2.5 Flash": "#5B4BA3",  # indigo-purple
    "GLM-4.6V": "#3B6F8F",
    "Kimi-K2.5": "#6A7FDB",
}


def include_mask(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().isin({"yes", "y", "true", "1", "include", "included"})


def choose_y_variable(df: pd.DataFrame) -> str:
    return "corrected_absorbance" if "corrected_absorbance" in df.columns else "absorbance"


def file_level_timecourse(long_df: pd.DataFrame, y_col: str) -> pd.DataFrame:
    required = [
        "source_file",
        "formulation_group",
        "formulation_label",
        "drug_label",
        "replicate_file_id",
        "measurement_id",
        "time_h",
        y_col,
    ]
    require_columns(long_df, required, "Fig. 5b long UV source data")
    df = long_df.copy()
    if "include_for_fig5b" in df.columns:
        df = df.loc[include_mask(df["include_for_fig5b"])].copy()
    df["time_h"] = pd.to_numeric(df["time_h"], errors="coerce")
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
    df = df.dropna(subset=["time_h", y_col])

    group_cols = [
        "source_file",
        "formulation_group",
        "formulation_label",
        "drug_label",
        "replicate_file_id",
        "time_h",
    ]
    curves = (
        df.groupby(group_cols, observed=False)
        .agg(
            uv_signal=(y_col, "mean"),
            n_technical_measurements=("measurement_id", "nunique"),
        )
        .reset_index()
    )
    curves["y_variable"] = y_col
    curves["baseline_added_for_plot"] = False

    baseline_rows = []
    metadata_cols = ["source_file", "formulation_group", "formulation_label", "drug_label", "replicate_file_id"]
    for keys, sdf in curves.groupby(metadata_cols, observed=False):
        if not np.isclose(sdf["time_h"], 0.0).any():
            row = dict(zip(metadata_cols, keys))
            row.update(
                {
                    "time_h": 0.0,
                    "uv_signal": 0.0,
                    "n_technical_measurements": int(sdf["n_technical_measurements"].max()),
                    "y_variable": y_col,
                    "baseline_added_for_plot": True,
                }
            )
            baseline_rows.append(row)
    if baseline_rows:
        curves = pd.concat([curves, pd.DataFrame(baseline_rows)], ignore_index=True)
    return curves.sort_values(["formulation_group", "replicate_file_id", "time_h"]).reset_index(drop=True)


def summarize_timecourse(curves: pd.DataFrame) -> pd.DataFrame:
    summary = (
        curves.groupby(["formulation_group", "time_h"], observed=False)
        .agg(
            n_files=("replicate_file_id", "nunique"),
            mean_uv_signal=("uv_signal", "mean"),
            sd_uv_signal=("uv_signal", lambda x: x.std(ddof=1)),
            y_variable=("y_variable", "first"),
        )
        .reset_index()
        .sort_values(["formulation_group", "time_h"])
    )
    summary["sd_uv_signal"] = summary["sd_uv_signal"].fillna(0.0)
    return summary


def plot_timecourse(summary: pd.DataFrame, order: list[str], outbase: Path) -> None:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(5.8, 2.45))
    for idx, group in enumerate(order):
        gdf = summary.loc[summary["formulation_group"] == group].sort_values("time_h")
        if gdf.empty:
            continue
        color = COOL_GROUP_COLORS.get(group, "#4F6D7A")
        x = gdf["time_h"].to_numpy(float)
        mean = gdf["mean_uv_signal"].to_numpy(float)
        sd = gdf["sd_uv_signal"].fillna(0).to_numpy(float)
        ax.plot(x, mean, color=color, linewidth=1.25, marker="o", markersize=3.0, label=group)
        ax.fill_between(x, mean - sd, mean + sd, color=color, alpha=0.16, linewidth=0)

    lower = float((summary["mean_uv_signal"] - summary["sd_uv_signal"]).min())
    upper = float((summary["mean_uv_signal"] + summary["sd_uv_signal"]).max())
    span = upper - lower if upper > lower else max(abs(upper), 0.1)
    y_min = 0.0 if lower >= 0 else lower - 0.08 * span
    y_max = upper + 0.10 * span
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("UV absorbance (a.u.)")
    ax.legend(loc="best", ncol=2, handlelength=1.5, columnspacing=0.9)
    add_panel_label(ax, "b")
    format_axis(ax)
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)


def plot_timecourse_errorbars(summary: pd.DataFrame, order: list[str], outbase: Path) -> None:
    """Plot group mean time courses with vertical SD error bars and no shaded bands."""
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(5.9, 2.45))
    for group in order:
        gdf = summary.loc[summary["formulation_group"] == group].sort_values("time_h")
        if gdf.empty:
            continue
        color = COOL_GROUP_COLORS.get(group, "#4F6D7A")
        ax.errorbar(
            gdf["time_h"],
            gdf["mean_uv_signal"],
            yerr=gdf["sd_uv_signal"],
            color=color,
            marker="o",
            markersize=3.0,
            markerfacecolor=color,
            markeredgecolor=color,
            linewidth=1.15,
            elinewidth=0.65,
            capsize=2.0,
            capthick=0.65,
            label=group,
            zorder=3,
        )

    lower = float((summary["mean_uv_signal"] - summary["sd_uv_signal"]).min())
    upper = float((summary["mean_uv_signal"] + summary["sd_uv_signal"]).max())
    span = upper - lower if upper > lower else max(abs(upper), 0.1)
    y_min = min(0.0, lower - 0.05 * span)
    y_max = upper + 0.08 * span
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("UV absorbance (a.u.)")
    ax.legend(loc="best", ncol=2, handlelength=1.5, columnspacing=0.9)
    add_panel_label(ax, "b")
    format_axis(ax)
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)


def plot_timecourse_0to8h_errorbars(
    summary: pd.DataFrame,
    order: list[str],
    outbase: Path,
) -> pd.DataFrame:
    """Plot the manuscript-ready 0-8 h mean time course with clean SD error bars."""
    plot_data = summary.loc[summary["time_h"] <= 8.0].copy()
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(5.9, 2.45))
    for group in order:
        gdf = plot_data.loc[plot_data["formulation_group"] == group].sort_values("time_h")
        if gdf.empty:
            continue
        color = COOL_GROUP_COLORS.get(group, "#4F6D7A")
        n_files = int(gdf["n_files"].max())
        ax.errorbar(
            gdf["time_h"],
            gdf["mean_uv_signal"],
            yerr=gdf["sd_uv_signal"],
            color=color,
            marker="o",
            markersize=2.5,
            markerfacecolor=color,
            markeredgecolor=color,
            linewidth=1.0,
            elinewidth=0.45,
            capsize=1.4,
            capthick=0.45,
            label=f"{group} (n={n_files})",
            zorder=3,
        )

    lower = float((plot_data["mean_uv_signal"] - plot_data["sd_uv_signal"]).min())
    upper = float((plot_data["mean_uv_signal"] + plot_data["sd_uv_signal"]).max())
    span = upper - lower if upper > lower else max(abs(upper), 0.1)
    y_min = min(0.0, lower - 0.04 * span)
    y_max = upper + 0.07 * span
    ax.set_xlim(-0.15, 8.15)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks([0, 0.5, 1, 2, 4, 6, 8])
    ax.set_xticklabels(["0", "0.5", "1", "2", "4", "6", "8"])
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("UV absorbance (a.u.)")
    ax.legend(loc="best", ncol=2, handlelength=1.5, columnspacing=0.9)
    add_panel_label(ax, "b")
    format_axis(ax)
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return plot_data


def curve_with_auc_boundaries(
    curve: pd.DataFrame,
    value_col: str = "uv_signal",
    start: float = 0.0,
    end: float = 8.0,
) -> pd.DataFrame:
    """Return a single replicate curve clipped to start/end with interpolated boundaries."""
    clean = curve[["time_h", value_col]].copy()
    clean["time_h"] = pd.to_numeric(clean["time_h"], errors="coerce")
    clean[value_col] = pd.to_numeric(clean[value_col], errors="coerce")
    clean = clean.dropna().sort_values("time_h")
    clean = clean.groupby("time_h", as_index=False, observed=False)[value_col].mean()
    if clean.empty or clean["time_h"].min() > start or clean["time_h"].max() < end:
        return pd.DataFrame(columns=["time_h", value_col])

    times = clean["time_h"].to_numpy(float)
    values = clean[value_col].to_numpy(float)
    time_points = sorted(set([start, end, *times[(times >= start) & (times <= end)]]))
    boundary_curve = pd.DataFrame(
        {
            "time_h": time_points,
            value_col: np.interp(time_points, times, values),
        }
    )
    return boundary_curve


def compute_relative_signal_curves(curves: pd.DataFrame) -> pd.DataFrame:
    """Normalize each file-level mean technical curve by its own AUC_0-8h."""
    metadata_cols = ["source_file", "formulation_group", "formulation_label", "drug_label", "replicate_file_id"]
    rows = []
    for keys, curve in curves.groupby(metadata_cols, observed=False):
        boundary_curve = curve_with_auc_boundaries(curve, value_col="uv_signal", start=0.0, end=8.0)
        if boundary_curve.empty:
            continue
        auc_0_8h = trapezoid_auc(
            boundary_curve["time_h"].to_numpy(),
            boundary_curve["uv_signal"].to_numpy(),
            start=0.0,
            end=8.0,
        )
        if pd.isna(auc_0_8h) or auc_0_8h <= 0:
            continue
        normalized = boundary_curve.copy()
        normalized["relative_uv_signal_per_h"] = normalized["uv_signal"] / auc_0_8h
        normalized["AUC_0_8h_denominator"] = auc_0_8h
        normalized["integral_0_8h"] = trapezoid_auc(
            normalized["time_h"].to_numpy(),
            normalized["relative_uv_signal_per_h"].to_numpy(),
            start=0.0,
            end=8.0,
        )
        for col, value in zip(metadata_cols, keys):
            normalized[col] = value
        rows.append(normalized)
    if not rows:
        return pd.DataFrame(
            columns=[
                *metadata_cols,
                "time_h",
                "uv_signal",
                "relative_uv_signal_per_h",
                "AUC_0_8h_denominator",
                "integral_0_8h",
            ]
        )
    return pd.concat(rows, ignore_index=True)[
        [
            *metadata_cols,
            "time_h",
            "uv_signal",
            "relative_uv_signal_per_h",
            "AUC_0_8h_denominator",
            "integral_0_8h",
        ]
    ]


def summarize_relative_signal(relative_curves: pd.DataFrame) -> pd.DataFrame:
    summary = (
        relative_curves.groupby(["formulation_group", "time_h"], observed=False)
        .agg(
            n_files=("replicate_file_id", "nunique"),
            mean_relative_uv_signal_per_h=("relative_uv_signal_per_h", "mean"),
            sd_relative_uv_signal_per_h=("relative_uv_signal_per_h", lambda x: x.std(ddof=1)),
            mean_integral_0_8h=("integral_0_8h", "mean"),
        )
        .reset_index()
        .sort_values(["formulation_group", "time_h"])
    )
    summary["sd_relative_uv_signal_per_h"] = summary["sd_relative_uv_signal_per_h"].fillna(0.0)
    summary["normalization_formula"] = "relative_uv_signal_per_h = file_level_mean_absorbance(t) / AUC_0_8h"
    summary["y_axis_definition"] = "normalized absorbance density; trapezoidal integral over 0-8 h equals 1 per file"
    return summary


def plot_relative_signal_timecourse(
    summary: pd.DataFrame,
    order: list[str],
    outbase: Path,
) -> pd.DataFrame:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(5.9, 2.45))
    plot_data = summary.copy()
    for group in order:
        gdf = plot_data.loc[plot_data["formulation_group"] == group].sort_values("time_h")
        if gdf.empty:
            continue
        color = COOL_GROUP_COLORS.get(group, "#4F6D7A")
        n_files = int(gdf["n_files"].max())
        ax.errorbar(
            gdf["time_h"],
            gdf["mean_relative_uv_signal_per_h"],
            yerr=gdf["sd_relative_uv_signal_per_h"],
            color=color,
            marker="o",
            markersize=2.5,
            markerfacecolor=color,
            markeredgecolor=color,
            linewidth=1.0,
            elinewidth=0.45,
            capsize=1.4,
            capthick=0.45,
            label=f"{group} (n={n_files})",
            zorder=3,
        )

    lower = float((plot_data["mean_relative_uv_signal_per_h"] - plot_data["sd_relative_uv_signal_per_h"]).min())
    upper = float((plot_data["mean_relative_uv_signal_per_h"] + plot_data["sd_relative_uv_signal_per_h"]).max())
    span = upper - lower if upper > lower else max(abs(upper), 0.1)
    ax.set_xlim(-0.15, 8.15)
    ax.set_ylim(min(0.0, lower - 0.04 * span), upper + 0.07 * span)
    ax.set_xticks([0, 0.5, 1, 2, 4, 6, 8])
    ax.set_xticklabels(["0", "0.5", "1", "2", "4", "6", "8"])
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("UV signal / AUC$_{0-8h}$ (h$^{-1}$)")
    ax.legend(loc="best", ncol=2, handlelength=1.5, columnspacing=0.9)
    add_panel_label(ax, "b")
    format_axis(ax)
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return plot_data


def compute_interval_fraction_curves(curves: pd.DataFrame) -> pd.DataFrame:
    """Calculate each interval's fraction of file-level AUC_0-8h."""
    metadata_cols = ["source_file", "formulation_group", "formulation_label", "drug_label", "replicate_file_id"]
    rows = []
    for keys, curve in curves.groupby(metadata_cols, observed=False):
        boundary_curve = curve_with_auc_boundaries(curve, value_col="uv_signal", start=0.0, end=8.0)
        if boundary_curve.empty:
            continue
        auc_0_8h = trapezoid_auc(
            boundary_curve["time_h"].to_numpy(),
            boundary_curve["uv_signal"].to_numpy(),
            start=0.0,
            end=8.0,
        )
        if pd.isna(auc_0_8h) or auc_0_8h <= 0:
            continue
        boundary_curve = boundary_curve.sort_values("time_h").reset_index(drop=True)
        for idx in range(1, len(boundary_curve)):
            t0 = float(boundary_curve.loc[idx - 1, "time_h"])
            t1 = float(boundary_curve.loc[idx, "time_h"])
            y0 = float(boundary_curve.loc[idx - 1, "uv_signal"])
            y1 = float(boundary_curve.loc[idx, "uv_signal"])
            interval_auc = (y0 + y1) * 0.5 * (t1 - t0)
            row = dict(zip(metadata_cols, keys))
            row.update(
                {
                    "interval_start_h": t0,
                    "interval_end_h": t1,
                    "interval_mid_h": (t0 + t1) * 0.5,
                    "interval_auc": interval_auc,
                    "AUC_0_8h_denominator": auc_0_8h,
                    "interval_auc_fraction": interval_auc / auc_0_8h,
                }
            )
            rows.append(row)
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows)
    out["sum_interval_auc_fraction_0_8h"] = out.groupby(
        ["source_file", "replicate_file_id"], observed=False
    )["interval_auc_fraction"].transform("sum")
    return out


def summarize_interval_fraction(interval_curves: pd.DataFrame) -> pd.DataFrame:
    summary = (
        interval_curves.groupby(["formulation_group", "interval_end_h"], observed=False)
        .agg(
            n_files=("replicate_file_id", "nunique"),
            interval_start_h=("interval_start_h", "first"),
            interval_mid_h=("interval_mid_h", "first"),
            mean_interval_auc_fraction=("interval_auc_fraction", "mean"),
            sd_interval_auc_fraction=("interval_auc_fraction", lambda x: x.std(ddof=1)),
            mean_sum_interval_auc_fraction_0_8h=("sum_interval_auc_fraction_0_8h", "mean"),
        )
        .reset_index()
        .sort_values(["formulation_group", "interval_end_h"])
    )
    summary["sd_interval_auc_fraction"] = summary["sd_interval_auc_fraction"].fillna(0.0)
    summary["normalization_formula"] = "interval_auc_fraction = AUC(t_previous,t_current) / AUC_0_8h"
    summary["y_axis_definition"] = "interval contribution to total 0-8 h AUC; interval fractions sum to 1 per file"
    return summary


def plot_interval_fraction_timecourse(
    summary: pd.DataFrame,
    order: list[str],
    outbase: Path,
) -> pd.DataFrame:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(5.9, 2.45))
    plot_data = summary.copy()
    for group in order:
        gdf = plot_data.loc[plot_data["formulation_group"] == group].sort_values("interval_end_h")
        if gdf.empty:
            continue
        color = COOL_GROUP_COLORS.get(group, "#4F6D7A")
        n_files = int(gdf["n_files"].max())
        ax.errorbar(
            gdf["interval_end_h"],
            gdf["mean_interval_auc_fraction"],
            yerr=gdf["sd_interval_auc_fraction"],
            color=color,
            marker="o",
            markersize=2.5,
            markerfacecolor=color,
            markeredgecolor=color,
            linewidth=1.0,
            elinewidth=0.45,
            capsize=1.4,
            capthick=0.45,
            label=f"{group} (n={n_files})",
            zorder=3,
        )

    lower = float((plot_data["mean_interval_auc_fraction"] - plot_data["sd_interval_auc_fraction"]).min())
    upper = float((plot_data["mean_interval_auc_fraction"] + plot_data["sd_interval_auc_fraction"]).max())
    span = upper - lower if upper > lower else max(abs(upper), 0.1)
    ax.set_xlim(-0.15, 8.15)
    ax.set_ylim(min(0.0, lower - 0.04 * span), upper + 0.07 * span)
    ax.set_xticks([0, 0.5, 1, 2, 4, 6, 8])
    ax.set_xticklabels(["0", "0.5", "1", "2", "4", "6", "8"])
    ax.set_xlabel("Interval end time (h)")
    ax.set_ylabel("Interval AUC / AUC$_{0-8h}$")
    ax.legend(loc="best", ncol=2, handlelength=1.5, columnspacing=0.9)
    add_panel_label(ax, "b")
    format_axis(ax)
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return plot_data


def compute_interval_average_fraction_curves(long_df: pd.DataFrame, y_col: str) -> pd.DataFrame:
    """Calculate interval fractions when UV values are interval-average signals."""
    required = [
        "source_file",
        "formulation_group",
        "formulation_label",
        "drug_label",
        "replicate_file_id",
        "measurement_id",
        "time_h",
        "duration_h",
        y_col,
    ]
    require_columns(long_df, required, "Fig. 5b long UV source data")
    df = long_df.copy()
    if "include_for_fig5b" in df.columns:
        df = df.loc[include_mask(df["include_for_fig5b"])].copy()
    df["time_h"] = pd.to_numeric(df["time_h"], errors="coerce")
    df["duration_h"] = pd.to_numeric(df["duration_h"], errors="coerce")
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
    df = df.dropna(subset=["time_h", y_col])
    df = df.loc[(df["time_h"] > 0.0) & (df["time_h"] <= 8.0)].copy()

    metadata_cols = ["source_file", "formulation_group", "formulation_label", "drug_label", "replicate_file_id"]
    interval_means = (
        df.groupby([*metadata_cols, "time_h"], observed=False)
        .agg(
            interval_mean_signal=(y_col, "mean"),
            duration_h=("duration_h", "median"),
            n_technical_measurements=("measurement_id", "nunique"),
        )
        .reset_index()
        .sort_values([*metadata_cols, "time_h"])
    )

    tables = []
    for _, sdf in interval_means.groupby(metadata_cols, observed=False):
        sdf = sdf.sort_values("time_h").copy()
        inferred_duration = sdf["time_h"].diff()
        if not sdf.empty:
            inferred_duration.iloc[0] = sdf["time_h"].iloc[0]
        sdf["duration_h"] = sdf["duration_h"].fillna(inferred_duration)
        sdf["interval_start_h"] = sdf["time_h"] - sdf["duration_h"]
        sdf["interval_end_h"] = sdf["time_h"]
        sdf["interval_auc"] = sdf["interval_mean_signal"] * sdf["duration_h"]
        total_auc = float(sdf["interval_auc"].sum())
        sdf["AUC_0_8h_denominator"] = total_auc
        sdf["interval_auc_fraction"] = np.where(total_auc > 0, sdf["interval_auc"] / total_auc, np.nan)
        sdf["sum_interval_auc_fraction_0_8h"] = sdf["interval_auc_fraction"].sum()
        sdf["y_variable"] = y_col
        sdf["normalization_formula"] = (
            "interval_auc_fraction = interval_mean_absorbance * interval_duration_h / "
            "sum(interval_mean_absorbance * interval_duration_h from 0 to 8 h)"
        )
        sdf["auc_method"] = "interval-average absorbance times duration; no trapezoidal interpolation"
        tables.append(sdf)
    if not tables:
        return pd.DataFrame()
    return pd.concat(tables, ignore_index=True)


def summarize_interval_average_fraction(interval_curves: pd.DataFrame) -> pd.DataFrame:
    summary = (
        interval_curves.dropna(subset=["interval_auc_fraction"])
        .groupby(["formulation_group", "interval_end_h"], observed=False)
        .agg(
            n_files=("replicate_file_id", "nunique"),
            interval_start_h=("interval_start_h", "first"),
            duration_h=("duration_h", "first"),
            mean_interval_auc_fraction=("interval_auc_fraction", "mean"),
            sd_interval_auc_fraction=("interval_auc_fraction", lambda x: x.std(ddof=1)),
            mean_sum_interval_auc_fraction_0_8h=("sum_interval_auc_fraction_0_8h", "mean"),
            y_variable=("y_variable", "first"),
        )
        .reset_index()
        .sort_values(["formulation_group", "interval_end_h"])
    )
    summary["sd_interval_auc_fraction"] = summary["sd_interval_auc_fraction"].fillna(0.0)
    summary["normalization_formula"] = (
        "interval_auc_fraction_i = absorbance_i * duration_i / "
        "sum(absorbance_j * duration_j for intervals from 0 to 8 h)"
    )
    summary["measurement_interpretation"] = (
        "Absorbance at each interval end is treated as the average absorbance over the preceding interval."
    )
    summary["auc_method"] = "interval-average absorbance times duration; no trapezoidal interpolation"
    return summary


def plot_corrected_interval_fraction(
    summary: pd.DataFrame,
    order: list[str],
    outbase: Path,
) -> pd.DataFrame:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(5.9, 2.45))
    plot_data = summary.copy()
    for group in order:
        gdf = plot_data.loc[plot_data["formulation_group"] == group].sort_values("interval_end_h")
        if gdf.empty:
            continue
        color = COOL_GROUP_COLORS.get(group, "#4F6D7A")
        n_files = int(gdf["n_files"].max())
        ax.errorbar(
            gdf["interval_end_h"],
            gdf["mean_interval_auc_fraction"],
            yerr=gdf["sd_interval_auc_fraction"],
            color=color,
            marker="o",
            markersize=2.5,
            markerfacecolor=color,
            markeredgecolor=color,
            linewidth=1.0,
            elinewidth=0.45,
            capsize=1.4,
            capthick=0.45,
            label=f"{group} (n={n_files})",
            zorder=3,
        )

    lower = float((plot_data["mean_interval_auc_fraction"] - plot_data["sd_interval_auc_fraction"]).min())
    upper = float((plot_data["mean_interval_auc_fraction"] + plot_data["sd_interval_auc_fraction"]).max())
    span = upper - lower if upper > lower else max(abs(upper), 0.1)
    ax.set_xlim(-0.15, 8.15)
    ax.set_ylim(min(0.0, lower - 0.04 * span), upper + 0.07 * span)
    ax.set_xticks([0, 0.5, 1, 2, 4, 6, 8])
    ax.set_xticklabels(["0", "0.5", "1", "2", "4", "6", "8"])
    ax.set_xlabel("Interval end time (h)")
    ax.set_ylabel("Interval fraction of AUC$_{0-8h}$")
    ax.legend(loc="best", ncol=2, handlelength=1.5, columnspacing=0.9)
    add_panel_label(ax, "b")
    format_axis(ax)
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return plot_data


def make_interval_fraction_file_qc(interval_curves: pd.DataFrame, tolerance: float = 1e-9) -> pd.DataFrame:
    """Create per-file interval-fraction QC table for the corrected interval interpretation."""
    qc = interval_curves.copy()
    qc = qc.rename(
        columns={
            "interval_end_h": "interval_end_time_h",
            "duration_h": "interval_duration_h",
            "interval_mean_signal": "interval_mean_absorbance",
            "interval_auc": "interval_AUC",
            "AUC_0_8h_denominator": "AUC_0_8h",
            "sum_interval_auc_fraction_0_8h": "sum_of_interval_fractions",
        }
    )
    qc["sum_check_pass"] = (qc["sum_of_interval_fractions"] - 1.0).abs() <= tolerance
    columns = [
        "source_file",
        "replicate_file_id",
        "formulation_group",
        "interval_end_time_h",
        "interval_duration_h",
        "interval_mean_absorbance",
        "interval_AUC",
        "AUC_0_8h",
        "interval_auc_fraction",
        "sum_of_interval_fractions",
        "sum_check_pass",
        "auc_method",
    ]
    return qc[columns].sort_values(["formulation_group", "replicate_file_id", "interval_end_time_h"])


def make_interval_fraction_group_qc(interval_summary: pd.DataFrame, tolerance: float = 1e-9) -> pd.DataFrame:
    """Create group-level interval-fraction QC table for plotted mean curves."""
    group_qc = interval_summary.copy()
    group_qc["sum_of_mean_interval_fractions"] = group_qc.groupby(
        "formulation_group", observed=False
    )["mean_interval_auc_fraction"].transform("sum")
    group_qc["group_sum_check_pass"] = (group_qc["sum_of_mean_interval_fractions"] - 1.0).abs() <= tolerance
    group_qc = group_qc.rename(columns={"interval_end_h": "interval_end_time_h"})
    columns = [
        "formulation_group",
        "interval_end_time_h",
        "interval_start_h",
        "duration_h",
        "n_files",
        "mean_interval_auc_fraction",
        "sd_interval_auc_fraction",
        "sum_of_mean_interval_fractions",
        "group_sum_check_pass",
        "normalization_formula",
        "measurement_interpretation",
        "auc_method",
    ]
    return group_qc[columns].sort_values(["formulation_group", "interval_end_time_h"])


def prepare_ratio_source(file_auc: pd.DataFrame) -> pd.DataFrame:
    required = ["formulation_group", "replicate_file_id", "relative_early_release_mean_curve"]
    require_columns(file_auc, required, "Fig. 5b file-level AUC data")
    ratio = file_auc.copy()
    ratio["relative_early_release_mean_curve"] = pd.to_numeric(
        ratio["relative_early_release_mean_curve"], errors="coerce"
    )
    ratio = ratio.dropna(subset=["relative_early_release_mean_curve"])
    ratio["relative_early_release_definition"] = "AUC_0_4h / AUC_0_8h"
    return ratio


def plot_ratio(ratio: pd.DataFrame, order: list[str], outbase: Path) -> pd.DataFrame:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(4.8, 2.35))
    summary = bar_with_points(
        ax,
        ratio,
        group_col="formulation_group",
        value_col="relative_early_release_mean_curve",
        order=order,
        palette=COOL_GROUP_COLORS,
        y_label="AUC$_{0-4h}$/AUC$_{0-8h}$",
        ylim=(0, 0.6),
    )
    ax.set_xlabel("")
    ax.set_title("Relative early release")
    add_panel_label(ax, "b")
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--long-source",
        default=ROOT / "outputs/source_data/fig5b_uv_long_source.csv",
        type=Path,
        help="Processed long-format Fig. 5b UV source table.",
    )
    parser.add_argument(
        "--file-auc",
        default=ROOT / "outputs/processed/fig5b_auc_file_level.csv",
        type=Path,
        help="File-level averaged AUC table.",
    )
    parser.add_argument("--outdir", default=ROOT / "outputs", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figdir = ensure_dir(args.outdir / "figures")
    processed_dir = ensure_dir(args.outdir / "processed")
    qc_dir = ensure_dir(args.outdir / "qc")

    long_df = pd.read_csv(args.long_source)
    file_auc = pd.read_csv(args.file_auc)
    y_col = choose_y_variable(long_df)
    curves = file_level_timecourse(long_df, y_col)
    summary = summarize_timecourse(curves)
    relative_curves = compute_relative_signal_curves(curves)
    relative_summary = summarize_relative_signal(relative_curves)
    interval_curves = compute_interval_fraction_curves(curves)
    interval_summary = summarize_interval_fraction(interval_curves)
    corrected_interval_curves = compute_interval_average_fraction_curves(long_df, y_col)
    corrected_interval_summary = summarize_interval_average_fraction(corrected_interval_curves)
    corrected_file_qc = make_interval_fraction_file_qc(corrected_interval_curves)
    corrected_group_qc = make_interval_fraction_group_qc(corrected_interval_summary)
    ratio = prepare_ratio_source(file_auc)
    order = present_order(
        pd.concat([summary["formulation_group"], ratio["formulation_group"]], ignore_index=True),
        PREFERRED_ORDER,
    )

    color_table = pd.DataFrame(
        [{"formulation_group": group, "color_hex": COOL_GROUP_COLORS.get(group, "#4F6D7A")} for group in order]
    )
    save_table(curves, processed_dir / "fig5b_timecourse_file_level_curves.csv")
    save_table(summary, processed_dir / "fig5b_timecourse_summary.csv")
    save_table(summary, processed_dir / "fig5b_timecourse_summary_revised.csv")
    save_table(relative_curves, processed_dir / "fig5b_timecourse_relative_file_level.csv")
    save_table(relative_summary, processed_dir / "fig5b_timecourse_relative_summary.csv")
    save_table(relative_summary, processed_dir / "fig5b_timecourse_normalized_main_summary.csv")
    save_table(interval_curves, processed_dir / "fig5b_timecourse_interval_fraction_file_level.csv")
    save_table(interval_summary, processed_dir / "fig5b_timecourse_interval_fraction_summary.csv")
    save_table(corrected_interval_curves, processed_dir / "fig5b_interval_fraction_corrected_file_level.csv")
    save_table(corrected_interval_summary, processed_dir / "fig5b_interval_fraction_corrected_summary.csv")
    save_table(corrected_file_qc, qc_dir / "fig5b_interval_fraction_file_sums.csv")
    save_table(corrected_group_qc, qc_dir / "fig5b_interval_fraction_group_sums.csv")
    save_table(corrected_group_qc, processed_dir / "fig5b_interval_fraction_plotting_table_checked.csv")
    save_table(ratio, processed_dir / "fig5b_relative_early_release_revised_source_data.csv")
    ratio_summary = plot_ratio(
        ratio,
        order=order,
        outbase=figdir / "fig5b_relative_early_release_revised",
    )
    save_table(ratio_summary, processed_dir / "fig5b_relative_early_release_revised_summary.csv")
    save_table(color_table, processed_dir / "fig5b_revised_color_assignments.csv")
    plot_timecourse(summary, order=order, outbase=figdir / "fig5b_timecourse_release")
    plot_timecourse_errorbars(
        summary,
        order=order,
        outbase=figdir / "fig5b_timecourse_release_revised",
    )
    summary_0to8h = plot_timecourse_0to8h_errorbars(
        summary,
        order=order,
        outbase=figdir / "fig5b_timecourse_release_0to8h_revised",
    )
    save_table(summary_0to8h, processed_dir / "fig5b_timecourse_summary_0to8h_revised.csv")
    plot_relative_signal_timecourse(
        relative_summary,
        order=order,
        outbase=figdir / "fig5b_timecourse_relative_revised",
    )
    plot_relative_signal_timecourse(
        relative_summary,
        order=order,
        outbase=figdir / "fig5b_timecourse_normalized_main",
    )
    plot_interval_fraction_timecourse(
        interval_summary,
        order=order,
        outbase=figdir / "fig5b_timecourse_interval_fraction_revised",
    )
    plot_corrected_interval_fraction(
        corrected_interval_summary,
        order=order,
        outbase=figdir / "fig5b_interval_fraction_corrected",
    )
    plot_corrected_interval_fraction(
        corrected_interval_summary,
        order=order,
        outbase=figdir / "fig5b_interval_fraction_checked",
    )

    counts = curves.groupby("formulation_group", observed=False)["replicate_file_id"].nunique().to_dict()
    baseline_count = int(curves.loc[curves["baseline_added_for_plot"], "replicate_file_id"].nunique())
    print(f"y_variable={y_col}")
    print("technical_replicate_handling=mean of measurement_id values within each source_file/replicate_file_id/time_h")
    print("group_file_counts=" + "; ".join(f"{group}: {counts.get(group, 0)}" for group in order))
    print("baseline_added_file_count=" + str(baseline_count))
    print("colors=" + "; ".join(f"{row.formulation_group}: {row.color_hex}" for row in color_table.itertuples()))
    print("timecourse_summary=outputs/processed/fig5b_timecourse_summary.csv")
    print("timecourse_summary_revised=outputs/processed/fig5b_timecourse_summary_revised.csv")
    print("ratio_source=outputs/processed/fig5b_relative_early_release_revised_source_data.csv")
    print("relative_timecourse_summary=outputs/processed/fig5b_timecourse_relative_summary.csv")
    print("normalized_main_summary=outputs/processed/fig5b_timecourse_normalized_main_summary.csv")
    print("interval_fraction_summary=outputs/processed/fig5b_timecourse_interval_fraction_summary.csv")
    print("corrected_interval_fraction_summary=outputs/processed/fig5b_interval_fraction_corrected_summary.csv")
    print("corrected_interval_fraction_file_sums=outputs/qc/fig5b_interval_fraction_file_sums.csv")
    print("corrected_interval_fraction_group_sums=outputs/qc/fig5b_interval_fraction_group_sums.csv")
    print("corrected_interval_fraction_plotting_table_checked=outputs/processed/fig5b_interval_fraction_plotting_table_checked.csv")
    print("timecourse_figure=outputs/figures/fig5b_timecourse_release.[pdf|svg|png]")
    print("timecourse_figure_revised=outputs/figures/fig5b_timecourse_release_revised.[pdf|svg|png]")
    print("timecourse_figure_0to8h_revised=outputs/figures/fig5b_timecourse_release_0to8h_revised.[pdf|svg|png]")
    print("timecourse_summary_0to8h_revised=outputs/processed/fig5b_timecourse_summary_0to8h_revised.csv")
    print("relative_timecourse_figure=outputs/figures/fig5b_timecourse_relative_revised.[pdf|svg|png]")
    print("normalized_main_figure=outputs/figures/fig5b_timecourse_normalized_main.[pdf|svg|png]")
    print("interval_fraction_figure=outputs/figures/fig5b_timecourse_interval_fraction_revised.[pdf|svg|png]")
    print("corrected_interval_fraction_figure=outputs/figures/fig5b_interval_fraction_corrected.[pdf|svg|png]")
    print("checked_interval_fraction_figure=outputs/figures/fig5b_interval_fraction_checked.[pdf|svg|png]")
    print("ratio_figure=outputs/figures/fig5b_relative_early_release_revised.[pdf|svg|png]")


if __name__ == "__main__":
    main()
