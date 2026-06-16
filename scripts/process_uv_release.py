#!/usr/bin/env python
"""Generate Fig. 5: optimized formulation validation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ncfigs.constants import MODEL_ALIASES, MODEL_ORDER, STANDARD_ALIASES
from ncfigs.io import (
    ensure_dir,
    load_table,
    require_columns,
    save_source_copy,
    save_table,
    standardize_category_names,
    write_qc_reports,
)
from ncfigs.plotting import bar_with_points, present_order, timecourse_mean_sd
from ncfigs.stats import dunnett_vs_control, one_way_test, trapezoid_auc
from ncfigs.style import GROUP_COLORS, add_panel_label, save_figure, set_nature_style


GROUP_ALIASES = {**MODEL_ALIASES, **STANDARD_ALIASES}
EXCEL_SUFFIXES = {".xlsx", ".xls", ".xlsm"}
MAPPING_REQUIRED_COLUMNS = [
    "source_file",
    "formulation_group",
    "formulation_label",
    "drug_label",
    "replicate_file_id",
    "include_for_fig5b",
]
UV_LONG_REQUIRED_COLUMNS = [
    "source_file",
    "formulation_group",
    "formulation_label",
    "drug_label",
    "replicate_file_id",
    "measurement_id",
    "sample_index",
    "time_h",
    "duration_h",
    "absorbance",
]


def standardize_groups(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    return standardize_category_names(df, "formulation_group", GROUP_ALIASES, dataset_name)


def _yes_no_to_bool(value: object) -> bool:
    if pd.isna(value):
        return False
    return str(value).strip().lower() in {"yes", "y", "true", "1", "include", "included"}


def _clean_header(value: object) -> str:
    return "" if pd.isna(value) else str(value).strip()


def _header_key(value: object) -> str:
    text = _clean_header(value).lower()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text


def list_uv_excel_files(input_dir: Path) -> list[Path]:
    if not input_dir.exists() or not input_dir.is_dir():
        return []
    return sorted(
        path
        for path in input_dir.iterdir()
        if path.suffix.lower() in EXCEL_SUFFIXES and not path.name.startswith("~$")
    )


def load_fig5b_mapping(mapping_path: Path) -> pd.DataFrame | None:
    if not mapping_path.exists():
        return None
    mapping = load_table(mapping_path)
    require_columns(mapping, MAPPING_REQUIRED_COLUMNS, "Fig. 5b manual file mapping")
    mapping = mapping.copy()
    mapping["source_file"] = mapping["source_file"].astype(str).str.strip()
    mapping = standardize_groups(mapping, "Fig. 5b manual file mapping")
    mapping["include_for_fig5b_bool"] = mapping["include_for_fig5b"].map(_yes_no_to_bool)
    if mapping["source_file"].duplicated().any():
        duplicated = ", ".join(mapping.loc[mapping["source_file"].duplicated(), "source_file"])
        raise ValueError(f"Fig. 5b mapping has duplicated source_file entries: {duplicated}")
    return mapping


def detect_time_column(columns: list[object]) -> object | None:
    for col in columns:
        if _clean_header(col) == "对应时间":
            return col
    preferred = {"time", "time-h", "time-(h)", "corresponding-time"}
    for col in columns:
        if _header_key(col) in preferred:
            return col
    for col in columns:
        text = _clean_header(col)
        if "时间" in text and "持续" not in text:
            return col
    return None


def detect_duration_column(columns: list[object]) -> object | None:
    for col in columns:
        if _clean_header(col) == "持续时间":
            return col
    for col in columns:
        key = _header_key(col)
        text = _clean_header(col)
        if "duration" in key or "interval" in key or "持续" in text:
            return col
    return None


def detect_sample_index_column(columns: list[object]) -> object | None:
    for col in columns:
        if _clean_header(col) == "编号":
            return col
    for col in columns:
        key = _header_key(col)
        text = _clean_header(col)
        if key in {"sample-index", "index", "id"} or "编号" in text:
            return col
    return None


def detect_absorbance_columns(columns: list[object]) -> list[object]:
    for idx, col in enumerate(columns):
        key = _header_key(col)
        text = _clean_header(col)
        if text == "吸光度" or "absorb" in key:
            candidate = columns[idx : idx + 3]
            if len(candidate) == 3:
                return candidate
    fallback = []
    for col in columns:
        key = _header_key(col)
        text = _clean_header(col)
        if text == "吸光度" or "吸光" in text or "absorb" in key or "repeat" in key or "meas" in key:
            fallback.append(col)
    return fallback[:3]


def auto_parse_uv_filename(source_file: str) -> dict[str, object]:
    name = source_file
    lower_name = source_file.lower()
    drug_label = "unknown"
    if "亚甲蓝" in name:
        drug_label = "methylene_blue"
    elif "格列齐特" in name:
        drug_label = "gliclazide"

    formulation_group = None
    formulation_label = None
    if "标准粘度" in name:
        formulation_group = "Standard"
        formulation_label = "Standard viscosity"
    elif "低粘度" in name:
        formulation_group = "Low viscosity"
        formulation_label = "Low viscosity"
    elif "高粘度" in name:
        formulation_group = "High viscosity"
        formulation_label = "High viscosity"
    elif "gpts" in lower_name or "gpt" in lower_name:
        formulation_group = "GPT-5-mini"
        formulation_label = "GPT-5-mini optimized"
    elif "gemini" in lower_name:
        formulation_group = "Gemini 2.5 Flash"
        formulation_label = "Gemini 2.5 Flash optimized"
    elif "qwen" in lower_name:
        formulation_group = "Qwen3.6-plus"
        formulation_label = "Qwen3.6-plus optimized"
    elif "glm" in lower_name:
        formulation_group = "GLM-4.6V"
        formulation_label = "GLM-4.6V optimized"
    elif "kimi" in lower_name:
        formulation_group = "Kimi-K2.5"
        formulation_label = "Kimi-K2.5 optimized"

    parsing_status = "auto_parsed" if formulation_group and drug_label != "unknown" else "needs_manual_mapping"
    replicate_id = Path(source_file).stem
    return {
        "source_file": source_file,
        "formulation_group": formulation_group or "Unmapped",
        "formulation_label": formulation_label or "Unmapped",
        "drug_label": drug_label,
        "replicate_file_id": replicate_id,
        "include_for_fig5b": "yes" if parsing_status == "auto_parsed" else "no",
        "include_for_fig5b_bool": parsing_status == "auto_parsed",
        "manual_mapping_used": False,
        "parsing_status": parsing_status,
    }


def metadata_for_uv_file(source_file: str, mapping: pd.DataFrame | None) -> dict[str, object]:
    if mapping is not None:
        hit = mapping.loc[mapping["source_file"] == source_file]
        if not hit.empty:
            row = hit.iloc[0].to_dict()
            row["manual_mapping_used"] = True
            row["parsing_status"] = "manual_mapping"
            return row
    return auto_parse_uv_filename(source_file)


def _column_list_text(columns: list[object]) -> str:
    return "|".join(_clean_header(col) for col in columns)


def _selected_missing_values(df: pd.DataFrame, columns: list[object]) -> str:
    parts = []
    for col in columns:
        if col is not None and col in df.columns:
            parts.append(f"{_clean_header(col)}={int(df[col].isna().sum())}")
    return "; ".join(parts)


def read_uv_excel_to_long(path: Path, metadata: dict[str, object]) -> tuple[pd.DataFrame, dict[str, object]]:
    source_file = path.name
    base_qc = {
        "source_file": source_file,
        "parsing_status": metadata.get("parsing_status", ""),
        "detected_time_column": "",
        "detected_absorbance_columns": "",
        "missing_values": "",
        "time_range_min": np.nan,
        "time_range_max": np.nan,
        "has_0h": False,
        "baseline_added": False,
        "covers_4h": False,
        "covers_8h": False,
        "negative_absorbance_values": np.nan,
        "excluded_reason": "",
        "manual_mapping_used": bool(metadata.get("manual_mapping_used", False)),
        "include_for_fig5b": metadata.get("include_for_fig5b", "no"),
    }
    try:
        raw = pd.read_excel(path, sheet_name=0)
    except Exception as exc:
        base_qc["excluded_reason"] = f"read_error: {exc}"
        return pd.DataFrame(columns=UV_LONG_REQUIRED_COLUMNS), base_qc

    columns = list(raw.columns)
    time_col = detect_time_column(columns)
    duration_col = detect_duration_column(columns)
    sample_index_col = detect_sample_index_column(columns)
    absorbance_cols = detect_absorbance_columns(columns)
    base_qc["detected_time_column"] = _clean_header(time_col)
    base_qc["detected_absorbance_columns"] = _column_list_text(absorbance_cols)

    selected_cols = [col for col in [sample_index_col, time_col, duration_col, *absorbance_cols] if col is not None]
    base_qc["missing_values"] = _selected_missing_values(raw, selected_cols)
    if time_col is None:
        base_qc["excluded_reason"] = "time_column_not_detected"
        return pd.DataFrame(columns=UV_LONG_REQUIRED_COLUMNS), base_qc
    if len(absorbance_cols) < 3:
        base_qc["excluded_reason"] = "fewer_than_three_absorbance_columns_detected"
        return pd.DataFrame(columns=UV_LONG_REQUIRED_COLUMNS), base_qc

    time_values = pd.to_numeric(raw[time_col], errors="coerce")
    valid_times = time_values.dropna()
    if not valid_times.empty:
        base_qc["time_range_min"] = float(valid_times.min())
        base_qc["time_range_max"] = float(valid_times.max())
        base_qc["has_0h"] = bool(np.isclose(valid_times, 0.0).any())
        base_qc["baseline_added"] = not base_qc["has_0h"]
        base_qc["covers_4h"] = bool(valid_times.min() <= 4.0 <= valid_times.max())
        base_qc["covers_8h"] = bool(valid_times.max() >= 8.0)
    abs_numeric = raw[absorbance_cols].apply(pd.to_numeric, errors="coerce")
    base_qc["negative_absorbance_values"] = int((abs_numeric < 0).sum().sum())

    if not bool(metadata.get("include_for_fig5b_bool", False)):
        base_qc["excluded_reason"] = "include_for_fig5b_no"
    if metadata.get("parsing_status") == "needs_manual_mapping":
        base_qc["excluded_reason"] = "needs_manual_mapping"
    if not base_qc["covers_8h"]:
        base_qc["excluded_reason"] = "does_not_cover_0_to_8h"

    sample_index = raw[sample_index_col] if sample_index_col is not None else pd.Series(np.arange(1, len(raw) + 1))
    duration = pd.to_numeric(raw[duration_col], errors="coerce") if duration_col is not None else pd.Series(np.nan, index=raw.index)

    rows = []
    for idx, abs_col in enumerate(absorbance_cols[:3], start=1):
        absorbance = pd.to_numeric(raw[abs_col], errors="coerce")
        for row_idx in raw.index:
            rows.append(
                {
                    "source_file": source_file,
                    "formulation_group": metadata.get("formulation_group"),
                    "formulation_label": metadata.get("formulation_label"),
                    "drug_label": metadata.get("drug_label"),
                    "replicate_file_id": metadata.get("replicate_file_id"),
                    "measurement_id": f"meas{idx}",
                    "sample_index": sample_index.loc[row_idx],
                    "time_h": time_values.loc[row_idx],
                    "duration_h": duration.loc[row_idx],
                    "absorbance": absorbance.loc[row_idx],
                    "include_for_fig5b": metadata.get("include_for_fig5b", "no"),
                    "manual_mapping_used": bool(metadata.get("manual_mapping_used", False)),
                    "parsing_status": metadata.get("parsing_status", ""),
                }
            )
    return pd.DataFrame(rows), base_qc


def _auc_for_curve(curve: pd.DataFrame, value_col: str = "absorbance") -> dict[str, object]:
    clean = curve[["time_h", value_col]].copy()
    clean["time_h"] = pd.to_numeric(clean["time_h"], errors="coerce")
    clean[value_col] = pd.to_numeric(clean[value_col], errors="coerce")
    clean = clean.dropna().sort_values("time_h")
    if clean.empty:
        return {
            "AUC_0_4h": np.nan,
            "AUC_0_8h": np.nan,
            "relative_early_release": np.nan,
            "baseline_added": False,
            "interpolation_used_4h": False,
            "interpolation_used_8h": False,
            "excluded_reason": "no_numeric_time_absorbance_values",
        }

    baseline_added = not np.isclose(clean["time_h"], 0.0).any()
    if baseline_added:
        clean = pd.concat(
            [pd.DataFrame({"time_h": [0.0], value_col: [0.0]}), clean],
            ignore_index=True,
        ).sort_values("time_h")
    time = clean["time_h"].to_numpy(float)
    signal = clean[value_col].to_numpy(float)
    covers_4h = bool(time.min() <= 4.0 <= time.max())
    covers_8h = bool(time.min() <= 0.0 and time.max() >= 8.0)
    interpolation_used_4h = covers_4h and not np.isclose(time, 4.0).any()
    interpolation_used_8h = covers_8h and not np.isclose(time, 8.0).any()
    if not covers_8h:
        return {
            "AUC_0_4h": np.nan,
            "AUC_0_8h": np.nan,
            "relative_early_release": np.nan,
            "baseline_added": baseline_added,
            "interpolation_used_4h": interpolation_used_4h,
            "interpolation_used_8h": interpolation_used_8h,
            "excluded_reason": "does_not_cover_0_to_8h",
        }

    auc_0_4 = trapezoid_auc(time, signal, start=0.0, end=4.0)
    auc_0_8 = trapezoid_auc(time, signal, start=0.0, end=8.0)
    if pd.isna(auc_0_8) or auc_0_8 <= 0:
        ratio = np.nan
        excluded_reason = "AUC_0_8h_non_positive"
    else:
        ratio = auc_0_4 / auc_0_8
        excluded_reason = ""
    return {
        "AUC_0_4h": auc_0_4,
        "AUC_0_8h": auc_0_8,
        "relative_early_release": ratio,
        "baseline_added": baseline_added,
        "interpolation_used_4h": interpolation_used_4h,
        "interpolation_used_8h": interpolation_used_8h,
        "excluded_reason": excluded_reason,
    }


def compute_fig5b_measurement_auc(long_df: pd.DataFrame) -> pd.DataFrame:
    included = long_df.loc[long_df["include_for_fig5b"].map(_yes_no_to_bool)].copy()
    rows = []
    group_cols = [
        "source_file",
        "formulation_group",
        "formulation_label",
        "drug_label",
        "replicate_file_id",
        "measurement_id",
    ]
    for keys, curve in included.groupby(group_cols, observed=False):
        result = _auc_for_curve(curve)
        row = dict(zip(group_cols, keys))
        row.update(result)
        rows.append(row)
    return pd.DataFrame(rows)


def make_fig5b_file_mean_curves(long_df: pd.DataFrame) -> pd.DataFrame:
    included = long_df.loc[long_df["include_for_fig5b"].map(_yes_no_to_bool)].copy()
    group_cols = [
        "source_file",
        "formulation_group",
        "formulation_label",
        "drug_label",
        "replicate_file_id",
        "time_h",
    ]
    if included.empty:
        return pd.DataFrame(columns=[*group_cols, "absorbance"])
    return (
        included.groupby(group_cols, observed=False)["absorbance"]
        .mean()
        .reset_index()
        .sort_values(["formulation_group", "replicate_file_id", "time_h"])
    )


def compute_fig5b_file_auc(long_df: pd.DataFrame, measurement_auc: pd.DataFrame) -> pd.DataFrame:
    mean_curves = make_fig5b_file_mean_curves(long_df)
    rows = []
    group_cols = [
        "source_file",
        "formulation_group",
        "formulation_label",
        "drug_label",
        "replicate_file_id",
    ]
    for keys, curve in mean_curves.groupby(group_cols, observed=False):
        result = _auc_for_curve(curve)
        row = dict(zip(group_cols, keys))
        row["AUC_0_4h_mean_curve"] = result["AUC_0_4h"]
        row["AUC_0_8h_mean_curve"] = result["AUC_0_8h"]
        row["relative_early_release_mean_curve"] = result["relative_early_release"]
        row["baseline_added"] = result["baseline_added"]
        row["interpolation_used_4h"] = result["interpolation_used_4h"]
        row["interpolation_used_8h"] = result["interpolation_used_8h"]
        row["excluded_reason"] = result["excluded_reason"]
        source_file, _, _, _, replicate_file_id = keys
        technical = measurement_auc.loc[
            (measurement_auc["source_file"] == source_file)
            & (measurement_auc["replicate_file_id"] == replicate_file_id),
            "relative_early_release",
        ].dropna()
        row["n_measurements"] = int(technical.shape[0])
        row["technical_sd_relative_early_release"] = technical.std(ddof=1)
        rows.append(row)
    return pd.DataFrame(rows)


def prepare_fig5b_uv_excel(input_dir: Path, mapping_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame | None]:
    mapping = load_fig5b_mapping(mapping_path)
    long_tables = []
    qc_rows = []
    for path in list_uv_excel_files(input_dir):
        metadata = metadata_for_uv_file(path.name, mapping)
        long_df, qc = read_uv_excel_to_long(path, metadata)
        long_tables.append(long_df)
        qc_rows.append(qc)
    long_source = (
        pd.concat(long_tables, ignore_index=True)
        if long_tables
        else pd.DataFrame(columns=[*UV_LONG_REQUIRED_COLUMNS, "include_for_fig5b", "manual_mapping_used", "parsing_status"])
    )
    qc = pd.DataFrame(qc_rows)
    measurement_auc = compute_fig5b_measurement_auc(long_source)
    file_auc = compute_fig5b_file_auc(long_source, measurement_auc)
    return long_source, measurement_auc, file_auc, qc, mapping


def prepare_fig5b_uv_from_simple_csv(release: pd.DataFrame, source_file: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    long_source = release.copy()
    long_source["source_file"] = source_file
    long_source["formulation_label"] = long_source["formulation_group"]
    long_source["drug_label"] = "methylene_blue"
    long_source["replicate_file_id"] = long_source["replicate_id"]
    long_source["measurement_id"] = "meas1"
    long_source["sample_index"] = long_source.groupby(["formulation_group", "replicate_id"], observed=False).cumcount() + 1
    long_source["duration_h"] = np.nan
    long_source["include_for_fig5b"] = "yes"
    long_source["manual_mapping_used"] = False
    long_source["parsing_status"] = "csv_input"
    long_source = long_source[[*UV_LONG_REQUIRED_COLUMNS, "include_for_fig5b", "manual_mapping_used", "parsing_status"]]

    qc_rows = []
    for (group, replicate_id), curve in release.groupby(["formulation_group", "replicate_id"], observed=False):
        times = pd.to_numeric(curve["time_h"], errors="coerce").dropna()
        signal = pd.to_numeric(curve["absorbance"], errors="coerce")
        has_0h = bool(np.isclose(times, 0.0).any()) if not times.empty else False
        covers_4h = bool(times.min() <= 4.0 <= times.max()) if not times.empty else False
        covers_8h = bool(times.max() >= 8.0) if not times.empty else False
        qc_rows.append(
            {
                "source_file": source_file,
                "replicate_file_id": replicate_id,
                "formulation_group": group,
                "parsing_status": "csv_input",
                "detected_time_column": "time_h",
                "detected_absorbance_columns": "absorbance",
                "missing_values": f"time_h={int(curve['time_h'].isna().sum())}; absorbance={int(curve['absorbance'].isna().sum())}",
                "time_range_min": float(times.min()) if not times.empty else np.nan,
                "time_range_max": float(times.max()) if not times.empty else np.nan,
                "has_0h": has_0h,
                "baseline_added": not has_0h,
                "covers_4h": covers_4h,
                "covers_8h": covers_8h,
                "negative_absorbance_values": int((signal < 0).sum()),
                "excluded_reason": "" if covers_8h else "does_not_cover_0_to_8h",
                "manual_mapping_used": False,
                "include_for_fig5b": "yes",
            }
        )
    measurement_auc = compute_fig5b_measurement_auc(long_source)
    file_auc = compute_fig5b_file_auc(long_source, measurement_auc)
    mean_curves = make_fig5b_file_mean_curves(long_source).rename(
        columns={"replicate_file_id": "replicate_id"}
    )
    return long_source, measurement_auc, file_auc, pd.DataFrame(qc_rows), mean_curves


def prepare_ratio_data(df: pd.DataFrame) -> pd.DataFrame:
    require_columns(df, ["formulation_group", "replicate_id"], "Fig. 5a formulation-ratio table")
    out = standardize_groups(df, "Fig. 5a formulation-ratio table")
    has_ratio = "k4m_k100lv_ratio" in out.columns
    has_amounts = {"k4m_amount", "k100lv_amount"}.issubset(out.columns)
    if has_ratio:
        out["k4m_k100lv_ratio"] = pd.to_numeric(out["k4m_k100lv_ratio"], errors="coerce")
    if has_amounts:
        out["k4m_amount"] = pd.to_numeric(out["k4m_amount"], errors="coerce")
        out["k100lv_amount"] = pd.to_numeric(out["k100lv_amount"], errors="coerce")
        computed_ratio = out["k4m_amount"] / out["k100lv_amount"]
        if has_ratio:
            out["k4m_k100lv_ratio"] = out["k4m_k100lv_ratio"].fillna(computed_ratio)
        else:
            out["k4m_k100lv_ratio"] = computed_ratio
    elif not has_ratio:
        require_columns(out, ["k4m_amount", "k100lv_amount"], "Fig. 5a formulation-ratio table")
    return out


def prepare_release_data(df: pd.DataFrame) -> pd.DataFrame:
    required = ["formulation_group", "replicate_id", "time_h", "absorbance"]
    require_columns(df, required, "Fig. 5b UV-release table")
    out = standardize_groups(df, "Fig. 5b UV-release table")
    out["time_h"] = pd.to_numeric(out["time_h"], errors="coerce")
    out["absorbance"] = pd.to_numeric(out["absorbance"], errors="coerce")
    return out


def compute_release_auc(release: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (group, replicate_id), sdf in release.groupby(["formulation_group", "replicate_id"], observed=False):
        sdf = sdf.sort_values("time_h")
        auc_0_4 = trapezoid_auc(sdf["time_h"].to_numpy(), sdf["absorbance"].to_numpy(), start=0.0, end=4.0)
        auc_0_8 = trapezoid_auc(sdf["time_h"].to_numpy(), sdf["absorbance"].to_numpy(), start=0.0, end=8.0)
        rows.append(
            {
                "formulation_group": group,
                "replicate_id": replicate_id,
                "auc_0_4h": auc_0_4,
                "auc_0_8h": auc_0_8,
                "relative_early_release": auc_0_4 / auc_0_8 if pd.notna(auc_0_8) and auc_0_8 != 0 else np.nan,
                "n_timepoints": sdf["time_h"].nunique(),
                "time_min_h": sdf["time_h"].min(),
                "time_max_h": sdf["time_h"].max(),
            }
        )
    return pd.DataFrame(rows)


def figure_group_order(series: pd.Series) -> list[str]:
    preferred = ["Standard", *MODEL_ORDER]
    return present_order(series, preferred)


def build_main_figure(
    ratio: pd.DataFrame,
    release_auc: pd.DataFrame,
    order: list[str],
    outbase: Path,
) -> pd.DataFrame:
    set_nature_style()
    fig, axes = plt.subplots(1, 2, figsize=(4.9, 2.35))

    summary_a = bar_with_points(
        axes[0],
        ratio,
        group_col="formulation_group",
        value_col="k4m_k100lv_ratio",
        order=order,
        palette=GROUP_COLORS,
        y_label="K4M/K100LV ratio",
    )
    axes[0].set_title("Polymer ratio")
    add_panel_label(axes[0], "a")

    summary_b = bar_with_points(
        axes[1],
        release_auc,
        group_col="formulation_group",
        value_col="relative_early_release",
        order=order,
        palette=GROUP_COLORS,
        y_label="Relative early release\n(AUC$_{0-4h}$/AUC$_{0-8h}$)",
        ylim=(0, 1.05),
    )
    axes[1].set_title("Early methylene blue release")
    add_panel_label(axes[1], "b")

    fig.tight_layout(w_pad=1.2)
    save_figure(fig, outbase)
    plt.close(fig)
    return pd.concat([summary_a.assign(panel="a"), summary_b.assign(panel="b")], ignore_index=True)


def build_fig5b_relative_early_release(
    file_auc: pd.DataFrame,
    order: list[str],
    outbase: Path,
) -> pd.DataFrame:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(3.0, 2.3))
    summary = bar_with_points(
        ax,
        file_auc,
        group_col="formulation_group",
        value_col="relative_early_release_mean_curve",
        order=order,
        palette=GROUP_COLORS,
        y_label="AUC$_{0-4h}$/AUC$_{0-8h}$",
        ylim=(0, 1.05),
    )
    ax.set_xlabel("")
    ax.set_title("Relative early release")
    add_panel_label(ax, "b")
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return summary


def build_fig5b_technical_measurement_plot(
    measurement_auc: pd.DataFrame,
    file_auc: pd.DataFrame,
    order: list[str],
    outbase: Path,
) -> pd.DataFrame:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(3.0, 2.3))
    summary = bar_with_points(
        ax,
        file_auc,
        group_col="formulation_group",
        value_col="relative_early_release_mean_curve",
        order=order,
        palette=GROUP_COLORS,
        y_label="AUC$_{0-4h}$/AUC$_{0-8h}$",
        ylim=(0, 1.05),
    )
    rng = np.random.default_rng(41)
    for idx, group in enumerate(order):
        values = pd.to_numeric(
            measurement_auc.loc[measurement_auc["formulation_group"] == group, "relative_early_release"],
            errors="coerce",
        ).dropna()
        jitter = rng.uniform(-0.22, 0.22, size=len(values))
        ax.scatter(
            np.full(len(values), idx) + jitter,
            values,
            s=7,
            facecolor=GROUP_COLORS.get(group, "#7F7F7F"),
            edgecolor="none",
            alpha=0.28,
            zorder=2,
        )
    ax.set_xlabel("")
    ax.set_title("Technical-measurement-level AUC ratios")
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return summary


def build_release_curves(release: pd.DataFrame, order: list[str], outbase: Path) -> pd.DataFrame:
    set_nature_style()
    fig, ax = plt.subplots(1, 1, figsize=(3.3, 2.3))
    summary = timecourse_mean_sd(
        ax,
        release,
        group_col="formulation_group",
        time_col="time_h",
        value_col="absorbance",
        subject_col="replicate_id",
        order=order,
        palette=GROUP_COLORS,
        y_label="UV absorbance (a.u.)",
        x_label="Time (h)",
        show_individual=True,
    )
    fig.tight_layout()
    save_figure(fig, outbase)
    plt.close(fig)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-ratio", default=ROOT / "data/raw/fig5a_formulation_ratios.csv", type=Path)
    parser.add_argument("--input-release", default=ROOT / "data/raw/fig5b_release_uv.csv", type=Path)
    parser.add_argument(
        "--input-release-dir",
        default=ROOT / "data/raw/fig5b_uv_excel",
        type=Path,
        help="Directory containing Fig. 5b raw UV Excel files. If Excel files are present, this workflow is used.",
    )
    parser.add_argument(
        "--file-mapping",
        default=ROOT / "data/raw/fig5b_file_mapping.csv",
        type=Path,
        help="Manual Fig. 5b Excel source-file mapping CSV.",
    )
    parser.add_argument("--ratio-sheet", default=None, help="Excel sheet name/index for --input-ratio.")
    parser.add_argument("--release-sheet", default=None, help="Excel sheet name/index for --input-release.")
    parser.add_argument("--outdir", default=ROOT / "outputs", type=Path)
    parser.add_argument(
        "--test",
        choices=["auto", "anova", "kruskal"],
        default="auto",
        help="Statistical test family for one-way comparisons.",
    )
    parser.add_argument(
        "--control",
        default="Standard",
        help="Control group for optional Dunnett comparisons. Use empty string to skip.",
    )
    parser.add_argument("--make-release-curves", action="store_true", help="Also export supplementary release curves.")
    parser.add_argument(
        "--make-fig5b-technical-plot",
        action="store_true",
        help="Also export a supplementary Fig. 5b plot with lighter technical-measurement-level dots.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figdir = ensure_dir(args.outdir / "figures")
    processed_dir = ensure_dir(args.outdir / "processed")
    stats_dir = ensure_dir(args.outdir / "stats")
    qc_dir = ensure_dir(args.outdir / "qc")
    source_dir = ensure_dir(args.outdir / "source_data")

    raw_ratio = load_table(args.input_ratio, sheet_name=args.ratio_sheet)
    save_source_copy(raw_ratio, source_dir / "fig5a_formulation_ratios_source.csv")
    ratio = prepare_ratio_data(raw_ratio)

    excel_files = list_uv_excel_files(args.input_release_dir)
    if excel_files:
        long_source, measurement_auc, file_auc, uv_qc, mapping = prepare_fig5b_uv_excel(
            args.input_release_dir,
            args.file_mapping,
        )
        if mapping is not None:
            save_source_copy(mapping, source_dir / "fig5b_file_mapping_source.csv")
        release_curve_input = make_fig5b_file_mean_curves(long_source).rename(
            columns={"replicate_file_id": "replicate_id"}
        )
    else:
        raw_release = load_table(args.input_release, sheet_name=args.release_sheet)
        save_source_copy(raw_release, source_dir / "fig5b_release_uv_source.csv")
        release = prepare_release_data(raw_release)
        write_qc_reports(
            release,
            qc_dir,
            "fig5b_release_uv",
            group_cols=["formulation_group"],
            replicate_col="replicate_id",
        )
        long_source, measurement_auc, file_auc, uv_qc, release_curve_input = prepare_fig5b_uv_from_simple_csv(
            release,
            args.input_release.name,
        )

    release_auc = file_auc.rename(
        columns={
            "replicate_file_id": "replicate_id",
            "AUC_0_4h_mean_curve": "auc_0_4h",
            "AUC_0_8h_mean_curve": "auc_0_8h",
            "relative_early_release_mean_curve": "relative_early_release",
        }
    )
    order = figure_group_order(pd.concat([ratio["formulation_group"], release_auc["formulation_group"]], ignore_index=True))
    fig5b_order = figure_group_order(file_auc["formulation_group"])

    write_qc_reports(
        ratio,
        qc_dir,
        "fig5a_formulation_ratios",
        group_cols=["formulation_group"],
        replicate_col="replicate_id",
    )
    save_table(uv_qc, qc_dir / "fig5b_uv_qc.csv")

    save_table(ratio, processed_dir / "fig5a_formulation_ratios_processed.csv")
    save_table(long_source, source_dir / "fig5b_uv_long_source.csv")
    save_table(long_source, processed_dir / "fig5b_release_uv_processed.csv")
    save_table(measurement_auc, processed_dir / "fig5b_auc_measurement_level.csv")
    save_table(file_auc, processed_dir / "fig5b_auc_file_level.csv")
    save_table(release_auc, processed_dir / "fig5b_release_auc_values.csv")

    summary = build_main_figure(
        ratio,
        release_auc,
        order=order,
        outbase=figdir / "fig5_optimized_formulation_validation",
    )
    save_table(summary, processed_dir / "fig5_optimized_formulation_validation_summary.csv")

    fig5b_summary = build_fig5b_relative_early_release(
        file_auc,
        order=fig5b_order,
        outbase=figdir / "fig5b_relative_early_release",
    )
    save_table(fig5b_summary, processed_dir / "fig5b_relative_early_release_summary.csv")

    if args.make_fig5b_technical_plot:
        technical_summary = build_fig5b_technical_measurement_plot(
            measurement_auc,
            file_auc,
            order=fig5b_order,
            outbase=figdir / "fig5b_relative_early_release_technical_measurements",
        )
        save_table(technical_summary, processed_dir / "fig5b_technical_measurement_summary.csv")

    if args.make_release_curves:
        curve_summary = build_release_curves(
            release_curve_input,
            order=fig5b_order,
            outbase=figdir / "fig5b_release_curves_supplementary",
        )
        save_table(curve_summary, processed_dir / "fig5b_release_curves_summary.csv")

    stats_rows = [
        one_way_test(
            ratio,
            "k4m_k100lv_ratio",
            "formulation_group",
            "Fig. 5a K4M/K100LV ratio",
            order=order,
            preferred=args.test,
            replicate_definition="Each point is one independently recommended or measured formulation replicate.",
        ),
        one_way_test(
            release_auc,
            "relative_early_release",
            "formulation_group",
            "Fig. 5b relative early release",
            order=order,
            preferred=args.test,
            replicate_definition="Each point is one independent UV-release replicate summarized as AUC0-4h/AUC0-8h.",
        ),
    ]
    fig5b_stats_rows = [
        one_way_test(
            file_auc,
            "relative_early_release_mean_curve",
            "formulation_group",
            "Fig. 5b relative early release from file-level averaged technical measurements",
            order=fig5b_order,
            preferred=args.test,
            replicate_definition=(
                "Each point is one independent Excel record file after averaging the three "
                "technical UV measurement columns within that file."
            ),
        )
    ]
    control = args.control.strip() if args.control else ""
    if control and control in order:
        stats_rows.extend(
            [
                dunnett_vs_control(
                    ratio,
                    "k4m_k100lv_ratio",
                    "formulation_group",
                    control_group=control,
                    analysis_label="Fig. 5a K4M/K100LV ratio versus control",
                    order=order,
                    replicate_definition="Each point is one independently recommended or measured formulation replicate.",
                ),
                dunnett_vs_control(
                    release_auc,
                    "relative_early_release",
                    "formulation_group",
                    control_group=control,
                    analysis_label="Fig. 5b relative early release versus control",
                    order=order,
                    replicate_definition="Each point is one independent UV-release replicate summarized as AUC0-4h/AUC0-8h.",
                ),
            ]
        )
    if control and control in fig5b_order:
        fig5b_stats_rows.append(
            dunnett_vs_control(
                file_auc,
                "relative_early_release_mean_curve",
                "formulation_group",
                control_group=control,
                analysis_label="Fig. 5b file-level relative early release versus control",
                order=fig5b_order,
                replicate_definition=(
                    "Each point is one independent Excel record file after averaging the three "
                    "technical UV measurement columns within that file."
                ),
            )
        )
    save_table(pd.concat(stats_rows, ignore_index=True), stats_dir / "fig5_optimized_formulation_validation_stats.csv")
    save_table(pd.concat(fig5b_stats_rows, ignore_index=True), stats_dir / "fig5b_relative_early_release_stats.csv")


if __name__ == "__main__":
    main()
