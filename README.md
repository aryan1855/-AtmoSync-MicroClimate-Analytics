# AtmoSync – Micro-Climate Arbitrage Analytics

An IoT-driven data analytics project developed as part of the Infotact Solutions Internship Program.

## 1. Project Overview

AtmoSync is a data analytics solution designed to monitor hyper-local environmental conditions during commodity transportation and identify potential spoilage risks.

The system simulates IoT sensor data, processes streaming information, stores it in a cloud data warehouse, transforms it into meaningful analytics, and presents actionable insights through interactive dashboards.

## 2. Problem Statement

Traditional supply chain systems often rely on general weather information and standard transit estimates. They may fail to detect sudden changes in conditions inside individual shipping containers.

Such changes can affect the quality of perishable agricultural commodities and cause financial losses.

AtmoSync aims to identify these risks early and help businesses evaluate alternative markets and rerouting opportunities.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | IoT sensor data simulation |
| Apache Kafka | Real-time data streaming |
| Snowflake | Cloud data storage |
| dbt | Data cleaning and transformation |
| Apache Superset | Analytics and dashboards |
| Git & GitHub | Version control and collaboration |

## 4. Project Architecture

Python IoT Simulator  
↓  
Apache Kafka  
↓  
Snowflake  
↓  
dbt Transformations  
↓  
Analytics Tables  
↓  
Apache Superset Dashboard

## 5. Key Project Features

- Simulated IoT sensor data generation.
- Continuous temperature, humidity and vibration monitoring.
- Streaming data ingestion.
- Cloud-based data storage.
- Data cleaning and transformation.
- Spoilage risk analysis.
- Spoilage Arbitrage calculations.
- Container health monitoring.
- Interactive analytics dashboards.

## 6. Repository Structure

- `config/` – Configuration files.
- `data/` – Raw and processed data.
- `dbt/` – Data transformation project.
- `docs/` – Project documentation and reports.
- `kafka/` – Kafka producers and consumers.
- `snowflake/` – Snowflake SQL scripts.
- `src/` – Python source code.
- `superset/` – Dashboard-related files.
- `tests/` – Testing and validation.

## 7. Project Duration

5 November 2026 – 4 December 2026

## 8. Team Information

Organization: Infotact Solutions  
Project: AtmoSync – Micro-Climate Arbitrage Analytics  
Domain: Data Analytics

Team Leader: Aryan Kumar

Team Members: ?

## 9. Project Status

Initial repository setup and project structure creation are in progress.

## 10. Disclaimer

This project uses simulated IoT sensor data for academic and internship development purposes. It is intended to demonstrate a data streaming and analytics workflow.