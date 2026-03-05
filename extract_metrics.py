import pandas as pd
import numpy as np

df = pd.read_csv('Credit_Card_Clustered_Results.csv')

print('='*80)
print('KÍCH THƯỚC CỤM')
print('='*80)
sizes = df['Cluster'].value_counts().sort_index()
for cluster_id in sorted(df['Cluster'].unique()):
    count = sizes[cluster_id]
    pct = 100 * count / len(df)
    print(f"Cụm {cluster_id}: {count:,} khách ({pct:.1f}%)")

print('\n' + '='*80)
print('OUTLIER (DBSCAN)')
print('='*80)
outlier_count = (df['Is_Outlier']).sum()
outlier_pct = 100 * outlier_count / len(df)
print(f"Outlier: {outlier_count} khách ({outlier_pct:.2f}%)")

print('\n' + '='*80)
print('THỐNG KÊ CHÍNH THEO CỤM')
print('='*80)
cols = ['BALANCE', 'PURCHASES', 'CASH_ADVANCE', 'CREDIT_LIMIT', 'PAYMENTS', 'PRC_FULL_PAYMENT', 'TENURE']
stats = df.groupby('Cluster')[cols].mean()
print(stats.round(2))

print('\n' + '='*80)
print('TỔNG CỘNG')
print('='*80)
print(f"Tổng khách hàng: {len(df):,}")
print(f"Số cột: {len(df.columns) - 2}")  # Bỏ Cluster và Is_Outlier
