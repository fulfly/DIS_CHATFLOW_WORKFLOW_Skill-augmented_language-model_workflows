#!/usr/bin/env python
"""Generate Fig. 4 all-condition normalized projected-area time-course plot."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ncfigs.io import ensure_dir, require_columns, save_source_copy, save_table
from ncfigs.style import add_panel_label, format_axis, save_figure, set_nature_style


FORMULATION_MAP = {
    "01": "01 high viscosity",
    "02": "02 low viscosity",
    "03": "03 standard viscosity",
}

FORMULATION_COLORS = {
    "01 high viscosity": "#0072B2",
    "02 low viscosity": "#009E73",
    "03 standard viscosity": "#5B4BA3",
}

PH_MARKERS = {
    "pH 1.2": "o",
    "pH 4.5": "^",
    "pH 6.8": "s",
}

FORMULATION_ORDER = ["01 high viscosity", "02 low viscosity", "03 standard viscosity"]
PH_ORDER = ["pH 1.2", "pH 4.5", "pH 6.8"]


def parse_source_video(source_video: str) -> tuple[str, str, str]:
    code_match = re.match(r"^(\d{2})-", str(source_video))
    ph_match = re.search(r"pH\s*([0-9]+(?:\.[0-9]+)?)", str(source_video), flags=re.IGNORECASE)
    formulation_code = code_match.group(1) if code_match else "unmapped"
    formulation_group = FORMULATION_MAP.get(formulation_code, f"{formulation_code} unmapped")
    pH_condition = f"pH {ph_match.group(1)}" if ph_match else "pH unmapped"
    return formulation_code, formulation_group, pH_condition


def prepare_plotting_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = [
        "source_video",
        "real_time_h",
        "normalized_projected_area",
        "projected_area_px",
        "mask_area_valid",
    ]
    require_columns(df, required, "Fig. 4 projected-area combined table")
    out = df.copy()
    parsed = out["source_video"].map(parse_source_video)
    out["formulation_code"] = parsed.map(lambda item: item[0])
    out["formulation_group_fig4"] = parsed.map(lambda item: item[1])
    out["pH_condition_fig4"] = parsed.map(lambda item: item[2])
    out["trace_id"] = out["formulation_code"] + "_" + out["pH_condition_fig4"].str.replace(" ", "", regex=False)
    out["real_time_h"] = pd.to_numeric(out["real_time_h"], errors="coerce")
    out["normalized_projected_area"] = pd.to_numeric(out["normalized_projected_area"], errors="coerce")
    out = out.dropna(subset=["real_time_h", "normalized_projected_area"])

    summary = (
        out.groupby(["formulation_group_fig4", "pH_condition_fig4", "real_time_h"], observed=False)
        .agg(
            n_videos=("source_video", "nunique"),
            mean_normalized_projected_area=("normalized_projected_area", "mean"),
            sd_normalized_projected_area=("normalized_projected_area", lambda x: x.std(ddof=1)),
            source_videos=("source_video", lambda x: "|".join(sorted(set(map(str, x))))),
        )
        .reset_index()
        .sort_values(["formulation_group_fig4", "pH_condition_fig4", "real_time_h"])
    )
    summary["sd_normalized_projected_area"] = summary["sd_normalized_projected_area"].fillna(0.0)

    counts = (
        out[["source_video", "formulation_code", "formulation_group_fig4", "pH_condition_fig4"]]
        .drop_duplicates()
        .groupby(["formulation_code", "formulation_group_fig4", "pH_condition_fig4"], observed=False)
        .agg(n_videos=("source_video", "nunique"), source_videos=("source_video", lambda x: "|".join(sorted(x))))
        .reset_index()
        .sort_values(["formulation_code", "pH_condition_fig4"])
    )
    counts["replicate_status"] = np.where(
        counts["n_videos"] > 1,
        "mean +/- SD available",
        "single video trace; SD not estimable",
    )
    return out, summary, counts


def choose_ymax(values: pd.Series) -> float:
    max_value = float(pd.to_numeric(values, errors="coerce").max())
    return float(np.ceil((max_value * 1.08) * 2.0) / 2.0)


def plot_all9(summary: pd.DataFrame, ymax: float, outbase: Path) -> None:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(6.2, 2.85))

    for formulation in FORMULATION_ORDER:
        for pH_condition in PH_ORDER:
            trace = summary.loc[
                (summary["formulation_group_fig4"] == formulation)
                & (summary["pH_condition_fig4"] == pH_condition)
            ].sort_values("real_time_h")
            if trace.empty:
                continue
            color = FORMULATION_COLORS[formulation]
            marker = PH_MARKERS[pH_condition]
            n_videos = int(trace["n_videos"].max())
            label = f"{formulation}, {pH_condition} (n={n_videos})"
            ax.plot(
                trace["real_time_h"],
                trace["mean_normalized_projected_area"],
                color=color,
                marker=marker,
                markevery=12,
                markersize=3.0,
                markerfacecolor="white",
                markeredgecolor=color,
                markeredgewidth=0.65,
                linewidth=1.05,
                label=label,
                zorder=3,
            )
            if n_videos > 1:
                ax.fill_between(
                    trace["real_time_h"],
                    trace["mean_normalized_projected_area"] - trace["sd_normalized_projected_area"],
                    trace["mean_normalized_projected_area"] + trace["sd_normalized_projected_area"],
                    color=color,
                    alpha=0.12,
                    linewidth=0,
                    zorder=1,
                )

    ax.set_xlim(0, 24)
    ax.set_ylim(0, ymax)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Normalized projected area\n(area$_t$/area$_0$)")
    add_panel_label(ax, "a")
    format_axis(ax)

    color_handles = [
        Line2D([0], [0], color=FORMULATION_COLORS[group], lw=1.4, label=group)
        for group in FORMULATION_ORDER
    ]
    marker_handles = [
        Line2D(
            [0],
            [0],
            color="black",
            marker=marker,
            lw=0,
            markersize=3.8,
            markerfacecolor="white",
            markeredgewidth=0.7,
            label=condition,
        )
        for condition, marker in PH_MARKERS.items()
    ]
    first_legend = ax.legend(
        handles=color_handles,
        title="Formulation",
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        borderaxespad=0,
        frameon=False,
    )
    ax.add_artist(first_legend)
    ax.legend(
        handles=marker_handles,
        title="pH",
        loc="upper left",
        bbox_to_anchor=(1.01, 0.46),
        borderaxespad=0,
        frameon=False,
    )
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)


def smooth_and_downsample(
    processed: pd.DataFrame,
    interval_h: float = 0.5,
    smoothing_window_h: float = 0.5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create a cleaner plotting table without modifying extracted source data."""
    rows = []
    method_rows = []
    window_points_by_trace = {}
    for (formulation, pH_condition, source_video), trace in processed.groupby(
        ["formulation_group_fig4", "pH_condition_fig4", "source_video"], observed=False
    ):
        trace = trace.sort_values("real_time_h").copy()
        median_dt = float(trace["real_time_h"].diff().median())
        window_points = max(1, int(round(smoothing_window_h / median_dt))) if median_dt > 0 else 1
        if window_points % 2 == 0:
            window_points += 1
        window_points_by_trace[source_video] = window_points
        trace["smoothed_normalized_projected_area"] = (
            trace["normalized_projected_area"]
            .rolling(window=window_points, center=True, min_periods=1)
            .mean()
        )
        target_times = np.arange(0, 24.0001, interval_h)
        source_times = trace["real_time_h"].to_numpy(float)
        source_values = trace["smoothed_normalized_projected_area"].to_numpy(float)
        interpolated = np.interp(target_times, source_times, source_values)
        for time_h, value in zip(target_times, interpolated):
            rows.append(
                {
                    "source_video": source_video,
                    "formulation_group_fig4": formulation,
                    "pH_condition_fig4": pH_condition,
                    "real_time_h": time_h,
                    "smoothed_normalized_projected_area": value,
                    "raw_points_in_trace": len(trace),
                    "downsample_interval_h": interval_h,
                    "smoothing_window_h": smoothing_window_h,
                    "smoothing_window_points": window_points,
                    "smoothing_method": "centered moving average on extracted normalized projected area",
                    "downsampling_method": "linear interpolation to regular 0.5 h grid after smoothing",
                }
            )
    smoothed = pd.DataFrame(rows)
    summary = (
        smoothed.groupby(["formulation_group_fig4", "pH_condition_fig4", "real_time_h"], observed=False)
        .agg(
            n_videos=("source_video", "nunique"),
            mean_smoothed_normalized_projected_area=("smoothed_normalized_projected_area", "mean"),
            sd_smoothed_normalized_projected_area=("smoothed_normalized_projected_area", lambda x: x.std(ddof=1)),
            source_videos=("source_video", lambda x: "|".join(sorted(set(map(str, x))))),
            raw_points_in_trace=("raw_points_in_trace", "first"),
            downsample_interval_h=("downsample_interval_h", "first"),
            smoothing_window_h=("smoothing_window_h", "first"),
            smoothing_window_points=("smoothing_window_points", "first"),
            smoothing_method=("smoothing_method", "first"),
            downsampling_method=("downsampling_method", "first"),
        )
        .reset_index()
        .sort_values(["formulation_group_fig4", "pH_condition_fig4", "real_time_h"])
    )
    summary["sd_smoothed_normalized_projected_area"] = summary["sd_smoothed_normalized_projected_area"].fillna(0.0)
    method = pd.DataFrame(
        [
            {
                "source_data_changed": False,
                "raw_points_per_trace": int(processed.groupby("source_video")["real_time_h"].nunique().median()),
                "plotted_points_per_trace": int(smoothed.groupby("source_video")["real_time_h"].nunique().median()),
                "raw_points_per_hour": 6.0,
                "plotted_points_per_hour": 1.0 / interval_h,
                "downsample_interval_h": interval_h,
                "smoothing_applied": True,
                "smoothing_method": "centered moving average",
                "smoothing_window_h": smoothing_window_h,
                "typical_smoothing_window_points": int(np.median(list(window_points_by_trace.values()))),
                "downsampling_method": "linear interpolation to regular grid after smoothing",
            }
        ]
    )
    return summary, method


