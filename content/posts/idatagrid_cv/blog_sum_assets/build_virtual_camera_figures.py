#!/usr/bin/env python3
"""Generate the SEUCM example and cross-model virtual-stereo figures for Chapter 5."""

import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

import cv2
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ASSETS = Path(__file__).resolve().parent
CALIBRATION = Path("/home/lsy/work/calibration")
SOURCE = CALIBRATION / "stereo_virtual/get_virtual_stereo.py"
DATA = Path("/data/calibration/virtual_cam")
RESULTS = DATA / "virtual_results_vfov70"
GD1_CALIB = CALIBRATION / "calibration_results/unitree/stereo_intrinsic.yaml"
CALIB_DIR = DATA / "episode_20260720_150841/calibration"
IMAGES = DATA / "episode_20260720_150841_transformed/images"
BLOG = CALIBRATION / "docs/09_双目虚拟相机_博客与示意图3"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Cannot decode image: {path}")
    return image


def build_cross_model_figure(k_virtual, ego_virtual, gd1_calibration) -> dict:
    fig, axes = plt.subplots(2, 4, figsize=(20, 8), layout="constrained")
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("#30343b")
    records = {}
    for row, (device, label, source_model, physical_size) in enumerate([
        ("ego_air", "Ego-Air", "seucm", (1600, 1200)),
        ("gd1", "unitree_gd1", gd1_calibration.camera_model, gd1_calibration.image_size),
    ]):
        calibration_path = RESULTS / f"{device}_virtual_rectified_calibration.json"
        calibration = json.loads(calibration_path.read_text())
        if calibration["image_size"] != {"width": 640, "height": 480}:
            raise ValueError(f"{device}: unexpected virtual image size")
        for side in ["left", "right"]:
            np.testing.assert_array_equal(calibration[side]["K"], k_virtual)
        baseline = calibration["rectified_translation_m"]["tx"]
        if device == "gd1":
            np.testing.assert_allclose(
                baseline, gd1_calibration.baseline, rtol=0, atol=1e-12
            )
        paths = {
            "calibration": calibration_path,
            "left": RESULTS / f"{device}_rectified/left_rect.png",
            "right": RESULTS / f"{device}_rectified/right_rect.png",
            "depth_input_left": RESULTS / f"{device}_stereo_depth/left.png",
            "depth_input_right": RESULTS / f"{device}_stereo_depth/right.png",
            "disparity_visualization": RESULTS / f"{device}_stereo_depth/disp_vis.png",
            "depth_m": RESULTS / f"{device}_stereo_depth/depth_meter.npy",
        }
        images = [read_image(paths[side]) for side in ["left", "right"]]
        for side, image in zip(["left", "right"], images):
            if image.shape != (480, 640, 3):
                raise ValueError(f"{device}: unexpected {side} image shape")
            np.testing.assert_array_equal(image, read_image(paths[f"depth_input_{side}"]))
        if device == "ego_air":
            for image, generated in zip(images, ego_virtual):
                np.testing.assert_array_equal(image, generated)
        disparity = read_image(paths["disparity_visualization"])
        if disparity.shape != (480, 1920, 3):
            raise ValueError(f"{device}: expected a left/right/disparity triptych")
        np.testing.assert_array_equal(disparity[:, :640], images[0])
        np.testing.assert_array_equal(disparity[:, 640:1280], images[1])
        depth = np.load(paths["depth_m"])
        if depth.shape != (480, 640):
            raise ValueError(f"{device}: depth does not use the virtual resolution")
        valid = np.isfinite(depth) & (depth > 0)
        if not valid.any():
            raise ValueError(f"{device}: no positive finite depth")
        for column, image in enumerate([*images, disparity[:, 1280:]]):
            axes[row, column].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        axes[row, 0].set_title(f"{label} / virtual left\nB = {baseline * 1000:.3f} mm")
        axes[row, 1].set_title("Virtual right")
        axes[row, 2].set_title("Disparity / supplied colors")
        plot = axes[row, 3].imshow(
            np.ma.masked_where(~valid, depth), cmap=cmap, vmin=0.25, vmax=5.5
        )
        axes[row, 3].set_title("Saved axial depth / gray = invalid")
        records[device] = {
            "label": label,
            "source_model": source_model,
            "physical_image_size_wh": list(physical_size),
            "virtual_image_size_wh": [640, 480],
            "baseline_m": baseline,
            "fB_m_px": float(k_virtual[0, 0] * baseline),
            "depth_positive_finite_ratio": float(valid.mean()),
            "positive_depth_range_m": [float(depth[valid].min()), float(depth[valid].max())],
            "depth_inputs_match_virtual_images": True,
            "sources": {name: {"path": str(path), "sha256": sha256(path)}
                        for name, path in paths.items()},
        }
    for axis in axes.flat:
        axis.set_axis_off()
    fig.colorbar(plot, ax=axes[:, 3], shrink=0.8, label="Axial depth Z (m)")
    fig.suptitle(
        "Different physical stereo cameras, the same virtual pinhole interface\n"
        "Shared 640 x 480 and K; real baselines preserved / not a shared-pose accuracy test",
        fontsize=16,
    )
    fig.savefig(ASSETS / "virtual_stereo_cross_model.png", dpi=150)
    plt.close(fig)
    return {
        "root": str(RESULTS),
        "K_virtual": k_virtual.tolist(),
        "depth_display_limits_m": [0.25, 5.5],
        "devices": records,
        "scope": (
            "Read existing result images and depth arrays; no new depth inference, "
            "shared-pose comparison or independent accuracy benchmark"
        ),
    }


