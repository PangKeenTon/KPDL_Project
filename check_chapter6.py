import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# Read and prepare data
df = pd.read_csv('CC GENERAL.csv')
df_features = df.drop('CUST_ID', axis=1)
df_filled = df_features.fillna(df_features.median())

# Log transformation
X_log = np.log1p(df_filled)

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_log)

# PCA for 2 components
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print("=== PCA ANALYSIS ===")
print(f"PC1 variance ratio: {pca.explained_variance_ratio_[0]:.1%}")
print(f"PC2 variance ratio: {pca.explained_variance_ratio_[1]:.1%}")
print(f"Cumulative variance: {pca.explained_variance_ratio_.sum():.2%}")

# K-means with K=4
kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, max_iter=300, tol=1e-4, random_state=42)
labels = kmeans.fit_predict(X_scaled)

print("\n=== K-MEANS CLUSTERING ===")
unique, counts = np.unique(labels, return_counts=True)
for label, count in zip(unique, counts):
    pct = count / len(labels) * 100
    print(f"Cluster {label}: {count} customers ({pct:.1f}%)")

print(f"\nTotal iterations: {kmeans.n_iter_}")
print(f"Final inertia: {kmeans.inertia_:.0f}")

# Silhouette score
sil_score = silhouette_score(X_scaled, labels)
print(f"Silhouette Score: {sil_score:.3f}")

# Davies-Bouldin index
db_index = davies_bouldin_score(X_scaled, labels)
print(f"Davies-Bouldin Index: {db_index:.2f}")

# Calinski-Harabasz index
ch_index = calinski_harabasz_score(X_scaled, labels)
print(f"Calinski-Harabasz Index: {ch_index:.0f}")

# DBSCAN for outlier detection
dbscan = DBSCAN(eps=0.5, min_samples=10)
dbscan_labels = dbscan.fit_predict(X_scaled)
n_clusters_dbscan = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_outliers = list(dbscan_labels).count(-1)

print("\n=== DBSCAN ANALYSIS ===")
print(f"Number of clusters: {n_clusters_dbscan}")
print(f"Number of outliers: {n_outliers} ({n_outliers/len(labels)*100:.2f}%)")

# Cluster centroids in PCA space
print("\n=== CLUSTER CENTROIDS (PCA 2D) ===")
for i in range(4):
    mask = labels == i
    pc1_mean = X_pca[mask, 0].mean()
    pc2_mean = X_pca[mask, 1].mean()
    print(f"Cluster {i}: PC1={pc1_mean:.2f}, PC2={pc2_mean:.2f}")

# Detailed cluster analysis with original features
print("\n=== DETAILED CLUSTER ANALYSIS ===")
df_with_labels = df_features.copy()
df_with_labels['Cluster'] = labels

for cluster_id in range(4):
    cluster_data = df_with_labels[df_with_labels['Cluster'] == cluster_id].drop('Cluster', axis=1)
    print(f"\nCluster {cluster_id} (n={len(cluster_data)}):")
    print(f"  BALANCE: ${cluster_data['BALANCE'].mean():.0f} (overall: ${df_features['BALANCE'].mean():.0f})")
    print(f"  PURCHASES: ${cluster_data['PURCHASES'].mean():.0f} (overall: ${df_features['PURCHASES'].mean():.0f})")
    print(f"  CASH_ADVANCE: ${cluster_data['CASH_ADVANCE'].mean():.0f} (overall: ${df_features['CASH_ADVANCE'].mean():.0f})")
    print(f"  CREDIT_LIMIT: ${cluster_data['CREDIT_LIMIT'].mean():.0f} (overall: ${df_features['CREDIT_LIMIT'].mean():.0f})")
    print(f"  PAYMENTS: ${cluster_data['PAYMENTS'].mean():.0f} (overall: ${df_features['PAYMENTS'].mean():.0f})")
    print(f"  PRC_FULL_PAYMENT: {cluster_data['PRC_FULL_PAYMENT'].mean():.2%} (overall: {df_features['PRC_FULL_PAYMENT'].mean():.2%})")