def plot_all9_smoothed(summary: pd.DataFrame, ymax: float, outbase: Path) -> None:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(6.2, 2.85))

    for formulation in FORMULATION_ORDER:
        for pH_condition in PH_ORDER:
            trace = summary.loc[
                (summary["formulation_group_fig4"] == formulation)
                & (summary["pH_condition_fig4"] == pH_condition)
            ].sort_values("real_time_h")
            if trace.empty:
                continue
            color = FORMULATION_COLORS[formulation]
            marker = PH_MARKERS[pH_condition]
            n_videos = int(trace["n_videos"].max())
            ax.plot(
                trace["real_time_h"],
                trace["mean_smoothed_normalized_projected_area"],
                color=color,
                marker=marker,
                markevery=4,
                markersize=3.0,
                markerfacecolor="white",
                markeredgecolor=color,
                markeredgewidth=0.65,
                linewidth=1.15,
                zorder=3,
            )
            if n_videos > 1:
                ax.fill_between(
                    trace["real_time_h"],
                    trace["mean_smoothed_normalized_projected_area"] - trace["sd_smoothed_normalized_projected_area"],
                    trace["mean_smoothed_normalized_projected_area"] + trace["sd_smoothed_normalized_projected_area"],
                    color=color,
                    alpha=0.12,
                    linewidth=0,
                    zorder=1,
                )

    ax.set_xlim(0, 24)
    ax.set_ylim(0, ymax)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Normalized projected area\n(area$_t$/area$_0$)")
    add_panel_label(ax, "a")
    format_axis(ax)

    color_handles = [
        Line2D([0], [0], color=FORMULATION_COLORS[group], lw=1.4, label=group)
        for group in FORMULATION_ORDER
    ]
    marker_handles = [
        Line2D(
            [0],
            [0],
            color="black",
            marker=marker,
            lw=0,
            markersize=3.8,
            markerfacecolor="white",
            markeredgewidth=0.7,
            label=condition,
        )
        for condition, marker in PH_MARKERS.items()
    ]
    first_legend = ax.legend(
        handles=color_handles,
        title="Formulation",
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        borderaxespad=0,
        frameon=False,
    )
    ax.add_artist(first_legend)
    ax.legend(
        handles=marker_handles,
        title="pH",
        loc="upper left",
        bbox_to_anchor=(1.01, 0.46),
        borderaxespad=0,
        frameon=False,
    )
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)


