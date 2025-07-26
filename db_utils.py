import sqlite3
import pandas as pd

DB_PATH = "saju.db"


def init_saju_db(db_path: str = DB_PATH) -> None:
    """Initialize the Saju_CaseStudies table if it does not exist."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Saju_CaseStudies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            heavenly_stems TEXT,
            earthly_branches TEXT,
            five_elements TEXT,
            yongshin TEXT,
            explanation TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def fetch_all_cases() -> pd.DataFrame:
    """Return all case studies from the database as a DataFrame."""
    init_saju_db()
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM Saju_CaseStudies", conn)
    conn.close()
    return df


def fetch_case_by_id(case_id: int):
    """Return a single case study as a dictionary or ``None``."""
    init_saju_db()
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM Saju_CaseStudies WHERE id = ?",
        conn,
        params=(case_id,),
    )
    conn.close()
    return df.iloc[0].to_dict() if not df.empty else None
