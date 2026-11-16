import pandas as pd
from pathlib import Path


# Locate project root
project_root = Path(__file__).resolve().parents[2]


# Load Avocado risk report
report_path = (
    project_root / "data" / "processed" /
    "avocado_spoilage_risk_report.csv"
)

df = pd.read_csv(report_path)


print("===== ATMOSYNC AVOCADO RISK REPORT VALIDATION =====")


# Test 1: Check required columns and missing identifiers
required_columns = {
    "container_id",
    "total_valid_hours",
    "temperature_exposure_hours",
    "humidity_exposure_hours",
    "temperature_risk_percent",
    "humidity_risk_percent",
    "risk_score",
    "risk_level"
}

assert required_columns.issubset(df.columns), (
    "Required columns are missing!"
)

assert df["container_id"].notna().all(), (
    "Missing container IDs found!"
)

assert df["risk_level"].notna().all(), (
    "Missing risk classifications found!"
)

print("Test 1 Passed: Required columns and container IDs are valid")


# Test 2: Check risk scores
known_risk = df["risk_level"] != "UNKNOWN"

assert df.loc[known_risk, "risk_score"].notna().all(), (
    "Missing risk scores found!"
)

assert df.loc[known_risk, "risk_score"].between(0, 100).all(), (
    "Invalid risk scores found!"
)

print("Test 2 Passed: Risk scores are within 0-100")


# Test 3: Check exposure percentages
assert df.loc[known_risk, "temperature_risk_percent"].between(
    0, 100
).all(), "Invalid temperature exposure percentages!"

assert df.loc[known_risk, "humidity_risk_percent"].between(
    0, 100
).all(), "Invalid humidity exposure percentages!"

print("Test 3 Passed: Exposure percentages are valid")


# Test 4: Check risk classifications
valid_levels = {"LOW", "MEDIUM", "HIGH", "UNKNOWN"}

assert set(df["risk_level"]).issubset(valid_levels), (
    "Invalid risk classifications found!"
)

print("Test 4 Passed: Risk classifications are valid")


# Test 5: Check unique container records
assert df["container_id"].nunique() == len(df), (
    "Duplicate container records found!"
)

print("Test 5 Passed: No duplicate container records")


# Display final result
print("\n===== VALIDATION SUMMARY =====")

print("Total Containers:", len(df))

print("\nRisk Distribution:")
print(df["risk_level"].value_counts())

print("\nAll validation tests passed successfully!")