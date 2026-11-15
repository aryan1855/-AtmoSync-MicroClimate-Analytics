# AtmoSync – Data Processing & EDA Report

## 1. Overview

This document describes the data cleaning, validation, exploratory data analysis (EDA), and visualization performed for the AtmoSync – Micro-Climate Arbitrage Analytics project.

The objective is to inspect environmental sensor data, identify potential data quality issues, transform the dataset into a consistent format, and understand temperature, humidity, and vibration patterns across simulated containers.

## 2. Dataset Information

The initial dataset was obtained from a Kaggle IoT telemetry dataset and transformed into the AtmoSync project format.

**Dataset Details:**

- Total Records: 405,184
- Total Columns: 5
- Number of Containers: 3
- Data Period: 12 July 2020 – 20 July 2020

**Final Dataset Columns:**

| Column | Description |
|---|---|
| container_id | Simulated container identifier |
| timestamp | Date and time of sensor reading |
| temperature | Temperature reading in °C |
| humidity | Humidity reading in percentage |
| vibration | Simulated vibration reading |

**Important Dataset Note:**

The original Kaggle dataset contains IoT device identifiers, temperature, humidity, and other environmental measurements.

The original device identifiers were mapped to simulated container IDs (C001, C002, C003) for project development.

Vibration values were synthetically generated for demonstration purposes. They are not actual vibration sensor measurements.

## 3. Data Cleaning and Validation

The dataset was inspected using Python and Pandas.

### Initial Data Inspection

| Check | Result |
|---|---:|
| Total Records | 405,184 |
| Missing Values | 0 |
| Duplicate Records | 0 |
| Invalid Timestamps | 0 |

### Data Quality Checks

| Validation | Result |
|---|---:|
| Zero Temperature Records | 7 |
| Negative Temperature Records | 0 |
| Humidity Below 0% | 0 |
| Humidity Above 100% | 0 |
| Vibration Below 0.1 | 0 |
| Vibration Above 3.0 | 0 |

The seven zero-temperature readings were identified during validation and retained for further investigation rather than automatically removed.

### Data Cleaning Results

- Timestamp values were converted into datetime format.
- Missing values were checked.
- Duplicate records were checked.
- Temperature, humidity, and vibration ranges were validated.
- The dataset was exported into a processed CSV file.

**Output File:** `data/processed/processed_sensor_data.csv`

| Metric | Result |
|---|---:|
| Original Records | 405,184 |
| Processed Records | 405,184 |
| Removed Records | 0 |
| Final Dataset Shape | (405184, 5) |

## 4. Exploratory Data Analysis (EDA)

EDA was performed using Pandas, NumPy, and Matplotlib.

### 4.1 Statistical Analysis

The dataset was analyzed using descriptive statistics, including:

- Mean
- Standard deviation
- Minimum value
- Maximum value
- 25th percentile
- Median
- 75th percentile

### 4.2 Container Distribution

| Container ID | Number of Records |
|---|---:|
| C001 | 187,451 |
| C002 | 111,815 |
| C003 | 105,918 |

The dataset contains three simulated containers with different numbers of sensor readings.

### 4.3 Container-wise Average Analysis

| Container ID | Average Temperature (°C) | Average Humidity (%) | Average Vibration |
|---|---:|---:|---:|
| C001 | 22.28 | 50.81 | 1.55 |
| C002 | 19.36 | 75.44 | 1.55 |
| C003 | 26.03 | 61.91 | 1.55 |

**Observations:**

- C003 has the highest average temperature.
- C002 has the highest average humidity.
- C001 has the lowest average humidity.
- Average vibration readings are approximately similar across all three containers.

## 5. Data Visualization

The following visualizations were generated using Matplotlib:

1. Temperature Distribution
2. Humidity Distribution
3. Average Temperature by Container
4. Average Humidity by Container
5. Hourly Temperature Trends by Container
6. Environmental Sensor Correlation Heatmap

These visualizations help understand the distribution of environmental readings and differences between simulated containers.

## 6. Time-Series Analysis

Hourly temperature averages were calculated for each simulated container.

The analysis helps identify temperature fluctuations over time and compare environmental patterns across containers.

The hourly aggregation was performed using the timestamp column and container identifiers.

## 7. Correlation Analysis

A correlation matrix was generated to understand linear relationships between environmental variables.

| Variables | Correlation |
|---|---:|
| Temperature & Humidity | -0.410427 |
| Temperature & Vibration | -0.000097 |
| Humidity & Vibration | -0.001234 |

**Observations:**

- Temperature and humidity show a moderate negative correlation.
- Temperature and vibration show almost no linear correlation.
- Humidity and vibration show almost no linear correlation.

Since vibration values were randomly generated, their near-zero correlations with the other variables are expected.

Correlation does not establish causation.

## 8. Technologies and Libraries Used

| Technology | Purpose |
|---|---|
| Python | Programming |
| Pandas | Data loading, cleaning, and analysis |
| NumPy | Numerical operations and synthetic data generation |
| Matplotlib | Data visualization |
| VS Code | Development environment |
| Git & GitHub | Version control |

## 9. Project Limitations

- The initial dataset is based on general IoT telemetry, not actual shipping-container sensor records.
- Container IDs are simulated mappings of original device IDs.
- Vibration readings are synthetically generated.
- The seven zero-temperature readings require further investigation.
- The current analysis is based on sample data and may need to be repeated when actual sensor data is provided by Infotact.

## 10. Conclusion

The initial data processing and exploratory analysis of the AtmoSync dataset have been completed successfully.

The dataset was inspected, validated, cleaned, and exported without removing any records. Statistical analysis, container-wise comparisons, time-series analysis, and correlation analysis were also performed.

The processed dataset is now available for subsequent analytical stages of the AtmoSync project.

**Output Dataset:** `data/processed/processed_sensor_data.csv`

**Module Status:** Initial Data Processing and EDA Completed.