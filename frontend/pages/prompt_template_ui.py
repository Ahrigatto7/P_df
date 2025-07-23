# frontend/pages/prompt_template_ui.py
import streamlit as st
from core.prompt_templates import list_prompts, load_prompt, save_prompt


def render():
    st.header("PromptTemplate 관리/테스트")
    files = list_prompts()
    selected = st.selectbox("프롬프트 선택", files)
    if selected:
        content = load_prompt(selected)
        new_content = st.text_area("내용 편집", content, height=300)
        if st.button("저장"):
            save_prompt(selected, new_content)
            st.success("저장 완료!")

        st.markdown("---")
        st.subheader("프롬프트 테스트")
        context = st.text_area("테스트 context", "")
        question = st.text_input("테스트 question", "")
        if st.button("테스트 실행") and (context or question):
            st.write("샘플 실행 결과")

