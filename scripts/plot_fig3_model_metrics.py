#!/usr/bin/env python
"""Generate final Fig. 3 panels from quality.xlsx only."""

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

from ncfigs.io import ensure_dir, load_table, save_source_copy, save_table
from ncfigs.style import add_panel_label, format_axis, save_figure, set_nature_style


MODEL_ORDER = ["GPT-5.5", "Qwen3.6-plus", "GLM-4.6V", "Kimi-K2.5"]
MODEL_COLORS = {
    "GPT-5.5": "#2F6DB3",
    "Qwen3.6-plus": "#008C9E",
    "GLM-4.6V": "#5B5FC7",
    "Kimi-K2.5": "#6C8AA3",
}
REFERENCE_COLOR = "#303030"

MODEL_COLUMN_CANDIDATES = ["model_bucket", "model_bu", "model", "model_label", "model_display_name"]
WEIGHT_COLUMN_CANDIDATES = ["mapped_model_label_count", "mapped_n", "supported_count", "supported", "file_count"]

PANEL_CONFIG = {
    "a": {
        "metric_candidates": ["avg_dimension_coverage_pct"],
        "plot_col": "avg_dimension_coverage_pct",
        "title": "Output completeness",
        "ylabel": "8-dimension coverage (%)",
        "output": "fig3a_output_completeness",
        "processed": "fig3_quality_panel_a_plotting.csv",
        "panel_label": "a",
    },
    "b": {
        "metric_candidates": ["repeat_consistency_rate_pct"],
        "plot_col": "repeat_consistency_rate_pct",
        "title": "Run-to-run consistency",
        "ylabel": "Repeat consistency (%)",
        "output": "fig3b_run_to_run_consistency",
        "processed": "fig3_quality_panel_b_plotting.csv",
        "panel_label": "b",
    },
    "c": {
        "metric_candidates": ["avg_overall_quality_score", "avg_overall_quality_score_pct"],
        "plot_col": "avg_overall_quality_score",
        "title": "Overall quality",
        "ylabel": "Overall quality score",
        "output": "fig3c_overall_quality_with_disgpt_reference",
        "processed": "fig3_quality_panel_c_plotting.csv",
        "panel_label": "c",
    },
}

MODEL_ALIASES = {
    "chatgpt": "GPT-5.5",
    "chat-gpt": "GPT-5.5",
    "gpt": "GPT-5.5",
    "gpt-5.5": "GPT-5.5",
    "gpt5.5": "GPT-5.5",
    "gpt-5-mini": "GPT-5.5",
    "gpt5-mini": "GPT-5.5",
    "qwen": "Qwen3.6-plus",
    "qwen3.6-plus": "Qwen3.6-plus",
    "qwen-3.6-plus": "Qwen3.6-plus",
    "glm": "GLM-4.6V",
    "glm-4.6v": "GLM-4.6V",
    "glm4.6v": "GLM-4.6V",
    "kimi": "Kimi-K2.5",
    "kimi-k2.5": "Kimi-K2.5",
}
DIS_GPT_KEYS = {"dis-gpt", "dis-gpt-old", "disgpt", "dis-gpt-reference", "dis-gpt-benchmark"}


def alias_key(value: object) -> str:
    text = "" if pd.isna(value) else str(value).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def standardize_model(value: object) -> str:
    key = alias_key(value)
    if key in DIS_GPT_KEYS:
        return "DIS GPT"
    if key in MODEL_ALIASES:
        return MODEL_ALIASES[key]
    if "qwen" in key:
        return "Qwen3.6-plus"
    if "glm" in key:
        return "GLM-4.6V"
    if "kimi" in key:
        return "Kimi-K2.5"
    if "gpt" in key or "chat" in key:
        return "GPT-5.5"
    return "" if pd.isna(value) else str(value).strip()


def detect_first_existing(df: pd.DataFrame, candidates: list[str], kind: str) -> str:
    for col in candidates:
        if col in df.columns:
            return col
    raise ValueError(f"quality.xlsx is missing a {kind} column. Tried: {', '.join(candidates)}")


def weighted_metric(group: pd.DataFrame, value_col: str, weight_col: str) -> float:
    values = pd.to_numeric(group[value_col], errors="coerce").to_numpy(float)
    weights = pd.to_numeric(group[weight_col], errors="coerce").fillna(1.0).to_numpy(float)
    valid = ~(np.isnan(values) | np.isnan(weights))
    if not valid.any() or weights[valid].sum() <= 0:
        return np.nan
    return float(np.average(values[valid], weights=weights[valid]))


