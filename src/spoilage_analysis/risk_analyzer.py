import pandas as pd
import json
from pathlib import Path


# Locate project root
project_root = Path(__file__).resolve().parents[2]

# Load configuration
config_path = project_root / "config" / "avocado_thresholds.json"

with open(config_path, "r") as file:
    config = json.load(file)


# Load processed sensor data
data_path = project_root / "data" / "processed" / "processed_sensor_data.csv"

df = pd.read_csv(data_path)

# Read recommended storage conditions
temperature_min = config["storage_conditions"]["temperature_celsius"]["minimum"]
temperature_max = config["storage_conditions"]["temperature_celsius"]["maximum"]

humidity_min = config["storage_conditions"]["humidity_percentage"]["minimum"]
humidity_max = config["storage_conditions"]["humidity_percentage"]["maximum"]


# Analyze temperature
df["temperature_status"] = df["temperature"].apply(
    lambda value: "Within Range"
    if temperature_min <= value <= temperature_max
    else "Outside Range"
)


# Analyze humidity
df["humidity_status"] = df["humidity"].apply(
    lambda value: "Within Range"
    if humidity_min <= value <= humidity_max
    else "Outside Range"
)


# Display analysis
print("===== ATMOSYNC ENVIRONMENTAL ANALYSIS =====")

print("\nTemperature Analysis:")
print(df["temperature_status"].value_counts())

print("\nHumidity Analysis:")
print(df["humidity_status"].value_counts())


# Container-wise analysis
print("\n===== CONTAINER-WISE ANALYSIS =====")

summary = df.groupby("container_id").agg(
    total_readings=("container_id", "count"),
    avg_temperature=("temperature", "mean"),
    avg_humidity=("humidity", "mean"),
    temperature_outside_range=(
        "temperature_status",
        lambda x: (x == "Outside Range").sum()
    ),
    humidity_outside_range=(
        "humidity_status",
        lambda x: (x == "Outside Range").sum()
    )
)

print(summary.round(2))


# Export analysis
output_path = (
    project_root / "data" / "processed" /
    "avocado_environment_analysis.csv"
)

df.to_csv(output_path, index=False)

print("\nAnalysis completed successfully!")
print("Output saved at:", output_path)