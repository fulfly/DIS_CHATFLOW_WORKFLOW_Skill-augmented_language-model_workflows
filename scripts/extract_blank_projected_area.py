#!/usr/bin/env python
"""Extract 2D projected tablet area from accelerated Fig. 4 disintegration videos.

This script implements transparent threshold-based segmentation for bright tablets
on a dark background. It extracts projected area in pixels and normalizes each
video to its first valid segmented frame. The quantity is projected area, not
true 3D volume.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".m4v", ".wmv"}
MAPPING_COLUMNS = [
    "source_video",
    "formulation_group",
    "pH_condition",
    "viscosity_group",
    "replicate_id",
    "include_for_fig4",
    "notes",
]


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_mapping_template(input_dir: Path) -> Path:
    template_path = input_dir / "video_mapping_template.csv"
    if not template_path.exists():
        pd.DataFrame(columns=MAPPING_COLUMNS).to_csv(template_path, index=False, encoding="utf-8-sig")
    return template_path


def list_videos(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    return sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS and not path.name.startswith("~$")
    )


def yes_no_to_bool(value: object) -> bool:
    if pd.isna(value):
        return False
    return str(value).strip().lower() in {"yes", "y", "true", "1", "include", "included"}


def load_mapping(input_dir: Path, mapping_file: Path | None) -> pd.DataFrame | None:
    mapping_path = mapping_file or (input_dir / "video_mapping.csv")
    if not mapping_path.exists():
        return None
    mapping = pd.read_csv(mapping_path)
    missing = [col for col in MAPPING_COLUMNS if col not in mapping.columns]
    if missing:
        raise ValueError(f"Mapping file is missing required columns: {', '.join(missing)}")
    mapping["source_video"] = mapping["source_video"].astype(str).str.strip()
    mapping["include_for_fig4_bool"] = mapping["include_for_fig4"].map(yes_no_to_bool)
    if mapping["source_video"].duplicated().any():
        duplicated = ", ".join(mapping.loc[mapping["source_video"].duplicated(), "source_video"])
        raise ValueError(f"Mapping file has duplicate source_video rows: {duplicated}")
    return mapping


def parse_video_filename(source_video: str) -> dict[str, object]:
    stem = Path(source_video).stem
    ph_match = re.search(r"pH\s*([0-9]+(?:\.[0-9]+)?)", stem, flags=re.IGNORECASE)
    replicate_match = re.match(r"^(\d+)", stem)
    pH_condition = f"pH {ph_match.group(1)}" if ph_match else ""
    replicate_id = replicate_match.group(1) if replicate_match else stem
    parsing_status = "auto_parsed" if pH_condition and replicate_id else "needs_manual_mapping"
    return {
        "source_video": source_video,
        "formulation_group": pH_condition or "Unmapped",
        "pH_condition": pH_condition,
        "viscosity_group": "",
        "replicate_id": replicate_id,
        "include_for_fig4": "yes" if parsing_status == "auto_parsed" else "no",
        "include_for_fig4_bool": parsing_status == "auto_parsed",
        "notes": parsing_status,
        "mapping_used": False,
        "parsing_status": parsing_status,
    }


def metadata_for_video(source_video: str, mapping: pd.DataFrame | None) -> dict[str, object]:
    if mapping is not None:
        hit = mapping.loc[mapping["source_video"] == source_video]
        if not hit.empty:
            row = hit.iloc[0].to_dict()
            row["mapping_used"] = True
            row["parsing_status"] = "manual_mapping"
            return row
    return parse_video_filename(source_video)


def safe_stem(path: Path) -> str:
    return re.sub(r"[^\w\-.一-龥]+", "_", path.stem, flags=re.UNICODE)


def otsu_threshold(gray_roi: np.ndarray) -> float:
    _, binary = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Re-run to retrieve threshold value explicitly.
    threshold_value, _ = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return float(threshold_value)


def segment_tablet(
    frame_bgr: np.ndarray,
    threshold: float | None,
    threshold_method: str,
    roi_y_min: int | None,
    roi_y_max: int | None,
    min_object_area: int,
    morph_kernel: int,
    keep_largest: bool,
) -> tuple[np.ndarray, float, bool, str]:
    height, width = frame_bgr.shape[:2]
    y_min = 0 if roi_y_min is None else max(0, int(roi_y_min))
    y_max = height if roi_y_max is None else min(height, int(roi_y_max))
    if y_max <= y_min:
        raise ValueError(f"Invalid ROI y range: roi_y_min={roi_y_min}, roi_y_max={roi_y_max}")

    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    gray_roi = gray[y_min:y_max, :]
    if threshold_method == "fixed":
        if threshold is None:
            raise ValueError("--threshold is required when --threshold-method fixed is used.")
        threshold_used = float(threshold)
    elif threshold_method == "otsu":
        threshold_used = otsu_threshold(gray_roi)
    else:
        raise ValueError(f"Unsupported threshold method: {threshold_method}")

    roi_mask = (gray_roi >= threshold_used).astype(np.uint8) * 255
    if morph_kernel > 1:
        kernel = np.ones((morph_kernel, morph_kernel), np.uint8)
        roi_mask = cv2.morphologyEx(roi_mask, cv2.MORPH_OPEN, kernel)
        roi_mask = cv2.morphologyEx(roi_mask, cv2.MORPH_CLOSE, kernel)

    n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(roi_mask, connectivity=8)
    cleaned = np.zeros_like(roi_mask)
    component_areas = []
    for label_id in range(1, n_labels):
        area = int(stats[label_id, cv2.CC_STAT_AREA])
        if area >= min_object_area:
            component_areas.append((label_id, area))
    if component_areas:
        if keep_largest:
            largest_label = max(component_areas, key=lambda item: item[1])[0]
            cleaned[labels == largest_label] = 255
        else:
            for label_id, _ in component_areas:
                cleaned[labels == label_id] = 255
    mask = np.zeros((height, width), dtype=np.uint8)
    mask[y_min:y_max, :] = cleaned
    mask_area_valid = bool(mask.sum() > 0)
    qc_flag = "" if mask_area_valid else "empty_mask"
    return mask, threshold_used, mask_area_valid, qc_flag


def overlay_mask(frame_bgr: np.ndarray, mask: np.ndarray) -> np.ndarray:
    overlay = frame_bgr.copy()
    color = np.zeros_like(frame_bgr)
    color[:, :, 1] = 255
    alpha = 0.35
    mask_bool = mask > 0
    overlay[mask_bool] = cv2.addWeighted(frame_bgr, 1 - alpha, color, alpha, 0)[mask_bool]
    return overlay


def imwrite_unicode(path: Path, image: np.ndarray) -> None:
    """Write images to Windows paths that may contain non-ASCII characters."""
    path.parent.mkdir(parents=True, exist_ok=True)
    success, encoded = cv2.imencode(path.suffix or ".png", image)
    if not success:
        raise RuntimeError(f"Could not encode image for writing: {path}")
    encoded.tofile(str(path))


def save_qc_triplet(
    qc_dir: Path,
    video_stem: str,
    real_time_h: float,
    frame_bgr: np.ndarray,
    mask: np.ndarray,
) -> dict[str, str]:
    time_label = f"{real_time_h:.2f}h".replace(".", "p")
    video_dir = ensure_dir(qc_dir / video_stem)
    original_path = video_dir / f"{video_stem}_{time_label}_original.png"
    mask_path = video_dir / f"{video_stem}_{time_label}_mask.png"
    overlay_path = video_dir / f"{video_stem}_{time_label}_overlay.png"
    imwrite_unicode(original_path, frame_bgr)
    imwrite_unicode(mask_path, mask)
    imwrite_unicode(overlay_path, overlay_mask(frame_bgr, mask))
    return {
        "qc_original": str(original_path),
        "qc_mask": str(mask_path),
        "qc_overlay": str(overlay_path),
    }


def read_frame(cap: cv2.VideoCapture, frame_index: int) -> tuple[bool, np.ndarray | None]:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
    ok, frame = cap.read()
    return ok, frame


def representative_indices(
    frame_count: int,
    fps: float,
    acceleration_factor: float,
    interval_real_min: float,
    qc_times_h: list[float],
) -> tuple[list[int], dict[int, float]]:
    frame_step = max(1, int(round((interval_real_min * 60.0 / acceleration_factor) * fps)))
    regular = list(range(0, frame_count, frame_step))
    if regular[-1] != frame_count - 1:
        regular.append(frame_count - 1)
    qc_indices = {
        min(frame_count - 1, max(0, int(round((time_h * 3600.0 / acceleration_factor) * fps)))): time_h
        for time_h in qc_times_h
    }
    all_indices = sorted(set(regular) | set(qc_indices.keys()))
    return all_indices, qc_indices


def process_video(
    video_path: Path,
    metadata: dict[str, object],
    output_dir: Path,
    qc_dir: Path,
    args: argparse.Namespace,
) -> tuple[pd.DataFrame, dict[str, object], pd.DataFrame]:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    if fps <= 0 or frame_count <= 0:
        raise RuntimeError(f"Invalid video metadata for {video_path}: fps={fps}, frame_count={frame_count}")

    video_duration_s = frame_count / fps
    real_duration_h = video_duration_s * args.acceleration_factor / 3600.0
    qc_times = [float(item) for item in args.qc_times_h.split(",") if item.strip()]
    indices, qc_indices = representative_indices(
        frame_count,
        fps,
        args.acceleration_factor,
        args.frame_interval_real_min,
        qc_times,
    )
    video_stem = safe_stem(video_path)
    rows = []
    qc_frame_rows = []
    failed_frames = 0
    threshold_values = []

    for frame_index in indices:
        ok, frame = read_frame(cap, frame_index)
        if not ok or frame is None:
            failed_frames += 1
            continue
        video_time_s = frame_index / fps
        real_time_h = video_time_s * args.acceleration_factor / 3600.0
        try:
            mask, threshold_used, mask_area_valid, qc_flag = segment_tablet(
                frame,
                threshold=args.threshold,
                threshold_method=args.threshold_method,
                roi_y_min=args.roi_y_min,
                roi_y_max=args.roi_y_max,
                min_object_area=args.min_object_area,
                morph_kernel=args.morph_kernel,
                keep_largest=not args.keep_all_components,
            )
        except Exception as exc:
            failed_frames += 1
            rows.append(
                {
                    "source_video": video_path.name,
                    "frame_index": frame_index,
                    "video_time_s": video_time_s,
                    "real_time_h": real_time_h,
                    "projected_area_px": np.nan,
                    "normalized_projected_area": np.nan,
                    "threshold_used": np.nan,
                    "roi_y_min": args.roi_y_min,
                    "roi_y_max": args.roi_y_max,
                    "mask_area_valid": False,
                    "qc_flag": f"segmentation_error: {exc}",
                }
            )
            continue
        projected_area_px = int((mask > 0).sum())
        threshold_values.append(threshold_used)
        rows.append(
            {
                "source_video": video_path.name,
                "frame_index": frame_index,
                "video_time_s": video_time_s,
                "real_time_h": real_time_h,
                "projected_area_px": projected_area_px,
                "normalized_projected_area": np.nan,
                "threshold_used": threshold_used,
                "roi_y_min": args.roi_y_min,
                "roi_y_max": args.roi_y_max,
                "mask_area_valid": mask_area_valid,
                "qc_flag": qc_flag,
                "formulation_group": metadata.get("formulation_group", ""),
                "pH_condition": metadata.get("pH_condition", ""),
                "viscosity_group": metadata.get("viscosity_group", ""),
                "replicate_id": metadata.get("replicate_id", ""),
                "include_for_fig4": metadata.get("include_for_fig4", ""),
                "mapping_used": metadata.get("mapping_used", False),
                "parsing_status": metadata.get("parsing_status", ""),
            }
        )
        if args.save_qc_frames and frame_index in qc_indices:
            paths = save_qc_triplet(qc_dir, video_stem, qc_indices[frame_index], frame, mask)
            qc_frame_rows.append(
                {
                    "source_video": video_path.name,
                    "target_real_time_h": qc_indices[frame_index],
                    "actual_real_time_h": real_time_h,
                    "frame_index": frame_index,
                    **paths,
                }
            )

    cap.release()
    df = pd.DataFrame(rows)
    valid_area = df.loc[df["mask_area_valid"] & df["projected_area_px"].notna(), "projected_area_px"]
    area_initial = float(valid_area.iloc[0]) if not valid_area.empty else np.nan
    if pd.notna(area_initial) and area_initial > 0:
        df["normalized_projected_area"] = df["projected_area_px"] / area_initial

    per_video_path = output_dir / f"{video_stem}_projected_area.csv"
    df.to_csv(per_video_path, index=False, encoding="utf-8-sig")

    warning_messages = []
    if abs(real_duration_h - args.expected_duration_h) > args.duration_tolerance_h:
        warning_messages.append(
            f"converted duration {real_duration_h:.2f} h differs from expected {args.expected_duration_h:.2f} h"
        )
    if valid_area.empty:
        warning_messages.append("no valid mask area detected")
    if str(metadata.get("parsing_status", "")) == "needs_manual_mapping":
        warning_messages.append("filename needs manual mapping")
    if not yes_no_to_bool(metadata.get("include_for_fig4", "no")):
        warning_messages.append("include_for_fig4 is no")

    qc = {
        "source_video": video_path.name,
        "fps": fps,
        "frame_count": frame_count,
        "width_px": width,
        "height_px": height,
        "video_duration_s": video_duration_s,
        "real_duration_h_converted": real_duration_h,
        "number_of_frames_processed": int(len(df)),
        "real_time_start_h": float(df["real_time_h"].min()) if not df.empty else np.nan,
        "real_time_end_h": float(df["real_time_h"].max()) if not df.empty else np.nan,
        "expected_duration_h": args.expected_duration_h,
        "area_initial_px": area_initial,
        "area_min_px": float(valid_area.min()) if not valid_area.empty else np.nan,
        "area_max_px": float(valid_area.max()) if not valid_area.empty else np.nan,
        "normalized_area_min": float(df["normalized_projected_area"].min()) if not df.empty else np.nan,
        "normalized_area_max": float(df["normalized_projected_area"].max()) if not df.empty else np.nan,
        "threshold_method": args.threshold_method,
        "median_threshold": float(np.nanmedian(threshold_values)) if threshold_values else np.nan,
        "threshold_value": float(np.nanmedian(threshold_values)) if threshold_values else np.nan,
        "roi_used": args.roi_y_min is not None or args.roi_y_max is not None,
        "roi_y_min": args.roi_y_min,
        "roi_y_max": args.roi_y_max,
        "number_of_failed_frames": int(failed_frames + (~df["mask_area_valid"]).sum()) if not df.empty else failed_frames,
        "warning_message": "; ".join(warning_messages),
        "per_video_csv": str(per_video_path),
        "formulation_group": metadata.get("formulation_group", ""),
        "pH_condition": metadata.get("pH_condition", ""),
        "viscosity_group": metadata.get("viscosity_group", ""),
        "replicate_id": metadata.get("replicate_id", ""),
        "include_for_fig4": metadata.get("include_for_fig4", ""),
        "mapping_used": metadata.get("mapping_used", False),
        "parsing_status": metadata.get("parsing_status", ""),
    }
    return df, qc, pd.DataFrame(qc_frame_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=r"D:\data\vedio\空白", type=Path)
    parser.add_argument("--output-dir", default=None, type=Path)
    parser.add_argument("--qc-dir", default=None, type=Path)
    parser.add_argument("--mapping-file", default=None, type=Path)
    parser.add_argument("--frame-interval-real-min", default=10.0, type=float)
    parser.add_argument("--threshold", default=None, type=float)
    parser.add_argument("--threshold-method", choices=["otsu", "fixed"], default="otsu")
    parser.add_argument("--roi-y-min", default=None, type=int)
    parser.add_argument("--roi-y-max", default=None, type=int)
    parser.add_argument("--min-object-area", default=1000, type=int)
    parser.add_argument("--morph-kernel", default=5, type=int)
    parser.add_argument("--keep-all-components", action="store_true")
    parser.add_argument("--save-qc-frames", action="store_true")
    parser.add_argument("--qc-times-h", default="0,1,2,4,8,12,24")
    parser.add_argument("--acceleration-factor", default=750.0, type=float)
    parser.add_argument("--expected-duration-h", default=24.0, type=float)
    parser.add_argument("--duration-tolerance-h", default=0.5, type=float)
    parser.add_argument("--video", default=None, help="Process only the named source video.")
    parser.add_argument("--max-videos", default=None, type=int)
    parser.add_argument("--create-template-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = args.input_dir
    output_dir = ensure_dir(args.output_dir or (input_dir / "processed_area_csv"))
    qc_dir = ensure_dir(args.qc_dir or (input_dir / "qc_frames"))
    template_path = write_mapping_template(input_dir)
    if args.create_template_only:
        print(f"mapping_template={template_path}")
        return

    mapping = load_mapping(input_dir, args.mapping_file)
    videos = list_videos(input_dir)
    if args.video:
        videos = [path for path in videos if path.name == args.video or path.stem == args.video]
        if not videos:
            raise FileNotFoundError(f"Requested video not found: {args.video}")
    if args.max_videos is not None:
        videos = videos[: args.max_videos]
    if not videos:
        raise FileNotFoundError(f"No supported video files found in {input_dir}")

    all_rows = []
    qc_rows = []
    qc_frame_rows = []
    for video_path in videos:
        metadata = metadata_for_video(video_path.name, mapping)
        if not yes_no_to_bool(metadata.get("include_for_fig4", "no")):
            qc_rows.append(
                {
                    "source_video": video_path.name,
                    "number_of_frames_processed": 0,
                    "real_time_start_h": np.nan,
                    "real_time_end_h": np.nan,
                    "expected_duration_h": args.expected_duration_h,
                    "area_initial_px": np.nan,
                    "area_min_px": np.nan,
                    "area_max_px": np.nan,
                    "threshold_method": args.threshold_method,
                    "threshold_value": args.threshold,
                    "roi_used": args.roi_y_min is not None or args.roi_y_max is not None,
                    "number_of_failed_frames": 0,
                    "warning_message": "not processed because include_for_fig4 is no or mapping uncertain",
                    **{k: metadata.get(k, "") for k in ["formulation_group", "pH_condition", "viscosity_group", "replicate_id", "include_for_fig4", "mapping_used", "parsing_status"]},
                }
            )
            continue
        df, qc, qc_frames = process_video(video_path, metadata, output_dir, qc_dir, args)
        all_rows.append(df)
        qc_rows.append(qc)
        if not qc_frames.empty:
            qc_frame_rows.append(qc_frames)

    combined = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    qc_report = pd.DataFrame(qc_rows)
    qc_frames_report = pd.concat(qc_frame_rows, ignore_index=True) if qc_frame_rows else pd.DataFrame()
    combined_path = output_dir / "fig4_projected_area_combined.csv"
    qc_path = output_dir / "fig4_segmentation_qc.csv"
    qc_frames_path = output_dir / "fig4_qc_frame_paths.csv"
    combined.to_csv(combined_path, index=False, encoding="utf-8-sig")
    qc_report.to_csv(qc_path, index=False, encoding="utf-8-sig")
    qc_frames_report.to_csv(qc_frames_path, index=False, encoding="utf-8-sig")

    print(f"videos_processed={len(all_rows)}")
    print(f"mapping_template={template_path}")
    print(f"combined_csv={combined_path}")
    print(f"qc_csv={qc_path}")
    print(f"qc_frame_paths={qc_frames_path}")
    if qc_rows:
        first = qc_rows[0]
        print(f"first_video={first.get('source_video')}")
        print(f"fps={first.get('fps')}")
        print(f"video_duration_s={first.get('video_duration_s')}")
        print(f"real_duration_h_converted={first.get('real_duration_h_converted')}")
        print(f"threshold_method={first.get('threshold_method')}")
        print(f"threshold_value={first.get('threshold_value')}")
        print(f"roi_y_min={first.get('roi_y_min')}")
        print(f"roi_y_max={first.get('roi_y_max')}")
        print(f"area_initial_px={first.get('area_initial_px')}")
        print(f"area_min_px={first.get('area_min_px')}")
        print(f"area_max_px={first.get('area_max_px')}")
        print(f"warning_message={first.get('warning_message')}")


if __name__ == "__main__":
    main()
