import pyodbc
import pandas as pd

# SQL Server connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=ANDY;' 
    'DATABASE=BankData;'  
    'Trusted_Connection=yes;'
)

# Defining queries
queries = {
    "clients": "SELECT * FROM clients_data",
    "portfolios": "SELECT * FROM portfolios_data",
    "transactions": "SELECT * FROM transactions_data"
}

# Extract and save to CSV
for name, query in queries.items():
    df = pd.read_sql(query, conn)
    df.to_csv(f"data/{name}_extracted.csv", index=False)
    print(f"{name} table extracted with {len(df)} rows")

conn.close()
