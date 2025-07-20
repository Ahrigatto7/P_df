import streamlit as st

def render():
    st.header("통합 RAG 검색(QA)")
    question = st.text_input("질문 입력")
    sources = st.multiselect("검색 범위", ["규칙", "사례", "용어", "PDF"], default=["규칙", "사례", "용어", "PDF"])
    if st.button("검색"):
        res = requests.post("http://localhost:8000/search", json={"question": question, "sources": sources})
        for doc in res.json()["sources"]:
            st.markdown(f"**[{doc['doc_type']}]** {doc['title']} : {doc['excerpt']}")
        st.success("AI 답변: " + res.json()["answer"])
