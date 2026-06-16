"""Input/output and validation helpers for reproducible figure scripts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_table(path: str | Path, sheet_name: str | int | None = None) -> pd.DataFrame:
    """Load a CSV or Excel table without modifying the source file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input table not found: {path}")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet_name if sheet_name is not None else 0)
    raise ValueError(f"Unsupported table format for {path}. Use CSV, XLSX, or XLS.")


def save_table(df: pd.DataFrame, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def save_source_copy(df: pd.DataFrame, path: str | Path) -> Path:
    """Save the exact loaded source table as CSV for figure reproducibility."""
    return save_table(df.copy(), path)


def require_columns(df: pd.DataFrame, required: Iterable[str], dataset_name: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            f"{dataset_name} is missing required column(s): {', '.join(missing)}"
        )


def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    n_rows = len(df)
    rows = []
    for col in df.columns:
        missing_n = int(df[col].isna().sum())
        rows.append(
            {
                "column": col,
                "missing_n": missing_n,
                "missing_pct": (missing_n / n_rows * 100.0) if n_rows else 0.0,
            }
        )
    return pd.DataFrame(rows)


def replicate_count_report(
    df: pd.DataFrame,
    group_cols: list[str],
    replicate_col: str | None = None,
) -> pd.DataFrame:
    require_columns(df, group_cols, "replicate count input")
    grouped = df.groupby(group_cols, dropna=False)
    report = grouped.size().reset_index(name="n_rows")
    if replicate_col and replicate_col in df.columns:
        reps = grouped[replicate_col].nunique(dropna=True).reset_index(name="n_replicates")
        report = report.merge(reps, on=group_cols, how="left")
    return report


def _alias_key(value: object) -> str:
    text = "" if pd.isna(value) else str(value).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text


def standardize_category_names(
    df: pd.DataFrame,
    column: str,
    aliases: dict[str, str],
    dataset_name: str,
) -> pd.DataFrame:
    """Standardize known names while preserving unknown labels for transparency."""
    require_columns(df, [column], dataset_name)
    alias_lookup = {_alias_key(k): v for k, v in aliases.items()}
    out = df.copy()
    out[column] = out[column].map(
        lambda value: alias_lookup.get(
            _alias_key(value), value if pd.isna(value) else str(value).strip()
        )
    )
    return out


def write_qc_reports(
    df: pd.DataFrame,
    outdir: str | Path,
    prefix: str,
    group_cols: list[str] | None = None,
    replicate_col: str | None = None,
) -> None:
    outdir = ensure_dir(outdir)
    save_table(missing_value_report(df), outdir / f"{prefix}_missing_values.csv")
    if group_cols:
        save_table(
            replicate_count_report(df, group_cols, replicate_col=replicate_col),
            outdir / f"{prefix}_replicate_counts.csv",
        )

