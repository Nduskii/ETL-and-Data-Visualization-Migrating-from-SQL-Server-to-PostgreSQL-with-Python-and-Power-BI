# ETL and Data Visualization: Migrating from SQL Server to PostgreSQL with Python and Power BI

##  Project Summary
This project showcases an end-to-end data pipeline and visualization workflow. It involves extracting legacy data from a SQL Server database, transforming and cleaning the data using Python, loading the cleaned data into PostgreSQL, and creating a one-page interactive Power BI dashboard. The data simulates a financial domain, including clients, portfolios, and transactions.

---

## Tools & Technologies Used
- **SQL Server** – Source (legacy) database
- **Python (pandas, psycopg2)** – Data extraction, transformation, and loading
- **PostgreSQL** – Target database for cleaned data
- **Power BI** – Data analysis and dashboard creation
- **pgAdmin** – PostgreSQL management and querying

---

##  ETL Process

### 1. Extract
Raw CSV files exported from SQL Server (`clients_extracted.csv`, `portfolios_extracted.csv`, and `transactions_extracted.csv`) are used as the data source.

### 2. Transform
Using Python and pandas, the following transformation steps were performed:
- Data cleaning (handling missing values, fixing types, filtering rows)
- Enriching the dataset (adding `client_id` to transactions using the portfolios table)
- Generating synthetic transactions for clients without portfolios to improve realism

### 3. Load
Cleaned data was loaded into corresponding PostgreSQL schemas:
- `raw`: Original extracted data
- `cleaned`: Transformed data (`clients_transformed.csv`, etc.)

---

##  Power BI Dashboard

A one-page Power BI report was built using data from the cleaned PostgreSQL tables. Key insights included:

- **KPIs:** Total clients, portfolios, transactions
- **Donut chart:** Clients by age group
- **Bar chart:** Transactions by asset and transaction type
- **Line chart:** Monthly transaction volume
- **Card visual:** Total Assets Under Management (AUM)
- **Analysis:** Clients without portfolios, multiple portfolios, portfolio types, and average initial investments

---
## Highlights
- End-to-end ETL pipeline simulation with realistic financial data
- Complex relationships modeled (e.g., clients without portfolios, multiple portfolios)
- Hands-on SQL analysis and transformation logic
- Power BI dashboard showcasing insights using PostgreSQL as the source

