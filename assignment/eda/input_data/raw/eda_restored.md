# Orbital Debris EDA

This project analyzes orbital debris and satellite catalogs to support a collision-avoidance simulation environment.

Primary objectives:
* profile debris and satellite populations
* clean and standardize source datasets
* produce evidence-driven insights for environment design and evaluation

Datasets used:
* CeleTrak SATCAT
* UCS Satellite Database
* ESA Kelvins "Space Debris: the origin"

## Data Loading and Initial Inspection

Load the raw datasets, verify file availability, and inspect basic structure (shape, columns, sample rows).

```python
from pathlib import Path
import pandas as pd

# Base paths
ROOT = Path.cwd()
RAW_DIR = ROOT / "input_data" / "raw"

# Files used in this analysis
SATCAT_PATH = RAW_DIR / "satcat.csv"
UCS_PATH = RAW_DIR / "satellites.csv"
KELVINS_DIR = RAW_DIR / "space-debris-the-origin"
KELVINS_LABELS_PATH = KELVINS_DIR / "labels_train.dat"

print("Root:", ROOT)
print("Raw data dir:", RAW_DIR)

# 1) Existence checks
required = {
    "satcat": SATCAT_PATH,
    "ucs": UCS_PATH,
    "kelvins_dir": KELVINS_DIR,
    "kelvins_labels": KELVINS_LABELS_PATH,
}

print("\nFile checks:")
for name, path in required.items():
    print(f"- {name}: {'OK' if path.exists() else 'MISSING'} -> {path}")

# 2) Read SATCAT
satcat_df = pd.read_csv(SATCAT_PATH)
print("\nSATCAT shape:", satcat_df.shape)
print("SATCAT columns:", list(satcat_df.columns))
print("SATCAT preview:")
display(satcat_df.head(3))

# 3) Read UCS
# Many UCS exports are semicolon-delimited; we load with ';' first and standardize later.
ucs_df = pd.read_csv(UCS_PATH, sep=";", engine="python")
print("\nUCS shape:", ucs_df.shape)
print("UCS columns (first 15):", list(ucs_df.columns[:15]))
print("UCS preview:")
display(ucs_df.head(3))

# 4) Read Kelvins labels (whitespace-delimited, no header)
# Column meaning from challenge docs:
# 0: originator satellite id
# 1: area-to-mass ratio
# 2..8: epoch/orbital-element values
kelvins_labels = pd.read_csv(KELVINS_LABELS_PATH, sep=r"\s+", header=None)
print("\nKelvins labels shape:", kelvins_labels.shape)
print("Kelvins labels preview:")
display(kelvins_labels.head(5))
```

## UCS Data Preparation

Standardize UCS fields and save cleaned output to `input_data/processed/ucs_clean.csv`.

```python
# Create a working copy of UCS data
ucs_clean = ucs_df.copy()

# Ensure processed output directory exists
PROCESSED_DIR = ROOT / "input_data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# 1) Normalize header spacing
ucs_clean.columns = [c.strip() for c in ucs_clean.columns]

# 2) Drop parser-generated placeholder columns from the raw export
# These often appear as Unnamed:* after parsing rows with trailing separators.
unnamed_cols = [c for c in ucs_clean.columns if c.startswith("Unnamed:")]
ucs_clean = ucs_clean.drop(columns=unnamed_cols, errors="ignore")

# 3) Split combined first field: "Name of Satellite, Alternate Names"
# into two explicit columns where possible.
first_col = "Name of Satellite, Alternate Names"
if first_col in ucs_clean.columns:
    split_cols = ucs_clean[first_col].astype(str).str.split(",", n=1, expand=True)
    ucs_clean["Name of Satellite"] = split_cols[0].str.strip()
    ucs_clean["Alternate Names (raw)"] = split_cols[1].fillna("").str.strip()

# 4) Standardize key numeric-like columns that may contain decimal commas
numeric_candidates = [
    "Perigee (km)",
    "Apogee (km)",
    "Eccentricity",
    "Inclination (degrees)",
    "Period (minutes)",
    "Launch Mass (kg.)",
    "Dry Mass (kg.)",
    "Power (watts)",
]

for col in numeric_candidates:
    if col in ucs_clean.columns:
        ucs_clean[col] = (
            ucs_clean[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace(" ", "", regex=False)
        )
        ucs_clean[col] = pd.to_numeric(ucs_clean[col], errors="coerce")

# 5) Parse launch date
if "Date of Launch" in ucs_clean.columns:
    ucs_clean["Date of Launch"] = pd.to_datetime(
        ucs_clean["Date of Launch"], errors="coerce", dayfirst=True, format="mixed"
    )

# 6) Persist cleaned dataset
ucs_clean_path = PROCESSED_DIR / "ucs_clean.csv"
ucs_clean.to_csv(ucs_clean_path, index=False)

print("Original UCS shape:", ucs_df.shape)
print("Cleaned UCS shape:", ucs_clean.shape)
print("Dropped unnamed columns:", len(unnamed_cols))
print("Saved cleaned file:", ucs_clean_path)

print("\nCleaned columns (first 25):")
print(list(ucs_clean.columns[:25]))

print("\nMissing values (top 10 columns):")
print(ucs_clean.isna().sum().sort_values(ascending=False).head(10))

display(ucs_clean.head(3))
```

