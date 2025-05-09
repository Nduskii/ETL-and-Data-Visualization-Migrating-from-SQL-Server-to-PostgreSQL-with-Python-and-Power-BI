# %%
## importing libraries
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta


# %%
## Loading extracted data
clients = pd.read_csv("data/clients_extracted.csv")
portfolios = pd.read_csv("data/portfolios_extracted.csv")
transactions = pd.read_csv("data/transactions_extracted.csv")


# %%
## sanity check
def sanity_check(dataframe):
    # Checking for missing values
    missing_data = dataframe.isnull().sum()

    # Checking for duplicate rows
    duplicated = dataframe.duplicated().sum()

    # Identifying potential garbage values in object columns
    garbage_values = {}
    for col in dataframe.select_dtypes(include="object").columns:
        garbage_values[col] = dataframe[col].value_counts(dropna=False)

    return missing_data, duplicated, garbage_values


missing, dupes, garbage = sanity_check(transactions)

print("Missing values:\n", missing)
print("\nDuplicated rows:", dupes)
print("\nObject column value counts:")
for col, values in garbage.items():
    print(f"\n{col}:\n{values}")



# %%
#cleaning clients csv
# filling missing full names using email
clients['full_name'] = clients.apply(
    lambda row: row['email'].split('@')[0].replace('.', ' ').title() if pd.isna(row['full_name']) and pd.notna(row['email']) else row['full_name'],
    axis=1)

# cleaning risk factor cases
# Standardizing risk profile to lowercase
clients['risk_factor'] = clients['risk_factor'].str.lower().str.strip()

#Replacing varitionsto common labels
clients['risk_factor'] = clients['risk_factor'].replace({
    'hi': 'high',
    'high': 'high',
    'medium': 'medium',
    'med': 'medium',
    'low': 'low'
})

# filling missing ages
# If age is missing and risk_profile is present, impute based on typical age group
def estimate_age(risk):
    if risk == 'high':
        return 25
    elif risk == 'medium':
        return 40
    elif risk == 'low':
        return 55
    return np.nan

clients['age'] = clients.apply(
    lambda row: estimate_age(row['risk_factor']) if pd.isna(row['age']) and pd.notna(row['risk_factor']) else row['age'],
    axis=1)

# filling missing risk factors
# If risk_profile is missing and age is present, infer from age
def estimate_risk(age):
    if age < 30:
        return 'high'
    elif age < 50:
        return 'medium'
    else:
        return 'low'

clients['risk_factor'] = clients.apply(
    lambda row: estimate_risk(row['age']) if pd.isna(row['risk_factor']) and pd.notna(row['age']) else row['risk_factor'],
    axis=1)

# if both risk and age missing
# Fill any remaining missing ages with median
clients['age'].fillna(clients['age'].median(), inplace=True)

# Fill any remaining missing risks with mode
clients['risk_factor'].fillna(clients['risk_factor'].mode()[0], inplace=True)

# ensuring data types are right
clients['age'] = clients['age'].astype(int)
clients['risk_factor'] = clients['risk_factor'].str.lower()

# Saving cleaned file
clients.to_csv("cleaned_data/clients_transformed.csv", index=False)

print(" Client data cleaned and saved successfully.")


# %%
clients_transformed=pd.read_csv("cleaned_data/clients_transformed.csv", parse_dates=['join_date'])

# %%

#cleaning portfolios csv
# Converting transaction date to datetime
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'], errors='coerce')

# Getting last transaction date for each portfolio
last_txn = transactions.groupby('portfolio_id')['transaction_date'].max().reset_index()
last_txn.columns = ['portfolio_id', 'last_transaction_date']

# Merge with portfolios data
portfolios = portfolios.merge(last_txn, on='portfolio_id', how='left')


# Cleaning up existing status values before filling missing
portfolios['status'] = portfolios['status'].str.strip().str.lower()
portfolios['status'] = portfolios['status'].replace({
    'closed': 'Closed',
    'inactive': 'Inactive',
    'active': 'Active'
})

# Setting cutoff date for Active accounts
cutoff = datetime.now() - timedelta(days=90)

# Filling only missing statuses using the logic of last transactions 
portfolios['status'] = portfolios.apply(
    lambda row: row['status'] if pd.notnull(row['status']) else (
        'Active' if pd.notnull(row['last_transaction_date']) and row['last_transaction_date'] > cutoff
        else 'Inactive' if pd.notnull(row['last_transaction_date'])
        else 'Closed'),axis=1)

# Dropping the helping column
portfolios.drop(columns=['last_transaction_date'], inplace=True)

# Saving the cleaned data
portfolios.to_csv("cleaned_data/portfolios_transformed.csv", index=False)
print("Portfolios data cleaned and saved!")
# %%
transformed_portfolio=pd.read_csv("cleaned_data/portfolios_transformed.csv")


# %%
#cleaning transactions csv

# saving incomplete financial transactions(missing critical field (amount)) before deleting 
# Counting rows with missing amount
missing_amount_rows = transactions[transactions['amount'].isnull()]
print(f"Dropping {len(missing_amount_rows)} rows with missing amount")

# Saving dropped rows to a separate CSV 
missing_amount_rows.to_csv("cleaned_data/dropped_transactions.csv", index=False)

# Dropping incomplete transactions from main DataFrame
transactions = transactions[transactions['amount'].notnull()]

# Saving the cleaned file
transactions.to_csv("cleaned_data/cleaned_transactions.csv", index=False)
print("Cleaned transactions saved.")


# %%

# Cleaning 'asset_type' values
asset_type_mapping = {
    'bond': 'Bond',
    'Bond': 'Bond',
    'stock': 'Stock',
    'Stock': 'Stock',
    'STOCK': 'Stock',
    'ETF': 'ETF',
    'etf': 'ETF',
    'Crypto': 'Crypto'
}

transactions['asset_type'] = transactions['asset_type'].map(asset_type_mapping)
transactions['asset_type'] = transactions['asset_type'].fillna('Unknown')

# Regenerating transaction type column based on amount
def classify_transaction(amount):
    if amount > 0:
        return 'Buy'
    elif amount < 0:
        return 'Sell'
    else:
        return 'Unknown'

transactions['transaction_type'] = transactions['amount'].apply(classify_transaction)

# Saving the cleaned file
transactions.to_csv("cleaned_data/transactions_transformed.csv", index=False)

print(" cleaned transactions file.")

# %%

transactions_data=pd.read_csv("cleaned_data/transactions_transformed.csv")

# %%
