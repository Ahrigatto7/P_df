import streamlit as st
import subprocess
import time

# FastAPI 백엔드 자동 실행 함수
def start_backend_if_needed():
    try:
        subprocess.Popen(
            ["uvicorn", "backend.api_router:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
    except Exception as e:
        print(f"❌ 백엔드 실행 실패: {e}")

# 백엔드 서버 실행 시도
start_backend_if_needed()

# Streamlit UI 설정
st.set_page_config(page_title="AI 데이터 QnA", layout="wide")
st.sidebar.title("메뉴")

menu = st.sidebar.radio(
    "이동", 
    ("문서 업로드/벡터화", "AI 검색(QA)", "프롬프트 관리", "CRUD/이력", "관계 시각화")
)

# 페이지별 라우팅
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
