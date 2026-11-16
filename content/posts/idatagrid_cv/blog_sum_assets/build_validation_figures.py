#!/usr/bin/env python3
"""Build Chapter 4 figures and audit the supplied, unmodified results."""

import argparse
import csv
import hashlib
import json
from pathlib import Path

import cv2
import matplotlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


TIMESTAMP = "1783697300274107904"
ASSETS = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sparse_vertical_residual(left: np.ndarray, right: np.ndarray) -> dict:
    detector = cv2.SIFT_create(nfeatures=3000)
    left_points, left_desc = detector.detectAndCompute(
        cv2.cvtColor(left, cv2.COLOR_RGB2GRAY), None
    )
    right_points, right_desc = detector.detectAndCompute(
        cv2.cvtColor(right, cv2.COLOR_RGB2GRAY), None
    )
    if left_desc is None or right_desc is None:
        raise ValueError("Both images must contain descriptors for the sparse check")
    matcher = cv2.BFMatcher(cv2.NORM_L2)

    def ratio_matches(source: np.ndarray, target: np.ndarray) -> dict[int, int]:
        return {
            pair[0].queryIdx: pair[0].trainIdx
            for pair in matcher.knnMatch(source, target, k=2)
            if len(pair) == 2 and pair[0].distance < 0.7 * pair[1].distance
        }

    forward = ratio_matches(left_desc, right_desc)
    backward = ratio_matches(right_desc, left_desc)
    pairs = [(i, j) for i, j in forward.items() if backward.get(j) == i]
    if not pairs:
        raise ValueError("No mutual ratio-test matches for the sparse check")
    residuals = np.array(
        [abs(left_points[i].pt[1] - right_points[j].pt[1]) for i, j in pairs]
    )
    return {
        "method": "SIFT nfeatures=3000; mutual L2 ratio<0.7; no geometric filtering",
        "opencv_version": cv2.__version__,
        "matches": len(pairs),
        "median_abs_dy_px": float(np.median(residuals)),
        "p95_abs_dy_px": float(np.percentile(residuals, 95)),
        "scope": "One frame; putative image matches, not independently verified truth",
    }


def build_stereo_figures(root: Path) -> dict:
    rectified = root / "rectified_images"
    depth_root = root / "depth_results"
    paths = {
        "left": rectified / f"{TIMESTAMP}_left_rect.png",
        "right": rectified / f"{TIMESTAMP}_right_rect.png",
        "rectification": rectified / "rectification.json",
        "disparity": depth_root / f"{TIMESTAMP}_disp.npy",
        "depth": depth_root / f"{TIMESTAMP}_depth_meter.npy",
        "depth_mm": depth_root / f"{TIMESTAMP}_depth_mm.png",
        "supplied_composite": ASSETS / f"{TIMESTAMP}_disp_vis.png",
    }
    left = np.array(Image.open(paths["left"]).convert("RGB"))
    right = np.array(Image.open(paths["right"]).convert("RGB"))
    composite = np.array(Image.open(paths["supplied_composite"]).convert("RGB"))
    height, width = left.shape[:2]
    if (
        right.shape != left.shape
        or composite.shape != (height, width * 3, 3)
        or not np.array_equal(composite[:, :width], left)
        or not np.array_equal(composite[:, width : width * 2], right)
    ):
        raise ValueError("The supplied composite must contain these exact stereo images")

    guided = Image.fromarray(composite.copy())
    draw = ImageDraw.Draw(guided)
    rows = list(range(120, height - 60, 120))
    for index, row in enumerate(rows):
        color = (45, 212, 222) if index % 2 == 0 else (255, 207, 82)
        draw.line((0, row, width * 2 - 1, row), fill=color, width=4)
    modified = np.array(guided)
    allowed = np.zeros((height, width * 3), dtype=bool)
    for row in rows:
        allowed[row - 1 : row + 3, : width * 2] = True
    if np.any(np.any(modified != composite, axis=2) & ~allowed):
        raise ValueError("Guide lines changed pixels outside the left/right guide rows")
    header = 84
    canvas = Image.new("RGB", (width * 3, height + header), "#101923")
    canvas.paste(guided, (0, header))
    font = ImageFont.truetype(font_manager.findfont("DejaVu Sans"), 38)
    labels = ["RECTIFIED LEFT", "RECTIFIED RIGHT", "DISPARITY / ORIGINAL COLORS"]
    for index, label in enumerate(labels):
        ImageDraw.Draw(canvas).text(
            (index * width + 28, 18), label, font=font, fill="#ecf1f7"
        )
    canvas.save(ASSETS / "stereo_rectified_guides.png")

    calibration = json.loads(paths["rectification"].read_text())
    disparity = np.load(paths["disparity"])
    depth = np.load(paths["depth"])
    depth_mm = np.array(Image.open(paths["depth_mm"]))
    if any(array.shape != (height, width) for array in (disparity, depth, depth_mm)):
        raise ValueError("Disparity and depth must use the rectified image resolution")
    valid = np.isfinite(depth) & (depth > 0)
    if not valid.any() or not np.all(np.isfinite(disparity[valid]) & (disparity[valid] > 0)):
        raise ValueError("Positive finite depth requires positive finite disparity")
    p1, p2 = np.array(calibration["P1"]), np.array(calibration["P2"])
    if not np.allclose(p1[:2, :3], p2[:2, :3]):
        raise ValueError("The simple fB/d check requires equal rectified intrinsics")
    fb = -float(p2[0, 3])
    if not np.isclose(fb, p1[0, 0] * calibration["baseline"]):
        raise ValueError("Rectified focal length and baseline disagree with P2")
    scale_error = np.abs(depth[valid] - fb / disparity[valid])
    if float(scale_error.max()) > 1e-5:
        raise ValueError("Saved depth does not agree with the saved disparity scale")
    if np.any(depth_mm[~valid] != 0):
        raise ValueError("Millimeter output must preserve invalid depth as zero")
    if float(np.max(np.abs(depth_mm[valid] / 1000.0 - depth[valid]))) > 0.0011:
        raise ValueError("Meter and millimeter depth disagree beyond quantization")

    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("#30343b")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), layout="constrained")
    axes[0].imshow(left)
    axes[0].set_title("Ego-Air / rectified left RGB")
    plot = axes[1].imshow(
        np.ma.masked_where(~valid, depth), cmap=cmap, vmin=0.5, vmax=5.0
    )
    axes[1].set_title("Same-frame axial depth / gray = invalid")
    for axis in axes:
        axis.set_axis_off()
    fig.colorbar(plot, ax=axes[1], shrink=0.8, label="Axial depth Z (m)")
    fig.savefig(ASSETS / "stereo_metric_depth.png", dpi=160)
    plt.close(fig)
    return {
        "timestamp_ns": TIMESTAMP,
        "sources": {name: {"path": str(path), "sha256": sha256(path)}
                    for name, path in paths.items()},
        "resolution_wh": [width, height],
        "guides": {"header_px": header, "rows_in_source": rows, "width_px": 4,
                   "disparity_panel_unchanged": True},
        "focal_length_px": float(p1[0, 0]),
        "baseline_m": calibration["baseline"],
        "fB_m_px": fb,
        "positive_finite_depth_pixels": int(valid.sum()),
        "positive_finite_depth_ratio": float(valid.mean()),
        "positive_depth_range_m": [float(depth[valid].min()), float(depth[valid].max())],
        "max_depth_vs_fB_over_d_difference_m": float(scale_error.max()),
        "depth_display_limits_m": [0.5, 5.0],
        "depth_model_version": None,
        "depth_model_note": "No model/version asserted from output filenames alone",
        "sparse_vertical_residual": sparse_vertical_residual(left, right),
    }


