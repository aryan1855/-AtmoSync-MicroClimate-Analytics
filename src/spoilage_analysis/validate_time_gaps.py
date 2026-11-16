import pandas as pd
from pathlib import Path

# Locate project root
project_root = Path(__file__).resolve().parents[2]

# Load processed data
data_path = (
    project_root / "data" / "processed" /
    "processed_sensor_data.csv"
)

df = pd.read_csv(data_path)

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort by container and timestamp
df = df.sort_values(["container_id", "timestamp"])

# Calculate time gaps
df["time_gap_seconds"] = (
    df.groupby("container_id")["timestamp"]
    .diff()
    .dt.total_seconds()
)

print("===== TIME GAP VALIDATION =====")

for container, group in df.groupby("container_id"):

    gaps = group["time_gap_seconds"].dropna()

    median_gap = gaps.median()

    # Define unusually large gap as more than 2x median
    long_gap_limit = median_gap * 2

    zero_gaps = (gaps == 0).sum()

    long_gaps = (gaps > long_gap_limit).sum()

    print(f"\nContainer: {container}")
    print(f"Median Interval: {median_gap:.2f} seconds")
    print(f"Zero Gaps: {zero_gaps}")
    print(f"Long Gap Limit: {long_gap_limit:.2f} seconds")
    print(f"Long Gaps: {long_gaps}")
    print(f"Maximum Gap: {gaps.max():.2f} seconds")

print("\nValidation completed successfully!")