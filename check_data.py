import pandas as pd

df = pd.read_csv('CC GENERAL.csv')
print(f'Shape: {df.shape}')
print(f'\nMissing values:')
print(df.isnull().sum()[df.isnull().sum() > 0])
print(f'\nMedian MINIMUM_PAYMENTS: ${df["MINIMUM_PAYMENTS"].median():.2f}')
print(f'Median CREDIT_LIMIT: ${df["CREDIT_LIMIT"].median():.2f}')
print(f'\nAfter dropping CUST_ID, features: {df.shape[1] - 1}')
