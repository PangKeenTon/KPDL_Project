import pandas as pd

df = pd.read_csv('CC GENERAL.csv')
df_numeric = df.drop('CUST_ID', axis=1)

# Show descriptive statistics
stats = df.describe()
print("Descriptive Statistics of All Variables:")
print(stats.to_string())
print("\n\nSpecific variables for table:")
print("\nBALANCE:")
print(f"Mean: ${df['BALANCE'].mean():.0f}")
print(f"Std: ${df['BALANCE'].std():.0f}")
print(f"Min: ${df['BALANCE'].min():.0f}")
print(f"Max: ${df['BALANCE'].max():.0f}")
print(f"Median: ${df['BALANCE'].median():.0f}")

print("\nPURCHASES:")
print(f"Mean: ${df['PURCHASES'].mean():.0f}")
print(f"Std: ${df['PURCHASES'].std():.0f}")
print(f"Min: ${df['PURCHASES'].min():.0f}")
print(f"Max: ${df['PURCHASES'].max():.0f}")
print(f"Median: ${df['PURCHASES'].median():.0f}")

print("\nCASH_ADVANCE:")
print(f"Mean: ${df['CASH_ADVANCE'].mean():.0f}")
print(f"Std: ${df['CASH_ADVANCE'].std():.0f}")
print(f"Min: ${df['CASH_ADVANCE'].min():.0f}")
print(f"Max: ${df['CASH_ADVANCE'].max():.0f}")
print(f"Median: ${df['CASH_ADVANCE'].median():.0f}")

print("\nCREDIT_LIMIT:")
print(f"Mean: ${df['CREDIT_LIMIT'].mean():.0f}")
print(f"Std: ${df['CREDIT_LIMIT'].std():.0f}")
print(f"Min: ${df['CREDIT_LIMIT'].min():.0f}")
print(f"Max: ${df['CREDIT_LIMIT'].max():.0f}")
print(f"Median: ${df['CREDIT_LIMIT'].median():.0f}")

print("\nPAYMENTS:")
print(f"Mean: ${df['PAYMENTS'].mean():.0f}")
print(f"Std: ${df['PAYMENTS'].std():.0f}")
print(f"Min: ${df['PAYMENTS'].min():.0f}")
print(f"Max: ${df['PAYMENTS'].max():.0f}")
print(f"Median: ${df['PAYMENTS'].median():.0f}")

print("\nMINIMUM_PAYMENTS:")
print(f"Mean: ${df['MINIMUM_PAYMENTS'].mean():.0f}")
print(f"Std: ${df['MINIMUM_PAYMENTS'].std():.0f}")
print(f"Min: ${df['MINIMUM_PAYMENTS'].min():.0f}")
print(f"Max: ${df['MINIMUM_PAYMENTS'].max():.0f}")
print(f"Median: ${df['MINIMUM_PAYMENTS'].median():.0f}")

print("\nTENURE:")
print(f"Mean: {df['TENURE'].mean():.1f}")
print(f"Std: {df['TENURE'].std():.1f}")
print(f"Min: {df['TENURE'].min():.0f}")
print(f"Max: {df['TENURE'].max():.0f}")
print(f"Median: {df['TENURE'].median():.0f}")

# Check correlations
print("\n\nCorrelation Analysis:")
corr = df_numeric.corr()
# Find strong correlations (> 0.6)
strong_corr = []
for i in range(len(corr.columns)):
    for j in range(i+1, len(corr.columns)):
        if abs(corr.iloc[i, j]) > 0.6:
            strong_corr.append((corr.columns[i], corr.columns[j], corr.iloc[i, j]))

strong_corr.sort(key=lambda x: abs(x[2]), reverse=True)
print("\nStrong correlations (> 0.6):")
for var1, var2, corr_val in strong_corr[:10]:
    print(f"{var1} <-> {var2}: {corr_val:.2f}")
