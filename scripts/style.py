"""Nature Communications-style plotting defaults and palettes."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


# Okabe-Ito-inspired, color-blind-friendly RGB palette.
OKABE_ITO = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "reddish_purple": "#CC79A7",
    "gray": "#7F7F7F",
}

MODEL_COLORS = {
    "GPT-5-mini": OKABE_ITO["blue"],
    "DIS GPT": OKABE_ITO["sky_blue"],
    "Qwen3.6-plus": OKABE_ITO["orange"],
    "GLM-4.6V": OKABE_ITO["bluish_green"],
    "Kimi-K2.5": OKABE_ITO["reddish_purple"],
    "Gemini 2.5 Flash": "#8A6F00",
}

VISCOSITY_COLORS = {
    "Low viscosity": OKABE_ITO["sky_blue"],
    "Medium viscosity": OKABE_ITO["orange"],
    "High viscosity": OKABE_ITO["blue"],
}

GROUP_COLORS = {
    "Standard": OKABE_ITO["gray"],
    **MODEL_COLORS,
    **VISCOSITY_COLORS,
}


def set_nature_style() -> None:
    """Apply compact, editable, white-background scientific figure styling."""
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 6,
            "axes.labelsize": 7,
            "axes.titlesize": 7,
            "xtick.labelsize": 6,
            "ytick.labelsize": 6,
            "legend.fontsize": 6,
            "figure.titlesize": 7,
            "axes.linewidth": 0.5,
            "axes.edgecolor": "black",
            "axes.facecolor": "white",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "savefig.edgecolor": "white",
            "axes.grid": False,
            "grid.linewidth": 0.3,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.size": 2.0,
            "ytick.major.size": 2.0,
            "xtick.major.width": 0.5,
            "ytick.major.width": 0.5,
            "lines.linewidth": 1.0,
            "lines.markersize": 3.0,
            "patch.linewidth": 0.5,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "figure.dpi": 150,
            "savefig.dpi": 450,
        }
    )


def format_axis(ax: plt.Axes) -> None:
    """Remove non-data ink while retaining readable axes."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", which="major", pad=1.5)


def add_panel_label(ax: plt.Axes, label: str, x: float = -0.18, y: float = 1.08) -> None:
    """Add lowercase bold panel label in journal-compatible sizing."""
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=8,
        fontweight="bold",
        va="top",
        ha="left",
    )


def save_figure(fig: plt.Figure, outbase: str | Path, dpi: int = 450) -> None:
    """Save editable vector and high-resolution raster outputs."""
    outbase = Path(outbase)
    outbase.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outbase.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(outbase.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(outbase.with_suffix(".png"), dpi=dpi, bbox_inches="tight")


def color_for_group(group: str, palette: dict[str, str], fallback_index: int = 0) -> str:
    """Return a palette color with deterministic fallback for unknown groups."""
    if group in palette:
        return palette[group]
    fallback = [
        OKABE_ITO["blue"],
        OKABE_ITO["orange"],
        OKABE_ITO["bluish_green"],
        OKABE_ITO["reddish_purple"],
        OKABE_ITO["sky_blue"],
        OKABE_ITO["yellow"],
        OKABE_ITO["gray"],
    ]
    return fallback[fallback_index % len(fallback)]
