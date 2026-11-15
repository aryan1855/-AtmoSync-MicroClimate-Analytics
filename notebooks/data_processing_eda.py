# AtmoSync - Exploratory Data Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("\n===== ATMOSYNC DATA ANALYSIS =====")

# 1. Load processed dataset
DATA_PATH = "data/processed/processed_sensor_data.csv"

df = pd.read_csv(DATA_PATH)

# 2. Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

print("\nDataset Loaded Successfully!")
print("Total Records:", len(df))

# 3. Statistical Summary
print("\n===== STATISTICAL SUMMARY =====")
print(df.describe())

# 4. Container Count
print("\n===== CONTAINER DISTRIBUTION =====")
print(df["container_id"].value_counts())

# 5. Container-wise Average
print("\n===== CONTAINER-WISE AVERAGES =====")

container_analysis = df.groupby("container_id")[
    ["temperature", "humidity", "vibration"]
].mean()

print(container_analysis)

print("\n===== INITIAL EDA COMPLETED =====")

# 6. Temperature Distribution

plt.figure(figsize=(10, 5))

plt.hist(df["temperature"], bins=30)

plt.title("Temperature Distribution")
plt.xlabel("Temperature (°C)")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()


# 7. Humidity Distribution

plt.figure(figsize=(10, 5))

plt.hist(df["humidity"], bins=30)

plt.title("Humidity Distribution")
plt.xlabel("Humidity (%)")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()


# 8. Container-wise Average Temperature

plt.figure(figsize=(8, 5))

container_analysis["temperature"].plot(kind="bar")

plt.title("Average Temperature by Container")
plt.xlabel("Container ID")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


# 9. Container-wise Average Humidity

plt.figure(figsize=(8, 5))

container_analysis["humidity"].plot(kind="bar")

plt.title("Average Humidity by Container")
plt.xlabel("Container ID")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

print("\n===== DATA VISUALIZATION COMPLETED =====")

# 10. Time-Series Analysis

print("\n===== TIME-SERIES ANALYSIS =====")

# Set timestamp as index
time_df = df.set_index("timestamp")

# Calculate hourly average temperature
hourly_temperature = time_df.groupby("container_id")[
    "temperature"
].resample("1h").mean().reset_index()

print("\nHourly Temperature Preview:")
print(hourly_temperature.head(10))

# Plot hourly temperature trends
plt.figure(figsize=(14, 6))

for container in hourly_temperature["container_id"].unique():

    container_data = hourly_temperature[
        hourly_temperature["container_id"] == container
    ]

    plt.plot(
        container_data["timestamp"],
        container_data["temperature"],
        label=container
    )

plt.title("Hourly Temperature Trends by Container")
plt.xlabel("Timestamp")
plt.ylabel("Average Temperature (°C)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n===== TIME-SERIES ANALYSIS COMPLETED =====")

# 11. Correlation Analysis

print("\n===== CORRELATION ANALYSIS =====")

# Select numerical columns
correlation_data = df[
    ["temperature", "humidity", "vibration"]
]

# Calculate correlation
correlation_matrix = correlation_data.corr()

print("\nCorrelation Matrix:")
print(correlation_matrix)

# Visualize correlation
plt.figure(figsize=(8, 6))

plt.imshow(correlation_matrix, cmap="coolwarm", vmin=-1, vmax=1)

plt.colorbar(label="Correlation")

plt.xticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns
)

plt.yticks(
    range(len(correlation_matrix.columns)),
    correlation_matrix.columns
)

plt.title("Environmental Sensor Correlation")

# Display correlation values
for i in range(len(correlation_matrix.columns)):
    for j in range(len(correlation_matrix.columns)):
        plt.text(
            j,
            i,
            f"{correlation_matrix.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.tight_layout()
plt.show()

print("\n===== CORRELATION ANALYSIS COMPLETED =====")