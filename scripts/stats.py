"""Statistical analysis helpers with CSV-friendly outputs."""

from __future__ import annotations

from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def group_summary(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    order: list[str] | None = None,
) -> pd.DataFrame:
    clean = df[[group_col, value_col]].dropna()
    summary = (
        clean.groupby(group_col, observed=False)[value_col]
        .agg(
            n="count",
            mean="mean",
            sd=lambda x: x.std(ddof=1),
            median="median",
            q1=lambda x: x.quantile(0.25),
            q3=lambda x: x.quantile(0.75),
        )
        .reset_index()
    )
    if order:
        summary[group_col] = pd.Categorical(summary[group_col], categories=order, ordered=True)
        summary = summary.sort_values(group_col).reset_index(drop=True)
        summary[group_col] = summary[group_col].astype(str)
    return summary


def _ordered_groups(df: pd.DataFrame, group_col: str, order: list[str] | None) -> list[str]:
    present = [g for g in (order or []) if g in set(df[group_col].dropna())]
    extras = sorted([g for g in df[group_col].dropna().unique() if g not in present])
    return present + extras


def _group_ns(clean: pd.DataFrame, group_col: str, value_col: str, groups: list[str]) -> str:
    parts = []
    for group in groups:
        n = int(clean.loc[clean[group_col] == group, value_col].dropna().shape[0])
        parts.append(f"{group}: n={n}")
    return "; ".join(parts)


def normality_report(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    order: list[str] | None = None,
) -> pd.DataFrame:
    clean = df[[group_col, value_col]].dropna()
    rows = []
    for group in _ordered_groups(clean, group_col, order):
        values = clean.loc[clean[group_col] == group, value_col].astype(float).to_numpy()
        if len(values) >= 3:
            stat, p_value = stats.shapiro(values)
            note = ""
        else:
            stat, p_value = np.nan, np.nan
            note = "Shapiro-Wilk not run because n < 3."
        rows.append(
            {
                "group": group,
                "n": len(values),
                "test": "Shapiro-Wilk",
                "statistic": stat,
                "p_value": p_value,
                "notes": note,
            }
        )
    return pd.DataFrame(rows)


