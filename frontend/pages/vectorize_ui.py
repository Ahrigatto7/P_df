import streamlit as st
from core.vector_ops import vectorize_file


def render():
    st.header("규칙/사례/용어/문서 통합 벡터화")
    files = st.file_uploader("파일 업로드", accept_multiple_files=True)
    doc_type = st.selectbox("유형", ["규칙", "사례", "용어", "PDF"])
    if st.button("업로드/임베딩") and files:
        for file in files:
            file.seek(0)
            res = vectorize_file(file, doc_type, {"filename": file.name})
            st.success(res)

