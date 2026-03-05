#!/usr/bin/env python3
import pandas as pd

df = pd.read_csv('Credit_Card_Clustered_Results.csv')

features = ['BALANCE', 'PURCHASES', 'CASH_ADVANCE', 'CREDIT_LIMIT', 'PAYMENTS', 
            'PRC_FULL_PAYMENT', 'PURCHASES_FREQUENCY', 'CASH_ADVANCE_FREQUENCY', 'TENURE']

for cluster in range(4):
    cluster_data = df[df['Cluster'] == cluster]
    size = len(cluster_data)
    pct = 100 * size / len(df)
    print(f'\n=== CLUSTER {cluster}: {size} khách ({pct:.1f}%) ===')
    for feat in features:
        if feat in df.columns:
            mean_val = cluster_data[feat].mean()
            if feat == 'PRC_FULL_PAYMENT':
                print(f'{feat}: {mean_val*100:.2f}%')
            elif feat in ['PURCHASES_FREQUENCY', 'CASH_ADVANCE_FREQUENCY']:
                print(f'{feat}: {mean_val:.2f}')
            elif feat == 'TENURE':
                print(f'{feat}: {mean_val:.1f} tháng')
            else:
                print(f'{feat}: ${mean_val:.0f}')