def one_way_test(
    df: pd.DataFrame,
    value_col: str,
    group_col: str,
    analysis_label: str,
    order: list[str] | None = None,
    replicate_definition: str = "Each point is one independent replicate.",
    preferred: str = "auto",
    alpha: float = 0.05,
    dunn_adjust: str = "holm",
) -> pd.DataFrame:
    """Run one-way ANOVA/Tukey or Kruskal-Wallis/Dunn and return tidy rows."""
    clean = df[[group_col, value_col]].dropna().copy()
    clean[value_col] = pd.to_numeric(clean[value_col], errors="coerce")
    clean = clean.dropna()
    groups = _ordered_groups(clean, group_col, order)
    samples = [clean.loc[clean[group_col] == group, value_col].to_numpy(float) for group in groups]
    n_total = int(sum(len(sample) for sample in samples))
    ns = _group_ns(clean, group_col, value_col, groups)

    base = {
        "analysis": analysis_label,
        "value": value_col,
        "group": group_col,
        "n_total": n_total,
        "group_ns": ns,
        "replicate_definition": replicate_definition,
    }

    if len(groups) < 2 or any(len(sample) < 2 for sample in samples):
        return pd.DataFrame(
            [
                {
                    **base,
                    "test": "not run",
                    "comparison": "overall",
                    "statistic": np.nan,
                    "p_value": np.nan,
                    "p_adjusted": np.nan,
                    "correction": "",
                    "notes": "At least two groups with n >= 2 are required.",
                }
            ]
        )

    norm = normality_report(clean, group_col, value_col, order=groups)
    normal_ok = bool(norm["p_value"].dropna().ge(alpha).all()) and norm["p_value"].notna().all()
    levene_stat, levene_p = stats.levene(*samples, center="median")
    variance_ok = bool(levene_p >= alpha)
    assumption_rows = []
    for _, row in norm.iterrows():
        assumption_rows.append(
            {
                **base,
                "test": "Shapiro-Wilk normality check",
                "comparison": row["group"],
                "statistic": row["statistic"],
                "p_value": row["p_value"],
                "p_adjusted": np.nan,
                "correction": "",
                "notes": row["notes"],
            }
        )
    assumption_rows.append(
        {
            **base,
            "test": "Levene variance check",
            "comparison": "all groups",
            "statistic": levene_stat,
            "p_value": levene_p,
            "p_adjusted": np.nan,
            "correction": "",
            "notes": "Median-centered Levene test used for variance check.",
        }
    )

    if preferred == "anova" or (preferred == "auto" and normal_ok and variance_ok):
        overall_test = "One-way ANOVA"
        overall_stat, overall_p = stats.f_oneway(*samples)
        overall_note = (
            f"Auto-selected parametric test. Levene p={levene_p:.6g}."
            if preferred == "auto"
            else f"Parametric test requested. Levene p={levene_p:.6g}."
        )
        rows = [
            {
                **base,
                "test": overall_test,
                "comparison": "overall",
                "statistic": overall_stat,
                "p_value": overall_p,
                "p_adjusted": np.nan,
                "correction": "",
                "notes": overall_note,
            }
        ]
        if len(groups) > 2:
            tukey = pairwise_tukeyhsd(endog=clean[value_col], groups=clean[group_col], alpha=alpha)
            table = pd.DataFrame(tukey._results_table.data[1:], columns=tukey._results_table.data[0])
            for _, row in table.iterrows():
                rows.append(
                    {
                        **base,
                        "test": "Tukey HSD",
                        "comparison": f"{row['group1']} vs {row['group2']}",
                        "statistic": row["meandiff"],
                        "p_value": np.nan,
                        "p_adjusted": float(row["p-adj"]),
                        "correction": "Tukey HSD family-wise correction",
                        "notes": f"reject={bool(row['reject'])}; lower={row['lower']}; upper={row['upper']}",
                    }
                )
        return pd.DataFrame(assumption_rows + rows)

    overall_stat, overall_p = stats.kruskal(*samples)
    rows = [
        {
            **base,
            "test": "Kruskal-Wallis",
            "comparison": "overall",
            "statistic": overall_stat,
            "p_value": overall_p,
            "p_adjusted": np.nan,
            "correction": "",
            "notes": (
                "Auto-selected non-parametric test because normality or variance "
                f"assumptions were not supported. Levene p={levene_p:.6g}."
            ),
        }
    ]
    if len(groups) > 2:
        try:
            import scikit_posthocs as sp

            pmat = sp.posthoc_dunn(clean, val_col=value_col, group_col=group_col, p_adjust=dunn_adjust)
            for group_a, group_b in combinations(groups, 2):
                rows.append(
                    {
                        **base,
                        "test": "Dunn post hoc",
                        "comparison": f"{group_a} vs {group_b}",
                        "statistic": np.nan,
                        "p_value": np.nan,
                        "p_adjusted": float(pmat.loc[group_a, group_b]),
                        "correction": f"Dunn test with {dunn_adjust} correction",
                        "notes": "",
                    }
                )
        except Exception as exc:  # pragma: no cover - depends on optional package behavior
            rows.append(
                {
                    **base,
                    "test": "Dunn post hoc",
                    "comparison": "all pairwise",
                    "statistic": np.nan,
                    "p_value": np.nan,
                    "p_adjusted": np.nan,
                    "correction": f"Dunn test with {dunn_adjust} correction",
                    "notes": f"Post hoc test failed: {exc}",
                }
            )
    return pd.DataFrame(assumption_rows + rows)


def dunnett_vs_control(
    df: pd.DataFrame,
    value_col: str,
    group_col: str,
    control_group: str,
    analysis_label: str,
    order: list[str] | None = None,
    replicate_definition: str = "Each point is one independent replicate.",
) -> pd.DataFrame:
    """Run Dunnett's test versus a control if SciPy provides it."""
    clean = df[[group_col, value_col]].dropna().copy()
    clean[value_col] = pd.to_numeric(clean[value_col], errors="coerce")
    clean = clean.dropna()
    groups = [g for g in _ordered_groups(clean, group_col, order) if g != control_group]
    control = clean.loc[clean[group_col] == control_group, value_col].to_numpy(float)
    base = {
        "analysis": analysis_label,
        "value": value_col,
        "group": group_col,
        "n_total": len(clean),
        "group_ns": _group_ns(clean, group_col, value_col, [control_group] + groups),
        "replicate_definition": replicate_definition,
    }
    if len(control) < 2 or not groups:
        return pd.DataFrame(
            [
                {
                    **base,
                    "test": "Dunnett",
                    "comparison": "all vs control",
                    "statistic": np.nan,
                    "p_value": np.nan,
                    "p_adjusted": np.nan,
                    "correction": "Dunnett multiple comparisons versus control",
                    "notes": "Control group with n >= 2 and at least one comparison group are required.",
                }
            ]
        )
    try:
        from scipy.stats import dunnett

        samples = [clean.loc[clean[group_col] == group, value_col].to_numpy(float) for group in groups]
        result = dunnett(*samples, control=control)
        rows = []
        for idx, group in enumerate(groups):
            rows.append(
                {
                    **base,
                    "test": "Dunnett",
                    "comparison": f"{group} vs {control_group}",
                    "statistic": float(result.statistic[idx]),
                    "p_value": np.nan,
                    "p_adjusted": float(result.pvalue[idx]),
                    "correction": "Dunnett multiple comparisons versus control",
                    "notes": "",
                }
            )
        return pd.DataFrame(rows)
    except Exception as exc:  # pragma: no cover - SciPy version dependent
        return pd.DataFrame(
            [
                {
                    **base,
                    "test": "Dunnett",
                    "comparison": "all vs control",
                    "statistic": np.nan,
                    "p_value": np.nan,
                    "p_adjusted": np.nan,
                    "correction": "Dunnett multiple comparisons versus control",
                    "notes": f"Dunnett test unavailable or failed: {exc}",
                }
            ]
        )


