import streamlit as st

st.set_page_config(page_title="AI 데이터 QnA", layout="wide")

st.sidebar.title("메뉴")
menu = st.sidebar.radio(
    "이동", 
    ("문서 업로드/벡터화", "AI 검색(QA)", "프롬프트 관리", "CRUD/이력", "관계 시각화")
)

if menu == "문서 업로드/벡터화":
    from pages import vectorize_ui
    vectorize_ui.render()
elif menu == "AI 검색(QA)":
    from pages import search_ui
    search_ui.render()
elif menu == "프롬프트 관리":
    from pages import prompt_template_ui
    prompt_template_ui.render()
elif menu == "CRUD/이력":
    from pages import edit_ui
    edit_ui.render()
elif menu == "관계 시각화":
    from pages import visualize_ui
    visualize_ui.render()