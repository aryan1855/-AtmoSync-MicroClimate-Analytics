"""
Avocado Temperature-Based Degradation Model

Scientific reference:
Perez et al. (2004)
Q10 = 2.75
Reference temperature = 10°C
Reference shelf life = 22 days

IMPORTANT:
This is an illustrative prototype model, not a validated
prediction of actual avocado spoilage.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    ROOT_DIR / "data" / "processed" / "avocado_exposure_analysis.csv"
)

CONFIG_FILE = ROOT_DIR / "config" / "avocado_thresholds.json"

OUTPUT_FILE = (
    ROOT_DIR / "data" / "processed" / "avocado_degradation_report.csv"
)

# Published empirical reference parameters
Q10 = 2.75
REFERENCE_TEMPERATURE = 10.0
REFERENCE_SHELF_LIFE_DAYS = 22.0

# Research observations covered 7°C to 25°C.
VALID_TEMPERATURE_MIN = 7.0
VALID_TEMPERATURE_MAX = 25.0


def load_data():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

    df = pd.read_csv(INPUT_FILE)

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config = json.load(file)

    required_columns = {
        "container_id",
        "timestamp",
        "temperature",
        "time_gap_seconds",
        "valid_interval",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df, config


def calculate_shelf_life(temperature):
    """
    Estimate temperature-dependent shelf life using Q10.

    Shelf life(T) = Reference shelf life /
                    Q10 ^ ((T - Reference temperature) / 10)
    """

    return REFERENCE_SHELF_LIFE_DAYS / (
        Q10 ** ((temperature - REFERENCE_TEMPERATURE) / 10)
    )


def analyze_container(group):
    group = group.sort_values("timestamp").copy()

    group["valid_interval"] = (
        group["valid_interval"].astype(str).str.lower() == "true"
    )

    group["temperature"] = pd.to_numeric(
        group["temperature"], errors="coerce"
    )

    group["time_gap_seconds"] = pd.to_numeric(
        group["time_gap_seconds"], errors="coerce"
    )

    # Only use valid intervals with temperatures inside
    # the empirical research range.
    valid = group[
        group["valid_interval"]
        & group["temperature"].between(
            VALID_TEMPERATURE_MIN,
            VALID_TEMPERATURE_MAX,
        )
        & group["time_gap_seconds"].gt(0)
    ].copy()

    if valid.empty:
        return {
            "container_id": group["container_id"].iloc[0],
            "modeled_exposure_hours": 0.0,
            "degradation_fraction": np.nan,
            "degradation_percent": np.nan,
            "remaining_hours_estimate": np.nan,
            "estimated_shelf_life_at_last_temp_days": np.nan,
            "last_temperature": np.nan,
            "model_status": "INSUFFICIENT_VALID_DATA",
        }

    # Convert seconds into days.
    valid["interval_days"] = valid["time_gap_seconds"] / 86400

    # Temperature-dependent estimated shelf life.
    valid["estimated_shelf_life_days"] = valid[
        "temperature"
    ].apply(calculate_shelf_life)

    # Fraction of shelf life consumed during each interval.
    valid["degradation_fraction"] = (
        valid["interval_days"] / valid["estimated_shelf_life_days"]
    )

    cumulative_degradation = valid["degradation_fraction"].sum()

    modeled_hours = valid["time_gap_seconds"].sum() / 3600

    last_temperature = float(group["temperature"].iloc[-1])

    last_temperature_valid = (
        VALID_TEMPERATURE_MIN
        <= last_temperature
        <= VALID_TEMPERATURE_MAX
    )

    if not last_temperature_valid:
        remaining_hours = np.nan
        shelf_life = np.nan
        status = "OUTSIDE_VALIDATION_RANGE"

    else:
        shelf_life = calculate_shelf_life(last_temperature)

        # Remaining time under the assumption that the
        # last observed temperature remains constant.
        remaining_fraction = max(0.0, 1.0 - cumulative_degradation)

        remaining_hours = (
            remaining_fraction * shelf_life * 24
        )

        if cumulative_degradation >= 1:
            status = "ESTIMATED_THRESHOLD_REACHED"
        else:
            status = "ESTIMATED_WITHIN_MODEL_THRESHOLD"

    return {
        "container_id": group["container_id"].iloc[0],
        "modeled_exposure_hours": round(modeled_hours, 2),
        "degradation_fraction": round(
            cumulative_degradation, 4
        ),
        "degradation_percent": round(
            cumulative_degradation * 100, 2
        ),
        "remaining_hours_estimate": (
            round(remaining_hours, 2)
            if pd.notna(remaining_hours)
            else np.nan
        ),
        "estimated_shelf_life_at_last_temp_days": (
            round(shelf_life, 2)
            if pd.notna(shelf_life)
            else np.nan
        ),
        "last_temperature": round(last_temperature, 2),
        "model_status": status,
    }


def main():
    df, config = load_data()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )

    df = df.dropna(
        subset=["container_id", "timestamp"]
    )

    results = []

    for _, group in df.groupby("container_id"):
        results.append(analyze_container(group))

    report = pd.DataFrame(results)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    report.to_csv(OUTPUT_FILE, index=False)

    print("\nAVOCADO DEGRADATION ANALYSIS")
    print("=" * 65)

    print(report.to_string(index=False))

    print("\nScientific reference:")
    print("Perez et al. (2004), Q10 = 2.75")
    print("Reference shelf life = 22 days at 10°C")

    print("\nCommodity:", config["commodity"])
    print("Output:", OUTPUT_FILE)
    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()