## SATCAT Preparation

Standardize SATCAT fields and save a cleaned table to `input_data/processed/satcat_clean.csv`.

```python
satcat_clean = satcat_df.copy()

for date_col in ["LAUNCH_DATE", "DECAY_DATE"]:
    if date_col in satcat_clean.columns:
        satcat_clean[date_col] = pd.to_datetime(satcat_clean[date_col], errors="coerce")

numeric_satcat = ["PERIOD", "INCLINATION", "APOGEE", "PERIGEE", "RCS"]
for col in numeric_satcat:
    if col in satcat_clean.columns:
        satcat_clean[col] = pd.to_numeric(satcat_clean[col], errors="coerce")

satcat_clean_path = PROCESSED_DIR / "satcat_clean.csv"
satcat_clean.to_csv(satcat_clean_path, index=False)

print("SATCAT original:", satcat_df.shape)
print("SATCAT cleaned:", satcat_clean.shape)
print("Saved:", satcat_clean_path)
display(satcat_clean.head(3))
```

## Kelvins Preparation

Parse labels and trajectory files, then save processed outputs under `input_data/processed`.

```python
from pathlib import Path

kelvins_labels_clean = kelvins_labels.copy()
kelvins_labels_clean.columns = [
    "originator_id",
    "area_to_mass_ratio",
    "feature_2",
    "feature_3",
    "semi_major_axis_km",
    "eccentricity",
    "inclination_deg",
    "mean_anomaly_deg",
    "raan_or_arg_deg",
]

kelvins_labels_path = PROCESSED_DIR / "kelvins_labels_clean.csv"
kelvins_labels_clean.to_csv(kelvins_labels_path, index=False)

def read_kelvins_folder(folder_path: Path):
    files = sorted(folder_path.glob("*.dat"))
    frames = []
    for file in files:
        temp = pd.read_csv(file, sep=r"\s+", header=None)
        temp["trajectory_file"] = file.name
        temp["trajectory_id"] = file.stem
        frames.append(temp)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)

kelvins_deb_train = read_kelvins_folder(KELVINS_DIR / "deb_train")
kelvins_deb_test = read_kelvins_folder(KELVINS_DIR / "deb_test")
kelvins_sat = read_kelvins_folder(KELVINS_DIR / "sat")

kelvins_deb_train.to_csv(PROCESSED_DIR / "kelvins_deb_train_long.csv", index=False)
kelvins_deb_test.to_csv(PROCESSED_DIR / "kelvins_deb_test_long.csv", index=False)
kelvins_sat.to_csv(PROCESSED_DIR / "kelvins_sat_long.csv", index=False)

print("Kelvins labels shape:", kelvins_labels_clean.shape)
print("Kelvins deb_train shape:", kelvins_deb_train.shape)
print("Kelvins deb_test shape:", kelvins_deb_test.shape)
print("Kelvins sat shape:", kelvins_sat.shape)
print("Saved label file:", kelvins_labels_path)
```

