#!/usr/bin/env python3
"""Batch-analyze local model output files and generate comparison reports."""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from collections import Counter
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile


CANONICAL_DIMENSIONS = {
    "color_change": ["color change", "color", "颜色", "色泽"],
    "shape_change": ["shape change", "shape", "形态", "形状"],
    "surface_texture_change": [
        "surface texture change",
        "surface texture",
        "texture",
        "表面纹理",
        "表面质地",
    ],
    "volume_change": ["volume change", "volume", "体积", "厚度"],
    "dissolution_speed_time": [
        "dissolution speed and time",
        "dissolution speed",
        "disintegration / dissolution speed",
        "速度",
        "时间",
    ],
    "physical_state_change": ["physical state change", "physical state", "物理状态"],
    "dissolution_medium": ["dissolution medium", "medium", "介质"],
    "fragment_distribution_density": [
        "fragment distribution with density",
        "fragment distribution",
        "density",
        "碎片分布",
        "密度",
    ],
}

DIMENSION_LABELS = {
    "color_change": "Color Change",
    "shape_change": "Shape Change",
    "surface_texture_change": "Surface Texture Change",
    "volume_change": "Volume Change",
    "dissolution_speed_time": "Dissolution Speed and Time",
    "physical_state_change": "Physical State Change",
    "dissolution_medium": "Dissolution Medium",
    "fragment_distribution_density": "Fragment Distribution with Density",
}

SECTION_KEYWORDS = {
    "experiment_setup": [
        "step 1",
        "experimental background",
        "experiment config (json)",
        "experiment_config",
    ],
    "image_analysis": [
        "step 2",
        "single-set image analysis",
        "eight_dimension_description",
    ],
    "mechanism": [
        "step 3",
        "mechanistic analysis",
        "mechanistic interpretation",
        "mechanism",
    ],
    "final_report": [
        "final report",
        "verdict:",
        "overall judgment",
        "总体判断",
    ],
}

KNOWN_VIEW_TOKENS = {"side", "top", "front", "back", "bottom"}

GENERIC_RESULT_BASENAMES = {
    "compare_answer",
    "compare_report",
    "final_answer",
    "final_report",
    "answer",
    "report",
}

PREFERRED_CASE_OUTPUTS = [
    ("compare_answer", ".md"),
    ("compare_report", ".docx"),
    ("compare_report", ".md"),
    ("final_report", ".docx"),
    ("final_report", ".md"),
    ("final_answer", ".md"),
    ("answer", ".md"),
    ("report", ".docx"),
    ("report", ".md"),
]

TEXT_REPLACEMENTS = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2212": "-",
    "\u3000": " ",
}

EXPERIMENT_CONFIG_FIELDS = [
    "drug_1_name",
    "drug_2_name",
    "medium_pH",
    "temperature_C",
    "total_duration_hours",
    "time_interval_hours",
    "other_conditions",
]

GENERIC_DIMENSION_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"no obvious change",
        r"no clear change",
        r"remains (?:the )?same",
        r"similar to (?:the )?previous",
        r"overall unchanged",
        r"无明显变化",
        r"基本一致",
        r"变化不大",
    ]
]

REASON_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bbecause\b",
        r"\btherefore\b",
        r"\bindicates?\b",
        r"\bsuggests?\b",
        r"\basis\b",
        r"原因",
        r"依据",
        r"说明",
        r"提示",
    ]
]

KNOWN_MODEL_PATTERNS = {
    "claude": "Claude",
    "gpt": "GPT",
    "chatgpt": "ChatGPT",
    "gemini": "Gemini",
    "deepseek": "DeepSeek",
    "qwen": "Qwen",
    "kimi": "Kimi",
    "doubao": "Doubao",
    "ernie": "ERNIE",
    "llama": "LLaMA",
}

STRUCTURED_REFERENCE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bdoi[:\s]",
        r"\bpmid[:\s]",
        r"\bet al\.",
        r"\b\d{4}\b",
        r"\[[0-9,\-\s]+\]",
    ]
]

REFERENCE_TRACE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\brefs?:",
        r"\bcitation",
        r"\bliterature",
        r"\bretrieval evidence",
        r"\breview",
        r"参考",
        r"文献",
        r"引用",
    ]
]


FILE_LEVEL_COLUMNS = [
    "relative_path",
    "file_name",
    "extension",
    "status",
    "read_error",
    "size_bytes",
    "drug_root_label",
    "primary_drug_label",
    "primary_pH_label",
    "condition_folder",
    "view_folder",
    "variant_label",
    "model_label",
    "model_label_source",
    "model_bucket",
    "comparison_pair_id",
    "reference_manufacturer_label",
    "manufacturer_label",
    "reference_batch_label",
    "comparison_batch_label",
    "batch_pair",
    "comparison_scope",
    "sample_replicate_id",
    "left_replicate_id",
    "right_replicate_id",
    "repeat_group_base_key",
    "repeat_group_model_key",
    "repeat_observation_key",
    "repeat_group_complete",
    "repeat_group_consistency_status",
    "repeat_group_consensus_verdict",
    "potential_error_label",
    "left_product_name",
    "left_manufacturer_label",
    "left_batch_label",
    "right_product_name",
    "right_manufacturer_label",
    "right_batch_label",
    "manufacturer_pair",
    "verdict",
    "verdict_raw",
    "char_count",
    "word_count",
    "has_experiment_section",
    "experiment_fields_expected",
    "experiment_fields_present",
    "experiment_completeness_pct",
    "experiment_time_interval_present",
    "experiment_other_conditions_present",
    "has_image_analysis_section",
    "image_analysis_block_count",
    "dimension_coverage_count",
    "dimension_coverage_pct",
    "dimension_avg_words",
    "dimension_generic_count",
    "dimension_duplicate_count",
    "dimension_detail_score_pct",
    "has_mechanism_section",
    "mechanism_hypothesis_count",
    "mechanism_follow_up_item_count",
    "mechanism_evidence_trace_count",
    "reference_trace_level",
    "possible_placeholder_reference",
    "mechanism_score_pct",
    "reference_verify_placeholder",
    "has_final_report_section",
    "comparison_table_present",
    "comparison_table_rows",
    "reason_keyword_count",
    "evidence_link_count",
    "judgment_basis_clear",
    "reasoning_score_pct",
    "structural_completeness_pct",
    "overall_quality_score_pct",
    "bert_score_mode",
    "bert_score_status",
    "bert_reference_key",
    "bert_reference_source",
    "bert_reference_count",
    "bert_precision_pct",
    "bert_recall_pct",
    "bert_f1_pct",
]

SUMMARY_COLUMNS = [
    "group_type",
    "group_value",
    "file_count",
    "supported_count",
    "unsupported_count",
    "verdict_same_count",
    "verdict_different_count",
    "verdict_unknown_count",
    "avg_experiment_completeness_pct",
    "avg_dimension_coverage_pct",
    "avg_dimension_detail_score_pct",
    "avg_mechanism_score_pct",
    "avg_reasoning_score_pct",
    "avg_structural_completeness_pct",
    "avg_overall_quality_score_pct",
    "comparison_table_rate_pct",
    "reference_trace_rate_pct",
    "placeholder_reference_rate_pct",
    "repeat_group_count",
    "complete_repeat_group_count",
    "consistent_repeat_group_count",
    "inconsistent_repeat_group_count",
    "potential_false_positive_count",
    "potential_false_negative_count",
    "repeat_consistency_rate_pct",
    "bert_scored_count",
    "avg_bert_f1_pct",
]

MODEL_COMPARISON_COLUMNS = [
    "model_bucket",
    "file_count",
    "supported_count",
    "mapped_model_label_count",
    "avg_overall_quality_score_pct",
    "avg_dimension_coverage_pct",
    "avg_mechanism_score_pct",
    "avg_reasoning_score_pct",
    "avg_experiment_completeness_pct",
    "verdict_same_rate_pct",
    "placeholder_reference_rate_pct",
    "avg_comparison_table_rows",
    "repeat_group_count",
    "complete_repeat_group_count",
    "consistent_repeat_group_count",
    "inconsistent_repeat_group_count",
    "potential_false_positive_count",
    "potential_false_negative_count",
    "repeat_consistency_rate_pct",
    "bert_scored_count",
    "avg_bert_precision_pct",
    "avg_bert_recall_pct",
    "avg_bert_f1_pct",
    "quality_rank",
]

BERT_SCORE_STATS_COLUMNS = [
    "group_type",
    "group_value",
    "supported_count",
    "bert_scored_count",
    "bert_available_rate_pct",
    "avg_bert_precision_pct",
    "avg_bert_recall_pct",
    "avg_bert_f1_pct",
    "bert_status_summary",
]

VERDICT_STATS_COLUMNS = [
    "group_type",
    "group_value",
    "same_count",
    "different_count",
    "unknown_count",
    "total_count",
    "same_ratio",
    "different_ratio",
    "unknown_ratio",
]

DRUG_PH_VERDICT_COLUMNS = [
    "primary_drug_label",
    "primary_pH_label",
    "model_bucket",
    "same_count",
    "different_count",
    "unknown_count",
    "total_count",
    "same_ratio",
    "different_ratio",
    "unknown_ratio",
    "repeat_group_count",
    "inconsistent_repeat_group_count",
]

REPLICATE_CONSISTENCY_COLUMNS = [
    "model_bucket",
    "primary_drug_label",
    "primary_pH_label",
    "reference_manufacturer_label",
    "manufacturer_label",
    "manufacturer_pair",
    "batch_pair",
    "comparison_scope",
    "repeat_group_base_key",
    "repeat_group_model_key",
    "replicate_count",
    "complete_replicate_group",
    "replicate_ids",
    "replicate_1_verdict",
    "replicate_2_verdict",
    "replicate_3_verdict",
    "replicate_1_path",
    "replicate_2_path",
    "replicate_3_path",
    "consistency_status",
    "consensus_verdict",
    "same_count",
    "different_count",
    "unknown_count",
    "potential_false_positive_count",
    "potential_false_negative_count",
    "potential_error_replicates",
    "manual_review_flag",
]

