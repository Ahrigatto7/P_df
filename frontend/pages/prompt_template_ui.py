# frontend/pages/prompt_template_ui.py
import streamlit as st
import requests


def render():
    st.header("PromptTemplate 관리/테스트")
    files = requests.get("http://localhost:8000/prompt_templates").json()["files"]
    selected = st.selectbox("프롬프트 선택", files)
    if selected:
        content = requests.get(
            "http://localhost:8000/prompt_template", params={"filename": selected}
        ).json()["content"]
        new_content = st.text_area("내용 편집", content, height=300)
        if st.button("저장"):
            requests.put(
                "http://localhost:8000/prompt_template",
                params={"filename": selected},
                data=new_content.encode(),
            )
            st.success("저장 완료!")

        st.markdown("---")
        st.subheader("프롬프트 테스트")
        context = st.text_area("테스트 context", "")
        question = st.text_input("테스트 question", "")
        if st.button("테스트 실행") and (context or question):
            res = requests.post(
                "http://localhost:8000/search", json={"question": question, "auto_tag": True}
            )
            st.write(res.json().get("tags", []))