def plot_all9_smoothed_v2(summary: pd.DataFrame, ymax: float, outbase: Path) -> None:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(6.2, 2.85))

    for formulation in FORMULATION_ORDER:
        for pH_condition in PH_ORDER:
            trace = summary.loc[
                (summary["formulation_group_fig4"] == formulation)
                & (summary["pH_condition_fig4"] == pH_condition)
            ].sort_values("real_time_h")
            if trace.empty:
                continue
            color = FORMULATION_COLORS[formulation]
            marker = PH_MARKERS[pH_condition]
            n_videos = int(trace["n_videos"].max())
            ax.plot(
                trace["real_time_h"],
                trace["mean_smoothed_normalized_projected_area"],
                color=color,
                marker=marker,
                markevery=2,
                markersize=3.0,
                markerfacecolor="white",
                markeredgecolor=color,
                markeredgewidth=0.65,
                linewidth=1.18,
                zorder=3,
            )
            if n_videos > 1:
                ax.fill_between(
                    trace["real_time_h"],
                    trace["mean_smoothed_normalized_projected_area"] - trace["sd_smoothed_normalized_projected_area"],
                    trace["mean_smoothed_normalized_projected_area"] + trace["sd_smoothed_normalized_projected_area"],
                    color=color,
                    alpha=0.12,
                    linewidth=0,
                    zorder=1,
                )

    ax.set_xlim(0, 24.8)
    ax.set_ylim(0, ymax)
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Normalized projected area\n(area$_t$/area$_0$)")
    add_panel_label(ax, "a")
    format_axis(ax)

    color_handles = [
        Line2D([0], [0], color=FORMULATION_COLORS[group], lw=1.4, label=group)
        for group in FORMULATION_ORDER
    ]
    marker_handles = [
        Line2D(
            [0],
            [0],
            color="black",
            marker=marker,
            lw=0,
            markersize=3.8,
            markerfacecolor="white",
            markeredgewidth=0.7,
            label=condition,
        )
        for condition, marker in PH_MARKERS.items()
    ]
    first_legend = ax.legend(
        handles=color_handles,
        title="Formulation",
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        borderaxespad=0,
        frameon=False,
    )
    ax.add_artist(first_legend)
    ax.legend(
        handles=marker_handles,
        title="pH",
        loc="upper left",
        bbox_to_anchor=(1.01, 0.46),
        borderaxespad=0,
        frameon=False,
    )
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)


