from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from .pdf_utils import extract_pdf_text_advanced, split_text_chunks

def vectorize_document(chunks, meta):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="./vector_db/chroma_db", embedding_function=embeddings)
    docs = [{"page_content": chunk, "metadata": meta} for chunk in chunks]
    vectordb.add_documents(docs)
    return {"msg": "임베딩 완료", "count": len(chunks)}

def vectorize_file(file, doc_type: str = "PDF", meta: dict | None = None):
    """Vectorize an uploaded file and store the embeddings."""
    import tempfile

    content = file.read()
    path = None
    if doc_type == "PDF":
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(content)
            path = tmp.name
        text = extract_pdf_text_advanced(path)
        chunks = split_text_chunks(text)
    else:
        text = content.decode()
        chunks = split_text_chunks(text)

    meta = meta or {}
    meta["doc_type"] = doc_type
    return vectorize_document(chunks, meta)

def hybrid_search(query, sources=None):
    vectordb = Chroma(persist_directory="./vector_db/chroma_db")
    filters = {"doc_type": {"$in": sources}} if sources else None
    results = vectordb.similarity_search(query, k=5, filter=filters)
    sources_out = [{
        "title": r.metadata.get("filename", ""),
        "doc_type": r.metadata.get("doc_type", ""),
        "excerpt": r.page_content[:100]
    } for r in results]
    answer = " ".join([r.page_content for r in results])[:300]
    return {"answer": answer, "sources": sources_out}
