import pandas as pd
import numpy as np

# Read data
df = pd.read_csv('CC GENERAL.csv')

# Drop CUST_ID
df_features = df.drop('CUST_ID', axis=1)

# Fill missing values with median
df_filled = df_features.fillna(df_features.median())

# Log transformation
X_log = np.log1p(df_filled)

# Get statistics for a few key variables
print("Statistics after log transformation (before standardization):")
print("\nBALANCE:")
print(X_log['BALANCE'].describe()[['mean', 'std', 'min', 'max', '50%']])
print("\nPURCHASES:")
print(X_log['PURCHASES'].describe()[['mean', 'std', 'min', 'max', '50%']])
print("\nCASH_ADVANCE:")
print(X_log['CASH_ADVANCE'].describe()[['mean', 'std', 'min', 'max', '50%']])
