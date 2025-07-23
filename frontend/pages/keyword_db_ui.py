import streamlit as st
from pyvis.network import Network
import tempfile

from core.saju_db import init_db, load_terms, build_keyword_graph
from core.db_utils import connect_db


def render():
    st.header("명리학 키워드 DB 관리")
    engine = connect_db()

    if st.button("DB 초기화 및 데이터 로드"):
        init_db(engine)
        st.success("데이터베이스가 초기화되었습니다.")

    if st.button("데이터 보기"):
        df = load_terms(engine)
        st.dataframe(df)

    if st.button("키워드 관계 그래프 보기"):
        df = load_terms(engine)
        graph = build_keyword_graph(df)
        net = Network(height="600px", notebook=False)
        net.from_nx(graph)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        net.save_graph(tmp.name)
        st.components.v1.html(open(tmp.name).read(), height=600)
