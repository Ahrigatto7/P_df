from pathlib import Path
import pandas as pd
from sqlalchemy import text

from .db_utils import connect_db

SQL_FILE = Path(__file__).resolve().parent.parent / "data" / "book_1_keywords.sql"


def init_db(engine=None, db_url: str = "sqlite:///app.db"):
    """Initialize the database using the bundled SQL script."""
    if engine is None:
        engine = connect_db(db_url)
    with engine.begin() as conn:
        script = SQL_FILE.read_text(encoding="utf-8")
        conn.executescript(script) if hasattr(conn, 'executescript') else conn.execute(text(script))
    return engine


def load_terms(engine=None, db_url: str = "sqlite:///app.db") -> pd.DataFrame:
    """Load the term table as a pandas DataFrame."""
    if engine is None:
        engine = connect_db(db_url)
    return pd.read_sql_table("명리학_제압격국", engine)


def build_keyword_graph(df: pd.DataFrame):
    """Create a NetworkX graph from the DataFrame."""
    import networkx as nx

    G = nx.Graph()
    for _, row in df.iterrows():
        term = row["격국명"]
        G.add_node(term, category=row["격국분류"])
        keywords = [k.strip() for k in row["관련키워드"].split(',') if k.strip()]
        for kw in keywords:
            G.add_edge(term, kw)
    return G