def extract_video_frame(video: Path, output: Path) -> None:
    capture = cv2.VideoCapture(str(video))
    try:
        if not capture.isOpened():
            raise ValueError(f"Cannot open video: {video}")
        capture.set(cv2.CAP_PROP_POS_MSEC, 12000)
        success, frame = capture.read()
        if not success or not cv2.imwrite(str(output), frame):
            raise ValueError(f"Cannot export the 12-second frame: {video}")
    finally:
        capture.release()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stereo-root", type=Path, default=Path(
        "/data/vslam/DataGridEgo-Air/episode_20260710_152807_transformed"))
    parser.add_argument("--pose-root", type=Path, default=Path(
        "/home/lsy/work/open_vins/ov_offline_test/results/multi_device_cross_pose/"
        "EGO_AZEB761000F_Joint_2_20260831_102919"))
    args = parser.parse_args()
    audit = {"stereo": build_stereo_figures(args.stereo_root)}
    local_video = ASSETS / "replay_stage_pose_graph.mp4"
    if sha256(local_video) != sha256(args.pose_root / local_video.name):
        raise ValueError("The supplied pose video differs from this saved run")
    backend = args.pose_root / "backend"
    stats_path = backend / "localization_stats.csv"
    with stats_path.open(newline="") as stream:
        stats = list(csv.DictReader(stream))
    with (backend / "stage_pose_graph/factor_stats.csv").open(newline="") as stream:
        factors = list(csv.DictReader(stream))
    audit["pose_graph"] = {
        "source_root": str(args.pose_root),
        "supplied_video_sha256": sha256(local_video),
        "localization_stats_sha256": sha256(stats_path),
        "localization_stats": stats,
        "factor_stats": factors,
        "summary": json.loads((backend / "summary.json").read_text()),
        "scope": "Saved pose-graph stage; not a new VIO run or absolute accuracy test",
    }
    for video_name, frame_name in [
        ("replay_stage_pose_graph.mp4", "pose_graph_frame_12s.png"),
        ("grid_cyl.mp4", "panorama_frame_12s.png"),
    ]:
        extract_video_frame(ASSETS / video_name, ASSETS / frame_name)
    (ASSETS / "validation_audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps({
        "stereo_sparse_check": audit["stereo"]["sparse_vertical_residual"],
        "saved_pose_queries": stats,
        "audit": str(ASSETS / "validation_audit.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
