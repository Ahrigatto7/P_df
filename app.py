import streamlit as st
from pipeline import load_documents, vectorize_documents, cluster_documents
from summarize import summarize_text_with_openai
from rag_module import build_retriever, ask_question
import pandas as pd
import os

# ✅ API 키 처리
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = st.text_input("🔑 OpenAI API Key", type="password")

st.set_page_config(page_title="문서 분석 + 질의응답", layout="wide")
st.title("📄 문서 클러스터링 및 질의응답 대시보드")

# 📁 문서 업로드
uploaded_files = st.file_uploader("📂 분석할 문서 업로드", type=["txt", "pdf", "docx"], accept_multiple_files=True)

# 🔘 요약 방식
summary_method = st.selectbox("요약 방식 선택", ["기본 요약 (TF-IDF)", "OpenAI GPT 요약"])

# 분석 실행
if st.button("문서 분석 시작"):
    os.makedirs("documents", exist_ok=True)
    for file in uploaded_files:
        with open(os.path.join("documents", file.name), "wb") as f:
            f.write(file.getbuffer())

    docs = load_documents("documents")
    embeddings = vectorize_documents(docs)
    clustered_docs = cluster_documents(docs, embeddings, n_clusters=4)

    # 요약 처리
    for doc in clustered_docs:
        if summary_method == "OpenAI GPT 요약" and api_key:
            try:
                doc["summary"] = summarize_text_with_openai(doc["text"], api_key)
            except Exception as e:
                doc["summary"] = f"❌ 요약 실패: {e}"
        else:
            doc.setdefault("summary", doc.get("summary", "요약 없음"))

    st.success("✅ 문서 클러스터링 완료")
    df = pd.DataFrame(clustered_docs)
    st.session_state["docs"] = clustered_docs  # RAG용 저장

    # 결과 출력
    for cluster_id in sorted(df["cluster"].unique()):
        st.header(f"🔹 클러스터 {cluster_id}")
        for _, row in df[df["cluster"] == cluster_id].iterrows():
            st.subheader(f"📄 {os.path.basename(row['file'])}")
            st.write(f"📝 요약: {row['summary']}")
            with st.expander("📚 전체 텍스트 보기"):
                st.write(row["text"])

# 🧠 RAG 기반 질의응답
st.markdown("---")
st.subheader("💬 업로드된 문서에 질문해보세요 (LangChain + OpenAI)")
question = st.text_input("❓ 질문을 입력하세요")

if st.button("질문 실행") and question:
    try:
        # retriever 생성 후 QA 실행
        retriever = build_retriever(st.session_state["docs"], api_key)
        response = ask_question(retriever, question, api_key)
        st.success("🧠 GPT 응답:")
        st.write(response)
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

# ========================
# 📊 추가 기능: 키워드 DB화, 클러스터링, HTML 리포트 생성
# ========================
from ingest_documents import ingest_all_documents
from visualize_clusters import run_clustering
from generate_html_report import generate_html_report

st.markdown("---")
st.subheader("📊 문서 클러스터링 및 리포트 자동화")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📂 문서 DB 저장 (키워드 추출)"):
        ingest_all_documents()
        st.success("✅ 문서 및 키워드가 DB에 저장되었습니다.")

with col2:
    if st.button("🧠 문서 클러스터링 수행"):
        run_clustering(output_csv="clustered_output.csv")
        st.success("✅ KMeans 클러스터링 완료 (CSV 저장됨)")

with col3:
    if st.button("📝 HTML 리포트 생성"):
        generate_html_report(csv_path="clustered_output.csv")
        st.success("✅ HTML 리포트 생성 완료: cluster_report.html")

# 클러스터 결과 미리보기
if os.path.exists("clustered_output.csv"):
    st.markdown("### 📄 클러스터링 결과 미리보기")
    df = pd.read_csv("clustered_output.csv")
    st.dataframe(df[['filename', 'cluster']])
