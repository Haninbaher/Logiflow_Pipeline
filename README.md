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
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql+psycopg2://flowtrack:flowtrack@localhost:5432/flowtrack"
)

df = pd.read_csv(
    r"C:\Users\Hanin Baher\Downloads\DataCoSupplyChainDataset (1).csv",
    encoding="latin1"
)

df.to_sql("raw_supply_chain", engine, if_exists="replace", index=False)

print("DONE", df.shape)
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

## 🧠 Phase 2: Spark JDBC Connection

- Connected Spark to PostgreSQL using JDBC driver
- Downloaded PostgreSQL driver manually
- Loaded raw data into Spark DataFrame

This enables distributed processing on relational data.

  ```python
# Download the PostgreSQL JDBC driver to enable communication between Spark and the database
wget https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

# Launch the PySpark shell and include the downloaded JAR file in the classpath
/opt/spark/bin/pyspark --jars postgresql-42.7.3.jar

# Configure the JDBC connection settings and load the database table into a Spark DataFrame
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://postgres:5432/flowtrack") \
  .option("dbtable", "raw_supply_chain") \
  .option("user", "flowtrack") \
  .option("password", "flowtrack") \
  .option("driver", "org.postgresql.Driver") \
  .load()

# Display the first 5 rows of the DataFrame to verify the data was loaded correctly
df.show(5)

  ```

## 🏗️ Phase 3: Data Transformation (Apache Spark)

In this phase, the raw supply chain data is processed using **Apache Spark** to convert it into a structured **Star Schema** optimized for analytical queries and data warehousing.

### 🎯 Key Objectives

* **Data Modeling**: Transformed the flat raw dataset into a relational structure consisting of:
    * **Customers Dimension**: Contains unique customer profiles and attributes.
    * **Products Dimension**: Handles product categorization and details.
    * **Orders Fact Table**: The central table containing transactional metrics and foreign keys.
* **Data Cleaning**: Applied **deduplication** logic to ensure data integrity and handled missing or null values.
* **Feature Engineering**: Selected relevant columns and optimized data types to ensure efficient storage and faster query performance.

### 🛠️ Implementation Details

The transformation process involves reading the raw JDBC source and mapping it to the new schema:

```python
# Logic Summary:
# 1. Remove duplicates from the raw source
# 2. Select and cast specific columns for the Fact and Dimension tables
# 3. Save the structured data for downstream analytics

# Example: Creating the Fact Table
orders_fact = df.select(
    "order_id", 
    "customer_id", 
    "product_id", 
    "order_date", 
    "sales_amount"
).dropDuplicates()
```

---

## 🏛️ Phase 4: Hive Warehouse Layer

In this phase, the transformed data is persisted into the **Hive Metastore**. This establishes the "Single Source of Truth" within the data warehouse layer, allowing for persistent storage and SQL-based analytics.

### ✅ Verification & Initial Load
After processing the raw data, the first table (`customers`) was successfully written to Hive. Despite common environment warnings regarding schema versions, the data integrity was verified using Spark SQL.

```python
# Verifying table existence in Hive
spark.sql("SHOW TABLES").show()

# Verifying data content
spark.sql("SELECT * FROM customers LIMIT 5").show()
```
---

## 💎 Phase 5: Analytics Engineering (dbt Modeling)

In this phase, we transitioned from data storage to data transformation using **dbt (data build tool)**. This layer injects business logic into our raw warehouse tables, creating refined, analytics-ready models optimized for BI tools and strategic reporting.

### 🚀 Implementation & Model Overview
We successfully developed and executed **three core dbt models** designed to monitor logistics performance and supply chain efficiency:

1.  **`order_delivery_monitoring`**: Built on top of the `fct_orders` table, this model prepares core shipment fields including delivery status, delay days, and late risk flags.
2.  **`region_delay_summary`**: Aggregates delay metrics by geographic area to pinpoint regional bottlenecks.
3.  **`shipping_mode_performance`**: Evaluates the efficiency of different carriers and shipping methods.

### 📊 Key Monitoring Metrics
The models transform raw transactional data into actionable insights by tracking:
* **Delivery Performance:** Monitors `delivery status` and flags `late delivery risk`.
* **Time Analysis:** Calculates `actual` vs. `scheduled` shipping days to compute `delay days`.
* **Logistics Context:** Organizes data by `shipping mode`, `order region`, and `order country`.

