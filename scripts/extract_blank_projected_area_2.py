#!/usr/bin/env python
"""Generate Fig. 4: time-resolved projected-area change by viscosity."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ncfigs.constants import VISCOSITY_ALIASES, VISCOSITY_ORDER
from ncfigs.io import (
    ensure_dir,
    load_table,
    require_columns,
    save_source_copy,
    save_table,
    standardize_category_names,
    write_qc_reports,
)
from ncfigs.plotting import present_order, timecourse_mean_sd
from ncfigs.stats import mixed_effects_timecourse, one_way_test, trapezoid_auc
from ncfigs.style import VISCOSITY_COLORS, add_panel_label, save_figure, set_nature_style


def prepare_timecourse(df: pd.DataFrame) -> pd.DataFrame:
    required = ["sample_id", "viscosity_group", "time_h", "projected_area"]
    require_columns(df, required, "Fig. 4 projected-area table")
    out = standardize_category_names(df, "viscosity_group", VISCOSITY_ALIASES, "Fig. 4 projected-area table")
    out["time_h"] = pd.to_numeric(out["time_h"], errors="coerce")
    out["projected_area"] = pd.to_numeric(out["projected_area"], errors="coerce")

    baseline = out.loc[out["time_h"] == 0, ["sample_id", "projected_area"]].dropna()
    if baseline.empty:
        raise ValueError("Fig. 4 requires a time_h == 0 baseline projected_area for each sample_id.")
    if baseline["sample_id"].duplicated().any():
        raise ValueError("Each sample_id must have exactly one time_h == 0 baseline row.")
    baseline = baseline.rename(columns={"projected_area": "projected_area_t0"})
    out = out.merge(baseline, on="sample_id", how="left")
    if out["projected_area_t0"].isna().any():
        missing = sorted(out.loc[out["projected_area_t0"].isna(), "sample_id"].astype(str).unique())
        raise ValueError(f"Missing time_h == 0 baseline for sample_id(s): {', '.join(missing)}")
    out["normalized_projected_area"] = out["projected_area"] / out["projected_area_t0"]
    return out


def compute_auc(timecourse: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (group, sample_id), sdf in timecourse.groupby(["viscosity_group", "sample_id"], observed=False):
        sdf = sdf.sort_values("time_h")
        rows.append(
            {
                "viscosity_group": group,
                "sample_id": sample_id,
                "auc_normalized_projected_area": trapezoid_auc(
                    sdf["time_h"].to_numpy(),
                    sdf["normalized_projected_area"].to_numpy(),
                ),
                "time_min_h": sdf["time_h"].min(),
                "time_max_h": sdf["time_h"].max(),
                "n_timepoints": sdf["time_h"].nunique(),
            }
        )
    return pd.DataFrame(rows)


def build_figure(timecourse: pd.DataFrame, order: list[str], outbase: Path) -> pd.DataFrame:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(3.3, 2.3))
    summary = timecourse_mean_sd(
        ax,
        timecourse,
        group_col="viscosity_group",
        time_col="time_h",
        value_col="normalized_projected_area",
        subject_col="sample_id",
        order=order,
        palette=VISCOSITY_COLORS,
        y_label="Normalized projected area (area$_t$/area$_0$)",
        x_label="Time (h)",
        show_individual=True,
    )
    add_panel_label(ax, "a")
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=ROOT / "data/raw/fig4_viscosity_timecourse.csv", type=Path)
    parser.add_argument("--sheet", default=None, help="Excel sheet name/index for --input.")
    parser.add_argument("--outdir", default=ROOT / "outputs", type=Path)
    parser.add_argument(
        "--test",
        choices=["auto", "anova", "kruskal"],
        default="auto",
        help="Statistical test family for AUC comparison.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figdir = ensure_dir(args.outdir / "figures")
    processed_dir = ensure_dir(args.outdir / "processed")
    stats_dir = ensure_dir(args.outdir / "stats")
    qc_dir = ensure_dir(args.outdir / "qc")
    source_dir = ensure_dir(args.outdir / "source_data")

    raw = load_table(args.input, sheet_name=args.sheet)
    save_source_copy(raw, source_dir / "fig4_viscosity_timecourse_source.csv")
    timecourse = prepare_timecourse(raw)
    write_qc_reports(
        timecourse,
        qc_dir,
        "fig4_viscosity_timecourse",
        group_cols=["viscosity_group"],
        replicate_col="sample_id",
    )
    order = present_order(timecourse["viscosity_group"], VISCOSITY_ORDER)

    auc = compute_auc(timecourse)
    save_table(timecourse, processed_dir / "fig4_viscosity_timecourse_processed.csv")
    save_table(auc, processed_dir / "fig4_viscosity_auc_values.csv")

    summary = build_figure(
        timecourse,
        order=order,
        outbase=figdir / "fig4_viscosity_timecourse",
    )
    save_table(summary, processed_dir / "fig4_viscosity_timecourse_summary.csv")

    stats_auc = one_way_test(
        auc,
        "auc_normalized_projected_area",
        "viscosity_group",
        "Fig. 4 AUC of normalized projected area",
        order=order,
        preferred=args.test,
        replicate_definition="Each point is one independent image-analysis sample trajectory.",
    )
    stats_mixed = mixed_effects_timecourse(
        timecourse,
        value_col="normalized_projected_area",
        group_col="viscosity_group",
        time_col="time_h",
        subject_col="sample_id",
        analysis_label="Fig. 4 repeated-measures time-course model",
        replicate_definition="Repeated observations are time points nested within each sample_id.",
    )
    save_table(pd.concat([stats_auc, stats_mixed], ignore_index=True), stats_dir / "fig4_viscosity_timecourse_stats.csv")


if __name__ == "__main__":
    main()

