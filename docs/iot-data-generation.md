# AtmoSync – IoT Data Generation Module

## 1. Module Overview

The IoT Data Generation module is responsible for preparing environmental sensor data for the AtmoSync Micro-Climate Arbitrage Analytics project.

This module uses an existing Kaggle IoT telemetry dataset and transforms its environmental readings into the common data structure required by the AtmoSync project.

The generated dataset serves as the input for the Data Processing module.

## 2. Module Objective

The main objectives are:

- Load the Kaggle IoT telemetry dataset.
- Explore and understand the available sensor readings.
- Map existing device IDs to simulated container IDs.
- Convert timestamps into a readable datetime format.
- Map temperature and humidity readings.
- Generate synthetic vibration readings for prototype testing.
- Prepare the required five-column dataset.
- Validate and export the generated sensor data.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Pandas | Dataset loading and manipulation |
| NumPy | Synthetic vibration generation |
| VS Code | Development environment |
| Git & GitHub | Version control |

## 4. Dataset Source

The initial dataset is obtained from Kaggle.

**Input file:**

`data/raw/iot_telemetry_data.csv`

The original dataset contains 405,184 records and the following columns:

- ts
- device
- co
- humidity
- light
- lpg
- motion
- smoke
- temp

The dataset contains environmental telemetry readings collected from three IoT devices.

This dataset is used for initial development and testing. It does not represent actual shipping-container sensor data.

## 5. Data Generation Process

The generator performs the following operations:

1. Loads the original Kaggle dataset using Pandas.
2. Converts the Unix timestamp into a datetime format.
3. Maps existing device IDs to simulated container IDs.
4. Copies the original temperature readings into the `temperature` column.
5. Uses the original humidity readings.
6. Generates synthetic vibration readings using NumPy.
7. Selects the five required project columns.
8. Validates the generated dataset.
9. Exports the final dataset as a CSV file.

## 6. Container ID Mapping

The original dataset contains three unique IoT device IDs.

For prototype development, these device IDs are mapped to simulated container IDs:

| Device | Simulated Container ID |
|---|---|
| First unique device | C001 |
| Second unique device | C002 |
| Third unique device | C003 |

These IDs are simulated identifiers and do not represent actual shipping containers.

## 7. Vibration Simulation

The original Kaggle dataset does not contain vibration readings.

Therefore, synthetic vibration values are generated using NumPy.

The simulation uses:

- Minimum value: 0.1
- Maximum value: 3.0
- Random seed: 42
- Decimal precision: 2

These values are generated for prototype testing and must not be treated as actual sensor measurements.

## 8. Final Dataset Schema

The generated dataset follows the common AtmoSync project schema.

| Column | Data Type | Description |
|---|---|---|
| container_id | String | Simulated container identifier |
| timestamp | Datetime | Sensor reading timestamp |
| temperature | Float | Temperature reading in Celsius |
| humidity | Float | Humidity reading in percentage |
| vibration | Float | Synthetic vibration reading |

## 9. Data Validation Results

The generated dataset was checked for basic data quality.

| Validation | Result |
|---|---:|
| Total records | 405,184 |
| Total columns | 5 |
| Unique containers | 3 |
| Missing values | 0 |
| Duplicate rows | 0 |
| Minimum temperature | 0.0°C |
| Maximum temperature | 30.6°C |
| Minimum humidity | 1.1% |
| Maximum humidity | 99.9% |
| Minimum vibration | 0.1 |
| Maximum vibration | 3.0 |

Unusual readings, including zero-temperature values, are retained for further investigation during the Data Processing stage.

## 10. Output File

The generated dataset is exported to:

`data/raw/raw_sensor_data.csv`

The output contains 405,184 records and five columns.

This file is the input dataset for the Data Processing module.

## 11. How to Run the Generator

### Step 1: Clone the repository

```bash
git clone https://github.com/aryan1855/-AtmoSync-MicroClimate-Analytics.git
```

### Step 2: Navigate to the project directory

```bash
cd -AtmoSync-MicroClimate-Analytics
```

### Step 3: Create a Python virtual environment

```bash
py -3.12 -m venv .venv
```

### Step 4: Activate the environment

For Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Place the input dataset

Ensure the Kaggle dataset is available at:

`data/raw/iot_telemetry_data.csv`

### Step 7: Run the generator

```bash
python src/iot_simulator/data_generator.py
```

After successful execution, the generated file will be available at:

`data/raw/raw_sensor_data.csv`

## 12. Limitations and Assumptions

- The initial dataset is sourced from Kaggle and is used for prototype development.
- Device-to-container mapping is simulated.
- Vibration readings are synthetically generated.
- The generated data does not represent actual shipping-container sensor measurements.
- Temperature readings of 0°C are retained for further investigation.
- Actual sensor data provided later by Infotact Solutions can be used for subsequent testing and integration.

## 13. Handover to Data Processing Module

The generated `raw_sensor_data.csv` file will be handed over to the Data Processing module.

The next module is responsible for:

- Dataset inspection.
- Missing value and duplicate checks.
- Data validation.
- Data cleaning and transformation.
- Exploratory Data Analysis.
- Exporting the final dataset as `processed_sensor_data.csv`.

The agreed five-column schema should be maintained to support the subsequent SQLite database integration.