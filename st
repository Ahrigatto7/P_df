
myproject_combined/
├── backend/
│   ├── api_router.py
│   ├── models.py           # 규칙/사례/용어/문서/히스토리
│   ├── crud.py
│   ├── vector_ops.py
│   ├── pdf_utils.py
│   ├── prompt_templates/
│   └── utils.py
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── vectorize_ui.py   # 업로드/임베딩 관리 (모든 타입)
│   │   ├── search_ui.py      # 검색/RAG QA
│   │   ├── edit_ui.py        # CRUD/히스토리 관리
│   │   ├── visualize_ui.py   # 관계망/통계 시각화
│   │   └── prompt_template_ui.py
├── vector_db/
├── data/
│   ├── master.json
│   ├── pdf_index.json
│   └── history.log