def mixed_effects_timecourse(
    df: pd.DataFrame,
    value_col: str,
    group_col: str,
    time_col: str,
    subject_col: str,
    analysis_label: str,
    replicate_definition: str,
) -> pd.DataFrame:
    """Fit a random-intercept mixed model for repeated time-course data."""
    clean = df[[value_col, group_col, time_col, subject_col]].dropna().copy()
    base = {
        "analysis": analysis_label,
        "value": value_col,
        "group": group_col,
        "n_total": len(clean),
        "group_ns": _group_ns(clean, group_col, value_col, _ordered_groups(clean, group_col, None)),
        "replicate_definition": replicate_definition,
    }
    if clean[subject_col].nunique() < 2 or clean[group_col].nunique() < 2:
        return pd.DataFrame(
            [
                {
                    **base,
                    "test": "linear mixed-effects model",
                    "comparison": "fixed effects",
                    "statistic": np.nan,
                    "p_value": np.nan,
                    "p_adjusted": np.nan,
                    "correction": "",
                    "notes": "At least two subjects and two groups are required.",
                }
            ]
        )
    try:
        import statsmodels.formula.api as smf

        formula = f"{value_col} ~ C({group_col}) * C({time_col})"
        model = smf.mixedlm(formula, clean, groups=clean[subject_col])
        fit = model.fit(reml=False, method="lbfgs")
        rows = []
        for term in fit.params.index:
            rows.append(
                {
                    **base,
                    "test": "linear mixed-effects model",
                    "comparison": term,
                    "statistic": float(fit.tvalues.get(term, np.nan)),
                    "p_value": float(fit.pvalues.get(term, np.nan)),
                    "p_adjusted": np.nan,
                    "correction": "",
                    "notes": "Random intercept by subject/sample; Wald z/t statistic reported.",
                }
            )
        return pd.DataFrame(rows)
    except Exception as exc:  # pragma: no cover - data dependent
        return pd.DataFrame(
            [
                {
                    **base,
                    "test": "linear mixed-effects model",
                    "comparison": "fixed effects",
                    "statistic": np.nan,
                    "p_value": np.nan,
                    "p_adjusted": np.nan,
                    "correction": "",
                    "notes": f"Model fitting failed: {exc}",
                }
            ]
        )


def trapezoid_auc(
    x: np.ndarray,
    y: np.ndarray,
    start: float | None = None,
    end: float | None = None,
) -> float:
    """Compute trapezoidal AUC, interpolating exact boundaries when requested."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    order = np.argsort(x)
    x = x[order]
    y = y[order]
    valid = ~(np.isnan(x) | np.isnan(y))
    x = x[valid]
    y = y[valid]
    if len(x) < 2:
        return np.nan
    if start is not None:
        if x.min() > start or x.max() < start:
            return np.nan
        y_start = np.interp(start, x, y)
        mask = x >= start
        x = np.r_[start, x[mask]]
        y = np.r_[y_start, y[mask]]
    if end is not None:
        if x.min() > end or x.max() < end:
            return np.nan
        y_end = np.interp(end, x, y)
        mask = x <= end
        x = np.r_[x[mask], end]
        y = np.r_[y[mask], y_end]
    unique_x, unique_idx = np.unique(x, return_index=True)
    x = unique_x
    y = y[unique_idx]
    if len(x) < 2:
        return np.nan
    if hasattr(np, "trapezoid"):
        return float(np.trapezoid(y, x))
    return float(np.trapz(y, x))