def prepare_quality(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, str], str, str]:
    model_col = detect_first_existing(raw, MODEL_COLUMN_CANDIDATES, "model")
    weight_col = next((col for col in WEIGHT_COLUMN_CANDIDATES if col in raw.columns), None)
    if weight_col is None:
        weight_col = "aggregation_weight"

    metric_sources = {
        panel: detect_first_existing(raw, config["metric_candidates"], f"{panel} metric")
        for panel, config in PANEL_CONFIG.items()
    }

    source = raw.copy()
    source["source_model_name"] = source[model_col].astype(str)
    source["standardized_model"] = source[model_col].map(standardize_model)
    if weight_col == "aggregation_weight":
        source[weight_col] = 1.0
    else:
        source[weight_col] = pd.to_numeric(source[weight_col], errors="coerce").fillna(1.0)
    source["row_role"] = np.where(source["standardized_model"] == "DIS GPT", "panel_c_reference_line", "bar_candidate")

    for panel, source_col in metric_sources.items():
        source[PANEL_CONFIG[panel]["plot_col"]] = pd.to_numeric(source[source_col], errors="coerce")

    bar_source = source.loc[source["standardized_model"].isin(MODEL_ORDER)].copy()
    extra_source = source.loc[~source["standardized_model"].isin(MODEL_ORDER)].copy()

    rows = []
    for model in MODEL_ORDER:
        group = bar_source.loc[bar_source["standardized_model"] == model]
        if group.empty:
            continue
        row = {
            "model": model,
            "model_order": MODEL_ORDER.index(model),
            "source_model_names": "|".join(group["source_model_name"].astype(str)),
            "n_source_rows": int(len(group)),
            "aggregation_weight_column": weight_col,
            "aggregation_weight_sum": float(pd.to_numeric(group[weight_col], errors="coerce").sum()),
            "display_type": "bar",
            "row_excluded": False,
        }
        for panel, config in PANEL_CONFIG.items():
            plot_col = config["plot_col"]
            row[plot_col] = weighted_metric(group, plot_col, weight_col)
            row[f"{plot_col}_source_column"] = metric_sources[panel]
            row[f"{plot_col}_source_values"] = "|".join(
                "" if pd.isna(value) else f"{float(value):.6g}" for value in group[plot_col]
            )
        row["aggregation_method"] = (
            f"weighted mean by {weight_col}" if len(group) > 1 else "single source row"
        )
        rows.append(row)
    bars = pd.DataFrame(rows).sort_values("model_order").reset_index(drop=True)
    return source, bars, extra_source, metric_sources, model_col, weight_col


def get_dis_gpt_reference(source: pd.DataFrame, weight_col: str, metric_col: str) -> tuple[float, pd.DataFrame]:
    ref = source.loc[source["standardized_model"] == "DIS GPT"].copy()
    if ref.empty:
        return np.nan, ref
    return weighted_metric(ref, metric_col, weight_col), ref


def y_limit(values: pd.Series, reference_value: float | None = None) -> tuple[float, float]:
    observed = pd.to_numeric(values, errors="coerce").dropna().tolist()
    if reference_value is not None and np.isfinite(reference_value):
        observed.append(float(reference_value))
    max_value = max(observed) if observed else 100.0
    if max_value <= 100:
        return 0.0, 100.0
    return 0.0, float(np.ceil(max_value * 1.08 / 10.0) * 10.0)


def draw_panel(
    ax: plt.Axes,
    bars: pd.DataFrame,
    panel: str,
    reference_value: float | None = None,
    show_panel_label: bool = True,
) -> None:
    config = PANEL_CONFIG[panel]
    plot_col = config["plot_col"]
    data = bars.sort_values("model_order").copy()
    x = np.arange(len(data))
    colors = [MODEL_COLORS.get(model, "#4F6D7A") for model in data["model"]]
    ax.bar(
        x,
        data[plot_col],
        width=0.64,
        color=colors,
        edgecolor="black",
        linewidth=0.5,
        zorder=2,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(data["model"], rotation=35, ha="right")
    ax.set_ylabel(config["ylabel"])
    ax.set_xlabel("")
    ax.set_title(config["title"])
    ax.set_ylim(*y_limit(data[plot_col], reference_value if panel == "c" else None))
    if panel == "c" and reference_value is not None and np.isfinite(reference_value):
        ax.axhline(
            reference_value,
            color=REFERENCE_COLOR,
            linestyle=(0, (3, 2)),
            linewidth=0.8,
            zorder=3,
        )
        ax.legend(
            handles=[
                Line2D(
                    [0],
                    [0],
                    color=REFERENCE_COLOR,
                    linestyle=(0, (3, 2)),
                    linewidth=0.8,
                    label="DIS GPT benchmark",
                )
            ],
            loc="upper right",
            frameon=False,
        )
    format_axis(ax)
    if show_panel_label:
        add_panel_label(ax, config["panel_label"])


def save_single_panel(
    bars: pd.DataFrame,
    panel: str,
    figdir: Path,
    reference_value: float | None = None,
) -> None:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(3.1, 2.35))
    draw_panel(ax, bars, panel, reference_value=reference_value, show_panel_label=True)
    fig.tight_layout()
    save_figure(fig, figdir / PANEL_CONFIG[panel]["output"])
    plt.close(fig)


