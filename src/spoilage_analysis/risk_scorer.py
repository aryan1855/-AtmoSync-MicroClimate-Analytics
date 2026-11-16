import pandas as pd
from pathlib import Path


# Locate project root
project_root = Path(__file__).resolve().parents[2]


# Load Avocado exposure data
data_path = (
    project_root / "data" / "processed" /
    "avocado_exposure_analysis.csv"
)

df = pd.read_csv(data_path)


# Calculate total valid monitoring hours
df["valid_interval_hours"] = (
    df["time_gap_seconds"].where(df["valid_interval"], 0) / 3600
)


# Container-wise aggregation
summary = df.groupby("container_id").agg(

    total_valid_hours=("valid_interval_hours", "sum"),

    temperature_exposure_hours=(
        "temperature_exposure_hours", "sum"
    ),

    humidity_exposure_hours=(
        "humidity_exposure_hours", "sum"
    )

)


# Calculate exposure percentages safely
summary["temperature_risk_percent"] = (
    summary["temperature_exposure_hours"]
    .div(summary["total_valid_hours"].replace(0, float("nan")))
    * 100
)

summary["humidity_risk_percent"] = (
    summary["humidity_exposure_hours"]
    .div(summary["total_valid_hours"].replace(0, float("nan")))
    * 100
)


# Calculate combined prototype risk score
summary["risk_score"] = (
    summary["temperature_risk_percent"]
    + summary["humidity_risk_percent"]
) / 2


# Classify risk
def classify_risk(score):

    if pd.isna(score):
        return "UNKNOWN"

    elif score <= 20:
        return "LOW"

    elif score <= 50:
        return "MEDIUM"

    else:
        return "HIGH"


summary["risk_level"] = summary["risk_score"].apply(
    classify_risk
)


# Round numerical values
summary = summary.round(2)


# Display results
print("===== ATMOSYNC AVOCADO SPOILAGE RISK ANALYSIS =====")

print(summary.to_string())


# Export Avocado risk report
output_path = (
    project_root / "data" / "processed" /
    "avocado_spoilage_risk_report.csv"
)

summary.to_csv(output_path)


print("\nAvocado risk analysis completed successfully!")
print("Report saved at:", output_path)