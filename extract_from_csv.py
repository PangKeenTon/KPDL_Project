#!/usr/bin/env python3
"""
Extract all metrics from Credit_Card_Clustered_Results.csv
This is the actual output from the notebook, so it's ground truth
"""
import pandas as pd

print("="*80)
print("LOADING CLUSTERED RESULTS")
print("="*80)

# Load the CSV that was exported by the notebook
df = pd.read_csv('Credit_Card_Clustered_Results.csv')
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

n_total = len(df)

print("\n" + "="*80)
print("CLUSTER DISTRIBUTION")
print("="*80)

cluster_counts = df['Cluster'].value_counts().sort_index()
print("\nCluster sizes:")
for cluster_id in sorted(df['Cluster'].unique()):
    count = (df['Cluster'] == cluster_id).sum()
    pct = 100 * count / n_total
    print(f"  Cluster {cluster_id}: {count:5d} ({pct:5.1f}%)")

print("\n" + "="*80)
print("OUTLIERS")
print("="*80)

# Check Is_Outlier column if exists
if 'Is_Outlier' in df.columns:
    outlier_count = df['Is_Outlier'].sum()
    outlier_pct = 100 * outlier_count / n_total
    normal_count = (~df['Is_Outlier']).sum()
    print(f"Outliers (DBSCAN): {outlier_count} ({outlier_pct:.2f}%)")
    print(f"Normal: {normal_count} ({100*normal_count/n_total:.2f}%)")
else:
    print("No Is_Outlier column found")

print(f"Total: {n_total}")

# Financial features for detailed stats
print("\n" + "="*80)
print("CLUSTER FINANCIAL PROFILES")
print("="*80)

key_features = ['BALANCE', 'PURCHASES', 'CASH_ADVANCE', 'CREDIT_LIMIT', 'PAYMENTS',
                'PRC_FULL_PAYMENT', 'PURCHASES_FREQUENCY', 'CASH_ADVANCE_FREQUENCY', 'TENURE']

# Only check features that exist in CSV
available_features = [f for f in key_features if f in df.columns]

for cluster_id in sorted(df['Cluster'].unique()):
    cluster_df = df[df['Cluster'] == cluster_id]
    size = len(cluster_df)
    pct = 100 * size / n_total
    
    print(f"\nCluster {cluster_id}: {size} khách ({pct:.1f}%)")
    print("-" * 60)
    
    for feat in available_features:
        mean_val = cluster_df[feat].mean()
        overall_mean = df[feat].mean()
        index = 100 * mean_val / overall_mean if overall_mean > 0 else 0
        
        if feat == 'PRC_FULL_PAYMENT':
            print(f"  {feat:25s}: {mean_val*100:6.2f}% (index: {index:6.1f})")
        elif feat in ['PURCHASES_FREQUENCY', 'CASH_ADVANCE_FREQUENCY']:
            print(f"  {feat:25s}: {mean_val:6.2f} (index: {index:6.1f})")
        elif feat == 'TENURE':
            print(f"  {feat:25s}: {mean_val:6.1f} months (index: {index:6.1f})")
        else:
            print(f"  {feat:25s}: ${mean_val:7.0f} (index: {index:6.1f})")

print("\n" + "="*80)
print("REPORT SUMMARY")
print("="*80)
print(f"""
CRITICAL NUMBERS FOR LATEX:
- Total samples: {n_total}
- Cluster 0: {cluster_counts[0]} ({100*cluster_counts[0]/n_total:.1f}%)
- Cluster 1: {cluster_counts[1]} ({100*cluster_counts[1]/n_total:.1f}%)
- Cluster 2: {cluster_counts[2]} ({100*cluster_counts[2]/n_total:.1f}%)
- Cluster 3: {cluster_counts[3]} ({100*cluster_counts[3]/n_total:.1f}%)
""")