### 💡 Business Value (The "Why")
This analytics layer is specifically designed to answer critical business questions:
* **Real-time Tracking:** Which specific orders are currently delayed?
* **Geographic Insights:** Which regions suffer from the highest delay rates?
* **Operational Efficiency:** Which shipping modes are consistently underperforming or overperforming?

### 🛠️ dbt Technical Stack
* **Layer:** Analytics Modeling (Gold/Data Mart Layer).
* **Source:** Built on structured `fct_orders` and dimension tables in the warehouse.
* **Outcome:** Materialized views that serve as the "Single Source of Truth" for Power BI, Tableau, or Metabase.

> **Status:** ✅ All models successfully compiled and ran. This marks the establishment of the **Analytics Modeling Layer**, enabling data-driven decision-making for the logistics department.

---

## ⚙️ Phase 6: Batch Orchestration (Apache Airflow)

To ensure the pipeline is reliable and production-ready, I implemented **Apache Airflow** to orchestrate the end-to-end workflow. The DAG, named `flowtrack_batch_pipeline`, serves as the control plane for the entire data movement.

### 🤖 Automation Workflow
The DAG automates the complex dependencies between our processing layers:
* **Spark Orchestration:** Automatically triggers the Spark batch jobs to transform raw data from the JDBC source into structured Hive warehouse tables (Raw → Clean).
* **dbt Orchestration:** Upon successful completion of Spark jobs, Airflow triggers the dbt transformation layer to refresh the analytics models (`order_delivery_monitoring`, etc.).

### 🌟 Key Benefits
* **Elimination of Manual Intervention:** Replaces manual script execution with a scheduled, hands-off workflow.
* **Dependency Management:** Ensures that the dbt models only run if the Spark data load succeeds, preventing data quality issues.
* **Reproducibility:** Provides a clear audit trail and the ability to re-run specific tasks or the entire pipeline in case of failure.
* **Monitoring & Alerting:** Leverages Airflow’s UI to monitor the health of the pipeline and track execution times.

### 🛠️ Technical Setup
* **DAG ID:** `flowtrack_batch_pipeline`
* **Operators Used:** `SparkSubmitOperator`, `BashOperator` (for dbt), and `DummyOperator` for flow control.
* **Schedule:** Configured for automated batch intervals to keep the warehouse updated.

> **Status:** ✅ Fully Operational. The pipeline is now a self-healing, automated system that moves data from source to insights without human oversight.


## ⚡ Phase 8: Real-Time Streaming Pipeline (Kafka & Spark)

To evolve the project from historical analysis to proactive monitoring, I implemented a real-time streaming layer. This phase introduces an **Event-Driven Architecture** to handle shipment lifecycle updates as they happen.

### 🏗️ Real-Time Architecture
The data flows through a modern streaming stack:
**Python Producer** ➡️ **Apache Kafka** ➡️ **Spark Structured Streaming** ➡️ **Real-Time Output**

---

### 🛠️ Technical Workflow

#### 1. Event Simulation (The Producer)
A custom Python script (`shipment_event_producer.py`) simulates the lifecycle of an order. It maps historical data into a stream of JSON events, including:
* `order_created` | `packed` | `shipped` | `in_transit` | `delivered`
* **Intelligent Tagging:** Automatically generates a `delayed` event if the `late_delivery_risk` flag is detected.

#### 2. Message Broker (Kafka)
**Apache Kafka** acts as the resilient buffer between the producer and the consumer.
* **Topic:** `shipment_events`
* Ensures high throughput and decoupling of data generation from data processing.

#### 3. Spark Structured Streaming (The Consumer)
A dedicated Spark streaming job (`consume_shipment_events.py`) consumes the Kafka topic in real-time.
* **Schema Enforcement:** Parses incoming JSON strings into a structured DataFrame.
* **Processing:** Transforms raw event logs into actionable columns for monitoring.
* **Sink:** Currently configured to output to the console for live validation, with architecture ready for database persistence.

#### 4. Streaming Output (Validation Layer)
The processed stream is currently written to the **Console** as a dedicated sink. This serves as a vital validation layer to confirm:
* **Production Integrity:** Events are successfully serialized and produced by Python.
* **Broker Reliability:** Kafka is receiving and persisting data without loss.
* **Processing Accuracy:** Spark is correctly parsing and transforming events in real time with minimal latency.

---

### ✅ Success Metrics & Validation
The pipeline is verified as "Production-Ready" once:
1. The Producer successfully broadcasts event batches.
2. Kafka maintains the message queue with zero data loss.
3. Spark processes and displays the streaming data with minimal latency.

---
