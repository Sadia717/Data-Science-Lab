#20-11-26
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

np.random.seed(5)

centres = [(25, 80), (55, 20), (85, 85), (55, 50), (25, 20)]
rows = []

for inc, score in centres:
    for _ in range(40):
        rows.append([np.random.normal(inc, 7), np.random.normal(score, 7)])

customers = pd.DataFrame(np.round(rows, 1),
                        columns=["annual_income_k", "spending_score"])
customers.insert(0, "customer_id", range(1, 201))

print("Mall Customer Segmentation using K-Means")
print("=" * 50)
print(customers.head().to_string(index=False))
print("Total customers:", len(customers))

X = StandardScaler().fit_transform(
    customers[["annual_income_k", "spending_score"]]
)

# Find the best number of clusters
wcss, sil = [], []
print("\nk   WCSS   Silhouette")

for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    wcss.append(km.inertia_)
    sil.append(silhouette_score(X, km.labels_))
    print(k, round(km.inertia_, 2), round(sil[-1], 4))

best_k = range(2, 9)[np.argmax(sil)]
print("\nBest k:", best_k)

# Final clustering
km = KMeans(n_clusters=best_k, n_init=10, random_state=0).fit(X)
customers["cluster"] = km.labels_

profile = customers.groupby("cluster")[
    ["annual_income_k", "spending_score"]
].mean().round(1)
profile["size"] = customers["cluster"].value_counts().sort_index()

def describe(row):
    inc = "High income" if row.annual_income_k > 70 else (
        "Low income" if row.annual_income_k < 40 else "Mid income")
    sp = "high spender" if row.spending_score > 65 else (
        "low spender" if row.spending_score < 35 else "average spender")
    return inc + ", " + sp

profile["segment"] = profile.apply(describe, axis=1)
print("\nCluster Profiles:")
print(profile.to_string())

# Graphs
plt.subplot(1, 2, 1)
plt.plot(range(2, 9), wcss, "o-")
plt.xlabel("Number of clusters (k)")
plt.ylabel("WCSS")
plt.title("Elbow Method")

plt.subplot(1, 2, 2)
plt.scatter(customers.annual_income_k, customers.spending_score,
            c=customers.cluster, s=20)
centres = customers.groupby("cluster")[
    ["annual_income_k", "spending_score"]
].mean()
plt.scatter(centres.iloc[:, 0], centres.iloc[:, 1],
            c="black", marker="X", s=150, label="Centroids")
plt.xlabel("Annual Income")
plt.ylabel("Spending Score")
plt.title("Customer Segments")
plt.legend()

plt.tight_layout()
plt.savefig("exp08_kmeans.png")
plt.show()
