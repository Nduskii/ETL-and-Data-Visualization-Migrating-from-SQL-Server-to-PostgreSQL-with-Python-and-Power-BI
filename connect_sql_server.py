import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;' 
        'DATABASE=BankData;' 
        'Trusted_Connection=yes;'
    )
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)
