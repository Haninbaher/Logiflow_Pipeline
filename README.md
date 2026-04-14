# 🚚 FlowTrack: Supply Chain Monitoring Pipeline

## 📌 Project Overview

FlowTrack is an end-to-end data pipeline designed to monitor and analyze supply chain operations using both batch and real-time data processing.

The system integrates static reference data (such as warehouses, routes, and carriers) with real-time shipment event streams to generate actionable insights about shipment performance, delivery delays, and operational efficiency.

This project simulates a real-world data platform used in logistics and supply chain companies.

---

## 🎯 Why This Project Matters

Supply chain systems rely heavily on real-time visibility and data-driven decisions. Delays, inefficiencies, or bottlenecks can significantly impact business performance.

This project demonstrates how modern data engineering tools can be combined to:

* Track shipments in real time
* Detect delivery delays early
* Analyze route and warehouse performance
* Build scalable data pipelines
* Combine batch and streaming processing in one system

💡 This makes the project highly relevant for real-world use cases in:

* Logistics companies
* E-commerce platforms
* Delivery services
* Operations analytics teams

---

## 🧠 Project Goals

The main objectives of this project are:

* Build a complete **data pipeline architecture**
* Integrate **batch + streaming data**
* Apply **data transformations using Spark and dbt**
* Orchestrate workflows using Airflow
* Store and query data efficiently using Hive
* Deliver insights through dashboards

---

## 🏗️ Architecture Overview

The pipeline consists of two main flows:

### 1. Static Data Pipeline (Batch)

CSV Files → PostgreSQL → Spark Batch → Hive

### 2. Real-Time Data Pipeline (Streaming)

Python Generator → Kafka → Spark Structured Streaming → Hive

### 3. Modeling Layer

Hive → dbt → Analytics Tables

### 4. Orchestration Layer

Airflow → Workflow Scheduling & Automation

### 5. Visualization Layer

Power BI / Superset → Dashboards & KPIs

---

## 🧰 Technology Stack & Roles

| Tool                           | Role in the Project                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------ |
| **PostgreSQL**                 | Stores static reference data such as warehouses, routes, carriers, and products      |
| **Python**                     | Generates simulated real-time shipment events                                        |
| **Kafka**                      | Handles real-time data streaming (shipment events pipeline)                          |
| **Spark Batch**                | Loads and transforms static data from PostgreSQL into Hive                           |
| **Spark Structured Streaming** | Processes real-time shipment events from Kafka                                       |
| **HDFS / Hive**                | Stores raw and processed data tables for querying and analytics                      |
| **dbt**                        | Transforms raw data into structured analytical models (staging, intermediate, marts) |
| **Airflow**                    | Orchestrates and schedules pipeline workflows                                        |
| **Power BI / Superset**        | Visualizes insights and KPIs                                                         |
| **Docker Compose**             | Runs the full data stack in a reproducible environment                               |

---

## 🟤 Phase 1: Raw Data Ingestion (PostgreSQL)

### 📌 Objective

Load the raw supply chain dataset into PostgreSQL without any transformation, preserving the original structure for downstream processing.



### 🧱 What We Did

* Downloaded the **DataCo Supply Chain dataset** 
* Loaded the dataset into PostgreSQL as a **raw table**
* Stored the data exactly as-is (no cleaning or transformation)



### 🧰 Tools Used

* **Python (pandas)** → for reading the CSV file and loading data
* **SQLAlchemy + psycopg2** → for connecting to PostgreSQL
* **PostgreSQL (Docker)** → for storing raw data



### ⚙️ Implementation

We used a Python script to load the dataset into PostgreSQL:

```python
import pandas as pd
from sqlalchemy import create_engine

# Path to dataset
csv_path = r"C:\Users\Hanin Baher\Downloads\DataCoSupplyChainDataset (1).csv"

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://external:external@localhost:5432/external"
)

# Read CSV
df = pd.read_csv(csv_path, encoding="latin1")

# Load into PostgreSQL
df.to_sql("raw_supply_chain", engine, if_exists="replace", index=False)

print("Loaded successfully")
print(df.shape)
```



### 📊 Output

* Table created in PostgreSQL:

  ```
  raw_supply_chain
  ```

* Dataset size:

  ```
  ~180,000 rows
  ~53 columns
  ```

---

## Phase 5: Spark Integration

- Connected Spark to PostgreSQL using JDBC
- Successfully loaded raw dataset into Spark DataFrame
- Previewed data using df.show()

This confirms that Spark can access and process the raw data.

Next step: Transform and split the dataset into structured tables
