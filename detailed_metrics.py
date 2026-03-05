import pandas as pd

df = pd.read_csv('Credit_Card_Clustered_Results.csv')

print("CLUSTER INFO FOR LATEX UPDATE")
print("="*80)

# Cụm 0
c0 = df[df['Cluster'] == 0]
print("\nCụm 0 (Active Customers):")
print(f"  Kích thước: {len(c0)} khách ({100*len(c0)/len(df):.1f}%)")
print(f"  BALANCE: ${c0['BALANCE'].mean():,.0f}")
print(f"  PURCHASES: ${c0['PURCHASES'].mean():,.0f}")
print(f"  CREDIT_LIMIT: ${c0['CREDIT_LIMIT'].mean():,.0f}")
print(f"  PAYMENTS: ${c0['PAYMENTS'].mean():,.0f}")
print(f"  PRC_FULL_PAYMENT: {c0['PRC_FULL_PAYMENT'].mean():.2%}")

# Cụm 1
c1 = df[df['Cluster'] == 1]
print("\nCụm 1 (Cash Advance Users):")
print(f"  Kích thước: {len(c1)} khách ({100*len(c1)/len(df):.1f}%)")
print(f"  CASH_ADVANCE: ${c1['CASH_ADVANCE'].mean():,.0f}")
print(f"  CASH_ADVANCE_FREQUENCY: {c1['CASH_ADVANCE_FREQUENCY'].mean():.2f}")
print(f"  PRC_FULL_PAYMENT: {c1['PRC_FULL_PAYMENT'].mean():.2%}")

# Cụm 2
c2 = df[df['Cluster'] == 2]
print("\nCụm 2 (Potential Customers):")
print(f"  Kích thước: {len(c2)} khách ({100*len(c2)/len(df):.1f}%)")
print(f"  BALANCE: ${c2['BALANCE'].mean():,.0f}")
print(f"  PURCHASES: ${c2['PURCHASES'].mean():,.0f}")
print(f"  CREDIT_LIMIT: ${c2['CREDIT_LIMIT'].mean():,.0f}")
print(f"  TENURE trung bình: {c2['TENURE'].mean():.1f} tháng")

# Cụm 3
c3 = df[df['Cluster'] == 3]
print("\nCụm 3 (Premium Customers):")
print(f"  Kích thước: {len(c3)} khách ({100*len(c3)/len(df):.1f}%)")
print(f"  BALANCE: ${c3['BALANCE'].mean():,.0f}")
print(f"  PURCHASES: ${c3['PURCHASES'].mean():,.0f}")
print(f"  CREDIT_LIMIT: ${c3['CREDIT_LIMIT'].mean():,.0f}")
print(f"  PAYMENTS: ${c3['PAYMENTS'].mean():,.0f}")
print(f"  PRC_FULL_PAYMENT: {c3['PRC_FULL_PAYMENT'].mean():.2%}")

print("\n" + "="*80)
print(f"Outlier (DBSCAN): {df['Is_Outlier'].sum()} khách ({100*df['Is_Outlier'].sum()/len(df):.2f}%)")
print(f"Total đã cluster: {len(df)} khách")
