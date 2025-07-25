import os
from database import init_db, insert_document_with_keywords
from keyword_extractor import extract_keywords
from utils import read_file_content

DOCUMENTS_PATH = "documents"

def ingest_all_documents():
    init_db()
    for file in os.listdir(DOCUMENTS_PATH):
        full_path = os.path.join(DOCUMENTS_PATH, file)
        try:
            content = read_file_content(full_path)
            keywords = extract_keywords(content)
            insert_document_with_keywords(file, content, keywords)
            print(f"✅ {file} 저장 완료. 키워드: {keywords}")
        except Exception as e:
            print(f"❌ {file} 처리 실패: {e}")

if __name__ == "__main__":
    ingest_all_documents()
