# AtmoSync - Dataset Exploration
# Author: Aryan Kumar

import pandas as pd

# 1. Dataset path
file_path = "data/raw/iot_telemetry_data.csv"

# 2. Load dataset
df = pd.read_csv(file_path)

# 3. Display dataset information
print("\n===== ATMOSYNC DATASET EXPLORATION =====")

print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. Column Names:")
print(df.columns.tolist())

print("\n3. First 10 Records:")
print(df.head(10))

print("\n4. Dataset Information:")
df.info()

print("\n5. Missing Values:")
print(df.isnull().sum())

print("\n6. Statistical Summary:")
print(df.describe())

print("\n===== EXPLORATION COMPLETED =====")

# 7. Unique Devices
print("\n7. Unique Devices:")
print(df["device"].nunique())

# 8. Average Temperature
print("\n8. Average Temperature:")
print(df["temp"].mean())

# 9. Average Humidity
print("\n9. Average Humidity:")
print(df["humidity"].mean())

# 10. Temperature Range
print("\n10. Temperature Range:")
print("Minimum:", df["temp"].min())
print("Maximum:", df["temp"].max())

# 11. Humidity Range
print("\n11. Humidity Range:")
print("Minimum:", df["humidity"].min())
print("Maximum:", df["humidity"].max())

# 12. Temperature Distribution
print("\n12. Temperature Distribution:")
print(df["temp"].value_counts().head(10))

# 13. Device-wise Readings
print("\n13. Device-wise Readings:")
print(df["device"].value_counts())

# 14. Timestamp Conversion

df["timestamp"] = pd.to_datetime(
    df["ts"], unit="s"
)

print("\n14. Timestamp Range:")
print("First Reading:", df["timestamp"].min())
print("Last Reading:", df["timestamp"].max())


# 15. Temperature Anomaly Check

zero_temp = df[df["temp"] == 0]

print("\n15. Zero Temperature Records:")
print("Total:", len(zero_temp))


# 16. Device-wise Temperature

print("\n16. Device-wise Average Temperature:")
print(df.groupby("device")["temp"].mean())


# 17. Device-wise Average Humidity

print("\n17. Device-wise Average Humidity:")
print(df.groupby("device")["humidity"].mean())