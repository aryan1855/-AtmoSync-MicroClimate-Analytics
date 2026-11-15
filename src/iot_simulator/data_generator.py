# AtmoSync - IoT Data Generator

import pandas as pd
import numpy as np

print("\n===== ATMOSYNC DATA GENERATOR =====")

# 1. Load Kaggle dataset
DATA_PATH = "data/raw/iot_telemetry_data.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", len(df), "records")

# 2. Convert timestamp
df["timestamp"] = pd.to_datetime(
    df["ts"], unit="s"
)

# 3. Map devices to simulated containers
device_mapping = {
    device: f"C{i+1:03d}"
    for i, device in enumerate(df["device"].unique())
}

df["container_id"] = df["device"].map(device_mapping)

# 4. Rename required columns
df["temperature"] = df["temp"]

# 5. Simulate vibration readings
np.random.seed(42)

df["vibration"] = np.round(
    np.random.uniform(0.1, 3.0, len(df)), 2
)

# 6. Select common project columns
atmosync_df = df[
    [
        "container_id",
        "timestamp",
        "temperature",
        "humidity",
        "vibration"
    ]
].copy()

# 7. Display results
print("\nAtmoSync Dataset Preview:")
print(atmosync_df.head(10))

print("\nTotal records:", len(atmosync_df))
print("\nContainer count:", atmosync_df["container_id"].nunique())

print("\n===== DATA GENERATION COMPLETED =====")
# 8. Validate generated dataset

print("\n===== DATA VALIDATION =====")

print("\nColumn Names:")
print(atmosync_df.columns.tolist())

print("\nMissing Values:")
print(atmosync_df.isnull().sum())

print("\nData Types:")
print(atmosync_df.dtypes)

print("\nTemperature Range:")
print(atmosync_df["temperature"].min(), "to", atmosync_df["temperature"].max())

print("\nHumidity Range:")
print(atmosync_df["humidity"].min(), "to", atmosync_df["humidity"].max())

print("\nVibration Range:")
print(atmosync_df["vibration"].min(), "to", atmosync_df["vibration"].max())

print("\nDuplicate Rows:", atmosync_df.duplicated().sum())

# 9. Export raw sensor dataset

OUTPUT_PATH = "data/raw/raw_sensor_data.csv"

atmosync_df.to_csv(OUTPUT_PATH, index=False)

print("\nRaw sensor dataset exported successfully!")
print("File location:", OUTPUT_PATH)