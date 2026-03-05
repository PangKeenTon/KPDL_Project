import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
    adjusted_rand_score,
)


def main() -> None:
    raw = pd.read_csv("CC GENERAL.csv")
    x = raw.drop(columns=["CUST_ID"]).copy()
    x["MINIMUM_PAYMENTS"] = x["MINIMUM_PAYMENTS"].fillna(x["MINIMUM_PAYMENTS"].median())
    x["CREDIT_LIMIT"] = x["CREDIT_LIMIT"].fillna(x["CREDIT_LIMIT"].median())

    x_log = np.log1p(x)
    x_scaled = StandardScaler().fit_transform(x_log)

    seeds = list(range(30))
    metrics = []
    labels_list = []

    for seed in seeds:
        model = KMeans(
            n_clusters=4,
            init="k-means++",
            n_init=10,
            max_iter=300,
            random_state=seed,
        )
        labels = model.fit_predict(x_scaled)
        labels_list.append(labels)
        metrics.append(
            {
                "seed": seed,
                "inertia": float(model.inertia_),
                "silhouette": float(silhouette_score(x_scaled, labels)),
                "dbi": float(davies_bouldin_score(x_scaled, labels)),
                "chi": float(calinski_harabasz_score(x_scaled, labels)),
                "n_iter": int(model.n_iter_),
                "sizes": sorted(np.bincount(labels, minlength=4).tolist()),
            }
        )

    aris = []
    for i in range(len(labels_list)):
        for j in range(i + 1, len(labels_list)):
            aris.append(adjusted_rand_score(labels_list[i], labels_list[j]))

    def arr(key: str) -> np.ndarray:
        return np.array([m[key] for m in metrics], dtype=float)

    summary = {
        "runs": len(seeds),
        "silhouette_mean": float(arr("silhouette").mean()),
        "silhouette_std": float(arr("silhouette").std(ddof=1)),
        "silhouette_min": float(arr("silhouette").min()),
        "silhouette_max": float(arr("silhouette").max()),
        "dbi_mean": float(arr("dbi").mean()),
        "dbi_std": float(arr("dbi").std(ddof=1)),
        "dbi_min": float(arr("dbi").min()),
        "dbi_max": float(arr("dbi").max()),
        "chi_mean": float(arr("chi").mean()),
        "chi_std": float(arr("chi").std(ddof=1)),
        "chi_min": float(arr("chi").min()),
        "chi_max": float(arr("chi").max()),
        "inertia_mean": float(arr("inertia").mean()),
        "inertia_std": float(arr("inertia").std(ddof=1)),
        "iter_mean": float(arr("n_iter").mean()),
        "iter_min": int(arr("n_iter").min()),
        "iter_max": int(arr("n_iter").max()),
        "ari_pairwise_mean": float(np.mean(aris)),
        "ari_pairwise_std": float(np.std(aris, ddof=1)),
        "ari_pairwise_min": float(np.min(aris)),
        "ari_pairwise_max": float(np.max(aris)),
        "sizes_example_seed0": metrics[0]["sizes"],
    }

    with open("stability_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