def main() -> None:
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("blog_virtual_stereo", SOURCE)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load the existing implementation: {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    size = (640, 480)
    calibration = module.build_StereoCalibration_from_ego_air(
        str(CALIB_DIR), "ego_air", calib_model="seucm"
    )
    k_virtual = module.make_virtual_K(
        size, hfov_deg=100, square_pixels=False, vfov_deg=70
    )
    model = module.build_virtual_stereo_model(calibration, k_virtual, size)
    paths = [
        IMAGES / "rgb_left/1784560121000000000.png",
        IMAGES / "rgb_right/1784560121000014080.png",
    ]
    raw = [read_image(path) for path in paths]
    if any((image.shape[1], image.shape[0]) != calibration.image_size for image in raw):
        raise ValueError("Source images do not match the physical calibration size")
    virtual = module.rectify_pair(*raw, model)
    for side, image in zip(["left", "right"], virtual):
        path = ASSETS / f"virtual_stereo_{side}.png"
        if not cv2.imwrite(str(path), image):
            raise OSError(f"Cannot save virtual image: {path}")
    virtual_calibration_path = ASSETS / "virtual_stereo_calibration.json"
    module.save_rectified_calibration(
        model, virtual_calibration_path, calibration.camera_model
    )

    masks = {
        "left": model.valid_1,
        "right": model.valid_2,
        "intersection": model.valid_1 & model.valid_2,
    }
    for name, mask in masks.items():
        path = ASSETS / f"virtual_stereo_mask_{name}.png"
        if not cv2.imwrite(str(path), mask.astype(np.uint8) * 255):
            raise OSError(f"Cannot save mask: {path}")

    geometry = BLOG / "assets/stereo_virtual_camera_comparison.png"
    shutil.copyfile(geometry, ASSETS / "virtual_stereo_geometry.png")
    fig, axes = plt.subplots(
        2, 3, figsize=(15, 8), width_ratios=[1, 1, 0.8], layout="constrained"
    )
    for column, side in enumerate(["left", "right"]):
        axes[0, column].imshow(cv2.cvtColor(raw[column], cv2.COLOR_BGR2RGB))
        axes[0, column].set_title(f"Physical RGB {side} / 1600 x 1200")
        axes[1, column].imshow(cv2.cvtColor(virtual[column], cv2.COLOR_BGR2RGB))
        axes[1, column].set_title(f"Virtual pinhole {side} / 640 x 480")
    axes[0, 2].text(
        0.04, 0.92,
        "SEUCM PRESET\n\n"
        f"Input: {calibration.camera_model.upper()}\n"
        "Output: pinhole\n"
        "HFOV / VFOV: 100 / 70 deg\n\n"
        f"fx = {k_virtual[0, 0]:.3f} px\n"
        f"fy = {k_virtual[1, 1]:.3f} px\n"
        "cx / cy = 319.5 / 239.5\n\n"
        f"B = {model.baseline * 1000:.3f} mm\n"
        "Real baseline preserved\n"
        "No optical-center translation",
        va="top", fontsize=13, linespacing=1.5,
    )
    axes[1, 2].imshow(
        masks["intersection"], cmap="gray", vmin=0, vmax=1, interpolation="nearest"
    )
    ratio = float(masks["intersection"].mean())
    axes[1, 2].set_title(
        f"Sampling-mask intersection: {ratio:.2%}\nWhite = valid; not depth confidence"
    )
    axes[1, 2].add_patch(plt.Rectangle(
        (-0.5, -0.5), size[0], size[1], fill=False, edgecolor="#748094", linewidth=2
    ))
    for axis in axes.flat:
        axis.set_axis_off()
    fig.suptitle(
        "Ego-Air: physical observations to standard virtual views\n"
        "Raw panels are display-scaled; each virtual optical center stays at its physical source",
        fontsize=15,
    )
    fig.savefig(ASSETS / "virtual_stereo_observations.png", dpi=150)
    plt.close(fig)

    algebra = module.validate_algebra(calibration, model)
    synthetic = module.validate_synthetic(calibration, model)
    if not all(np.isfinite(value) for value in [*algebra.values(), *synthetic.values()]):
        raise ValueError("Non-finite algebra or synthetic diagnostic")
    comparison_path = RESULTS / "gd1_virtual_rectified_calibration.json"
    comparison = json.loads(comparison_path.read_text())
    np.testing.assert_array_equal(comparison["left"]["K"], k_virtual)
    gd1_calibration = module.build_StereoCalibration_from_gd1(
        str(GD1_CALIB), "unitree_gd1"
    )
    cross_model = build_cross_model_figure(k_virtual, virtual, gd1_calibration)
    np.testing.assert_allclose(
        cross_model["devices"]["ego_air"]["baseline_m"],
        model.baseline, rtol=0, atol=1e-12,
    )
    sources = {
        "implementation": SOURCE,
        "geometry_illustration": geometry,
        "physical_calibration_left": CALIB_DIR / "rgb_left.json",
        "physical_calibration_right": CALIB_DIR / "rgb_right.json",
        "raw_left": paths[0],
        "raw_right": paths[1],
        "comparison_calibration_snapshot": comparison_path,
        "gd1_physical_calibration": GD1_CALIB,
    }
    audit = {
        "episode": "episode_20260720_150841",
        "sources": {name: {"path": str(path), "sha256": sha256(path)}
                    for name, path in sources.items()},
        "opencv_version": cv2.__version__,
        "source_model": calibration.camera_model,
        "model_selection_basis": (
            "SEUCM selected from the user's previously verified undistortion comparison; "
            "this run does not repeat the comparative benchmark"
        ),
        "virtual_projection_model": "pinhole",
        "virtual_size_wh": list(size),
        "hfov_vfov_deg": [100, 70],
        "fov_definition": "Principal-point scanlines; endpoint centers 0..W-1, 0..H-1",
        "square_pixels": False,
        "K_virtual": k_virtual.tolist(),
        "baseline_m": model.baseline,
        "T_V1_V2": model.T_V1_V2.tolist(),
        "P_V1": model.P_V1.tolist(),
        "P_V2": model.P_V2.tolist(),
        "Q": model.Q.tolist(),
        "mask_positive_ratios": {name: float(mask.mean()) for name, mask in masks.items()},
        "mask_scope": "Finite in-bounds source coordinates with a one-pixel margin only",
        "generated_virtual_calibration": virtual_calibration_path.name,
        "generated_virtual_images": ["virtual_stereo_left.png", "virtual_stereo_right.png"],
        "algebra": algebra,
        "synthetic_projection_roundtrip": synthetic,
        "comparison_snapshot_baseline_m": comparison["rectified_translation_m"]["tx"],
        "cross_model_results": cross_model,
        "scope": "SEUCM geometry/preset generation, not new real-image accuracy acceptance",
    }
    (ASSETS / "virtual_stereo_audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps({
        "source_model": calibration.camera_model,
        "baseline_m": model.baseline,
        "mask_positive_ratios": audit["mask_positive_ratios"],
        "audit": str(ASSETS / "virtual_stereo_audit.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
