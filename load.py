import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection 
user = "postgres"
password = "andy"
host = "localhost"
port = "5432"
database = "etl_project"

# Building the connection string
connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

# File paths
raw_paths = {
    "clients": r"C:\Users\Other\Downloads\ssms_postgres\data\clients_extracted.csv",
    "portfolios": r"C:\Users\Other\Downloads\ssms_postgres\data\portfolios_extracted.csv",
    "transactions": r"C:\Users\Other\Downloads\ssms_postgres\data\transactions_extracted.csv"
}

cleaned_paths = {
    "clients": r"C:\Users\Other\Downloads\ssms_postgres\cleaned_data\clients_transformed.csv",
    "portfolios": r"C:\Users\Other\Downloads\ssms_postgres\cleaned_data\portfolios_transformed.csv",
    "transactions": r"C:\Users\Other\Downloads\ssms_postgres\cleaned_data\transactions_transformed.csv"
}

# Loading CSVs into Postgres
def load_csv_to_postgres(csv_path, table_name, schema):
    df = pd.read_csv(csv_path)
    df.to_sql(name=table_name, con=engine, schema=schema, if_exists='replace', index=False)
    print(f"Loaded {schema}.{table_name} successfully")

# Loading raw files into 'raw' schema
for table, path in raw_paths.items():
    load_csv_to_postgres(path, table_name=table, schema="raw")

# Loading cleaned files into 'cleaned' schema
for table, path in cleaned_paths.items():
    load_csv_to_postgres(path, table_name=table, schema="cleaned")
