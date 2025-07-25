import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def load_documents(db_path="keywords.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM documents", conn)
    conn.close()
    return df

def run_clustering(num_clusters=3):
    df = load_documents()
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(df['content'].fillna(""))
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)

    for cluster_id in range(num_clusters):
        print(f"\n[Cluster {cluster_id}]")
        print(df[df['cluster'] == cluster_id]['filename'].values)

    plt.figure(figsize=(8, 5))
    plt.hist(df['cluster'], bins=num_clusters, edgecolor='black')
    plt.title("문서 클러스터 분포")
    plt.xlabel("클러스터 ID")
    plt.ylabel("문서 수")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_clustering()
