import pandas as pd
import json
from pathlib import Path


# Locate project root
project_root = Path(__file__).resolve().parents[2]

# Load commodity configuration
config_path = project_root / "config" / "avocado_thresholds.json"

with open(config_path, "r") as file:
    config = json.load(file)


# Load processed sensor data
data_path = (
    project_root / "data" / "processed" /
    "processed_sensor_data.csv"
)

df = pd.read_csv(data_path)

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort records
df = df.sort_values(["container_id", "timestamp"])

# Read recommended ranges
temp_min = config["storage_conditions"]["temperature_celsius"]["minimum"]
temp_max = config["storage_conditions"]["temperature_celsius"]["maximum"]

humidity_min = config["storage_conditions"]["humidity_percentage"]["minimum"]
humidity_max = config["storage_conditions"]["humidity_percentage"]["maximum"]


# Calculate time gaps separately for each container
df["time_gap_seconds"] = (
    df.groupby("container_id")["timestamp"]
    .diff()
    .dt.total_seconds()
)


# Identify normal and uncertain intervals
df["median_gap"] = (
    df.groupby("container_id")["time_gap_seconds"]
    .transform("median")
)

df["long_gap_limit"] = df["median_gap"] * 2

df["valid_interval"] = (
    df["time_gap_seconds"].notna()
    & (df["time_gap_seconds"] > 0)
    & (df["time_gap_seconds"] <= df["long_gap_limit"])
)


# Check environmental conditions
df["temperature_outside"] = (
    (df["temperature"] < temp_min)
    | (df["temperature"] > temp_max)
)

df["humidity_outside"] = (
    (df["humidity"] < humidity_min)
    | (df["humidity"] > humidity_max)
)


# Calculate exposure duration in hours
df["temperature_exposure_hours"] = (
    df["time_gap_seconds"].where(
        df["valid_interval"] & df["temperature_outside"],
        0
    ) / 3600
)

df["humidity_exposure_hours"] = (
    df["time_gap_seconds"].where(
        df["valid_interval"] & df["humidity_outside"],
        0
    ) / 3600
)


# Container-wise summary
summary = df.groupby("container_id").agg(
    total_readings=("container_id", "count"),

    temperature_exposure_hours=(
        "temperature_exposure_hours", "sum"
    ),

    humidity_exposure_hours=(
        "humidity_exposure_hours", "sum"
    ),

    excluded_intervals=(
        "valid_interval",
        lambda x: (~x).sum()
    )
).round(4)


print("===== ATMOSYNC EXPOSURE DURATION ANALYSIS =====")

print(summary)


# Export detailed results
detail_path = (
    project_root / "data" / "processed" /
    "avocado_exposure_analysis.csv"
)

df.to_csv(detail_path, index=False)

# Export summary
summary_path = (
    project_root / "data" / "processed" /
    "avocado_exposure_summary.csv"
)

summary.to_csv(summary_path)

print("\nExposure analysis completed successfully!")
print("Detailed output:", detail_path)
print("Summary output:", summary_path)