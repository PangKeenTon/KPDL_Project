#!/usr/bin/env python3
"""
Comprehensive verification script to extract and verify all metrics
used in the LaTeX report against actual notebook code and outputs
"""
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# Load data
print("="*80)
print("LOADING DATA AND PREPROCESSING")
print("="*80)
df = pd.read_csv('CC GENERAL.csv')
print(f"Original shape: {df.shape}")

# Handle missing values
df['MINIMUM_PAYMENTS'].fillna(df['MINIMUM_PAYMENTS'].median(), inplace=True)
df['CREDIT_LIMIT'].fillna(df['CREDIT_LIMIT'].median(), inplace=True)

# Drop NaN rows
df = df.dropna()
print(f"After dropping NaN: {df.shape}")
n_samples = len(df)

# Log transform
X = df[['BALANCE', 'PURCHASES', 'ONEOFF_PURCHASES', 'INSTALLMENTS_PURCHASES',
         'CASH_ADVANCE', 'PURCHASES_FREQUENCY', 'ONEOFF_PURCHASES_FREQUENCY',
         'PURCHASES_INSTALLMENTS_FREQUENCY', 'CASH_ADVANCE_FREQUENCY',
         'CASH_ADVANCE_TRX', 'PURCHASES_TRX', 'CREDIT_LIMIT', 'PAYMENTS',
         'MINIMUM_PAYMENTS', 'PRC_FULL_PAYMENT', 'TENURE']].copy()

print(f"\nOriginal features shape: {X.shape}")

X_log = np.log(1 + X)

# Standardization
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_log)
print(f"Scaled shape: {X_scaled.shape}")

# PCA
print("\n" + "="*80)
print("PCA ANALYSIS")
print("="*80)
pca_full = PCA()
X_pca_full = pca_full.fit_transform(X_scaled)
variance_ratio = pca_full.explained_variance_ratio_
cumsum = np.cumsum(variance_ratio)

print(f"Total features: {len(variance_ratio)}")
print(f"PC1 variance: {variance_ratio[0]*100:.2f}%")
print(f"PC2 variance: {variance_ratio[1]*100:.2f}%")
print(f"PC1+PC2 variance: {cumsum[1]*100:.2f}%")

# Use 2D PCA for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(f"\n2D PCA variance ratio:")
print(f"  PC1: {pca.explained_variance_ratio_[0]*100:.2f}%")
print(f"  PC2: {pca.explained_variance_ratio_[1]*100:.2f}%")
print(f"  Total: {sum(pca.explained_variance_ratio_)*100:.2f}%")

# K-means Elbow & Silhouette
print("\n" + "="*80)
print("K-MEANS ELBOW & SILHOUETTE ANALYSIS")
print("="*80)
K_range = range(2, 11)
inertias = []
silhouette_scores = []

for k in K_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sil_score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(sil_score)
    
print("\nK | Inertia | Silhouette")
print("-" * 30)
for k, inertia, sil in zip(K_range, inertias, silhouette_scores):
    print(f"{k} | {inertia:7.0f} | {sil:.4f}")

# K-means with K=4
print("\n" + "="*80)
print("K-MEANS CLUSTERING (K=4)")
print("="*80)
kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
labels = kmeans.fit_predict(X_scaled)
df['Cluster'] = labels

cluster_sizes = pd.Series(labels).value_counts().sort_index()
print("\nCluster sizes:")
for cluster, size in cluster_sizes.items():
    pct = 100 * size / n_samples
    print(f"  Cluster {cluster}: {size:4d} ({pct:5.1f}%)")

print(f"\nTotal: {cluster_sizes.sum()}")

# Evaluation metrics for K=4
silhouette_k4 = silhouette_score(X_scaled, labels)
davies_bouldin_k4 = davies_bouldin_score(X_scaled, labels)
calinski_harabasz_k4 = calinski_harabasz_score(X_scaled, labels)

print(f"\nK=4 metrics:")
print(f"  Silhouette Score: {silhouette_k4:.4f}")
print(f"  Davies-Bouldin Index: {davies_bouldin_k4:.4f}")
print(f"  Calinski-Harabasz Index: {calinski_harabasz_k4:.2f}")

# Cluster statistics
print("\n" + "="*80)
print("CLUSTER FINANCIAL STATISTICS")
print("="*80)

