# 📄 문서 클러스터링 및 요약 프로젝트

이 프로젝트는 PDF, DOCX, TXT 형식의 문서를 자동으로 처리하여:

- 텍스트 추출
- 문서 벡터화 (Sentence Transformers)
- 클러스터링 (KMeans)
- 문서 및 클러스터 요약 (TF-IDF 기반)
- HTML 리포트 생성
- Streamlit 대시보드 제공

## 📁 폴더 구조
```
document_cluster_full_project/
│
├── documents/               # 샘플 문서들 (txt, docx, pdf)
├── document_clustering.ipynb # 전체 파이프라인 Jupyter 노트북
├── app.py                   # Streamlit 대시보드
├── pipeline.py              # 문서 처리 및 요약 코드
├── requirements.txt         # 의존성 목록
└── README.md                # 사용 설명서
```

## ⚙️ 설치 방법

```bash
pip install -r requirements.txt
```

## 🚀 실행 방법

### 1. Jupyter Notebook으로 실행
```bash
jupyter notebook document_clustering.ipynb
```

### 2. Streamlit 대시보드 실행
```bash
streamlit run app.py
```

## ✅ 주요 라이브러리
- sentence-transformers
- pymupdf
- python-docx
- scikit-learn
- streamlit
- plotly
- weasyprint