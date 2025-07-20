import streamlit as st
from your_util_module import start_backend_if_needed  # 또는 코드 그대로 붙여넣기

start_backend_if_needed()
st.set_page_config(page_title="AI 데이터 QnA", layout="wide")

st.sidebar.title("메뉴")
menu = st.sidebar.radio(
    "이동", 
    ("문서 업로드/벡터화", "AI 검색(QA)", "프롬프트 관리", "CRUD/이력", "관계 시각화")
)

if menu == "문서 업로드/벡터화":
    try:
        from pages import vectorize_ui
        vectorize_ui.render()
    except Exception as e:
        st.error(f"vectorize_ui 오류: {e}")
elif menu == "AI 검색(QA)":
    try:
        from pages import search_ui
        search_ui.render()
    except Exception as e:
        st.error(f"search_ui 오류: {e}")
elif menu == "프롬프트 관리":
    try:
        from pages import prompt_template_ui
        prompt_template_ui.render()
    except Exception as e:
        st.error(f"prompt_template_ui 오류: {e}")
elif menu == "관계 시각화":
    try:
        from pages import visualize_ui
        visualize_ui.render()
    except Exception as e:
        st.error(f"visualize_ui 오류: {e}")
