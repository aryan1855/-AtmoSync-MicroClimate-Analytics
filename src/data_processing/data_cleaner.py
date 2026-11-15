# AtmoSync - Data Processing Module

import pandas as pd
import numpy as np

print("\n===== ATMOSYNC DATA PROCESSING MODULE =====")

# 1. Input dataset path
INPUT_PATH = "data/raw/raw_sensor_data.csv"

# 2. Load raw sensor dataset
df = pd.read_csv(INPUT_PATH)

print("\nDataset loaded successfully!")

# 3. Basic dataset information
print("\nTotal Records:", len(df))

print("\nDataset Columns:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

print("\n===== INITIAL DATA INSPECTION COMPLETED =====")

# 4. Convert timestamp into datetime format

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

print("\nTimestamp Conversion Completed!")

# 5. Check invalid timestamps

invalid_timestamps = df["timestamp"].isnull().sum()

print("Invalid Timestamps:", invalid_timestamps)

# 6. Check temperature readings

print("\nTemperature Quality Check:")

print("Zero Temperature Records:",
      (df["temperature"] == 0).sum())

print("Negative Temperature Records:",
      (df["temperature"] < 0).sum())

# 7. Check humidity readings

print("\nHumidity Quality Check:")

print("Humidity Below 0:",
      (df["humidity"] < 0).sum())

print("Humidity Above 100:",
      (df["humidity"] > 100).sum())

# 8. Check vibration readings

print("\nVibration Quality Check:")

print("Vibration Below 0.1:",
      (df["vibration"] < 0.1).sum())

print("Vibration Above 3.0:",
      (df["vibration"] > 3.0).sum())

# 9. Check container IDs

print("\nUnique Containers:")

print(df["container_id"].unique())

print("\n===== DATA QUALITY CHECK COMPLETED =====")

# 10. Data Cleaning and Transformation

print("\n===== DATA CLEANING STARTED =====")

# Create a separate copy
cleaned_df = df.copy()

# Remove duplicate records if any
cleaned_df = cleaned_df.drop_duplicates()

# Remove records with invalid timestamps
cleaned_df = cleaned_df.dropna(subset=["timestamp"])

# Validate humidity range
cleaned_df = cleaned_df[
    (cleaned_df["humidity"] >= 0) &
    (cleaned_df["humidity"] <= 100)
]

# Validate vibration range
cleaned_df = cleaned_df[
    (cleaned_df["vibration"] >= 0.1) &
    (cleaned_df["vibration"] <= 3.0)
]

# Keep zero temperature readings for investigation

print("\nData cleaning completed!")

# 11. Export processed dataset

OUTPUT_PATH = "data/processed/processed_sensor_data.csv"

cleaned_df.to_csv(OUTPUT_PATH, index=False)

print("\nProcessed Dataset Exported Successfully!")

print("Output File:", OUTPUT_PATH)

print("Original Records:", len(df))

print("Processed Records:", len(cleaned_df))

print("Removed Records:", len(df) - len(cleaned_df))

print("\nFinal Dataset Shape:", cleaned_df.shape)

print("\nFinal Data Types:")
print(cleaned_df.dtypes)

print("\n===== DATA PROCESSING COMPLETED =====")