key_features = ['BALANCE', 'PURCHASES', 'CASH_ADVANCE', 'CREDIT_LIMIT', 'PAYMENTS',
                'PRC_FULL_PAYMENT', 'PURCHASES_FREQUENCY', 'CASH_ADVANCE_FREQUENCY', 'TENURE']

for cluster in range(4):
    cluster_data = df[df['Cluster'] == cluster]
    size = len(cluster_data)
    pct = 100 * size / n_samples
    print(f"\n--- Cluster {cluster} ({size} khách, {pct:.1f}%) ---")
    
    for feat in key_features:
        mean_val = cluster_data[feat].mean()
        all_mean = df[feat].mean()
        idx = 100 * mean_val / all_mean if all_mean != 0 else 0
        
        print(f"{feat:25s}: ${mean_val:7.0f} (index: {idx:6.1f})" if feat not in ['PRC_FULL_PAYMENT', 'PURCHASES_FREQUENCY', 'CASH_ADVANCE_FREQUENCY', 'TENURE'] else f"{feat:25s}: {mean_val*100:6.2f}%" if feat == 'PRC_FULL_PAYMENT' else f"{feat:25s}: {mean_val:6.2f}")

# PCA centroids
print("\n" + "="*80)
print("PCA CENTROIDS (K=4)")
print("="*80)
centroids_pca = pca.transform(kmeans.cluster_centers_)
print("\nCluster centroids in 2D PCA space:")
print("Cluster | PC1    | PC2")
print("-" * 30)
for i, centroid in enumerate(centroids_pca):
    print(f"   {i}    | {centroid[0]:6.2f} | {centroid[1]:6.2f}")

# DBSCAN anomaly detection
print("\n" + "="*80)
print("DBSCAN OUTLIER DETECTION")
print("="*80)
dbscan = DBSCAN(eps=0.5, min_samples=10)
dbscan_labels = dbscan.fit_predict(X_scaled)
df['Is_Outlier'] = (dbscan_labels == -1)

outlier_count = (dbscan_labels == -1).sum()
outlier_pct = 100 * outlier_count / n_samples

print(f"\nDBSCAN results (eps=0.5, min_samples=10):")
print(f"  Outliers found: {outlier_count}")
print(f"  Percentage: {outlier_pct:.2f}%")
print(f"  Normal points: {n_samples - outlier_count} ({100-outlier_pct:.2f}%)")

# Summary
print("\n" + "="*80)
print("SUMMARY FOR LATEX REPORT VERIFICATION")
print("="*80)
print(f"""
PCA (Chapter 5/6):
  - PC1 variance: {pca.explained_variance_ratio_[0]*100:.2f}%
  - PC2 variance: {pca.explained_variance_ratio_[1]*100:.2f}%
  - Total 2D variance: {sum(pca.explained_variance_ratio_)*100:.2f}%

K-means (Chapter 6):
  - Optimal K: 4
  - Cluster 0: {cluster_sizes[0]:4d} ({100*cluster_sizes[0]/n_samples:5.1f}%)
  - Cluster 1: {cluster_sizes[1]:4d} ({100*cluster_sizes[1]/n_samples:5.1f}%)
  - Cluster 2: {cluster_sizes[2]:4d} ({100*cluster_sizes[2]/n_samples:5.1f}%)
  - Cluster 3: {cluster_sizes[3]:4d} ({100*cluster_sizes[3]/n_samples:5.1f}%)
  - Silhouette K=4: {silhouette_k4:.4f}
  - Davies-Bouldin K=4: {davies_bouldin_k4:.4f}
  - Calinski-Harabasz K=4: {calinski_harabasz_k4:.2f}
  - Inertia K=4: {kmeans.inertia_:.0f}

DBSCAN (Chapter 6 & 8):
  - Outliers: {outlier_count} ({outlier_pct:.2f}%)
  - Normal: {n_samples - outlier_count} ({100-outlier_pct:.2f}%)
  - Total: {n_samples}

Centroids in PCA 2D:
  - C0: ({centroids_pca[0][0]:6.2f}, {centroids_pca[0][1]:6.2f})
  - C1: ({centroids_pca[1][0]:6.2f}, {centroids_pca[1][1]:6.2f})
  - C2: ({centroids_pca[2][0]:6.2f}, {centroids_pca[2][1]:6.2f})
  - C3: ({centroids_pca[3][0]:6.2f}, {centroids_pca[3][1]:6.2f})
""")
