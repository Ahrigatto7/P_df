import os
import fitz  # PyMuPDF
from docx import Document
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- 문서 로딩 함수 ---
def load_documents(directory):
    docs = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        elif filename.endswith(".pdf"):
            text = extract_text_from_pdf(filepath)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(filepath)
        else:
            continue
        docs.append({"file": filename, "text": text})
    return docs

# --- PDF 텍스트 추출 ---
def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# --- DOCX 텍스트 추출 ---
def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 벡터화 ---
def vectorize_documents(docs, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    texts = [doc["text"] for doc in docs]
    embeddings = model.encode(texts)
    return embeddings

# --- 클러스터링 ---
def cluster_documents(docs, embeddings, n_clusters=4):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    clusters = kmeans.fit_predict(embeddings)
    for doc, cluster_id in zip(docs, clusters):
        doc["cluster"] = cluster_id
    return docs
