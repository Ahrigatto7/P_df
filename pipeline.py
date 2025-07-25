import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from jinja2 import Template
from utils import extract_text_from_file


def load_documents(folder_path):
    """Load documents from a folder and extract text."""
    docs = []
    for fname in sorted(os.listdir(folder_path)):
        path = os.path.join(folder_path, fname)
        if os.path.isfile(path):
            text = extract_text_from_file(path)
            docs.append({"file": path, "text": text})
    return docs


def get_embedding_model(model_name="all-MiniLM-L6-v2"):
    """Return a sentence transformer model."""
    return SentenceTransformer(model_name)


def vectorize_documents(docs, model_name="all-MiniLM-L6-v2"):
    """Vectorize documents using SentenceTransformer."""
    model = get_embedding_model(model_name)
    embeddings = model.encode([d["text"] for d in docs])
    return embeddings


def summarize_text(text, num_sentences=2):
    """Simple TF-IDF based summarization."""
    sentences = [s.strip() for s in text.replace("\n", " ").split(". ") if s.strip()]
    if len(sentences) <= num_sentences:
        return " ".join(sentences)
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(sentences)
    scores = tfidf.sum(axis=1).A1
    top_idx = np.argsort(scores)[-num_sentences:][::-1]
    selected = [sentences[i] for i in sorted(top_idx)]
    return ". ".join(selected)


def cluster_documents(docs, embeddings, n_clusters=4):
    """Cluster documents and create summaries."""
    km = KMeans(n_clusters=n_clusters, random_state=42)
    labels = km.fit_predict(embeddings)
    for doc, label in zip(docs, labels):
        doc["cluster"] = int(label)
        doc["summary"] = summarize_text(doc["text"])
    summaries = {}
    for label in sorted(set(labels)):
        combined = " ".join(d["text"] for d in docs if d["cluster"] == label)
        summaries[int(label)] = summarize_text(combined)
    return docs, summaries


def generate_html_report(docs, summaries, output_path="cluster_report.html"):
    """Generate an HTML report for clustered documents."""
    df = pd.DataFrame(docs)
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    html_template = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>문서 클러스터링 리포트</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; }
            .cluster { margin-bottom: 40px; background: #fff; padding: 15px; border-left: 5px solid #4CAF50; }
            h2 { margin-top: 0; }
        </style>
    </head>
    <body>
        <h1>📄 문서 클러스터링 리포트</h1>
        <div>생성일시: {{ timestamp }}</div>
        {% for cluster_id in clusters %}
        <div class="cluster">
            <h2>🔹 클러스터 {{ cluster_id }}</h2>
            <p><strong>요약:</strong> {{ summaries[cluster_id] }}</p>
            <ul>
            {% for doc in docs[cluster_id] %}
                <li><strong>{{ doc['file'] | basename }}</strong><br>
                {{ doc['summary'] }}</li>
            {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </body>
    </html>
    """

    cluster_docs = {}
    for cluster_id in sorted(df["cluster"].unique()):
        cluster_docs[cluster_id] = df[df["cluster"] == cluster_id].to_dict("records")

    template = Template(html_template)
    html_content = template.render(
        timestamp=timestamp,
        clusters=cluster_docs.keys(),
        summaries=summaries,
        docs=cluster_docs,
        basename=os.path.basename,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ HTML 리포트 저장 완료: {output_path}")
