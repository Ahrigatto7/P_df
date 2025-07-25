import unittest
import os
from database import init_db, insert_document_with_keywords
import sqlite3

DB_PATH = "test_keywords.db"

class TestDatabase(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db(DB_PATH)

    def test_insert_and_deduplication(self):
        content = "이것은 테스트 문서입니다."
        keywords = ["테스트", "문서"]
        insert_document_with_keywords("test1.txt", content, keywords, DB_PATH)
        insert_document_with_keywords("test1.txt", content, keywords, DB_PATH)  # 중복 삽입 방지 확인

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM documents")
        doc_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM keywords")
        kw_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM document_keywords")
        relation_count = cur.fetchone()[0]
        conn.close()

        self.assertEqual(doc_count, 1)
        self.assertEqual(kw_count, 2)
        self.assertEqual(relation_count, 2)

if __name__ == '__main__':
    unittest.main()