def save_combined(bars: pd.DataFrame, figdir: Path, reference_value: float | None = None) -> None:
    set_nature_style()
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.35))
    for ax, panel in zip(axes, ["a", "b", "c"]):
        draw_panel(ax, bars, panel, reference_value=reference_value if panel == "c" else None)
    fig.tight_layout(w_pad=1.1)
    save_figure(fig, figdir / "fig3_combined")
    plt.close(fig)


def make_panel_table(
    bars: pd.DataFrame,
    panel: str,
    dis_reference_value: float | None,
    dis_reference_rows: pd.DataFrame,
    metric_sources: dict[str, str],
) -> pd.DataFrame:
    plot_col = PANEL_CONFIG[panel]["plot_col"]
    table = bars[
        [
            "model",
            "model_order",
            "source_model_names",
            "display_type",
            "n_source_rows",
            "aggregation_weight_column",
            "aggregation_weight_sum",
            "aggregation_method",
            plot_col,
            f"{plot_col}_source_column",
            f"{plot_col}_source_values",
            "row_excluded",
        ]
    ].rename(columns={plot_col: "plotted_value"})
    table["panel"] = panel
    if panel == "c" and dis_reference_rows is not None and not dis_reference_rows.empty:
        ref_row = {
            "model": "DIS GPT",
            "model_order": np.nan,
            "source_model_names": "|".join(dis_reference_rows["source_model_name"].astype(str)),
            "display_type": "horizontal dashed reference line",
            "n_source_rows": int(len(dis_reference_rows)),
            "aggregation_weight_column": table["aggregation_weight_column"].iloc[0] if not table.empty else "",
            "aggregation_weight_sum": float(dis_reference_rows["aggregation_weight"].sum())
            if "aggregation_weight" in dis_reference_rows.columns
            else np.nan,
            "aggregation_method": "DIS GPT benchmark from quality.xlsx",
            "plotted_value": dis_reference_value,
            f"{plot_col}_source_column": metric_sources[panel],
            f"{plot_col}_source_values": "|".join(
                "" if pd.isna(value) else f"{float(value):.6g}" for value in dis_reference_rows[plot_col]
            ),
            "row_excluded": False,
            "panel": panel,
        }
        table = pd.concat([table, pd.DataFrame([ref_row])], ignore_index=True)
    return table