POTENTIAL_ERROR_SUMMARY_COLUMNS = [
    "summary_scope",
    "model_bucket",
    "primary_drug_label",
    "primary_pH_label",
    "reference_manufacturer_label",
    "manufacturer_label",
    "manufacturer_pair",
    "batch_pair",
    "comparison_scope",
    "repeat_group_total",
    "complete_repeat_group_count",
    "consistent_group_count",
    "inconsistent_group_count",
    "ambiguous_group_count",
    "potential_false_positive_count",
    "potential_false_negative_count",
    "consistency_rate_pct",
    "inconsistency_rate_pct",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan a folder recursively, parse local model result files, and "
            "generate an overall Markdown report plus CSV statistics."
        )
    )
    parser.add_argument("source_dir", help="Folder to scan recursively.")
    parser.add_argument(
        "--output-dir",
        help="Directory for generated report files. Defaults to <source_dir>/_batch_analysis.",
    )
    parser.add_argument(
        "--model-map",
        help=(
            "Optional CSV or JSON file describing regex-based path mapping to "
            "model labels."
        ),
    )
    parser.add_argument(
        "--reference-audit-mode",
        choices=["trace", "verify"],
        default="trace",
        help=(
            "trace: extract citation traces only. "
            "verify: reserved placeholder for future network-backed checks."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional cap on eligible files for smoke tests.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-file progress.",
    )
    parser.add_argument(
        "--error-analysis-mode",
        choices=["repeat_proxy", "ground_truth"],
        default="repeat_proxy",
        help=(
            "repeat_proxy: use replicate-consistency proxy analysis. "
            "ground_truth: reserved for future truth-labeled strict FP/FN analysis."
        ),
    )
    parser.add_argument(
        "--ground-truth-file",
        help="Reserved placeholder for future truth-labeled strict FP/FN analysis.",
    )
    parser.add_argument(
        "--bert-score-mode",
        choices=["off", "consensus", "reference_file"],
        default="off",
        help=(
            "off: skip BERTScore. consensus: compare each result against other "
            "models for the same case. reference_file: compare against an external "
            "reference CSV/JSON."
        ),
    )
    parser.add_argument(
        "--bert-reference-file",
        help=(
            "CSV or JSON file for --bert-score-mode reference_file. CSV should "
            "include reference_key or comparison_pair_id plus reference_text."
        ),
    )
    parser.add_argument(
        "--bert-model",
        default="",
        help="Optional BERTScore model_type passed to bert_score.score.",
    )
    parser.add_argument(
        "--bert-lang",
        default="zh",
        help="Language code passed to bert_score.score when --bert-model is omitted.",
    )
    parser.add_argument(
        "--bert-max-chars",
        type=int,
        default=4000,
        help="Maximum characters from candidate/reference text used for BERTScore.",
    )
    parser.add_argument(
        "--bert-rescale-with-baseline",
        action="store_true",
        help="Pass rescale_with_baseline=True to BERTScore.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.error_analysis_mode == "ground_truth":
        raise SystemExit(
            "ground_truth mode is reserved for a future release. "
            "Use --error-analysis-mode repeat_proxy in v1."
        )
    source_dir = Path(args.source_dir).expanduser().resolve()
    if not source_dir.exists():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else source_dir / "_batch_analysis"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    model_rules = load_model_rules(args.model_map)
    run_started = datetime.now()

    scan = scan_source_directory(
        source_dir=source_dir,
        output_dir=output_dir,
        limit=args.limit,
        verbose=args.verbose,
    )
    records: list[dict[str, Any]] = []
    for file_meta in scan["eligible_files"]:
        record = analyze_file(
            file_meta=file_meta,
            source_dir=source_dir,
            model_rules=model_rules,
            reference_audit_mode=args.reference_audit_mode,
        )
        records.append(record)
        if args.verbose:
            print(f"[{record['status']}] {record['relative_path']}")

    apply_bert_scores(
        records=records,
        mode=args.bert_score_mode,
        reference_file=args.bert_reference_file,
        model_type=args.bert_model,
        lang=args.bert_lang,
        max_chars=args.bert_max_chars,
        rescale_with_baseline=args.bert_rescale_with_baseline,
    )
    initialize_repeat_defaults(records)
    replicate_rows, record_annotations = build_replicate_consistency_rows(
        records=records,
        error_analysis_mode=args.error_analysis_mode,
    )
    apply_record_annotations(records, record_annotations)

    summary_rows = build_summary_rows(records, replicate_rows)
    model_rows = build_model_comparison_rows(records, replicate_rows)
    verdict_rows = build_verdict_stats_rows(records)
    drug_ph_rows = build_drug_ph_verdict_rows(records, replicate_rows)
    potential_error_rows = build_potential_error_summary_rows(replicate_rows)
    bert_score_rows = build_bert_score_rows(records)

    report_path = output_dir / "OVERALL_REPORT.md"
    summary_path = output_dir / "SUMMARY_STATS.csv"
    file_index_path = output_dir / "FILE_LEVEL_INDEX.csv"
    model_comparison_path = output_dir / "MODEL_COMPARISON.csv"
    verdict_stats_path = output_dir / "VERDICT_STATS.csv"
    drug_ph_stats_path = output_dir / "DRUG_PH_VERDICT_STATS.csv"
    replicate_consistency_path = output_dir / "REPLICATE_CONSISTENCY.csv"
    potential_error_path = output_dir / "POTENTIAL_ERROR_SUMMARY.csv"
    bert_score_path = output_dir / "BERT_SCORE_STATS.csv"
    dimension_chart_path = output_dir / "DIMENSION_COVERAGE_BY_MODEL.svg"
    consistency_chart_path = output_dir / "REPEAT_CONSISTENCY_BY_MODEL.svg"
    bert_chart_path = output_dir / "BERT_SCORE_BY_MODEL.svg"

    write_csv(file_index_path, records, FILE_LEVEL_COLUMNS)
    write_csv(summary_path, summary_rows, SUMMARY_COLUMNS)
    write_csv(model_comparison_path, model_rows, MODEL_COMPARISON_COLUMNS)
    write_csv(verdict_stats_path, verdict_rows, VERDICT_STATS_COLUMNS)
    write_csv(drug_ph_stats_path, drug_ph_rows, DRUG_PH_VERDICT_COLUMNS)
    write_csv(replicate_consistency_path, replicate_rows, REPLICATE_CONSISTENCY_COLUMNS)
    write_csv(potential_error_path, potential_error_rows, POTENTIAL_ERROR_SUMMARY_COLUMNS)
    write_csv(bert_score_path, bert_score_rows, BERT_SCORE_STATS_COLUMNS)
    write_model_charts(
        dimension_chart_path=dimension_chart_path,
        consistency_chart_path=consistency_chart_path,
        bert_chart_path=bert_chart_path,
        model_rows=model_rows,
    )
    write_report(
        report_path=report_path,
        source_dir=source_dir,
        output_dir=output_dir,
        records=records,
        summary_rows=summary_rows,
        model_rows=model_rows,
        verdict_rows=verdict_rows,
        drug_ph_rows=drug_ph_rows,
        replicate_rows=replicate_rows,
        potential_error_rows=potential_error_rows,
        bert_score_rows=bert_score_rows,
        chart_paths=[dimension_chart_path, consistency_chart_path, bert_chart_path],
        scan=scan,
        run_started=run_started,
        reference_audit_mode=args.reference_audit_mode,
        error_analysis_mode=args.error_analysis_mode,
        bert_score_mode=args.bert_score_mode,
    )

    print(f"Generated: {report_path}")
    print(f"Generated: {summary_path}")
    print(f"Generated: {file_index_path}")
    print(f"Generated: {model_comparison_path}")
    print(f"Generated: {verdict_stats_path}")
    print(f"Generated: {drug_ph_stats_path}")
    print(f"Generated: {replicate_consistency_path}")
    print(f"Generated: {potential_error_path}")
    print(f"Generated: {bert_score_path}")
    print(f"Generated: {dimension_chart_path}")
    print(f"Generated: {consistency_chart_path}")
    print(f"Generated: {bert_chart_path}")
    return 0


def scan_source_directory(
    source_dir: Path,
    output_dir: Path,
    limit: int,
    verbose: bool,
) -> dict[str, Any]:
    eligible_extensions = {".docx", ".doc", ".md"}
    all_files = 0
    eligible_candidates: list[dict[str, Any]] = []
    ignored_by_extension: Counter[str] = Counter()

    for path in source_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            relative_to_output = path.resolve().relative_to(output_dir.resolve())
            if relative_to_output:
                continue
        except ValueError:
            pass
        if path.name.startswith("~$"):
            continue
        all_files += 1
        suffix = path.suffix.lower()
        if suffix not in eligible_extensions:
            ignored_by_extension[suffix or "<no_extension>"] += 1
            continue
        eligible_candidates.append(
            {
                "absolute_path": path,
                "relative_path": path.resolve().relative_to(source_dir).as_posix(),
                "file_name": path.name,
                "suffix": suffix,
                "size_bytes": path.stat().st_size,
            }
        )
    eligible_files = select_preferred_outputs(eligible_candidates)
    if limit:
        eligible_files = eligible_files[:limit]

    if verbose:
        print(f"Scanned {all_files} files; eligible={len(eligible_files)}.")
    return {
        "all_files_seen": all_files,
        "eligible_files": eligible_files,
        "ignored_by_extension": ignored_by_extension,
    }


def analyze_file(
    file_meta: dict[str, Any],
    source_dir: Path,
    model_rules: list[dict[str, Any]],
    reference_audit_mode: str,
) -> dict[str, Any]:
    path = Path(file_meta["absolute_path"])
    text_result = read_supported_text(path)
    record: dict[str, Any] = {
        "relative_path": file_meta["relative_path"],
        "file_name": file_meta["file_name"],
        "extension": file_meta["suffix"],
        "size_bytes": file_meta["size_bytes"],
        "status": text_result["status"],
        "read_error": text_result.get("error", ""),
        "reference_audit_mode": reference_audit_mode,
    }

    path_meta = extract_path_metadata(path=path, source_dir=source_dir)
    record.update(path_meta)

    if text_result["status"] != "ok":
        fill_empty_metrics(record)
        return record

    text = normalize_text(text_result["text"])
    record["_analysis_text"] = text
    analysis = analyze_text_payload(
        text=text,
        relative_path=file_meta["relative_path"],
        path_meta=path_meta,
        model_rules=model_rules,
        reference_audit_mode=reference_audit_mode,
    )
    record.update(analysis)
    return record


def read_supported_text(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        try:
            return {"status": "ok", "text": read_docx_text(path)}
        except (BadZipFile, ET.ParseError, OSError, KeyError, ValueError) as exc:
            return {"status": "parse_error", "error": str(exc), "text": ""}
    if suffix == ".md":
        try:
            return {"status": "ok", "text": read_markdown_text(path)}
        except OSError as exc:
            return {"status": "parse_error", "error": str(exc), "text": ""}
    if suffix == ".doc":
        return {
            "status": "unsupported",
            "error": (
                "Legacy .doc binary skipped in v1 to avoid unsafe or lossy "
                "extraction without a dedicated parser."
            ),
            "text": "",
        }
    return {"status": "ignored", "error": "", "text": ""}


def read_docx_text(path: Path) -> str:
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with ZipFile(path) as archive:
        xml_bytes = archive.read("word/document.xml")
    root = ET.fromstring(xml_bytes)
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", namespace):
        text_nodes = [node.text for node in paragraph.findall(".//w:t", namespace) if node.text]
        if not text_nodes:
            continue
        joined = "".join(text_nodes).strip()
        if joined:
            paragraphs.append(joined)
    return "\n".join(paragraphs)


def read_markdown_text(path: Path) -> str:
    encodings = ["utf-8", "utf-8-sig", "gb18030", "gbk", "latin-1"]
    last_error: Exception | None = None
    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    if last_error:
        raise last_error
    return path.read_text()


def normalize_text(text: str) -> str:
    for old, new in TEXT_REPLACEMENTS.items():
        text = text.replace(old, new)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def analyze_text_payload(
    text: str,
    relative_path: str,
    path_meta: dict[str, Any],
    model_rules: list[dict[str, Any]],
    reference_audit_mode: str,
) -> dict[str, Any]:
    lowered = text.lower()
    sections_present = {
        name: any(keyword in lowered for keyword in keywords)
        for name, keywords in SECTION_KEYWORDS.items()
    }
    experiment_config = extract_experiment_config(text)
    image_blocks = extract_image_analysis_blocks(text)
    mechanism_section = extract_mechanism_section(text)
    final_section = extract_final_section(text)
    verdict, verdict_raw = extract_verdict(final_section or text)
    dimension_metrics = compute_dimension_metrics(image_blocks=image_blocks, text=text)
    mechanism_metrics = compute_mechanism_metrics(
        mechanism_text=mechanism_section,
        reference_audit_mode=reference_audit_mode,
    )
    final_metrics = compute_final_report_metrics(final_section=final_section, verdict=verdict)
    experiment_metrics = compute_experiment_metrics(
        experiment_config=experiment_config,
        comparison_expected=bool(path_meta.get("comparison_pair_id")),
    )

    model_label, model_label_source = detect_model_label(
        relative_path=relative_path,
        text=text,
        model_rules=model_rules,
        variant_label=path_meta.get("variant_label", ""),
    )
    model_bucket = model_label or path_meta.get("variant_label") or "unassigned"
    repeat_group_model_key = build_compound_key(
        path_meta.get("repeat_group_base_key", ""),
        model_bucket,
    )
    structural_completeness = percentage(sum(sections_present.values()), len(sections_present))

    overall_quality_score = round(
        (
            experiment_metrics["experiment_completeness_pct"] * 0.20
            + dimension_metrics["dimension_coverage_pct"] * 0.20
            + dimension_metrics["dimension_detail_score_pct"] * 0.15
            + mechanism_metrics["mechanism_score_pct"] * 0.15
            + final_metrics["reasoning_score_pct"] * 0.15
            + structural_completeness * 0.15
        ),
        2,
    )

    result = {
        "char_count": len(text),
        "word_count": count_text_units(text),
        "model_label": model_label,
        "model_label_source": model_label_source,
        "model_bucket": model_bucket,
        "verdict": verdict,
        "verdict_raw": verdict_raw,
        "repeat_group_model_key": repeat_group_model_key,
        "has_experiment_section": int(sections_present["experiment_setup"]),
        "has_image_analysis_section": int(sections_present["image_analysis"]),
        "has_mechanism_section": int(sections_present["mechanism"]),
        "has_final_report_section": int(sections_present["final_report"]),
        "structural_completeness_pct": structural_completeness,
        "overall_quality_score_pct": overall_quality_score,
    }
    result.update(experiment_metrics)
    result.update(dimension_metrics)
    result.update(mechanism_metrics)
    result.update(final_metrics)
    return result


def extract_path_metadata(path: Path, source_dir: Path) -> dict[str, Any]:
    relative = path.resolve().relative_to(source_dir.resolve())
    parts = list(relative.parts)
    stem = derive_metadata_stem(path)
    base_stem = stem
    variant_label = ""
    match = re.match(r"^(.*)-(\d+)$", stem)
    if match and "vs" in match.group(1):
        base_stem = match.group(1)
        variant_label = f"slot_{match.group(2)}"

    pair_meta = parse_pair_metadata(base_stem)
    drug_root_label = parts[0] if len(parts) > 1 else ""
    condition_folder = next((part for part in parts[:-1] if is_ph_token(part)), "")
    view_folder = next(
        (part for part in parts[:-1] if part.lower() in KNOWN_VIEW_TOKENS),
        "",
    )
    primary_drug_label = (
        pair_meta.get("left_product_name")
        or pair_meta.get("right_product_name")
        or drug_root_label
        or "unknown"
    )
    primary_pH_label = normalize_condition_label(
        condition_folder
        or pair_meta.get("left_condition_label")
        or pair_meta.get("right_condition_label")
    )
    reference_manufacturer_label = pair_meta.get("left_manufacturer_label", "")
    manufacturer_label = pair_meta.get("right_manufacturer_label") or reference_manufacturer_label
    reference_batch_label = pair_meta.get("left_batch_label", "")
    comparison_batch_label = pair_meta.get("right_batch_label") or reference_batch_label
    batch_pair = build_batch_pair(reference_batch_label, comparison_batch_label)
    comparison_scope = classify_comparison_scope(
        reference_manufacturer_label=reference_manufacturer_label,
        manufacturer_label=manufacturer_label,
    )
    sample_replicate_id = pair_meta.get("right_replicate_id") or pair_meta.get("left_replicate_id") or ""
    repeat_group_base_key = build_compound_key(
        primary_drug_label,
        primary_pH_label,
        pair_meta.get("manufacturer_pair", ""),
        batch_pair,
    )
    repeat_observation_key = build_compound_key(repeat_group_base_key, sample_replicate_id)

    return {
        "relative_dir": "/".join(parts[:-1]),
        "drug_root_label": drug_root_label,
        "primary_drug_label": primary_drug_label,
        "primary_pH_label": primary_pH_label,
        "condition_folder": condition_folder,
        "view_folder": view_folder,
        "variant_label": variant_label,
        "reference_manufacturer_label": reference_manufacturer_label,
        "manufacturer_label": manufacturer_label,
        "reference_batch_label": reference_batch_label,
        "comparison_batch_label": comparison_batch_label,
        "batch_pair": batch_pair,
        "comparison_scope": comparison_scope,
        "sample_replicate_id": sample_replicate_id,
        "repeat_group_base_key": repeat_group_base_key,
        "repeat_observation_key": repeat_observation_key,
        **pair_meta,
    }


def parse_pair_metadata(base_stem: str) -> dict[str, Any]:
    base_stem = normalize_pair_identifier(base_stem)
    left_sample = ""
    right_sample = ""
    comparison_pair_id = base_stem if "vs" in base_stem else ""
    if "vs" in base_stem:
        left_sample, right_sample = base_stem.split("vs", 1)
    left_meta = parse_sample_fragment(left_sample) if left_sample else empty_sample_meta("")
    right_meta = parse_sample_fragment(right_sample) if right_sample else empty_sample_meta("")
    manufacturer_pair = ""
    if left_meta["manufacturer_label"] or right_meta["manufacturer_label"]:
        manufacturer_pair = (
            f"{left_meta['manufacturer_label'] or 'unknown'} vs "
            f"{right_meta['manufacturer_label'] or 'unknown'}"
        )

    return {
        "comparison_pair_id": comparison_pair_id,
        "left_sample_raw": left_meta["raw"],
        "left_product_name": left_meta["product_name"],
        "left_manufacturer_label": left_meta["manufacturer_label"],
        "left_batch_label": left_meta["batch_label"],
        "left_replicate_id": left_meta["replicate_id"],
        "left_condition_label": left_meta["condition_label"],
        "left_duration_label": left_meta["duration_label"],
        "left_magnification_label": left_meta["magnification_label"],
        "left_view_label": left_meta["view_label"],
        "right_sample_raw": right_meta["raw"],
        "right_product_name": right_meta["product_name"],
        "right_manufacturer_label": right_meta["manufacturer_label"],
        "right_batch_label": right_meta["batch_label"],
        "right_replicate_id": right_meta["replicate_id"],
        "right_condition_label": right_meta["condition_label"],
        "right_duration_label": right_meta["duration_label"],
        "right_magnification_label": right_meta["magnification_label"],
        "right_view_label": right_meta["view_label"],
        "manufacturer_pair": manufacturer_pair,
    }


def select_preferred_outputs(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generic_groups: dict[str, list[dict[str, Any]]] = {}
    selected: list[dict[str, Any]] = []

    for item in candidates:
        path = Path(item["absolute_path"])
        if path.stem.lower() in GENERIC_RESULT_BASENAMES:
            generic_groups.setdefault(str(path.parent), []).append(item)
            continue
        selected.append(item)

    for items in generic_groups.values():
        selected.append(choose_preferred_case_output(items))

    return sorted(selected, key=lambda item: item["relative_path"])


def choose_preferred_case_output(items: list[dict[str, Any]]) -> dict[str, Any]:
    lookup = {
        (Path(item["file_name"]).stem.lower(), item["suffix"].lower()): item for item in items
    }
    for stem, suffix in PREFERRED_CASE_OUTPUTS:
        candidate = lookup.get((stem, suffix))
        if candidate and candidate.get("size_bytes", 0) > 0:
            return candidate
    for stem, suffix in PREFERRED_CASE_OUTPUTS:
        candidate = lookup.get((stem, suffix))
        if candidate:
            return candidate
    return max(items, key=lambda item: (item.get("size_bytes", 0), item["relative_path"]))


def derive_metadata_stem(path: Path) -> str:
    if path.stem.lower() in GENERIC_RESULT_BASENAMES and "vs" in path.parent.name.lower():
        return path.parent.name
    return path.stem


def normalize_pair_identifier(value: str) -> str:
    normalized = value.strip().strip("_")
    normalized = re.sub(r"(?i)__+\s*vs\s*__+", "vs", normalized)
    normalized = re.sub(r"(?i)__+rep0*([0-9]+)$", r"-\1", normalized)
    normalized = normalized.replace("__", "-")
    normalized = re.sub(r"_+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized.strip("-")


def parse_sample_fragment(fragment: str) -> dict[str, str]:
    if not fragment:
        return empty_sample_meta("")

    tokens = [token.strip() for token in fragment.split("-") if token.strip()]
    core_tokens = list(tokens)
    product_name = ""
    manufacturer = ""
    batch_label = ""
    condition_label = ""
    duration_label = ""
    view_label = ""
    magnification_label = ""
    replicate_id = ""

    ph_index = -1
    for index, token in enumerate(tokens):
        if is_ph_token(token):
            condition_label = token
            ph_index = index
            break

    if ph_index >= 0 and ph_index + 1 < len(tokens):
        product_name = tokens[ph_index + 1]
        start_index = ph_index + 2
    else:
        start_index = 0
        for index, token in enumerate(tokens):
            if not looks_like_prefix_token(token):
                product_name = token
                start_index = index + 1
                break

    if core_tokens and re.fullmatch(r"\d+", core_tokens[-1]):
        replicate_id = core_tokens[-1]
        core_tokens = core_tokens[:-1]

    for token in core_tokens:
        lowered = token.lower()
        if not duration_label and re.fullmatch(r"\d+(?:\.\d+)?(?:h|hr|hrs|min|mins)", lowered):
            duration_label = token
        if not view_label and lowered in KNOWN_VIEW_TOKENS:
            view_label = token
        if not magnification_label and re.fullmatch(r"\d+x", lowered):
            magnification_label = token

    for token in core_tokens[start_index:]:
        lowered = token.lower()
        if token == product_name or token == condition_label:
            continue
        if re.fullmatch(r"\d+(?:\.\d+)?(?:h|hr|hrs|min|mins)", lowered):
            continue
        if lowered in KNOWN_VIEW_TOKENS:
            continue
        if re.fullmatch(r"\d+x", lowered):
            continue
        if not manufacturer:
            manufacturer = token
            continue
        if not batch_label:
            batch_label = token
            break

    return {
        "raw": fragment,
        "product_name": product_name,
        "manufacturer_label": manufacturer,
        "batch_label": batch_label,
        "replicate_id": replicate_id,
        "condition_label": condition_label,
        "duration_label": duration_label,
        "magnification_label": magnification_label,
        "view_label": view_label,
    }


def empty_sample_meta(fragment: str) -> dict[str, str]:
    return {
        "raw": fragment,
        "product_name": "",
        "manufacturer_label": "",
        "batch_label": "",
        "replicate_id": "",
        "condition_label": "",
        "duration_label": "",
        "magnification_label": "",
        "view_label": "",
    }


def looks_like_prefix_token(token: str) -> bool:
    lowered = token.lower()
    return bool(
        re.fullmatch(r"\d{1,8}", token)
        or is_ph_token(token)
        or re.fullmatch(r"\d+(?:\.\d+)?(?:h|hr|hrs|min|mins)", lowered)
        or lowered in KNOWN_VIEW_TOKENS
        or re.fullmatch(r"\d+x", lowered)
    )


def is_ph_token(token: str) -> bool:
    return bool(re.search(r"(?i)\bph\s*\d+(?:\.\d+)?t?\b", token))


def normalize_condition_label(value: str) -> str:
    if not value:
        return ""
    match = re.search(r"(?i)pH\s*(\d+(?:\.\d+)?)", value)
    if match:
        return f"pH{match.group(1)}"
    return value.strip()


def build_batch_pair(left_batch: str, right_batch: str) -> str:
    if not left_batch and not right_batch:
        return ""
    return f"{left_batch or 'unknown'} vs {right_batch or 'unknown'}"


def classify_comparison_scope(
    reference_manufacturer_label: str,
    manufacturer_label: str,
) -> str:
    if not reference_manufacturer_label and not manufacturer_label:
        return "unknown"
    if reference_manufacturer_label and manufacturer_label and reference_manufacturer_label == manufacturer_label:
        return "same_manufacturer"
    if reference_manufacturer_label and manufacturer_label:
        return "cross_manufacturer"
    return "single_or_unknown"


def build_compound_key(*parts: str) -> str:
    cleaned = [part.strip() for part in parts if isinstance(part, str) and part.strip()]
    return " || ".join(cleaned)


def extract_experiment_config(text: str) -> dict[str, Any]:
    direct_labels = ["Experiment config (json)", '"experiment_config"', "experiment_config"]
    for label in direct_labels:
        payload = extract_json_after_label(text, label)
        if payload:
            if "experiment_config" in payload and isinstance(payload["experiment_config"], dict):
                return payload["experiment_config"]
            if any(key in payload for key in EXPERIMENT_CONFIG_FIELDS):
                return payload

    plan_payload = extract_json_after_label(text, "LLM parsing / plan")
    if plan_payload and isinstance(plan_payload.get("experiment_config"), dict):
        return plan_payload["experiment_config"]
    return {}


def extract_image_analysis_blocks(text: str) -> list[dict[str, Any]]:
    return extract_json_blocks_after_anchor(text, re.compile(r"llm image analysis output", re.IGNORECASE))


def extract_mechanism_section(text: str) -> str:
    return extract_section(
        text=text,
        start_markers=["Step 3", "mechanistic analysis", "mechanistic interpretation"],
        end_markers=["Final report", "Final report & export"],
    )


def extract_final_section(text: str) -> str:
    return extract_section(
        text=text,
        start_markers=["Final report", "Overall judgment", "总体判断"],
        end_markers=[],
    )


def extract_section(text: str, start_markers: list[str], end_markers: list[str]) -> str:
    lower_text = text.lower()
    start_index = -1
    for marker in start_markers:
        candidate = lower_text.find(marker.lower())
        if candidate >= 0 and (start_index < 0 or candidate < start_index):
            start_index = candidate
    if start_index < 0:
        return ""

    end_index = len(text)
    if end_markers:
        for marker in end_markers:
            candidate = lower_text.find(marker.lower(), start_index + 1)
            if candidate >= 0:
                end_index = min(end_index, candidate)
    return text[start_index:end_index].strip()


def extract_json_after_label(text: str, label: str) -> dict[str, Any] | None:
    lower_text = text.lower()
    index = lower_text.find(label.lower())
    if index < 0:
        return None
    brace_index = text.find("{", index)
    if brace_index < 0:
        return None
    block = extract_braced_block(text, brace_index)
    if not block:
        return None
    return parse_jsonish(block)


def extract_json_blocks_after_anchor(text: str, anchor_pattern: re.Pattern[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for match in anchor_pattern.finditer(text):
        brace_index = text.find("{", match.end())
        if brace_index < 0:
            continue
        block = extract_braced_block(text, brace_index)
        if not block:
            continue
        parsed = parse_jsonish(block)
        if isinstance(parsed, dict):
            results.append(parsed)
    return results


def extract_braced_block(text: str, start_index: int) -> str:
    if start_index < 0 or start_index >= len(text) or text[start_index] != "{":
        return ""
    depth = 0
    in_string = False
    escaped = False
    quote_char = '"'
    for index in range(start_index, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote_char:
                in_string = False
            continue
        if char in {'"', "'"}:
            in_string = True
            quote_char = char
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start_index : index + 1]
    return ""


def parse_jsonish(payload: str) -> dict[str, Any] | None:
    normalized = normalize_jsonish(payload)
    try:
        return json.loads(normalized)
    except json.JSONDecodeError:
        return None


def normalize_jsonish(payload: str) -> str:
    for old, new in TEXT_REPLACEMENTS.items():
        payload = payload.replace(old, new)
    payload = payload.replace("None", "null")
    payload = re.sub(r",\s*}", "}", payload)
    payload = re.sub(r",\s*]", "]", payload)
    return payload


def compute_experiment_metrics(
    experiment_config: dict[str, Any],
    comparison_expected: bool,
) -> dict[str, Any]:
    if not experiment_config:
        return {
            "experiment_fields_expected": 6 if comparison_expected else 5,
            "experiment_fields_present": 0,
            "experiment_completeness_pct": 0.0,
            "experiment_time_interval_present": 0,
            "experiment_other_conditions_present": 0,
        }

    expected_fields = ["drug_1_name", "medium_pH", "temperature_C", "total_duration_hours", "other_conditions"]
    if comparison_expected:
        expected_fields.append("drug_2_name")

    present_fields = sum(
        1 for field in expected_fields if has_meaningful_value(experiment_config.get(field))
    )
    return {
        "experiment_fields_expected": len(expected_fields),
        "experiment_fields_present": present_fields,
        "experiment_completeness_pct": percentage(present_fields, len(expected_fields)),
        "experiment_time_interval_present": int(
            has_meaningful_value(experiment_config.get("time_interval_hours"))
        ),
        "experiment_other_conditions_present": int(
            has_meaningful_value(experiment_config.get("other_conditions"))
        ),
    }


def compute_dimension_metrics(
    image_blocks: list[dict[str, Any]],
    text: str,
) -> dict[str, Any]:
    descriptions: dict[str, list[str]] = {key: [] for key in CANONICAL_DIMENSIONS}
    for block in image_blocks:
        payload = block.get("eight_dimension_description")
        if not isinstance(payload, dict):
            continue
        for key in CANONICAL_DIMENSIONS:
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                descriptions[key].append(value.strip())

    covered_keys = [key for key, values in descriptions.items() if values]
    if not covered_keys:
        lowered = text.lower()
        for key, aliases in CANONICAL_DIMENSIONS.items():
            if any(alias.lower() in lowered for alias in aliases):
                covered_keys.append(key)

    all_texts = [value for values in descriptions.values() for value in values]
    avg_words = (
        round(statistics.mean(count_text_units(value) for value in all_texts), 2)
        if all_texts
        else 0.0
    )

    generic_count = sum(
        1
        for value in all_texts
        if len(value.split()) < 10 or any(pattern.search(value) for pattern in GENERIC_DIMENSION_PATTERNS)
    )
    normalized_samples = [normalize_loose_text(value) for value in all_texts if value.strip()]
    duplicate_count = max(0, len(normalized_samples) - len(set(normalized_samples)))

    detail_score = 0.0
    if covered_keys:
        coverage_component = len(set(covered_keys)) / len(CANONICAL_DIMENSIONS)
        density_component = min(avg_words / 28.0, 1.0)
        generic_penalty = generic_count / max(len(all_texts), 1)
        duplicate_penalty = duplicate_count / max(len(all_texts), 1)
        detail_score = clamp(
            (coverage_component * 0.55 + density_component * 0.45)
            * (1.0 - 0.35 * generic_penalty)
            * (1.0 - 0.25 * duplicate_penalty),
            0.0,
            1.0,
        )

    return {
        "image_analysis_block_count": len(image_blocks),
        "dimension_coverage_count": len(set(covered_keys)),
        "dimension_coverage_pct": percentage(len(set(covered_keys)), len(CANONICAL_DIMENSIONS)),
        "dimension_avg_words": avg_words,
        "dimension_generic_count": generic_count,
        "dimension_duplicate_count": duplicate_count,
        "dimension_detail_score_pct": round(detail_score * 100.0, 2),
    }


def compute_mechanism_metrics(
    mechanism_text: str,
    reference_audit_mode: str,
) -> dict[str, Any]:
    if not mechanism_text:
        return {
            "mechanism_hypothesis_count": 0,
            "mechanism_follow_up_item_count": 0,
            "mechanism_evidence_trace_count": 0,
            "reference_trace_level": "none",
            "possible_placeholder_reference": 0,
            "mechanism_score_pct": 0.0,
            "reference_verify_placeholder": int(reference_audit_mode == "verify"),
        }

    hypothesis_count = len(re.findall(r"(?i)hypothesis\s+\d+", mechanism_text))
    follow_up_count = count_list_like_lines(mechanism_text)
    evidence_trace_count = len(
        re.findall(r"(?i)evidence|phenomenon review|key observations|observable phenomena", mechanism_text)
    )
    trace_level = "none"
    if any(pattern.search(mechanism_text) for pattern in STRUCTURED_REFERENCE_PATTERNS):
        trace_level = "structured"
    elif any(pattern.search(mechanism_text) for pattern in REFERENCE_TRACE_PATTERNS):
        trace_level = "generic"

    placeholder_flag = int(trace_level == "generic")
    trace_score = {"none": 0.0, "generic": 0.45, "structured": 1.0}[trace_level]
    mechanism_score = clamp(
        (
            min(hypothesis_count / 3.0, 1.0) * 0.35
            + min(follow_up_count / 4.0, 1.0) * 0.25
            + min(evidence_trace_count / 2.0, 1.0) * 0.20
            + trace_score * 0.20
        ),
        0.0,
        1.0,
    )
    return {
        "mechanism_hypothesis_count": hypothesis_count,
        "mechanism_follow_up_item_count": follow_up_count,
        "mechanism_evidence_trace_count": evidence_trace_count,
        "reference_trace_level": trace_level,
        "possible_placeholder_reference": placeholder_flag,
        "mechanism_score_pct": round(mechanism_score * 100.0, 2),
        "reference_verify_placeholder": int(reference_audit_mode == "verify"),
    }


def compute_final_report_metrics(final_section: str, verdict: str) -> dict[str, Any]:
    if not final_section:
        return {
            "comparison_table_present": 0,
            "comparison_table_rows": 0,
            "reason_keyword_count": 0,
            "evidence_link_count": 0,
            "judgment_basis_clear": 0,
            "reasoning_score_pct": 0.0,
        }

    table_rows = count_dimension_table_rows(final_section)
    reason_keyword_count = sum(1 for pattern in REASON_PATTERNS if pattern.search(final_section))
    evidence_link_count = sum(
        1
        for keyword in [
            "dimension",
            "time",
            "mechanism",
            "experiment",
            "condition",
            "table",
            "medium",
            "fragment",
            "surface",
            "体积",
            "机理",
            "条件",
        ]
        if keyword.lower() in final_section.lower()
    )
    judgment_basis_clear = int(bool(verdict != "unknown" and table_rows >= 4 and reason_keyword_count >= 1))
    reasoning_score = clamp(
        (
            (1.0 if verdict != "unknown" else 0.0) * 0.25
            + min(table_rows / 8.0, 1.0) * 0.30
            + min(reason_keyword_count / 3.0, 1.0) * 0.20
            + min(evidence_link_count / 6.0, 1.0) * 0.25
        ),
        0.0,
        1.0,
    )
    return {
        "comparison_table_present": int(table_rows > 0),
        "comparison_table_rows": table_rows,
        "reason_keyword_count": reason_keyword_count,
        "evidence_link_count": evidence_link_count,
        "judgment_basis_clear": judgment_basis_clear,
        "reasoning_score_pct": round(reasoning_score * 100.0, 2),
    }


def extract_verdict(text: str) -> tuple[str, str]:
    verdict_patterns = [
        re.compile(r"(?i)verdict:\s*([a-z ]+)"),
        re.compile(r"(?i)overall judgment.*?(same|different|similar|not similar)", re.DOTALL),
        re.compile(r"(相似|不相似|同一|不同)"),
    ]
    for pattern in verdict_patterns:
        match = pattern.search(text)
        if not match:
            continue
        raw = match.group(1).strip()
        lowered = raw.lower()
        if lowered in {"same", "similar", "相似", "同一"}:
            return "same", raw
        if lowered in {"different", "not similar", "不相似", "不同"}:
            return "different", raw
    return "unknown", ""


def detect_model_label(
    relative_path: str,
    text: str,
    model_rules: list[dict[str, Any]],
    variant_label: str,
) -> tuple[str, str]:
    for rule in model_rules:
        if re.search(rule["pattern"], relative_path, re.IGNORECASE):
            return rule["model_label"], "mapping_file"

    lowered_path = relative_path.lower()
    lowered_text = text.lower()
    for token, label in KNOWN_MODEL_PATTERNS.items():
        if token in lowered_path or token in lowered_text:
            return label, "auto_detected"

    if variant_label:
        return "", "variant_fallback"
    return "", "unassigned"


def load_model_rules(path_value: str | None) -> list[dict[str, Any]]:
    if not path_value:
        return []
    path = Path(path_value).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Model map does not exist: {path}")

    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            items = payload.get("rules", [])
        else:
            items = payload
        rules = [normalize_model_rule(item) for item in items]
    else:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rules = [normalize_model_rule(row) for row in reader]
    return sorted(rules, key=lambda item: item["priority"])


def normalize_model_rule(raw: dict[str, Any]) -> dict[str, Any]:
    pattern = str(raw.get("pattern", "")).strip()
    model_label = str(raw.get("model_label", "")).strip()
    if not pattern or not model_label:
        raise SystemExit("Each model-map rule requires pattern and model_label.")
    priority_value = raw.get("priority", 100)
    try:
        priority = int(priority_value)
    except (TypeError, ValueError):
        priority = 100
    return {"pattern": pattern, "model_label": model_label, "priority": priority}


def initialize_repeat_defaults(records: list[dict[str, Any]]) -> None:
    defaults = {
        "repeat_group_model_key": "",
        "repeat_group_complete": 0,
        "repeat_group_consistency_status": "not_grouped",
        "repeat_group_consensus_verdict": "",
        "potential_error_label": "",
    }
    for record in records:
        for key, value in defaults.items():
            record.setdefault(key, value)


def apply_record_annotations(
    records: list[dict[str, Any]],
    annotations: dict[str, dict[str, Any]],
) -> None:
    for record in records:
        if record["relative_path"] in annotations:
            record.update(annotations[record["relative_path"]])


def build_replicate_consistency_rows(
    records: list[dict[str, Any]],
    error_analysis_mode: str,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        if record.get("status") != "ok":
            continue
        if not record.get("repeat_group_model_key") or not record.get("sample_replicate_id"):
            continue
        grouped.setdefault(record["repeat_group_model_key"], []).append(record)

    rows: list[dict[str, Any]] = []
    annotations: dict[str, dict[str, Any]] = {}
    for group_key, bucket in sorted(grouped.items()):
        replicate_map: dict[str, list[dict[str, Any]]] = {}
        for record in bucket:
            replicate_map.setdefault(record["sample_replicate_id"], []).append(record)

        replicate_ids = sorted(replicate_map.keys(), key=natural_sort_key)
        verdict_by_replicate: dict[str, str] = {}
        path_by_replicate: dict[str, str] = {}
        for replicate_id in replicate_ids:
            sample_records = sorted(replicate_map[replicate_id], key=lambda item: item["relative_path"])
            verdicts = {item.get("verdict", "unknown") for item in sample_records}
            verdict_by_replicate[replicate_id] = (
                next(iter(verdicts)) if len(verdicts) == 1 else "mixed"
            )
            path_by_replicate[replicate_id] = sample_records[0]["relative_path"]

        valid_verdicts = [
            verdict
            for verdict in verdict_by_replicate.values()
            if verdict in {"same", "different", "unknown"}
        ]
        binary_verdicts = [verdict for verdict in valid_verdicts if verdict in {"same", "different"}]
        verdict_counter = Counter(valid_verdicts)
        complete_replicate_group = int(len(replicate_ids) >= 3)
        consistency_status = "insufficient"
        if len(binary_verdicts) >= 2:
            if len(set(binary_verdicts)) <= 1:
                consistency_status = "consistent"
            else:
                consistency_status = "inconsistent"
        consensus_verdict = ""
        if verdict_counter.get("same", 0) > verdict_counter.get("different", 0):
            consensus_verdict = "same"
        elif verdict_counter.get("different", 0) > verdict_counter.get("same", 0):
            consensus_verdict = "different"

        potential_fp_count = 0
        potential_fn_count = 0
        potential_error_replicates: list[str] = []
        if (
            error_analysis_mode == "repeat_proxy"
            and complete_replicate_group
            and consensus_verdict in {"same", "different"}
            and consistency_status == "inconsistent"
        ):
            minority_verdict = "different" if consensus_verdict == "same" else "same"
            minority_count = verdict_counter.get(minority_verdict, 0)
            if minority_count > 0:
                if minority_verdict == "same":
                    potential_fp_count = minority_count
                else:
                    potential_fn_count = minority_count
                potential_error_replicates = [
                    replicate_id
                    for replicate_id, verdict in verdict_by_replicate.items()
                    if verdict == minority_verdict
                ]

        row = {
            "model_bucket": bucket[0].get("model_bucket", "unassigned"),
            "primary_drug_label": bucket[0].get("primary_drug_label", ""),
            "primary_pH_label": bucket[0].get("primary_pH_label", ""),
            "reference_manufacturer_label": bucket[0].get("reference_manufacturer_label", ""),
            "manufacturer_label": bucket[0].get("manufacturer_label", ""),
            "manufacturer_pair": bucket[0].get("manufacturer_pair", ""),
            "batch_pair": bucket[0].get("batch_pair", ""),
            "comparison_scope": bucket[0].get("comparison_scope", ""),
            "repeat_group_base_key": bucket[0].get("repeat_group_base_key", ""),
            "repeat_group_model_key": group_key,
            "replicate_count": len(replicate_ids),
            "complete_replicate_group": complete_replicate_group,
            "replicate_ids": ",".join(replicate_ids),
            "replicate_1_verdict": verdict_by_replicate.get("1", ""),
            "replicate_2_verdict": verdict_by_replicate.get("2", ""),
            "replicate_3_verdict": verdict_by_replicate.get("3", ""),
            "replicate_1_path": path_by_replicate.get("1", ""),
            "replicate_2_path": path_by_replicate.get("2", ""),
            "replicate_3_path": path_by_replicate.get("3", ""),
            "consistency_status": consistency_status,
            "consensus_verdict": consensus_verdict,
            "same_count": verdict_counter.get("same", 0),
            "different_count": verdict_counter.get("different", 0),
            "unknown_count": verdict_counter.get("unknown", 0),
            "potential_false_positive_count": potential_fp_count,
            "potential_false_negative_count": potential_fn_count,
            "potential_error_replicates": ",".join(potential_error_replicates),
            "manual_review_flag": int(consistency_status != "consistent"),
        }
        rows.append(row)

        for replicate_id, sample_records in replicate_map.items():
            for record in sample_records:
                potential_error_label = ""
                if potential_fp_count and replicate_id in potential_error_replicates:
                    potential_error_label = "potential_false_positive"
                elif potential_fn_count and replicate_id in potential_error_replicates:
                    potential_error_label = "potential_false_negative"
                annotations[record["relative_path"]] = {
                    "repeat_group_complete": complete_replicate_group,
                    "repeat_group_consistency_status": consistency_status,
                    "repeat_group_consensus_verdict": consensus_verdict,
                    "potential_error_label": potential_error_label,
                }

    return rows, annotations


def build_verdict_stats_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    supported = [record for record in records if record["status"] == "ok"]
    group_specs = [
        ("OVERALL", lambda record: "ALL"),
        ("MODEL_BUCKET", lambda record: record.get("model_bucket") or "unassigned"),
        ("DRUG", lambda record: record.get("primary_drug_label") or "unknown"),
    ]
    rows: list[dict[str, Any]] = []
    for group_type, key_fn in group_specs:
        buckets: dict[str, list[dict[str, Any]]] = {}
        for record in supported:
            buckets.setdefault(key_fn(record), []).append(record)
        for group_value, bucket in sorted(buckets.items()):
            rows.append(
                {
                    "group_type": group_type,
                    "group_value": group_value,
                    **summarize_verdict_counts(bucket),
                }
            )
    return rows


def build_drug_ph_verdict_rows(
    records: list[dict[str, Any]],
    replicate_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    supported = [record for record in records if record["status"] == "ok"]
    rows: list[dict[str, Any]] = []
    model_buckets = sorted({record.get("model_bucket") or "unassigned" for record in supported})
    for model_bucket in ["ALL"] + model_buckets:
        scoped_records = (
            supported
            if model_bucket == "ALL"
            else [record for record in supported if (record.get("model_bucket") or "unassigned") == model_bucket]
        )
        grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for record in scoped_records:
            key = (
                record.get("primary_drug_label") or "unknown",
                record.get("primary_pH_label") or "unknown",
            )
            grouped.setdefault(key, []).append(record)

        for (drug_label, ph_label), bucket in sorted(grouped.items()):
            scoped_repeat_rows = [
                row
                for row in replicate_rows
                if row.get("primary_drug_label") == drug_label
                and row.get("primary_pH_label") == ph_label
                and (model_bucket == "ALL" or row.get("model_bucket") == model_bucket)
            ]
            rows.append(
                {
                    "primary_drug_label": drug_label,
                    "primary_pH_label": ph_label,
                    "model_bucket": model_bucket,
                    **summarize_verdict_counts(bucket),
                    "repeat_group_count": len(scoped_repeat_rows),
                    "inconsistent_repeat_group_count": sum(
                        row.get("consistency_status") == "inconsistent" for row in scoped_repeat_rows
                    ),
                }
            )
    return rows


def build_potential_error_summary_rows(
    replicate_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    scope_specs = [
        (
            "ALL_MODELS",
            lambda row: (
                row.get("primary_drug_label") or "unknown",
                row.get("primary_pH_label") or "unknown",
                row.get("reference_manufacturer_label") or "unknown",
                row.get("manufacturer_label") or "unknown",
                row.get("manufacturer_pair") or "unknown",
                row.get("batch_pair") or "unknown",
                row.get("comparison_scope") or "unknown",
            ),
        ),
        (
            "MODEL_BUCKET",
            lambda row: (
                row.get("model_bucket") or "unassigned",
                row.get("primary_drug_label") or "unknown",
                row.get("primary_pH_label") or "unknown",
                row.get("reference_manufacturer_label") or "unknown",
                row.get("manufacturer_label") or "unknown",
                row.get("manufacturer_pair") or "unknown",
                row.get("batch_pair") or "unknown",
                row.get("comparison_scope") or "unknown",
            ),
        ),
    ]
    for summary_scope, key_fn in scope_specs:
        buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
        for row in replicate_rows:
            buckets.setdefault(key_fn(row), []).append(row)
        for key, bucket in sorted(buckets.items()):
            if summary_scope == "ALL_MODELS":
                (
                    drug_label,
                    ph_label,
                    ref_manufacturer,
                    manufacturer_label,
                    manufacturer_pair,
                    batch_pair,
                    comparison_scope,
                ) = key
                model_bucket = "ALL"
            else:
                (
                    model_bucket,
                    drug_label,
                    ph_label,
                    ref_manufacturer,
                    manufacturer_label,
                    manufacturer_pair,
                    batch_pair,
                    comparison_scope,
                ) = key
            rows.append(
                {
                    "summary_scope": summary_scope,
                    "model_bucket": model_bucket,
                    "primary_drug_label": drug_label,
                    "primary_pH_label": ph_label,
                    "reference_manufacturer_label": ref_manufacturer,
                    "manufacturer_label": manufacturer_label,
                    "manufacturer_pair": manufacturer_pair,
                    "batch_pair": batch_pair,
                    "comparison_scope": comparison_scope,
                    **summarize_replicate_bucket(bucket),
                }
            )
    return rows


def apply_bert_scores(
    records: list[dict[str, Any]],
    mode: str,
    reference_file: str | None,
    model_type: str,
    lang: str,
    max_chars: int,
    rescale_with_baseline: bool,
) -> None:
    for record in records:
        record.update(default_bert_fields(mode, "disabled" if mode == "off" else "not_scored"))

    if mode == "off":
        return

    reference_payloads = build_bert_reference_payloads(records, mode, reference_file, max_chars)
    try:
        from bert_score import score as bert_score  # type: ignore
    except ImportError:
        for record in records:
            if record.get("status") != "ok":
                record.update(default_bert_fields(mode, "unavailable"))
            elif reference_payloads.get(record["relative_path"]):
                record.update(default_bert_fields(mode, "dependency_missing"))
            else:
                record.update(default_bert_fields(mode, "no_reference"))
        return

    scored_records: list[dict[str, Any]] = []
    candidates: list[str] = []
    references: list[str] = []
    for record in records:
        payload = reference_payloads.get(record.get("relative_path", ""))
        if record.get("status") != "ok":
            record.update(default_bert_fields(mode, "unavailable"))
            continue
        if not payload:
            record.update(default_bert_fields(mode, "no_reference"))
            continue
        candidate_text = truncate_for_bert(record.get("_analysis_text", ""), max_chars)
        reference_text = payload["reference_text"]
        if not candidate_text or not reference_text:
            record.update(default_bert_fields(mode, "no_reference"))
            continue
        record.update(
            {
                **default_bert_fields(mode, "pending"),
                "bert_reference_key": payload["reference_key"],
                "bert_reference_source": payload["reference_source"],
                "bert_reference_count": payload["reference_count"],
            }
        )
        scored_records.append(record)
        candidates.append(candidate_text)
        references.append(reference_text)

    if not scored_records:
        return

    try:
        kwargs: dict[str, Any] = {"rescale_with_baseline": rescale_with_baseline}
        if model_type:
            kwargs["model_type"] = model_type
        else:
            kwargs["lang"] = lang
        precision, recall, f1 = bert_score(candidates, references, **kwargs)
        precision_values = tensor_to_float_list(precision)
        recall_values = tensor_to_float_list(recall)
        f1_values = tensor_to_float_list(f1)
    except Exception as exc:  # BERTScore can fail on missing model weights or torch backends.
        message = f"bert_error:{type(exc).__name__}"
        for record in scored_records:
            record.update(default_bert_fields(mode, message))
        return

    for index, record in enumerate(scored_records):
        record.update(
            {
                "bert_score_mode": mode,
                "bert_score_status": "ok",
                "bert_precision_pct": round(precision_values[index] * 100.0, 2),
                "bert_recall_pct": round(recall_values[index] * 100.0, 2),
                "bert_f1_pct": round(f1_values[index] * 100.0, 2),
            }
        )


def build_bert_reference_payloads(
    records: list[dict[str, Any]],
    mode: str,
    reference_file: str | None,
    max_chars: int,
) -> dict[str, dict[str, Any]]:
    if mode == "reference_file":
        references = load_bert_reference_file(reference_file)
        payloads: dict[str, dict[str, Any]] = {}
        for record in records:
            reference_key = select_bert_reference_key(record)
            reference_text = references.get(reference_key) or references.get(record.get("relative_path", ""))
            if reference_text:
                payloads[record["relative_path"]] = {
                    "reference_key": reference_key,
                    "reference_source": "reference_file",
                    "reference_count": 1,
                    "reference_text": truncate_for_bert(reference_text, max_chars),
                }
        return payloads

    groups: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        if record.get("status") != "ok":
            continue
        key = select_bert_reference_key(record)
        groups.setdefault(key, []).append(record)

    payloads = {}
    for key, group in groups.items():
        for record in group:
            model_bucket = record.get("model_bucket")
            reference_records = [
                item
                for item in group
                if item["relative_path"] != record["relative_path"]
                and item.get("model_bucket") != model_bucket
                and item.get("_analysis_text")
            ]
            if not reference_records:
                reference_records = [
                    item
                    for item in group
                    if item["relative_path"] != record["relative_path"] and item.get("_analysis_text")
                ]
            if not reference_records:
                continue
            reference_text = "\n\n".join(
                truncate_for_bert(item.get("_analysis_text", ""), max_chars)
                for item in reference_records
            )
            payloads[record["relative_path"]] = {
                "reference_key": key,
                "reference_source": "consensus_leave_one_out",
                "reference_count": len(reference_records),
                "reference_text": truncate_for_bert(reference_text, max_chars),
            }
    return payloads


def load_bert_reference_file(path_value: str | None) -> dict[str, str]:
    if not path_value:
        raise SystemExit("--bert-reference-file is required for --bert-score-mode reference_file.")
    path = Path(path_value).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"BERT reference file does not exist: {path}")
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            return {str(key): str(value) for key, value in data.items()}
        if isinstance(data, list):
            return {
                str(item.get("reference_key") or item.get("comparison_pair_id")): str(
                    item.get("reference_text", "")
                )
                for item in data
                if isinstance(item, dict)
                and (item.get("reference_key") or item.get("comparison_pair_id"))
            }
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        references = {}
        for row in reader:
            key = row.get("reference_key") or row.get("comparison_pair_id") or row.get("relative_path")
            text = row.get("reference_text") or row.get("text") or row.get("answer")
            if key and text:
                references[key] = text
        return references
    raise SystemExit("BERT reference file must be CSV or JSON.")


def select_bert_reference_key(record: dict[str, Any]) -> str:
    return (
        record.get("comparison_pair_id")
        or record.get("repeat_observation_key")
        or record.get("relative_path", "")
    )


def truncate_for_bert(text: str, max_chars: int) -> str:
    normalized = normalize_text(text)
    if max_chars <= 0 or len(normalized) <= max_chars:
        return normalized
    return normalized[:max_chars]


def tensor_to_float_list(values: Any) -> list[float]:
    if hasattr(values, "detach"):
        values = values.detach()
    if hasattr(values, "cpu"):
        values = values.cpu()
    if hasattr(values, "tolist"):
        return [float(value) for value in values.tolist()]
    return [float(value) for value in values]


def default_bert_fields(mode: str, status: str) -> dict[str, Any]:
    return {
        "bert_score_mode": mode,
        "bert_score_status": status,
        "bert_reference_key": "",
        "bert_reference_source": "",
        "bert_reference_count": 0,
        "bert_precision_pct": "",
        "bert_recall_pct": "",
        "bert_f1_pct": "",
    }


def build_bert_score_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    supported = [record for record in records if record["status"] == "ok"]
    group_specs = [
        ("OVERALL", lambda record: "ALL"),
        ("MODEL_BUCKET", lambda record: record.get("model_bucket") or "unassigned"),
        ("DRUG", lambda record: record.get("primary_drug_label") or "unknown"),
    ]
    rows: list[dict[str, Any]] = []
    for group_type, key_fn in group_specs:
        buckets: dict[str, list[dict[str, Any]]] = {}
        for record in supported:
            buckets.setdefault(key_fn(record), []).append(record)
        for group_value, bucket in sorted(buckets.items()):
            scored = [record for record in bucket if record.get("bert_score_status") == "ok"]
            rows.append(
                {
                    "group_type": group_type,
                    "group_value": group_value,
                    "supported_count": len(bucket),
                    "bert_scored_count": len(scored),
                    "bert_available_rate_pct": percentage(len(scored), len(bucket)),
                    "avg_bert_precision_pct": mean_metric(scored, "bert_precision_pct"),
                    "avg_bert_recall_pct": mean_metric(scored, "bert_recall_pct"),
                    "avg_bert_f1_pct": mean_metric(scored, "bert_f1_pct"),
                    "bert_status_summary": summarize_statuses(bucket, "bert_score_status"),
                }
            )
    return rows


def summarize_statuses(records: list[dict[str, Any]], key: str) -> str:
    counter = Counter(str(record.get(key, "")) for record in records)
    return "; ".join(f"{status}:{count}" for status, count in sorted(counter.items()))


def build_summary_rows(
    records: list[dict[str, Any]],
    replicate_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    group_specs = [
        ("OVERALL", lambda record: "ALL"),
        ("MODEL_BUCKET", lambda record: record.get("model_bucket") or "unassigned"),
        ("DRUG", lambda record: record.get("primary_drug_label") or "unknown"),
        (
            "MANUFACTURER_PAIR",
            lambda record: record.get("manufacturer_pair") or "unknown",
        ),
        ("FORMAT", lambda record: record.get("extension") or "unknown"),
    ]

    for group_type, key_fn in group_specs:
        buckets: dict[str, list[dict[str, Any]]] = {}
        for record in records:
            group_value = key_fn(record)
            buckets.setdefault(group_value, []).append(record)
        for group_value, bucket in sorted(buckets.items()):
            rows.append(summarize_bucket(group_type, group_value, bucket, replicate_rows))
    return rows


def summarize_bucket(
    group_type: str,
    group_value: str,
    records: list[dict[str, Any]],
    replicate_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    supported = [record for record in records if record["status"] == "ok"]
    verdict_counter = Counter(record.get("verdict", "unknown") for record in supported)
    matched_repeat_rows = match_replicate_rows(group_type, group_value, replicate_rows)
    repeat_summary = summarize_replicate_bucket(matched_repeat_rows)

    return {
        "group_type": group_type,
        "group_value": group_value,
        "file_count": len(records),
        "supported_count": len(supported),
        "unsupported_count": sum(record["status"] != "ok" for record in records),
        "verdict_same_count": verdict_counter.get("same", 0),
        "verdict_different_count": verdict_counter.get("different", 0),
        "verdict_unknown_count": verdict_counter.get("unknown", 0),
        "avg_experiment_completeness_pct": mean_metric(supported, "experiment_completeness_pct"),
        "avg_dimension_coverage_pct": mean_metric(supported, "dimension_coverage_pct"),
        "avg_dimension_detail_score_pct": mean_metric(supported, "dimension_detail_score_pct"),
        "avg_mechanism_score_pct": mean_metric(supported, "mechanism_score_pct"),
        "avg_reasoning_score_pct": mean_metric(supported, "reasoning_score_pct"),
        "avg_structural_completeness_pct": mean_metric(supported, "structural_completeness_pct"),
        "avg_overall_quality_score_pct": mean_metric(supported, "overall_quality_score_pct"),
        "comparison_table_rate_pct": percentage(
            sum(record.get("comparison_table_present", 0) for record in supported),
            len(supported),
        ),
        "reference_trace_rate_pct": percentage(
            sum(record.get("reference_trace_level") != "none" for record in supported),
            len(supported),
        ),
        "placeholder_reference_rate_pct": percentage(
            sum(record.get("possible_placeholder_reference", 0) for record in supported),
            len(supported),
        ),
        "repeat_group_count": repeat_summary["repeat_group_total"],
        "complete_repeat_group_count": repeat_summary["complete_repeat_group_count"],
        "consistent_repeat_group_count": repeat_summary["consistent_group_count"],
        "inconsistent_repeat_group_count": repeat_summary["inconsistent_group_count"],
        "potential_false_positive_count": repeat_summary["potential_false_positive_count"],
        "potential_false_negative_count": repeat_summary["potential_false_negative_count"],
        "repeat_consistency_rate_pct": repeat_summary["consistency_rate_pct"],
        "bert_scored_count": sum(
            record.get("bert_score_status") == "ok" for record in supported
        ),
        "avg_bert_f1_pct": mean_metric(
            [record for record in supported if record.get("bert_score_status") == "ok"],
            "bert_f1_pct",
        ),
    }


def match_replicate_rows(
    group_type: str,
    group_value: str,
    replicate_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if group_type == "OVERALL":
        return list(replicate_rows)
    if group_type == "MODEL_BUCKET":
        return [row for row in replicate_rows if row.get("model_bucket") == group_value]
    if group_type == "DRUG":
        return [row for row in replicate_rows if row.get("primary_drug_label") == group_value]
    if group_type == "MANUFACTURER_PAIR":
        return [row for row in replicate_rows if row.get("manufacturer_pair") == group_value]
    return []


def build_model_comparison_rows(
    records: list[dict[str, Any]],
    replicate_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        key = record.get("model_bucket") or "unassigned"
        buckets.setdefault(key, []).append(record)

    rows: list[dict[str, Any]] = []
    for bucket_name, bucket in sorted(buckets.items()):
        supported = [record for record in bucket if record["status"] == "ok"]
        if not supported:
            continue
        repeat_summary = summarize_replicate_bucket(
            [row for row in replicate_rows if row.get("model_bucket") == bucket_name]
        )
        rows.append(
            {
                "model_bucket": bucket_name,
                "file_count": len(bucket),
                "supported_count": len(supported),
                "mapped_model_label_count": sum(
                    1 for record in supported if record.get("model_label_source") == "mapping_file"
                ),
                "avg_overall_quality_score_pct": mean_metric(supported, "overall_quality_score_pct"),
                "avg_dimension_coverage_pct": mean_metric(supported, "dimension_coverage_pct"),
                "avg_mechanism_score_pct": mean_metric(supported, "mechanism_score_pct"),
                "avg_reasoning_score_pct": mean_metric(supported, "reasoning_score_pct"),
                "avg_experiment_completeness_pct": mean_metric(
                    supported, "experiment_completeness_pct"
                ),
                "verdict_same_rate_pct": percentage(
                    sum(record.get("verdict") == "same" for record in supported),
                    len(supported),
                ),
                "placeholder_reference_rate_pct": percentage(
                    sum(record.get("possible_placeholder_reference", 0) for record in supported),
                    len(supported),
                ),
                "avg_comparison_table_rows": mean_metric(supported, "comparison_table_rows"),
                "repeat_group_count": repeat_summary["repeat_group_total"],
                "complete_repeat_group_count": repeat_summary["complete_repeat_group_count"],
                "consistent_repeat_group_count": repeat_summary["consistent_group_count"],
                "inconsistent_repeat_group_count": repeat_summary["inconsistent_group_count"],
                "potential_false_positive_count": repeat_summary["potential_false_positive_count"],
                "potential_false_negative_count": repeat_summary["potential_false_negative_count"],
                "repeat_consistency_rate_pct": repeat_summary["consistency_rate_pct"],
                "bert_scored_count": sum(
                    record.get("bert_score_status") == "ok" for record in supported
                ),
                "avg_bert_precision_pct": mean_metric(
                    [record for record in supported if record.get("bert_score_status") == "ok"],
                    "bert_precision_pct",
                ),
                "avg_bert_recall_pct": mean_metric(
                    [record for record in supported if record.get("bert_score_status") == "ok"],
                    "bert_recall_pct",
                ),
                "avg_bert_f1_pct": mean_metric(
                    [record for record in supported if record.get("bert_score_status") == "ok"],
                    "bert_f1_pct",
                ),
            }
        )

    ranked = sorted(
        rows,
        key=lambda row: (
            -row["repeat_consistency_rate_pct"],
            -row["avg_overall_quality_score_pct"],
            row["model_bucket"],
        ),
    )
    for index, row in enumerate(ranked, start=1):
        row["quality_rank"] = index
    return ranked


def summarize_verdict_counts(records: list[dict[str, Any]]) -> dict[str, Any]:
    counter = Counter(record.get("verdict", "unknown") for record in records)
    total = len(records)
    return {
        "same_count": counter.get("same", 0),
        "different_count": counter.get("different", 0),
        "unknown_count": counter.get("unknown", 0),
        "total_count": total,
        "same_ratio": percentage(counter.get("same", 0), total),
        "different_ratio": percentage(counter.get("different", 0), total),
        "unknown_ratio": percentage(counter.get("unknown", 0), total),
    }


def summarize_replicate_bucket(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    complete_count = sum(int(row.get("complete_replicate_group", 0)) for row in rows)
    consistent_count = sum(row.get("consistency_status") == "consistent" for row in rows)
    inconsistent_count = sum(row.get("consistency_status") == "inconsistent" for row in rows)
    ambiguous_count = sum(row.get("consistency_status") not in {"consistent", "inconsistent"} for row in rows)
    potential_fp_count = sum(int(row.get("potential_false_positive_count", 0)) for row in rows)
    potential_fn_count = sum(int(row.get("potential_false_negative_count", 0)) for row in rows)
    comparable_total = consistent_count + inconsistent_count
    return {
        "repeat_group_total": total,
        "complete_repeat_group_count": complete_count,
        "consistent_group_count": consistent_count,
        "inconsistent_group_count": inconsistent_count,
        "ambiguous_group_count": ambiguous_count,
        "potential_false_positive_count": potential_fp_count,
        "potential_false_negative_count": potential_fn_count,
        "consistency_rate_pct": percentage(consistent_count, comparable_total),
        "inconsistency_rate_pct": percentage(inconsistent_count, comparable_total),
    }


def natural_sort_key(value: str) -> tuple[int, str]:
    if value.isdigit():
        return (int(value), "")
    match = re.search(r"(\d+)", value)
    if match:
        return (int(match.group(1)), value)
    return (10**9, value)


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_model_charts(
    dimension_chart_path: Path,
    consistency_chart_path: Path,
    bert_chart_path: Path,
    model_rows: list[dict[str, Any]],
) -> None:
    write_bar_chart_svg(
        path=dimension_chart_path,
        title="Eight-Dimension Coverage by Model",
        y_label="Average coverage (%)",
        rows=model_rows,
        label_key="model_bucket",
        value_key="avg_dimension_coverage_pct",
    )
    write_bar_chart_svg(
        path=consistency_chart_path,
        title="Repeat Consistency by Model",
        y_label="Consistency rate (%)",
        rows=model_rows,
        label_key="model_bucket",
        value_key="repeat_consistency_rate_pct",
    )
    write_bar_chart_svg(
        path=bert_chart_path,
        title="BERTScore F1 by Model",
        y_label="Average BERTScore F1 (%)",
        rows=[row for row in model_rows if int(row.get("bert_scored_count", 0)) > 0],
        label_key="model_bucket",
        value_key="avg_bert_f1_pct",
    )


def write_bar_chart_svg(
    path: Path,
    title: str,
    y_label: str,
    rows: list[dict[str, Any]],
    label_key: str,
    value_key: str,
) -> None:
    chart_rows = []
    for row in rows:
        value = safe_float(row.get(value_key))
        if value is None:
            continue
        chart_rows.append((str(row.get(label_key, "unassigned")), value))

    width = 960
    height = 560
    margin_left = 90
    margin_right = 48
    margin_top = 80
    margin_bottom = 110
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    colors = ["#2f6f73", "#c34f32", "#6b7f2a", "#465f91", "#9a6a28", "#5f6f73"]

    if not chart_rows:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{width / 2}" y="70" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" font-weight="700">{escape(title)}</text>
  <text x="{width / 2}" y="{height / 2}" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" fill="#666666">No numeric data available</text>
</svg>
"""
        path.write_text(svg, encoding="utf-8")
        return

    max_value = max(100.0, max(value for _, value in chart_rows))
    bar_gap = 22
    bar_width = max(28, (plot_width - bar_gap * (len(chart_rows) + 1)) / len(chart_rows))
    x_axis_y = margin_top + plot_height

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="42" text-anchor="middle" font-family="Arial, sans-serif" font-size="26" font-weight="700" fill="#1f2933">{escape(title)}</text>',
        f'<text x="26" y="{margin_top + plot_height / 2}" text-anchor="middle" transform="rotate(-90 26 {margin_top + plot_height / 2})" font-family="Arial, sans-serif" font-size="15" fill="#46515a">{escape(y_label)}</text>',
        f'<line x1="{margin_left}" y1="{x_axis_y}" x2="{margin_left + plot_width}" y2="{x_axis_y}" stroke="#222" stroke-width="1.2"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{x_axis_y}" stroke="#222" stroke-width="1.2"/>',
    ]

    for tick in range(0, 101, 20):
        y = x_axis_y - (tick / max_value) * plot_height
        lines.append(
            f'<line x1="{margin_left - 6}" y1="{y:.2f}" x2="{margin_left + plot_width}" y2="{y:.2f}" stroke="#d9dee3" stroke-width="1"/>'
        )
        lines.append(
            f'<text x="{margin_left - 12}" y="{y + 5:.2f}" text-anchor="end" font-family="Arial, sans-serif" font-size="13" fill="#56616b">{tick}</text>'
        )

    for index, (label, value) in enumerate(chart_rows):
        x = margin_left + bar_gap + index * (bar_width + bar_gap)
        bar_height = (value / max_value) * plot_height
        y = x_axis_y - bar_height
        color = colors[index % len(colors)]
        center_x = x + bar_width / 2
        lines.extend(
            [
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.2f}" fill="{color}" rx="4"/>',
                f'<text x="{center_x:.2f}" y="{y - 10:.2f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#1f2933">{value:.2f}%</text>',
                f'<text x="{center_x:.2f}" y="{x_axis_y + 28}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#1f2933">{escape(label)}</text>',
            ]
        )

    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(
    report_path: Path,
    source_dir: Path,
    output_dir: Path,
    records: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    model_rows: list[dict[str, Any]],
    verdict_rows: list[dict[str, Any]],
    drug_ph_rows: list[dict[str, Any]],
    replicate_rows: list[dict[str, Any]],
    potential_error_rows: list[dict[str, Any]],
    bert_score_rows: list[dict[str, Any]],
    chart_paths: list[Path],
    scan: dict[str, Any],
    run_started: datetime,
    reference_audit_mode: str,
    error_analysis_mode: str,
    bert_score_mode: str,
) -> None:
    supported = [record for record in records if record["status"] == "ok"]
    overall_row = next(row for row in summary_rows if row["group_type"] == "OVERALL")
    overall_verdict_row = next(row for row in verdict_rows if row["group_type"] == "OVERALL")
    unsupported = [record for record in records if record["status"] != "ok"]
    top_drugs = [
        row
        for row in summary_rows
        if row["group_type"] == "DRUG" and row["group_value"] not in {"", "unknown"}
    ]
    top_drugs = sorted(top_drugs, key=lambda row: (-row["file_count"], row["group_value"]))[:5]
    top_different_rows = [
        row for row in drug_ph_rows if row["model_bucket"] == "ALL" and row["total_count"] > 0
    ]
    top_different_rows = sorted(
        top_different_rows,
        key=lambda row: (-row["different_ratio"], -row["total_count"], row["primary_drug_label"]),
    )[:5]
    overall_potential_rows = [
        row for row in potential_error_rows if row["summary_scope"] == "ALL_MODELS"
    ]
    top_unstable_rows = sorted(
        overall_potential_rows,
        key=lambda row: (
            -row["inconsistent_group_count"],
            -row["potential_false_positive_count"] - row["potential_false_negative_count"],
            row["primary_drug_label"],
        ),
    )[:5]
    repeat_summary = summarize_replicate_bucket(replicate_rows)
    overall_bert_row = next(
        (row for row in bert_score_rows if row["group_type"] == "OVERALL"),
        {
            "bert_scored_count": 0,
            "supported_count": 0,
            "avg_bert_f1_pct": 0.0,
            "bert_status_summary": "",
        },
    )

    lines = [
        "# Overall Result Analysis",
        "",
        "## Run Scope",
        f"- Source directory: `{source_dir}`",
        f"- Output directory: `{output_dir}`",
        f"- Generated at: `{run_started.isoformat(timespec='seconds')}`",
        f"- Reference audit mode: `{reference_audit_mode}`",
        f"- Error analysis mode: `{error_analysis_mode}`",
        f"- BERTScore mode: `{bert_score_mode}`",
        f"- Files seen during scan: `{scan['all_files_seen']}`",
        f"- Eligible files (`.docx` / `.doc` / `.md`): `{len(records)}`",
        f"- Supported files parsed successfully: `{len(supported)}`",
        f"- Unsupported or failed files: `{len(unsupported)}`",
        "",
        "## Key Findings",
        f"- Verdict distribution: `same={overall_verdict_row['same_count']}`, `different={overall_verdict_row['different_count']}`, `unknown={overall_verdict_row['unknown_count']}`",
        f"- Average experiment-condition completeness: `{overall_row['avg_experiment_completeness_pct']:.2f}%`",
        f"- Average eight-dimension coverage: `{overall_row['avg_dimension_coverage_pct']:.2f}%`",
        f"- Average eight-dimension detail score: `{overall_row['avg_dimension_detail_score_pct']:.2f}%`",
        f"- Average mechanism score: `{overall_row['avg_mechanism_score_pct']:.2f}%`",
        f"- Average final-judgment basis score: `{overall_row['avg_reasoning_score_pct']:.2f}%`",
        f"- Average structural completeness: `{overall_row['avg_structural_completeness_pct']:.2f}%`",
        f"- Average overall quality score: `{overall_row['avg_overall_quality_score_pct']:.2f}%`",
        f"- Average BERTScore F1: `{overall_bert_row['avg_bert_f1_pct']:.2f}%` from `{overall_bert_row['bert_scored_count']}` scored files",
        "",
        "## Verdict Proxy Rules",
        "- `same` and `different` are the core verdict labels for all downstream tables.",
        "- Default v1 proxy mode uses replicate consistency, not external truth labels.",
        "- Positive class convention: `same`.",
        "- Minority `same` in a `different`-majority complete 3-repeat group -> `potential_false_positive`.",
        "- Minority `different` in a `same`-majority complete 3-repeat group -> `potential_false_negative`.",
        "",
        "## Drug × pH Hotspots",
    ]

    if top_different_rows:
        lines.append("")
        lines.extend(
            markdown_table(
                headers=["Drug", "pH", "Different", "Same", "Total", "Different Ratio"],
                rows=[
                    [
                        row["primary_drug_label"],
                        row["primary_pH_label"],
                        row["different_count"],
                        row["same_count"],
                        row["total_count"],
                        f"{row['different_ratio']:.2f}%",
                    ]
                    for row in top_different_rows
                ],
            )
        )
    else:
        lines.append("- No drug × pH verdict rows were available.")

    lines.extend(
        [
            "",
        "## Repeat Consistency",
        f"- Repeat groups analyzed (model-specific): `{repeat_summary['repeat_group_total']}`",
        f"- Complete 3-repeat groups: `{repeat_summary['complete_repeat_group_count']}`",
        f"- Consistent groups: `{repeat_summary['consistent_group_count']}`",
        f"- Inconsistent groups: `{repeat_summary['inconsistent_group_count']}`",
        "- Potential FP/FN counts are assigned only to complete 3-repeat groups with a clear majority verdict.",
        f"- Potential false positives (proxy): `{repeat_summary['potential_false_positive_count']}`",
        f"- Potential false negatives (proxy): `{repeat_summary['potential_false_negative_count']}`",
    ]
    )

    if top_unstable_rows:
        lines.append("")
        lines.extend(
            markdown_table(
                headers=[
                    "Drug",
                    "Target Manufacturer",
                    "pH",
                    "Repeat Groups",
                    "Complete 3-Repeat",
                    "Inconsistent",
                    "Potential FP",
                    "Potential FN",
                ],
                rows=[
                    [
                        row["primary_drug_label"],
                        row["manufacturer_label"],
                        row["primary_pH_label"],
                        row["repeat_group_total"],
                        row["complete_repeat_group_count"],
                        row["inconsistent_group_count"],
                        row["potential_false_positive_count"],
                        row["potential_false_negative_count"],
                    ]
                    for row in top_unstable_rows
                ],
            )
        )
    else:
        lines.append("- No unstable repeat groups were detected.")

    lines.extend(["", "## Model / Variant Stability"])

    if not model_rows:
        lines.append("- No supported files were available for model or slot comparison.")
    else:
        lines.append("")
        lines.extend(
            markdown_table(
                headers=[
                    "Model Bucket",
                    "Files",
                    "Quality",
                    "Consistency",
                    "Inconsistent Groups",
                    "Potential FP",
                    "Potential FN",
                    "Same Rate",
                    "BERT F1",
                    "Rank",
                ],
                rows=[
                    [
                        row["model_bucket"],
                        row["file_count"],
                        f"{row['avg_overall_quality_score_pct']:.2f}%",
                        f"{row['repeat_consistency_rate_pct']:.2f}%",
                        row["inconsistent_repeat_group_count"],
                        row["potential_false_positive_count"],
                        row["potential_false_negative_count"],
                        f"{row['verdict_same_rate_pct']:.2f}%",
                        f"{row['avg_bert_f1_pct']:.2f}%",
                        row["quality_rank"],
                    ]
                    for row in model_rows[:10]
                ],
            )
        )
        if all(row["mapped_model_label_count"] == 0 for row in model_rows):
            lines.extend(
                [
                    "",
                    "- Explicit model names were not detected. This run fell back to filename slot labels such as `slot_1`, `slot_2`, `slot_3`.",
                    "- Add `--model-map` in future runs if those slots correspond to fixed models.",
                ]
            )

    lines.extend(["", "## BERTScore"])
    if bert_score_mode == "off":
        lines.append("- BERTScore was disabled for this run. Use `--bert-score-mode consensus` or `--bert-score-mode reference_file` to enable it.")
    elif int(overall_bert_row.get("bert_scored_count", 0)) == 0:
        lines.append(
            f"- No files received a BERTScore. Status summary: `{overall_bert_row.get('bert_status_summary', '')}`."
        )
        lines.append("- If the status is `dependency_missing`, install the optional `bert-score` package plus its model backend before rerunning.")
    else:
        lines.append(
            "- BERTScore F1 measures semantic similarity against a reference, not factual correctness."
        )
        lines.append(
            "- In `consensus` mode, the reference is the leave-one-out text from other models for the same case."
        )
        lines.append("")
        lines.extend(
            markdown_table(
                headers=["Model", "Scored Files", "BERT Precision", "BERT Recall", "BERT F1"],
                rows=[
                    [
                        row["group_value"],
                        row["bert_scored_count"],
                        f"{row['avg_bert_precision_pct']:.2f}%",
                        f"{row['avg_bert_recall_pct']:.2f}%",
                        f"{row['avg_bert_f1_pct']:.2f}%",
                    ]
                    for row in bert_score_rows
                    if row["group_type"] == "MODEL_BUCKET"
                ],
            )
        )

    lines.extend(["", "## Model Comparison Charts"])
    for path in chart_paths:
        lines.append(f"- `{path.name}`")

    lines.extend(["", "## Drug Groups"])
    if top_drugs:
        lines.append("")
        lines.extend(
            markdown_table(
                headers=["Drug", "Files", "Avg Quality", "Inconsistent Groups", "Consistency Rate"],
                rows=[
                    [
                        row["group_value"],
                        row["file_count"],
                        f"{row['avg_overall_quality_score_pct']:.2f}%",
                        row["inconsistent_repeat_group_count"],
                        f"{row['repeat_consistency_rate_pct']:.2f}%",
                    ]
                    for row in top_drugs
                ],
            )
        )
    else:
        lines.append("- No stable drug-root folders were extracted from the scanned paths.")

    lines.extend(["", "## Unsupported / Risk Flags"])
    if unsupported:
        for record in unsupported[:15]:
            lines.append(
                f"- `{record['relative_path']}` -> `{record['status']}`: {record.get('read_error', '')}"
            )
        if len(unsupported) > 15:
            lines.append(f"- Additional unsupported entries not shown: `{len(unsupported) - 15}`")
    else:
        lines.append("- No unsupported or failed files in this run.")

    lines.extend(
        [
            "",
            "## Generated Files",
            "- `OVERALL_REPORT.md`: narrative summary of verdict distribution, repeat consistency, and model stability.",
            "- `SUMMARY_STATS.csv`: grouped statistics table (overall, model bucket, drug, manufacturer pair, format).",
            "- `FILE_LEVEL_INDEX.csv`: one record per file for drill-down and later joins.",
            "- `MODEL_COMPARISON.csv`: model or slot ranking table with repeat-stability metrics.",
            "- `VERDICT_STATS.csv`: overall / model / drug verdict count table.",
            "- `DRUG_PH_VERDICT_STATS.csv`: drug × pH verdict distribution table.",
            "- `REPLICATE_CONSISTENCY.csv`: model-specific 3-repeat verdict consistency table.",
            "- `POTENTIAL_ERROR_SUMMARY.csv`: proxy potential FP/FN summary table.",
            "- `BERT_SCORE_STATS.csv`: BERTScore availability and average semantic-similarity scores.",
            "- `DIMENSION_COVERAGE_BY_MODEL.svg`: model-level eight-dimension coverage chart.",
            "- `REPEAT_CONSISTENCY_BY_MODEL.svg`: model-level repeat-consistency chart.",
            "- `BERT_SCORE_BY_MODEL.svg`: model-level BERTScore F1 chart.",
        ]
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    table = [
        "| " + " | ".join(str(value) for value in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        table.append("| " + " | ".join(str(value) for value in row) + " |")
    return table


def fill_empty_metrics(record: dict[str, Any]) -> None:
    defaults = {
        "char_count": 0,
        "word_count": 0,
        "model_label": "",
        "model_label_source": "unavailable",
        "model_bucket": record.get("variant_label") or "unassigned",
        "verdict": "unknown",
        "verdict_raw": "",
        "primary_drug_label": record.get("primary_drug_label", record.get("drug_root_label", "")),
        "primary_pH_label": record.get("primary_pH_label", ""),
        "reference_manufacturer_label": record.get("reference_manufacturer_label", ""),
        "manufacturer_label": record.get("manufacturer_label", ""),
        "reference_batch_label": record.get("reference_batch_label", ""),
        "comparison_batch_label": record.get("comparison_batch_label", ""),
        "batch_pair": record.get("batch_pair", ""),
        "comparison_scope": record.get("comparison_scope", ""),
        "sample_replicate_id": record.get("sample_replicate_id", ""),
        "left_replicate_id": record.get("left_replicate_id", ""),
        "right_replicate_id": record.get("right_replicate_id", ""),
        "repeat_group_base_key": record.get("repeat_group_base_key", ""),
        "repeat_group_model_key": record.get("repeat_group_model_key", ""),
        "repeat_observation_key": record.get("repeat_observation_key", ""),
        "repeat_group_complete": 0,
        "repeat_group_consistency_status": "not_grouped",
        "repeat_group_consensus_verdict": "",
        "potential_error_label": "",
        "has_experiment_section": 0,
        "has_image_analysis_section": 0,
        "has_mechanism_section": 0,
        "has_final_report_section": 0,
        "structural_completeness_pct": 0.0,
        "experiment_fields_expected": 0,
        "experiment_fields_present": 0,
        "experiment_completeness_pct": 0.0,
        "experiment_time_interval_present": 0,
        "experiment_other_conditions_present": 0,
        "image_analysis_block_count": 0,
        "dimension_coverage_count": 0,
        "dimension_coverage_pct": 0.0,
        "dimension_avg_words": 0.0,
        "dimension_generic_count": 0,
        "dimension_duplicate_count": 0,
        "dimension_detail_score_pct": 0.0,
        "mechanism_hypothesis_count": 0,
        "mechanism_follow_up_item_count": 0,
        "mechanism_evidence_trace_count": 0,
        "reference_trace_level": "none",
        "possible_placeholder_reference": 0,
        "mechanism_score_pct": 0.0,
        "reference_verify_placeholder": 0,
        "comparison_table_present": 0,
        "comparison_table_rows": 0,
        "reason_keyword_count": 0,
        "evidence_link_count": 0,
        "judgment_basis_clear": 0,
        "reasoning_score_pct": 0.0,
        "overall_quality_score_pct": 0.0,
        "bert_score_mode": "off",
        "bert_score_status": "unavailable",
        "bert_reference_key": "",
        "bert_reference_source": "",
        "bert_reference_count": 0,
        "bert_precision_pct": "",
        "bert_recall_pct": "",
        "bert_f1_pct": "",
    }
    record.update(defaults)


def has_meaningful_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        normalized = value.strip()
        return normalized not in {"", "null", "none", "unknown"}
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def mean_metric(records: list[dict[str, Any]], key: str) -> float:
    values = [safe_float(record.get(key)) for record in records]
    values = [value for value in values if value is not None]
    if not values:
        return 0.0
    return round(statistics.mean(values), 2)


def safe_float(value: Any) -> float | None:
    if value in {"", None}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def percentage(value: int | float, total: int | float) -> float:
    if not total:
        return 0.0
    return round(float(value) * 100.0 / float(total), 2)


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


def count_text_units(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]", text))


def normalize_loose_text(text: str) -> str:
    lowered = text.lower().strip()
    lowered = re.sub(r"\s+", " ", lowered)
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff ]+", "", lowered)
    return lowered


def count_list_like_lines(text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return sum(
        1
        for line in lines
        if line.startswith("-")
        or line.startswith("*")
        or re.match(r"^\d+\)", line)
        or re.match(r"^\d+\.", line)
    )


def count_dimension_table_rows(text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip().startswith("|")]
    count = 0
    for line in lines:
        compact = line.replace(" ", "")
        if set(compact) <= {"|", "-", ":", "—"}:
            continue
        lowered = line.lower()
        if any(label.lower() in lowered for label in DIMENSION_LABELS.values()):
            count += 1
    if count:
        return count
    if "|" in text:
        return sum(1 for label in DIMENSION_LABELS.values() if label.lower() in text.lower())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
