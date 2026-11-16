#!/usr/bin/env python3
"""Render Chapter 3 figures from native calibration; never modify input data.

Run: python blog_sum_assets/build_spatial_figures.py
Optional inputs: --sample ULTRA_SESSION --duo-sample DUO_SESSION.
Uses the existing build_fov.py projection helpers and its installed dependencies.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

import matplotlib
import numpy as np
import yaml

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "egocentric_blog_bundle_revised/ego_blog/repro"))
from build_fov import boundary, metrics, project, transform, unproject

BG = "#061321"
FG = "#e8f4ff"
MUTED = "#93adc7"
COLORS = ["#44e3ff", "#ffba62", "#b89bff", "#54efae"]
AXIS_COLORS = ["#ff758c", "#6ceda3", "#7faeff"]
NAMES = ["C0 / FRONT LEFT", "C1 / FRONT RIGHT",
         "C2 / SIDE RIGHT", "C3 / SIDE LEFT"]


def load_sample(root: Path) -> tuple[list[dict], dict]:
    metas = list(root.glob("meta_*.json"))
    if len(metas) != 1:
        raise ValueError(f"Expected one session metadata file, found {metas}")
    meta = json.loads(metas[0].read_text())
    paths = [root / meta["files"][key]
             for key in ("calibration_camera", "calibration_imu")]
    camera = yaml.safe_load(paths[0].read_text())
    imu = yaml.safe_load(paths[1].read_text().replace("%YAML:1.0", ""))
    count = camera["calibration_info"]["num_cameras"]
    if count not in (2, 4) or len(camera["cameras"]) != count:
        raise ValueError("This figure requires two or four calibrated cameras")
    if camera["calibration_info"]["reference_camera"] != "cam_0":
        raise ValueError("Expected cam_0 as reference camera")
    T_c0_i = np.array(imu["cam0"]["T_cam_imu"], dtype=float)
    T_c0_i[:3, 3] *= 0.001
    cameras = []
    for i, raw in enumerate(camera["cameras"]):
        if raw["distortion_model"] != "KB" or raw["id"] != f"cam_{i}":
            raise ValueError("Unexpected camera model or ordering")
        if any(raw["distortion"].get(k, 0) != 0
               for k in ("k5", "k6", "p1", "p2")):
            raise ValueError("Nonzero coefficients outside the KB4 model")
        T_c_c0 = transform(raw["extrinsics"]["rotation"],
                           np.array(raw["extrinsics"]["translation"]) * 0.001)
        T_i_c = np.linalg.inv(T_c_c0 @ T_c0_i)
        np.testing.assert_allclose(T_i_c @ T_c_c0 @ T_c0_i, np.eye(4), atol=1e-12)
        rotation_error = float(np.max(np.abs(
            T_i_c[:3, :3].T @ T_i_c[:3, :3] - np.eye(3))))
        # Six-decimal input rotations are retained, not re-orthonormalized.
        if rotation_error > 2e-6:
            raise ValueError(f"Rotation rounding exceeds tolerance: {rotation_error}")
        if np.linalg.det(T_i_c[:3, :3]) <= 0:
            raise ValueError("Camera rotation must preserve handedness")
        c = dict(name=NAMES[i], source_name=raw["name"], model="KB4",
                 K=[raw["intrinsics"][k] for k in ("fx", "fy", "cx", "cy")],
                 D=[raw["distortion"][f"k{j}"] for j in range(1, 5)],
                 resolution=[raw["image_width"], raw["image_height"]],
                 T_imu_cam=T_i_c.tolist(), index=i)
        metrics(c)
        c["rotation_orthogonality_max_error"] = rotation_error
        axis = T_i_c[:3, 2]
        c["optical_axis_imu"] = (axis / np.linalg.norm(axis)).tolist()
        w, h = c["resolution"]
        u, v = np.meshgrid(np.linspace(0, w - 1, 65),
                           np.linspace(0, h - 1, 49))
        pixels = np.column_stack((u.ravel(), v.ravel()))
        rays = unproject(c, pixels)
        if not np.isfinite(rays).all():
            raise ValueError("Invalid ray in sampled image domain")
        error = float(np.max(np.linalg.norm(project(c, rays) - pixels, axis=1)))
        if error >= 1e-6:
            raise ValueError(f"Projection round trip exceeds tolerance: {error}")
        c["grid_roundtrip_max_px"] = error
        c["color"] = COLORS[i]
        cameras.append(c)
    audit = dict(
        product_name="EGO-MATE-ULTRA" if count == 4 else "EGO-MATE-DUO",
        transform_convention="p_I = T_I_C p_C; T_I_C = inv(T_C_C0 @ T_C0_I)",
        input_translation_unit="mm", output_translation_unit="m",
        session_device_id=meta["device"]["serial_number"],
        calibration_device_id=camera["calibration_info"]["serial_number"],
        source_files=[dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                      for p in paths],
        baseline_mm=float(np.linalg.norm(
            np.array(cameras[0]["position_m"]) - cameras[1]["position_m"]) * 1000),
        cameras=cameras,
    )
    if count == 4:
        pts = {}
        for name in ("left", "right", "left_side", "right_side"):
            path = root / meta["files"][f"video_{name}_pts"]
            with path.open() as f:
                pts[name] = np.array([int(row["timestamp_us"])
                                      for row in csv.DictReader(f)], dtype=np.int64)
            if len(pts[name]) < 2 or np.any(np.diff(pts[name]) <= 0):
                raise ValueError(f"Invalid or non-monotonic PTS stream: {name}")
        pair_count = min(len(pts["left"]), len(pts["right"]))
        delta = pts["right"][:pair_count] - pts["left"][:pair_count]
        audit.update(
            pts_counts={name: len(values) for name, values in pts.items()},
            index_pairing_note="Equal file indices only; not verified exposure pairing",
            right_minus_left_pts_us=dict(min=int(delta.min()),
                                        median=float(np.median(delta)),
                                        max=int(delta.max()), equal=int((delta == 0).sum())),
        )
    return cameras, audit


def style_3d(ax, bounds: list[tuple[float, float]], unit: str) -> None:
    ax.set_facecolor(BG)
    ax.set_proj_type("ortho")
    ax.view_init(elev=27, azim=-57)
    ax.set_box_aspect([b - a for a, b in bounds])
    for axis, (lo, hi), label in zip(
            (ax.xaxis, ax.yaxis, ax.zaxis), bounds, ("I_X", "I_Y", "I_Z")):
        axis.set_pane_color((0.02, 0.05, 0.09, 0))
        axis.line.set_color("#39526c")
        axis._axinfo["grid"]["color"] = "#233b51"
        axis._axinfo["grid"]["linewidth"] = 0.5
        axis.set_ticks(np.linspace(lo, hi, 5))
        axis.set_label_text(f"{label} ({unit})", color=MUTED, fontsize=9)
        axis.labelpad = 5
        axis.set_tick_params(colors=MUTED, labelsize=8, pad=0)
    ax.set_xlim(*bounds[0])
    ax.set_ylim(*bounds[1])
    ax.set_zlim(*bounds[2])


def triad(ax, origin, rotation, length: float, labels: bool = False) -> None:
    for j, color in enumerate(AXIS_COLORS):
        direction = rotation[:, j] * length
        ax.quiver(*origin, *direction, color=color, linewidth=1.5,
                  arrow_length_ratio=0.16)
        if labels:
            ax.text(*(origin + 1.15 * direction), f"I_{'XYZ'[j]}",
                    color=color, fontsize=8)


def rig_figure(cameras: list[dict], audit: dict, out: Path, filename: str) -> None:
    fig = plt.figure(figsize=(19, 11), facecolor=BG)
    fig.text(0.04, 0.95, f"{audit['product_name']} / CALIBRATED SENSOR RIG",
             fontsize=25, color=FG, weight="bold")
    fig.text(0.04, 0.91, f"{len(cameras)} native KB4 cameras | 1600 x 1200 | IMU reference frame",
             fontsize=12, color=MUTED)
    coverage = fig.add_axes([0.00, 0.27, 0.54, 0.59], projection="3d")
    style_3d(coverage, [(-0.7, 0.7)] * 3, "m")
    close = fig.add_axes([0.55, 0.30, 0.41, 0.53], projection="3d")
    bounds = ([(-25, 85), (-115, 115), (-35, 75)] if len(cameras) == 4
              else [(-45, 145), (-65, 65), (-20, 85)])
    style_3d(close, bounds, "mm")
    fig.text(0.04, 0.86, "01 / MODEL RAY ENVELOPES", color=MUTED, fontsize=11)
    fig.text(0.58, 0.86, "02 / SENSOR CENTRES + LOCAL AXES", color=MUTED, fontsize=11)
    for ax, length in ((coverage, 0.18), (close, 24)):
        ax.scatter(0, 0, 0, color="white", marker="D", s=65, depthshade=False)
        triad(ax, np.zeros(3), np.eye(3), length, labels=True)
    close.text(-7, 0, -13, "IMU / ORIGIN", color=FG, fontsize=8)
    for i, c in enumerate(cameras):
        T = np.array(c["T_imu_cam"])
        p, R, color = T[:3, 3], T[:3, :3], c["color"]
        rays = unproject(c, boundary(c, 61))
        ends = p + 0.65 * (rays @ R.T)
        faces = [[p, a, b] for a, b in zip(ends[:-1], ends[1:])]
        coverage.add_collection3d(Poly3DCollection(
            faces, facecolors=color, alpha=0.025, edgecolors="none"))
        coverage.plot(*ends.T, color=color, lw=1.2, alpha=0.9)
        for fraction in (0.25, 0.5, 0.75):
            ring = p + fraction * (ends - p)
            coverage.plot(*ring.T, color=color, lw=0.45, alpha=0.24)
        for end in ends[::30]:
            coverage.plot(*np.array([p, end]).T, color=color, lw=0.6, alpha=0.35)
        coverage.quiver(*p, *(R[:, 2] * 0.40), color=color, linewidth=2,
                        arrow_length_ratio=0.1)
        coverage.scatter(*p, color=color, s=28, depthshade=False)
        coverage.text(*(p + R[:, 2] * 0.43), f"C{i}", color=color, fontsize=10)
        mm = p * 1000
        close.scatter(*mm, color=color, s=95, depthshade=False, edgecolor="white")
        close.plot(*np.array([np.zeros(3), mm]).T,
                   color=color, ls=":", lw=1, alpha=0.6)
        triad(close, mm, R, 16)
        x, y, _ = proj3d.proj_transform(*mm, close.get_proj())
        offset = [(24, 15), (-32, -22), (-24, 18), (22, 18)][i]
        close.annotate(f"C{i}", (x, y), xytext=offset,
                       textcoords="offset points", color=color, fontsize=11,
                       weight="bold", arrowprops=dict(arrowstyle="-", color=color))
    p0, p1 = [np.array(c["position_m"]) * 1000 for c in cameras[:2]]
    close.plot(*np.array([p0, p1]).T, color="#f5d992", ls="--", lw=1.4)
    close.text(45, 0, -17, f"FRONT BASELINE / {audit['baseline_mm']:.3f} mm",
               color="#f5d992", fontsize=8)
    fig.text(0.04, 0.24, "CAMERA / MODEL H x V", color=MUTED, fontsize=10)
    fig.text(0.04, 0.20, "POSITION IN IMU / mm", color=MUTED, fontsize=10)
    for i, c in enumerate(cameras):
        x = 0.21 + i * (0.19 if len(cameras) == 4 else 0.38)
        fig.text(x, 0.24, c["name"], color=c["color"], fontsize=10, weight="bold")
        fig.text(x, 0.21, f"{c['hfov_deg']:.1f} deg x {c['vfov_deg']:.1f} deg",
                 color=FG, fontsize=12)
        fig.text(x, 0.18, "(" + ", ".join(f"{p * 1000:.2f}"
                                        for p in c["position_m"]) + ")",
                 color=MUTED, fontsize=10)
    fig.text(0.04, 0.115,
             "Local axes: X red / Y green / Z blue. Coloured long arrows: camera optical axes.",
             color=FG, fontsize=11)
    fig.text(0.04, 0.075,
             "0.65 m rays are display lengths, NOT sensing range. Native calibration; no crop or resize.",
             color=MUTED, fontsize=10)
    fig.text(0.04, 0.040,
             "IMU axes are NOT a verified worn/world frame. Model envelopes exclude no housing or image-validity masks.",
             color=MUTED, fontsize=10)
    fig.savefig(out / filename, dpi=180, facecolor=BG)
    plt.close(fig)


def timing_figure(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(16, 5.4), facecolor=BG)
    ax.set_facecolor(BG)
    fig.subplots_adjust(left=0.25, right=0.97, bottom=0.17, top=0.76)
    times = np.arange(0, 120, 33.333)
    rows = [(4.5, "Device A / stereo_left", times, COLORS[0], "o"),
            (3.4, "Device A / stereo_right", times, COLORS[1], "o"),
            (2.3, "IMU / software alignment", np.arange(0, 121, 2), COLORS[2], "|"),
            (1.2, "Wrist / cross-device pairing", times + 11, COLORS[3], "o")]
    for y, label, values, color, marker in rows:
        ax.hlines(y, 0, 125, color="#294358", lw=1)
        ax.scatter(values, np.full(values.shape, y), color=color, marker=marker, s=50)
        ax.text(-6, y, label, color=FG, ha="right", va="center", fontsize=10)
    for t in times:
        ax.plot([t, t], [3.15, 4.75], color=COLORS[0], lw=1.5, ls="--")
        imu_shift = round(t / 2) * 2 - t
        for y, shift, color in ((2.3, imu_shift, COLORS[2]), (1.2, 11, COLORS[3])):
            ax.annotate("", (t, 4.35), (t + shift, y + 0.1),
                        arrowprops=dict(arrowstyle="->", color=color, alpha=0.55, lw=1))
    ax.set_xlim(-2, 125)
    ax.set_ylim(0.65, 5)
    ax.set_yticks([])
    ax.set_xlabel("Illustrative common timeline / ms", color=MUTED)
    ax.tick_params(colors=MUTED)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(0.04, 0.91, "HARD SYNC + SOFTWARE ALIGNMENT",
             color=FG, fontsize=21, weight="bold")
    fig.text(0.04, 0.83, "Within-device cameras: shared capture time and timestamp. IMU / cross-device: software alignment.",
             color=MUTED, fontsize=12)
    fig.text(0.04, 0.035,
             "SCHEMATIC ONLY: offsets and sample spacing are illustrative, not measured synchronization errors.",
             color=MUTED, fontsize=10)
    fig.savefig(out / "time_alignment.png", dpi=180, facecolor=BG)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, default=Path(
        "/data/vslam/orbbec/EGO_Pro_AZLR860009Y_20210101_201712"))
    parser.add_argument("--duo-sample", type=Path, default=Path(
        "/data/vslam/orbbec/orbbec_finger/1-2/EGO_AZEB761000F_20261109_155057"))
    args = parser.parse_args()
    out = Path(__file__).resolve().parent
    for root, product, filename, audit_name in (
        (args.sample, "EGO-MATE-ULTRA", "ego_mate_ultra_rig.png",
         "spatial_calibration_audit.json"),
        (args.duo_sample, "EGO-MATE-DUO", "ego_mate_duo_rig.png",
         "duo_spatial_calibration_audit.json"),
    ):
        cameras, audit = load_sample(root)
        if audit["product_name"] != product:
            raise ValueError(f"Unexpected camera count for {product}")
        rig_figure(cameras, audit, out, filename)
        (out / audit_name).write_text(json.dumps(audit, indent=2) + "\n")
        print(product, "baseline / mm:", audit["baseline_mm"])
        print("Maximum grid round-trip error / px:",
              max(c["grid_roundtrip_max_px"] for c in cameras))
        if audit["session_device_id"] != audit["calibration_device_id"]:
            print("WARNING: session and calibration device IDs differ; binding requires verification.")
    timing_figure(out)


if __name__ == "__main__":
    main()
