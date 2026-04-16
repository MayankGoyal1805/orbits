from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _round(value: float) -> float:
    return round(float(value), 4)


def build_priors(processed_dir: Path) -> dict:
    satcat = pd.read_csv(processed_dir / "satcat_clean.csv")
    ucs = pd.read_csv(processed_dir / "ucs_clean.csv")
    kelvins = pd.read_csv(processed_dir / "kelvins_labels_clean.csv")

    debris_ratio = (satcat["OBJECT_TYPE"].fillna("UNK") == "DEB").mean()
    payload_ratio = (satcat["OBJECT_TYPE"].fillna("UNK") == "PAY").mean()

    orbit_norm = ucs["Class of Orbit"].astype(str).str.strip().str.upper().str.replace(r"\s+", "", regex=True)
    leo_ratio = (orbit_norm == "LEO").mean()
    geo_ratio = (orbit_norm == "GEO").mean()

    ecc_candidate = pd.to_numeric(kelvins.get("eccentricity"), errors="coerce")
    if ecc_candidate.dropna().quantile(0.95) <= 1.2:
        ecc = ecc_candidate.dropna()
    else:
        # In this dataset variant, the column named "semi_major_axis_km" behaves like
        # an eccentricity-like bounded feature (~0..1), so use it for uncertainty scaling.
        ecc = pd.to_numeric(kelvins.get("semi_major_axis_km"), errors="coerce").dropna()
    inc = pd.to_numeric(kelvins.get("inclination_deg"), errors="coerce").dropna()
    area_mass = pd.to_numeric(kelvins.get("area_to_mass_ratio"), errors="coerce").dropna()

    ecc_p75 = float(ecc.quantile(0.75)) if not ecc.empty else 0.08
    inc_std = float(inc.std()) if not inc.empty else 12.0
    area_mass_p50 = float(area_mass.quantile(0.5)) if not area_mass.empty else 8.0

    # Dataset-informed scaling terms for conjunction uncertainty/growth behavior.
    risk_scale = _clamp(0.95 + 0.22 * debris_ratio + 0.12 * leo_ratio, 1.0, 1.2)
    uncertainty_scale = _clamp(0.9 + 2.2 * ecc_p75, 0.95, 1.25)
    tracking_scale = _clamp(0.85 + 0.35 * leo_ratio + 0.015 * (inc_std / 10.0), 0.9, 1.2)

    priors = {
        "metadata": {
            "source": "assignment/eda/input_data/processed",
            "version": 1,
            "notes": "Auto-generated task overrides derived from SATCAT/UCS/Kelvins EDA outputs.",
        },
        "dataset_stats": {
            "satcat_rows": int(len(satcat)),
            "ucs_rows": int(len(ucs)),
            "kelvins_rows": int(len(kelvins)),
            "debris_ratio": _round(debris_ratio),
            "payload_ratio": _round(payload_ratio),
            "leo_ratio": _round(leo_ratio),
            "geo_ratio": _round(geo_ratio),
            "kelvins_eccentricity_p75": _round(ecc_p75),
            "kelvins_inclination_std": _round(inc_std),
            "kelvins_area_to_mass_p50": _round(area_mass_p50),
            "risk_scale": _round(risk_scale),
            "uncertainty_scale": _round(uncertainty_scale),
            "tracking_scale": _round(tracking_scale),
        },
        "task_overrides": {
            "collision_avoidance_easy": {
                "initial_tracking_quality": _round(_clamp(0.8 + 0.05 * (1.0 - leo_ratio), 0.78, 0.86)),
                "success_probability_threshold": _round(_clamp(0.19 + 0.02 * debris_ratio, 0.18, 0.23)),
                "conjunctions": [
                    {
                        "uncertainty": _round(_clamp(0.12 * uncertainty_scale, 0.1, 0.2)),
                        "risk_growth_rate": _round(_clamp(0.058 * risk_scale, 0.05, 0.08)),
                        "tracking_sensitivity": _round(_clamp(0.44 * tracking_scale, 0.4, 0.62)),
                    }
                ],
            },
            "collision_avoidance_medium": {
                "initial_tracking_quality": _round(_clamp(0.66 + 0.05 * (1.0 - leo_ratio), 0.64, 0.74)),
                "success_probability_threshold": _round(_clamp(0.245 + 0.03 * debris_ratio, 0.24, 0.29)),
                "conjunctions": [
                    {
                        "uncertainty": _round(_clamp(0.2 * uncertainty_scale, 0.18, 0.3)),
                        "risk_growth_rate": _round(_clamp(0.053 * risk_scale, 0.05, 0.08)),
                        "tracking_sensitivity": _round(_clamp(0.53 * tracking_scale, 0.45, 0.72)),
                    },
                    {
                        "uncertainty": _round(_clamp(0.24 * uncertainty_scale, 0.2, 0.32)),
                        "risk_growth_rate": _round(_clamp(0.049 * risk_scale, 0.045, 0.075)),
                        "tracking_sensitivity": _round(_clamp(0.47 * tracking_scale, 0.4, 0.7)),
                    },
                ],
            },
            "collision_avoidance_hard": {
                "initial_tracking_quality": _round(_clamp(0.55 + 0.04 * (1.0 - leo_ratio), 0.54, 0.62)),
                "success_probability_threshold": _round(_clamp(0.285 + 0.03 * debris_ratio, 0.28, 0.33)),
                "conjunctions": [
                    {
                        "uncertainty": _round(_clamp(0.3 * uncertainty_scale, 0.26, 0.4)),
                        "risk_growth_rate": _round(_clamp(0.067 * risk_scale, 0.06, 0.095)),
                        "tracking_sensitivity": _round(_clamp(0.6 * tracking_scale, 0.5, 0.82)),
                    },
                    {
                        "uncertainty": _round(_clamp(0.26 * uncertainty_scale, 0.22, 0.36)),
                        "risk_growth_rate": _round(_clamp(0.054 * risk_scale, 0.05, 0.085)),
                        "tracking_sensitivity": _round(_clamp(0.5 * tracking_scale, 0.42, 0.75)),
                    },
                    {
                        "uncertainty": _round(_clamp(0.32 * uncertainty_scale, 0.26, 0.42)),
                        "risk_growth_rate": _round(_clamp(0.059 * risk_scale, 0.053, 0.09)),
                        "tracking_sensitivity": _round(_clamp(0.57 * tracking_scale, 0.5, 0.8)),
                    },
                ],
            },
        },
    }
    return priors


def main() -> None:
    parser = argparse.ArgumentParser(description="Build task priors from processed EDA datasets.")
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("assignment/eda/input_data/processed"),
        help="Directory containing processed EDA CSV files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("src/orbits_env/tasks/task_priors.json"),
        help="Output JSON path for task priors.",
    )
    args = parser.parse_args()

    priors = build_priors(args.processed_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(priors, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote task priors: {args.output}")
    print(json.dumps(priors["dataset_stats"], indent=2))


if __name__ == "__main__":
    main()
