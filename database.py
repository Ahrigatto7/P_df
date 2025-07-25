import sqlite3

def init_db(db_path="keywords.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE,
        content TEXT
    );

    CREATE TABLE IF NOT EXISTS keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS document_keywords (
        document_id INTEGER,
        keyword_id INTEGER,
        PRIMARY KEY (document_id, keyword_id),
        FOREIGN KEY (document_id) REFERENCES documents(id),
        FOREIGN KEY (keyword_id) REFERENCES keywords(id)
    );
    """)
    conn.commit()
    conn.close()

def insert_document_with_keywords(filename, content, keywords, db_path="keywords.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute("INSERT OR IGNORE INTO documents (filename, content) VALUES (?, ?)", (filename, content))
        cur.execute("SELECT id FROM documents WHERE filename = ?", (filename,))
        document_id = cur.fetchone()[0]

        for kw in keywords:
            cur.execute("INSERT OR IGNORE INTO keywords (keyword) VALUES (?)", (kw,))
            cur.execute("SELECT id FROM keywords WHERE keyword = ?", (kw,))
            keyword_id = cur.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO document_keywords (document_id, keyword_id) VALUES (?, ?)", (document_id, keyword_id))

        conn.commit()
    finally:
        conn.close()