def marker_subset(trace: pd.DataFrame, interval_h: float = 2.0) -> pd.DataFrame:
    """Return the nearest available rows to sparse marker target times."""
    if trace.empty:
        return trace
    target_times = np.arange(0, 24.0001, interval_h)
    chosen_indices = []
    times = trace["real_time_h"].to_numpy(float)
    for target in target_times:
        chosen_indices.append(trace.index[int(np.argmin(np.abs(times - target)))])
    return trace.loc[sorted(set(chosen_indices))].sort_values("real_time_h")


def plot_all9_markerlight(
    summary: pd.DataFrame,
    ymax: float,
    outbase: Path,
    marker_interval_h: float = 2.0,
) -> pd.DataFrame:
    """Plot smoothed Fig. 4 curves with sparse pH markers overlaid."""
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(6.2, 2.85))
    marker_rows = []

    for formulation in FORMULATION_ORDER:
        for pH_condition in PH_ORDER:
            trace = summary.loc[
                (summary["formulation_group_fig4"] == formulation)
                & (summary["pH_condition_fig4"] == pH_condition)
            ].sort_values("real_time_h")
            if trace.empty:
                continue
            color = FORMULATION_COLORS[formulation]
            marker = PH_MARKERS[pH_condition]
            n_videos = int(trace["n_videos"].max())
            ax.plot(
                trace["real_time_h"],
                trace["mean_smoothed_normalized_projected_area"],
                color=color,
                linewidth=1.18,
                zorder=3,
            )
            markers = marker_subset(trace, interval_h=marker_interval_h)
            ax.plot(
                markers["real_time_h"],
                markers["mean_smoothed_normalized_projected_area"],
                linestyle="none",
                color=color,
                marker=marker,
                markersize=3.0,
                markerfacecolor="white",
                markeredgecolor=color,
                markeredgewidth=0.65,
                zorder=4,
            )
            for row in markers.itertuples(index=False):
                marker_rows.append(
                    {
                        "formulation_group_fig4": formulation,
                        "pH_condition_fig4": pH_condition,
                        "source_videos": row.source_videos,
                        "n_videos": n_videos,
                        "marker_time_h": row.real_time_h,
                        "marker_y": row.mean_smoothed_normalized_projected_area,
                        "marker_interval_h": marker_interval_h,
                    }
                )
            if n_videos > 1:
                ax.fill_between(
                    trace["real_time_h"],
                    trace["mean_smoothed_normalized_projected_area"] - trace["sd_smoothed_normalized_projected_area"],
                    trace["mean_smoothed_normalized_projected_area"] + trace["sd_smoothed_normalized_projected_area"],
                    color=color,
                    alpha=0.12,
                    linewidth=0,
                    zorder=1,
                )

    ax.set_xlim(0, 24.8)
    ax.set_ylim(0, ymax)
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Normalized projected area\n(area$_t$/area$_0$)")
    add_panel_label(ax, "a")
    format_axis(ax)

    color_handles = [
        Line2D([0], [0], color=FORMULATION_COLORS[group], lw=1.4, label=group)
        for group in FORMULATION_ORDER
    ]
    marker_handles = [
        Line2D(
            [0],
            [0],
            color="black",
            marker=marker,
            lw=0,
            markersize=3.8,
            markerfacecolor="white",
            markeredgewidth=0.7,
            label=condition,
        )
        for condition, marker in PH_MARKERS.items()
    ]
    first_legend = ax.legend(
        handles=color_handles,
        title="Formulation",
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        borderaxespad=0,
        frameon=False,
    )
    ax.add_artist(first_legend)
    ax.legend(
        handles=marker_handles,
        title="pH",
        loc="upper left",
        bbox_to_anchor=(1.01, 0.46),
        borderaxespad=0,
        frameon=False,
    )
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return pd.DataFrame(marker_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default=Path(r"D:\data\vedio\空白\processed_area_csv\fig4_projected_area_combined.csv"),
        type=Path,
    )
    parser.add_argument("--outdir", default=ROOT / "outputs", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figdir = ensure_dir(args.outdir / "figures")
    processed_dir = ensure_dir(args.outdir / "processed")
    source_dir = ensure_dir(args.outdir / "source_data")
    stats_dir = ensure_dir(args.outdir / "stats")
    qc_dir = ensure_dir(args.outdir / "qc")

    raw = pd.read_csv(args.input)
    save_source_copy(raw, source_dir / "fig4_projected_area_combined_source.csv")
    processed, summary, counts = prepare_plotting_data(raw)
    ymax = choose_ymax(summary["mean_normalized_projected_area"])
    smoothed_summary, smoothing_method = smooth_and_downsample(
        processed,
        interval_h=0.5,
        smoothing_window_h=0.5,
    )
    smoothed_summary_v2, smoothing_method_v2 = smooth_and_downsample(
        processed,
        interval_h=1.0 / 3.0,
        smoothing_window_h=0.75,
    )
    smoothed_ymax = choose_ymax(smoothed_summary["mean_smoothed_normalized_projected_area"])
    smoothed_ymax_v2 = choose_ymax(smoothed_summary_v2["mean_smoothed_normalized_projected_area"])
    summary["y_axis_min"] = 0.0
    summary["y_axis_max"] = ymax
    smoothed_summary["y_axis_min"] = 0.0
    smoothed_summary["y_axis_max"] = smoothed_ymax
    smoothed_summary_v2["y_axis_min"] = 0.0
    smoothed_summary_v2["y_axis_max"] = smoothed_ymax_v2
    smoothed_summary_v2["x_axis_min"] = 0.0
    smoothed_summary_v2["x_axis_max"] = 24.8
    smoothed_summary_v2["x_axis_ticks"] = "0,4,8,12,16,20,24"
    marker_interval_h = 2.0
    marker_target_times = ",".join(str(int(t)) for t in np.arange(0, 24.0001, marker_interval_h))
    smoothed_summary_markerlight = smoothed_summary_v2.copy()
    smoothed_summary_markerlight["marker_interval_h"] = marker_interval_h
    smoothed_summary_markerlight["marker_target_times_h"] = marker_target_times
    smoothed_summary_markerlight["marker_display"] = (
        "line drawn from all smoothed v2 points; markers overlaid at nearest 2 h positions"
    )

    color_table = pd.DataFrame(
        [{"formulation_group": group, "color_hex": FORMULATION_COLORS[group]} for group in FORMULATION_ORDER]
    )
    marker_table = pd.DataFrame(
        [{"pH_condition": condition, "marker": marker} for condition, marker in PH_MARKERS.items()]
    )
    stats_note = counts.copy()
    stats_note["statistical_test"] = "not run"
    stats_note["reason"] = "one video per formulation x pH condition; SD/statistical comparison not estimable per condition"

    save_table(processed, processed_dir / "fig4_projected_area_timecourse_all9_processed.csv")
    save_table(summary, processed_dir / "fig4_projected_area_timecourse_all9_plotting_table.csv")
    save_table(counts, qc_dir / "fig4_projected_area_timecourse_all9_qc.csv")
    save_table(stats_note, stats_dir / "fig4_projected_area_timecourse_all9_stats.csv")
    save_table(color_table, processed_dir / "fig4_projected_area_timecourse_all9_colors.csv")
    save_table(marker_table, processed_dir / "fig4_projected_area_timecourse_all9_markers.csv")
    save_table(smoothed_summary, processed_dir / "fig4_projected_area_timecourse_all9_smoothed_plotting_table.csv")
    save_table(smoothing_method, qc_dir / "fig4_projected_area_timecourse_all9_smoothed_method.csv")
    save_table(smoothed_summary_v2, processed_dir / "fig4_projected_area_timecourse_all9_smoothed_v2_plotting_table.csv")
    smoothing_method_v2["x_axis_ticks"] = "0,4,8,12,16,20,24"
    smoothing_method_v2["x_axis_max"] = 24.8
    smoothing_method_v2["right_side_padding_h"] = 0.8
    save_table(smoothing_method_v2, qc_dir / "fig4_projected_area_timecourse_all9_smoothed_v2_method.csv")
    save_table(
        smoothed_summary_markerlight,
        processed_dir / "fig4_projected_area_timecourse_all9_markerlight_plotting_table.csv",
    )
    save_table(
        smoothed_summary_markerlight,
        processed_dir / "fig4_projected_area_timecourse_all9_corrected_mapping_plotting_table.csv",
    )
    save_table(
        color_table,
        processed_dir / "fig4_projected_area_timecourse_all9_corrected_mapping_colors.csv",
    )

    plot_all9(summary, ymax=ymax, outbase=figdir / "fig4_projected_area_timecourse_all9")
    plot_all9_smoothed(
        smoothed_summary,
        ymax=smoothed_ymax,
        outbase=figdir / "fig4_projected_area_timecourse_all9_smoothed",
    )
    plot_all9_smoothed_v2(
        smoothed_summary_v2,
        ymax=smoothed_ymax_v2,
        outbase=figdir / "fig4_projected_area_timecourse_all9_smoothed_v2",
    )
    marker_positions = plot_all9_markerlight(
        smoothed_summary_v2,
        ymax=smoothed_ymax_v2,
        outbase=figdir / "fig4_projected_area_timecourse_all9_markerlight",
        marker_interval_h=marker_interval_h,
    )
    corrected_marker_positions = plot_all9_markerlight(
        smoothed_summary_v2,
        ymax=smoothed_ymax_v2,
        outbase=figdir / "fig4_projected_area_timecourse_all9_corrected_mapping",
        marker_interval_h=marker_interval_h,
    )
    marker_counts = (
        marker_positions.groupby(["formulation_group_fig4", "pH_condition_fig4"], observed=False)
        .agg(n_marker_positions=("marker_time_h", "nunique"))
        .reset_index()
    )
    markerlight_method = smoothing_method_v2.copy()
    markerlight_method["marker_interval_h"] = marker_interval_h
    markerlight_method["marker_target_times_h"] = marker_target_times
    markerlight_method["marker_positions_per_curve"] = int(marker_counts["n_marker_positions"].median())
    markerlight_method["underlying_curve_data_changed_from_smoothed_v2"] = False
    markerlight_method["marker_display_method"] = (
        "continuous line uses all smoothed v2 plotting points; pH marker symbols are drawn only "
        "at nearest available 2 h target times"
    )
    save_table(marker_positions, processed_dir / "fig4_projected_area_timecourse_all9_markerlight_marker_positions.csv")
    save_table(
        corrected_marker_positions,
        processed_dir / "fig4_projected_area_timecourse_all9_corrected_mapping_marker_positions.csv",
    )
    save_table(markerlight_method, qc_dir / "fig4_projected_area_timecourse_all9_markerlight_method.csv")

    print(f"input_csv={args.input}")
    print("formulation_mapping=01 high viscosity; 02 low viscosity; 03 standard viscosity")
    print("pH_mapping=pH1.2 -> pH 1.2; pH4.5 -> pH 4.5; pH6.8 -> pH 6.8")
    print("replicate_counts=" + "; ".join(f"{row.formulation_group_fig4} {row.pH_condition_fig4}: n={row.n_videos}" for row in counts.itertuples()))
    print("colors=" + "; ".join(f"{row.formulation_group}: {row.color_hex}" for row in color_table.itertuples()))
    print("markers=pH 1.2: circle; pH 4.5: triangle; pH 6.8: square")
    print(f"y_axis_range=0,{ymax}")
    print("figure=outputs/figures/fig4_projected_area_timecourse_all9.[pdf|svg|png]")
    print("smoothed_figure=outputs/figures/fig4_projected_area_timecourse_all9_smoothed.[pdf|svg|png]")
    print("smoothed_v2_figure=outputs/figures/fig4_projected_area_timecourse_all9_smoothed_v2.[pdf|svg|png]")
    print("markerlight_figure=outputs/figures/fig4_projected_area_timecourse_all9_markerlight.[pdf|svg|png]")
    print("corrected_mapping_figure=outputs/figures/fig4_projected_area_timecourse_all9_corrected_mapping.[pdf|svg|png]")
    print("plotting_table=outputs/processed/fig4_projected_area_timecourse_all9_plotting_table.csv")
    print("smoothed_plotting_table=outputs/processed/fig4_projected_area_timecourse_all9_smoothed_plotting_table.csv")
    print("smoothed_v2_plotting_table=outputs/processed/fig4_projected_area_timecourse_all9_smoothed_v2_plotting_table.csv")
    print("markerlight_plotting_table=outputs/processed/fig4_projected_area_timecourse_all9_markerlight_plotting_table.csv")
    print("corrected_mapping_plotting_table=outputs/processed/fig4_projected_area_timecourse_all9_corrected_mapping_plotting_table.csv")
    print("markerlight_marker_positions=outputs/processed/fig4_projected_area_timecourse_all9_markerlight_marker_positions.csv")
    print("corrected_mapping_marker_positions=outputs/processed/fig4_projected_area_timecourse_all9_corrected_mapping_marker_positions.csv")
    print("smoothing_method=outputs/qc/fig4_projected_area_timecourse_all9_smoothed_method.csv")
    print("smoothing_v2_method=outputs/qc/fig4_projected_area_timecourse_all9_smoothed_v2_method.csv")
    print("markerlight_method=outputs/qc/fig4_projected_area_timecourse_all9_markerlight_method.csv")
    print(f"markerlight_marker_interval_h={marker_interval_h}")
    print(f"markerlight_marker_positions_per_curve={int(marker_counts['n_marker_positions'].median())}")
    print("source=outputs/source_data/fig4_projected_area_combined_source.csv")
    print("qc=outputs/qc/fig4_projected_area_timecourse_all9_qc.csv")
    print("stats=outputs/stats/fig4_projected_area_timecourse_all9_stats.csv")


if __name__ == "__main__":
    main()
