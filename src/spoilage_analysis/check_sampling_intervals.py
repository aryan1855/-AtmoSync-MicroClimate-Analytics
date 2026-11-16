import pandas as pd
from pathlib import Path

# Locate project directory
project_root = Path(__file__).resolve().parents[2]

# Load processed dataset
data_path = project_root / "data" / "processed" / "processed_sensor_data.csv"

df = pd.read_csv(data_path)

# Convert timestamp into datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort records
df = df.sort_values(["container_id", "timestamp"])

# Calculate time difference between consecutive readings
df["time_gap"] = (
    df.groupby("container_id")["timestamp"].diff()
)

# Convert time difference into seconds
df["time_gap_seconds"] = df["time_gap"].dt.total_seconds()

# Display sampling interval analysis
print("===== SAMPLING INTERVAL ANALYSIS =====")

print("\nOverall Time Gap Statistics:")
print(df["time_gap_seconds"].describe())

print("\nContainer-wise Time Gap Statistics:")

summary = df.groupby("container_id")["time_gap_seconds"].describe()

print(summary.round(2))

print("\nMost Common Time Gaps:")

print(
    df["time_gap_seconds"]
    .value_counts()
    .head(10)
)