def build_qc(
    raw: pd.DataFrame,
    source: pd.DataFrame,
    bars: pd.DataFrame,
    extra_source: pd.DataFrame,
    model_col: str,
    metric_sources: dict[str, str],
    weight_col: str,
    dis_reference_value: float,
    dis_reference_rows: pd.DataFrame,
) -> pd.DataFrame:
    rows = [
        {
            "check": "detected_columns",
            "value": "|".join(map(str, raw.columns)),
            "notes": "Exact columns detected in quality.xlsx.",
        },
        {
            "check": "model_column",
            "value": model_col,
            "notes": "Column used as x-axis grouping source before standardization.",
        },
        {
            "check": "source_model_rows",
            "value": "|".join(source["source_model_name"].astype(str)),
            "notes": "All rows present in quality.xlsx.",
        },
        {
            "check": "bar_model_rows",
            "value": "|".join(bars["model"].astype(str)),
            "notes": "Regular model bars shown in all three panels.",
        },
        {
            "check": "dis_gpt_reference_row",
            "value": "|".join(dis_reference_rows["source_model_name"].astype(str)) if not dis_reference_rows.empty else "",
            "notes": "Used for the panel c dashed benchmark line.",
        },
        {
            "check": "dis_gpt_benchmark_value",
            "value": "" if not np.isfinite(dis_reference_value) else f"{dis_reference_value:.10g}",
            "notes": "Panel c dashed-line value from the DIS GPT row.",
        },
        {
            "check": "rows_excluded_from_bars",
            "value": str(int(len(extra_source))),
            "notes": (
                "No rows excluded from bars."
                if extra_source.empty
                else "|".join(extra_source["source_model_name"].astype(str))
            ),
        },
        {
            "check": "rows_discarded",
            "value": "0",
            "notes": "No quality.xlsx row was discarded; DIS GPT is represented as a panel c reference line.",
        },
        {
            "check": "aggregation_weight_column",
            "value": weight_col,
            "notes": "Used only if multiple rows map to the same displayed model.",
        },
    ]
    for panel, source_col in metric_sources.items():
        rows.append(
            {
                "check": f"panel_{panel}_metric",
                "value": source_col,
                "notes": PANEL_CONFIG[panel]["ylabel"],
            }
        )
    for row in source.itertuples(index=False):
        rows.append(
            {
                "check": "model_standardization",
                "value": f"{row.source_model_name} -> {row.standardized_model}",
                "notes": row.row_role,
            }
        )
    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-quality",
        default=Path(r"E:\桌面\办公\符\论文\药学大模型推进\图\数据处理\3c\quality.xlsx"),
        type=Path,
    )
    parser.add_argument("--quality-sheet", default=None, help="Excel sheet name/index for --input-quality.")
    parser.add_argument("--outdir", default=ROOT / "outputs", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figdir = ensure_dir(args.outdir / "figures")
    processed_dir = ensure_dir(args.outdir / "processed")
    source_dir = ensure_dir(args.outdir / "source_data")
    qc_dir = ensure_dir(args.outdir / "qc")

    raw = load_table(args.input_quality, sheet_name=args.quality_sheet)
    save_source_copy(raw, source_dir / "fig3_quality_source_table.csv")

    source, bars, extra_source, metric_sources, model_col, weight_col = prepare_quality(raw)
    dis_reference_value, dis_reference_rows = get_dis_gpt_reference(
        source,
        weight_col,
        PANEL_CONFIG["c"]["plot_col"],
    )

    save_single_panel(bars, "a", figdir)
    save_single_panel(bars, "b", figdir)
    save_single_panel(bars, "c", figdir, reference_value=dis_reference_value)
    save_combined(bars, figdir, reference_value=dis_reference_value)

    for panel, config in PANEL_CONFIG.items():
        save_table(
            make_panel_table(bars, panel, dis_reference_value, dis_reference_rows, metric_sources),
            processed_dir / config["processed"],
        )
    save_table(
        build_qc(
            raw,
            source,
            bars,
            extra_source,
            model_col,
            metric_sources,
            weight_col,
            dis_reference_value,
            dis_reference_rows,
        ),
        qc_dir / "fig3_quality_plotting_qc.csv",
    )

    print(f"input_quality={args.input_quality}")
    print("detected_columns=" + "|".join(map(str, raw.columns)))
    print(f"model_column={model_col}")
    print("source_model_rows=" + "; ".join(source["source_model_name"].astype(str)))
    print("bar_model_rows=" + "; ".join(bars["model"].astype(str)))
    print("dis_gpt_row=" + ("; ".join(dis_reference_rows["source_model_name"].astype(str)) if not dis_reference_rows.empty else "not found"))
    print(f"dis_gpt_benchmark_value={dis_reference_value:.10g}" if np.isfinite(dis_reference_value) else "dis_gpt_benchmark_value=not found")
    print(f"panel_a_metric={metric_sources['a']}")
    print(f"panel_b_metric={metric_sources['b']}")
    print(f"panel_c_metric={metric_sources['c']}")
    print(
        "rows_excluded_from_bars="
        + (str(int(len(extra_source))) if len(extra_source) else "0")
        + (" (" + "; ".join(extra_source["source_model_name"].astype(str)) + ")" if len(extra_source) else "")
    )
    print("rows_discarded=0")
    print("figure_a=outputs/figures/fig3a_output_completeness.[pdf|svg|png]")
    print("figure_b=outputs/figures/fig3b_run_to_run_consistency.[pdf|svg|png]")
    print("figure_c=outputs/figures/fig3c_overall_quality_with_disgpt_reference.[pdf|svg|png]")
    print("figure_combined=outputs/figures/fig3_combined.[pdf|svg|png]")
    print("panel_a=outputs/processed/fig3_quality_panel_a_plotting.csv")
    print("panel_b=outputs/processed/fig3_quality_panel_b_plotting.csv")
    print("panel_c=outputs/processed/fig3_quality_panel_c_plotting.csv")
    print("source=outputs/source_data/fig3_quality_source_table.csv")
    print("qc=outputs/qc/fig3_quality_plotting_qc.csv")


if __name__ == "__main__":
    main()
