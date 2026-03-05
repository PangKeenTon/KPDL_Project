import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN

# Read and prepare data
df = pd.read_csv('CC GENERAL.csv')
df_features = df.drop('CUST_ID', axis=1)
df_filled = df_features.fillna(df_features.median())

# Log transformation and scaling
X_log = np.log1p(df_filled)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_log)

# K-means clustering
kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, max_iter=300, tol=1e-4, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# Add labels to data
df_labeled = df_features.copy()
df_labeled['Cluster'] = labels

print("=== CLUSTER DETAILED STATISTICS ===")
for cluster_id in range(4):
    cluster_data = df_labeled[df_labeled['Cluster'] == cluster_id].drop('Cluster', axis=1)
    n_customers = len(cluster_data)
    pct = n_customers / len(df_labeled) * 100
    
    print(f"\nCluster {cluster_id}: {n_customers} customers ({pct:.1f}%)")
    print(f"  BALANCE: ${cluster_data['BALANCE'].mean():.0f} (overall: ${df_features['BALANCE'].mean():.0f}, diff: {(cluster_data['BALANCE'].mean()/df_features['BALANCE'].mean()-1)*100:.1f}%)")
    print(f"  PURCHASES: ${cluster_data['PURCHASES'].mean():.0f} (overall: ${df_features['PURCHASES'].mean():.0f}, diff: {(cluster_data['PURCHASES'].mean()/df_features['PURCHASES'].mean()-1)*100:.1f}%)")
    print(f"  CASH_ADVANCE: ${cluster_data['CASH_ADVANCE'].mean():.0f} (overall: ${df_features['CASH_ADVANCE'].mean():.0f}, diff: {(cluster_data['CASH_ADVANCE'].mean()/df_features['CASH_ADVANCE'].mean()-1)*100:.1f}%)")
    print(f"  CREDIT_LIMIT: ${cluster_data['CREDIT_LIMIT'].mean():.0f} (overall: ${df_features['CREDIT_LIMIT'].mean():.0f}, diff: {(cluster_data['CREDIT_LIMIT'].mean()/df_features['CREDIT_LIMIT'].mean()-1)*100:.1f}%)")
    print(f"  PAYMENTS: ${cluster_data['PAYMENTS'].mean():.0f} (overall: ${df_features['PAYMENTS'].mean():.0f}, diff: {(cluster_data['PAYMENTS'].mean()/df_features['PAYMENTS'].mean()-1)*100:.1f}%)")
    print(f"  PRC_FULL_PAYMENT: {cluster_data['PRC_FULL_PAYMENT'].mean():.2%} (overall: {df_features['PRC_FULL_PAYMENT'].mean():.2%})")
    print(f"  TENURE: {cluster_data['TENURE'].mean():.1f} months (overall: {df_features['TENURE'].mean():.1f})")

# Overall average for baseline
print("\n=== OVERALL STATISTICS ===")
print(f"BALANCE: ${df_features['BALANCE'].mean():.0f}")
print(f"PURCHASES: ${df_features['PURCHASES'].mean():.0f}")
print(f"CASH_ADVANCE: ${df_features['CASH_ADVANCE'].mean():.0f}")
print(f"CREDIT_LIMIT: ${df_features['CREDIT_LIMIT'].mean():.0f}")
print(f"PAYMENTS: ${df_features['PAYMENTS'].mean():.0f}")
print(f"PRC_FULL_PAYMENT: {df_features['PRC_FULL_PAYMENT'].mean():.2%}")

# DBSCAN
print("\n=== DBSCAN (eps=0.5, min_samples=10) ===")
dbscan = DBSCAN(eps=0.5, min_samples=10)
dbscan_labels = dbscan.fit_predict(X_scaled)
n_clusters_dbscan = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_outliers = list(dbscan_labels).count(-1)
print(f"Clusters: {n_clusters_dbscan}")
print(f"Outliers: {n_outliers} ({n_outliers/len(labels)*100:.2f}%)")
