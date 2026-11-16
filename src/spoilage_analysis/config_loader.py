import json
from pathlib import Path


# Locate project root directory
project_root = Path(__file__).resolve().parents[2]

# Locate commodity configuration file
config_path = project_root / "config" / "commodity_thresholds.json"


# Load JSON configuration
with open(config_path, "r") as file:
    commodity_config = json.load(file)


# Display commodity information
print("===== ATMOSYNC COMMODITY CONFIGURATION =====")

print("Commodity:", commodity_config["commodity"])
print("Maturity Stage:", commodity_config["maturity_stage"])

print("\n===== STORAGE CONDITIONS =====")

conditions = commodity_config["storage_conditions"]

print(
    "Temperature:",
    conditions["temperature_celsius"]["minimum"],
    "-",
    conditions["temperature_celsius"]["maximum"],
    "°C"
)

print(
    "Humidity:",
    conditions["humidity_percentage"]["minimum"],
    "-",
    conditions["humidity_percentage"]["maximum"],
    "%"
)

print(
    "Storage Duration:",
    conditions["reference_storage_duration_days"]["minimum"],
    "-",
    conditions["reference_storage_duration_days"]["maximum"],
    "days"
)

print("\nConfiguration loaded successfully!")