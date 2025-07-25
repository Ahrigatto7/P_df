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

def run_clustering(num_clusters=3, output_csv="clustered_output.csv"):
    df = load_documents()
    contents = df['content'].fillna("")
    vectorizer = TfidfVectorizer(max_features=300)
    X = vectorizer.fit_transform(contents)

    model = KMeans(n_clusters=num_clusters, random_state=42)
    df['cluster'] = model.fit_predict(X)

    # 결과 출력
    for i in range(num_clusters):
        print(f"\n📂 Cluster {i}:")
        print(df[df['cluster'] == i]['filename'].tolist())

    # 시각화
    plt.figure(figsize=(8, 5))
    plt.hist(df['cluster'], bins=num_clusters, edgecolor='black')
    plt.title("문서 클러스터 분포")
    plt.xlabel("클러스터 ID")
    plt.ylabel("문서 수")
    plt.grid(True)
    plt.show()

    # CSV로 저장
    df.to_csv(output_csv, index=False)
    print(f"\n✅ 군집화 결과 저장 완료: {output_csv}")
