# 📄 문서 클러스터링 및 요약 프로젝트

간단한 Streamlit 앱으로 PDF, DOCX, TXT 문서를 클러스터링하고 요약합니다. 별도의 백엔드 서버 없이 Streamlit만으로 실행할 수 있습니다.

## 📁 폴더 구조
```
document_cluster_full_project/
├── documents/               # 샘플 문서들
├── app.py                   # Streamlit 대시보드
├── pipeline.py              # 문서 처리 파이프라인
├── requirements.txt         # 의존성 목록
└── README.md                # 사용 설명서
```

## ⚙️ 설치
```bash
pip install -r requirements.txt
```

## 🚀 실행
```bash
streamlit run app.py
```

## ✅ 주요 라이브러리
- sentence-transformers
- scikit-learn
- streamlit
- PyPDF2
- python-docx
- pandas
- jinja2
