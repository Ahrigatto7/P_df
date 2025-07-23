import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.saju_db import init_db, load_terms
from core.db_utils import connect_db

def test_init_and_load(tmp_path):
    db_url = f"sqlite:///{tmp_path/'test.db'}"
    engine = connect_db(db_url)
    init_db(engine)
    df = load_terms(engine)
    assert len(df) == 12