## Data Quality Summary

Create compact quality tables for cleaned SATCAT, cleaned UCS, and Kelvins labels.

```python
def quality_table(df: pd.DataFrame, name: str) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "dataset": [name],
            "rows": [len(df)],
            "columns": [df.shape[1]],
            "duplicate_rows": [int(df.duplicated().sum())],
            "missing_cells": [int(df.isna().sum().sum())],
            "missing_pct": [round(df.isna().sum().sum() / (df.shape[0] * df.shape[1]) * 100, 2)],
        }
    )

quality_overview = pd.concat(
    [
        quality_table(satcat_clean, "satcat_clean"),
        quality_table(ucs_clean, "ucs_clean"),
        quality_table(kelvins_labels_clean, "kelvins_labels_clean"),
    ],
    ignore_index=True,
)

display(quality_overview)

missing_by_dataset = {
    "satcat_clean": satcat_clean.isna().sum().sort_values(ascending=False).head(10),
    "ucs_clean": ucs_clean.isna().sum().sort_values(ascending=False).head(10),
    "kelvins_labels_clean": kelvins_labels_clean.isna().sum().sort_values(ascending=False).head(10),
}

for name, series in missing_by_dataset.items():
    print(f"\nTop missing columns in {name}:")
    print(series)
```

## SATCAT Analysis

Summarize object composition and temporal launch trend.

```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# Object type distribution
obj_counts = satcat_clean["OBJECT_TYPE"].fillna("UNKNOWN").value_counts().reset_index()
obj_counts.columns = ["OBJECT_TYPE", "count"]
display(obj_counts)

plt.figure(figsize=(8, 4))
sns.barplot(data=obj_counts, x="OBJECT_TYPE", y="count")
plt.title("SATCAT Object Type Distribution")
plt.xlabel("Object Type")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Launch trend by year
launch_year_counts = (
    satcat_clean.dropna(subset=["LAUNCH_DATE"])
    .assign(launch_year=satcat_clean["LAUNCH_DATE"].dt.year)
    .groupby("launch_year")
    .size()
    .reset_index(name="count")
)

display(launch_year_counts.tail(15))

plt.figure(figsize=(10, 4))
sns.lineplot(data=launch_year_counts, x="launch_year", y="count")
plt.title("SATCAT Launch Count by Year")
plt.xlabel("Launch Year")
plt.ylabel("Number of Objects")
plt.tight_layout()
plt.show()
```

## UCS Analysis

Summarize operational satellite purpose, orbit class, and launch trend.

```python
ucs_purpose = (
    ucs_clean["Purpose"].fillna("Unknown").value_counts().reset_index()
)
ucs_purpose.columns = ["Purpose", "count"]
display(ucs_purpose.head(15))

plt.figure(figsize=(10, 5))
sns.barplot(data=ucs_purpose.head(12), x="count", y="Purpose")
plt.title("Top UCS Satellite Purposes")
plt.xlabel("Count")
plt.ylabel("Purpose")
plt.tight_layout()
plt.show()

orbit_norm = (
    ucs_clean["Class of Orbit"]
    .astype(str)
    .str.strip()
    .str.upper()
    .replace({"LEO": "LEO", "LEO ": "LEO", "LEO0": "LEO", "LEO": "LEO", "LEO": "LEO", "LEO": "LEO"})
)
orbit_norm = orbit_norm.where(orbit_norm.isin(["LEO", "MEO", "GEO", "ELLIPTICAL"]), "OTHER/UNKNOWN")
ucs_orbit = orbit_norm.value_counts().reset_index()
ucs_orbit.columns = ["Class of Orbit", "count"]
display(ucs_orbit)

plt.figure(figsize=(7, 4))
sns.barplot(data=ucs_orbit, x="Class of Orbit", y="count")
plt.title("UCS Orbit Class Distribution")
plt.xlabel("Orbit Class")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

ucs_launch_year = (
    ucs_clean.dropna(subset=["Date of Launch"])
    .assign(launch_year=lambda d: d["Date of Launch"].dt.year)
)
ucs_launch_year = ucs_launch_year[
    (ucs_launch_year["launch_year"] >= 1957) & (ucs_launch_year["launch_year"] <= 2035)
]
ucs_launch_year = (
    ucs_launch_year.groupby("launch_year").size().reset_index(name="count")
)

display(ucs_launch_year.tail(15))

plt.figure(figsize=(10, 4))
sns.lineplot(data=ucs_launch_year, x="launch_year", y="count")
plt.title("UCS Launch Count by Year")
plt.xlabel("Launch Year")
plt.ylabel("Number of Satellites")
plt.tight_layout()
plt.show()
```

