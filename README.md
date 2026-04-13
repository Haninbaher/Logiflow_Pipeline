## 🚀 Data Ingestion Phase (Phase 1)

In this phase, I successfully migrated the **DataCo Smart Supply Chain** dataset into my local Big Data Cluster.

### 🛠 Prerequisites
- Docker & Docker Compose.
- Python 3.x installed on the host machine.
- Pandas & SQLAlchemy libraries.

### 📥 Step 1: Data Preparation
The raw dataset was originally in CSV format. To handle encoding issues and unquoted newlines in the source data:
1. Opened the `DataCoSupplyChainDataset.csv` in Excel.
2. Saved the file as an **Excel Workbook (.xlsx)** named `DataCoSupplyChainDataset.xlsx`.
   *This step ensures all special characters and nested commas are properly escaped.*

### 🐍 Step 2: Automated Loading via Python
Instead of traditional SQL `COPY` commands (which are sensitive to formatting), we used a Python script for a more robust ingestion process.

**Run the following Python script on your host machine:**

```python
import pandas as pd
from sqlalchemy import create_engine

# 1. Load the cleaned Excel file
path = r"C:\Users\YourUser\Downloads\DataCoSupplyChainDataset.xlsx"
df = pd.read_excel(path)

# 2. Clean column names for SQL compatibility
# Removing spaces, dots, and dashes
df.columns = [c.replace(' ', '_').replace('.', '').replace('-', '_') for c in df.columns]

# 3. Establish connection to the Dockerized PostgreSQL
# Connection String: postgresql://[user]:[password]@[host]:[port]/[db_name]
engine = create_engine('postgresql://external:external@localhost:5432/external')

# 4. Upload to Postgres
print("Uploading data to 'supply_chain_data' table...")
df.to_sql('supply_chain_data', engine, if_exists='replace', index=False)
print("Ingestion Completed Successfully!")
