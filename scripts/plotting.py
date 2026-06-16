"""Reusable matplotlib plotting functions for the manuscript figures."""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .stats import group_summary
from .style import color_for_group, format_axis


def present_order(values: pd.Series, preferred_order: list[str] | None = None) -> list[str]:
    preferred_order = preferred_order or []
    present = [v for v in preferred_order if v in set(values.dropna())]
    extras = sorted([v for v in values.dropna().unique() if v not in present])
    return present + extras


def bar_with_points(
    ax: plt.Axes,
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    order: list[str],
    palette: dict[str, str],
    y_label: str,
    x_label: str = "",
    ylim: tuple[float, float] | None = None,
    seed: int = 13,
) -> pd.DataFrame:
    """Plot mean +/- SD bars with individual dots and return summary data."""
    summary = group_summary(df, group_col, value_col, order=order)
    x = np.arange(len(order))
    means = []
    sds = []
    colors = []
    for idx, group in enumerate(order):
        row = summary.loc[summary[group_col] == group]
        means.append(float(row["mean"].iloc[0]) if not row.empty else np.nan)
        sd = float(row["sd"].iloc[0]) if not row.empty else np.nan
        sds.append(0.0 if np.isnan(sd) else sd)
        colors.append(color_for_group(group, palette, idx))
    ax.bar(
        x,
        means,
        yerr=sds,
        width=0.64,
        color=colors,
        edgecolor="black",
        linewidth=0.5,
        error_kw={"elinewidth": 0.6, "capsize": 2, "capthick": 0.6},
        zorder=1,
    )
    rng = np.random.default_rng(seed)
    for idx, group in enumerate(order):
        values = pd.to_numeric(df.loc[df[group_col] == group, value_col], errors="coerce").dropna()
        jitter = rng.uniform(-0.12, 0.12, size=len(values))
        ax.scatter(
            np.full(len(values), idx) + jitter,
            values,
            s=10,
            facecolor="white",
            edgecolor="black",
            linewidth=0.45,
            zorder=3,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(order, rotation=35, ha="right")
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    if ylim:
        ax.set_ylim(*ylim)
    format_axis(ax)
    return summary


def box_with_points(
    ax: plt.Axes,
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    order: list[str],
    palette: dict[str, str],
    y_label: str,
    x_label: str = "",
    ylim: tuple[float, float] | None = None,
    seed: int = 29,
) -> pd.DataFrame:
    """Plot boxplots with individual dots and return summary data."""
    data = [
        pd.to_numeric(df.loc[df[group_col] == group, value_col], errors="coerce").dropna().to_numpy()
        for group in order
    ]
    positions = np.arange(len(order))
    box = ax.boxplot(
        data,
        positions=positions,
        widths=0.56,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "black", "linewidth": 0.7},
        boxprops={"linewidth": 0.6},
        whiskerprops={"linewidth": 0.6},
        capprops={"linewidth": 0.6},
    )
    for idx, patch in enumerate(box["boxes"]):
        patch.set_facecolor(color_for_group(order[idx], palette, idx))
        patch.set_alpha(0.45)
        patch.set_edgecolor("black")
    rng = np.random.default_rng(seed)
    for idx, values in enumerate(data):
        jitter = rng.uniform(-0.12, 0.12, size=len(values))
        ax.scatter(
            np.full(len(values), idx) + jitter,
            values,
            s=10,
            facecolor="white",
            edgecolor="black",
            linewidth=0.45,
            zorder=3,
        )
    ax.set_xticks(positions)
    ax.set_xticklabels(order, rotation=35, ha="right")
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    if ylim:
        ax.set_ylim(*ylim)
    format_axis(ax)
    return group_summary(df, group_col, value_col, order=order)


def timecourse_mean_sd(
    ax: plt.Axes,
    df: pd.DataFrame,
    group_col: str,
    time_col: str,
    value_col: str,
    subject_col: str,
    order: list[str],
    palette: dict[str, str],
    y_label: str,
    x_label: str,
    show_individual: bool = True,
) -> pd.DataFrame:
    """Plot mean +/- SD time courses, optionally with light replicate traces."""
    summary_rows = []
    for idx, group in enumerate(order):
        gdf = df.loc[df[group_col] == group].copy()
        if gdf.empty:
            continue
        color = color_for_group(group, palette, idx)
        if show_individual:
            for _, sdf in gdf.groupby(subject_col):
                sdf = sdf.sort_values(time_col)
                ax.plot(
                    sdf[time_col],
                    sdf[value_col],
                    color=color,
                    alpha=0.22,
                    linewidth=0.55,
                    zorder=1,
                )
        summary = (
            gdf.groupby(time_col, observed=False)[value_col]
            .agg(n="count", mean="mean", sd=lambda x: x.std(ddof=1))
            .reset_index()
            .sort_values(time_col)
        )
        summary[group_col] = group
        summary_rows.append(summary)
        x = summary[time_col].to_numpy(float)
        mean = summary["mean"].to_numpy(float)
        sd = summary["sd"].fillna(0).to_numpy(float)
        ax.plot(
            x,
            mean,
            color=color,
            marker="o",
            markersize=3,
            linewidth=1.1,
            label=group,
            zorder=3,
        )
        ax.fill_between(x, mean - sd, mean + sd, color=color, alpha=0.16, linewidth=0, zorder=2)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(loc="best")
    format_axis(ax)
    if summary_rows:
        return pd.concat(summary_rows, ignore_index=True)
    return pd.DataFrame(columns=[group_col, time_col, "n", "mean", "sd"])