## Kelvins Analysis

Debris-vs-satellite class balance and basic orbital element distributions.

```python
kelvins_numeric = kelvins_labels_clean.apply(pd.to_numeric, errors="coerce")
kelvins_stats = kelvins_numeric.describe().T
kelvins_stats["missing_ratio"] = kelvins_numeric.isna().mean()
display(kelvins_stats)

kelvins_plot_cols = [
    "area_to_mass_ratio",
    "semi_major_axis_km",
    "eccentricity",
    "inclination_deg",
]
kelvins_plot_cols = [c for c in kelvins_plot_cols if c in kelvins_numeric.columns]

if kelvins_plot_cols:
    fig, axes = plt.subplots(1, len(kelvins_plot_cols), figsize=(4 * len(kelvins_plot_cols), 3.5))
    if len(kelvins_plot_cols) == 1:
        axes = [axes]
    for ax, col in zip(axes, kelvins_plot_cols):
        sns.histplot(kelvins_numeric[col].dropna(), bins=30, kde=False, ax=ax)
        ax.set_title(col)
    plt.tight_layout()
    plt.show()

trajectory_summary = pd.DataFrame(
    [
        {
            "subset": "deb_train",
            "rows": len(kelvins_deb_train),
            "trajectories": kelvins_deb_train["trajectory_id"].nunique(),
            "avg_points_per_trajectory": round(len(kelvins_deb_train) / kelvins_deb_train["trajectory_id"].nunique(), 2),
        },
        {
            "subset": "deb_test",
            "rows": len(kelvins_deb_test),
            "trajectories": kelvins_deb_test["trajectory_id"].nunique(),
            "avg_points_per_trajectory": round(len(kelvins_deb_test) / kelvins_deb_test["trajectory_id"].nunique(), 2),
        },
        {
            "subset": "sat",
            "rows": len(kelvins_sat),
            "trajectories": kelvins_sat["trajectory_id"].nunique(),
            "avg_points_per_trajectory": round(len(kelvins_sat) / kelvins_sat["trajectory_id"].nunique(), 2),
        },
    ]
)
display(trajectory_summary)
```

## Integrated Findings

Final EDA summary and checks for modeling-ready artifacts.

```python
summary_points = pd.DataFrame(
    [
        {
            "dataset": "SATCAT",
            "rows": len(satcat_clean),
            "notes": "Large historical object catalog; object types and launch trends available",
        },
        {
            "dataset": "UCS",
            "rows": len(ucs_clean),
            "notes": "Operational context with purpose and orbit class",
        },
        {
            "dataset": "Kelvins",
            "rows": len(kelvins_labels_clean),
            "notes": "Labeled orbital features plus long-form trajectory files",
        },
    ]
)

display(summary_points)

expected_outputs = [
    PROCESSED_DIR / "satcat_clean.csv",
    PROCESSED_DIR / "ucs_clean.csv",
    PROCESSED_DIR / "kelvins_labels_clean.csv",
    PROCESSED_DIR / "kelvins_deb_train_long.csv",
    PROCESSED_DIR / "kelvins_deb_test_long.csv",
    PROCESSED_DIR / "kelvins_sat_long.csv",
]

outputs_status = pd.DataFrame(
    {
        "file": [p.name for p in expected_outputs],
        "exists": [p.exists() for p in expected_outputs],
    }
)
display(outputs_status)

print("EDA complete: cleaned artifacts are ready under input_data/processed/")
```
