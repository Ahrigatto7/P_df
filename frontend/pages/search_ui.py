import streamlit as st
from core.vector_ops import hybrid_search


def render():
    st.header("통합 RAG 검색(QA)")

    question = st.text_input("질문 입력")
    sources = st.multiselect(
        "검색 범위", ["규칙", "사례", "용어", "PDF"],
        default=["규칙", "사례", "용어", "PDF"],
    )

    if st.button("검색"):
        if not question.strip():
            st.warning("질문을 입력해주세요.")
            return

        data = hybrid_search(question, sources=sources)
        for doc in data.get("sources", []):
            st.markdown(f"**[{doc['doc_type']}]** {doc['title']} : {doc['excerpt']}")
        st.success("AI 답변: " + data.get("answer", ""))

