import os
import pandas as pd
import streamlit as st
from pipeline import (
    load_documents,
    vectorize_documents,
    cluster_documents,
    generate_html_report,
)

st.title("📄 문서 클러스터링 및 요약 대시보드")

if st.button("문서 분석 시작"):
    docs = load_documents("documents")
    embeddings = vectorize_documents(docs)
    docs, summaries = cluster_documents(docs, embeddings, n_clusters=4)

    df = pd.DataFrame(docs)
    df.to_csv("clustered_documents.csv", index=False)
    generate_html_report(docs, summaries, "report.html")

    for cluster_id in sorted(df["cluster"].unique()):
        st.header(f"🔹 클러스터 {cluster_id}")
        st.write(f"**요약**: {summaries[cluster_id]}")
        for _, row in df[df["cluster"] == cluster_id].iterrows():
            st.subheader(os.path.basename(row["file"]))
            st.write(row["summary"])
            with st.expander("전체 텍스트 보기"):
                st.write(row["text"])

