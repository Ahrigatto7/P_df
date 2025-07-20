import os
import pandas as pd
from sqlalchemy import create_engine


def connect_db(db_url: str = "sqlite:///app.db"):
    """Create a SQLAlchemy engine for the given database URL."""
    return create_engine(db_url)


def load_file_to_db(file_path: str, engine, table_name: str | None = None):
    """Load CSV, Excel or JSON file into a database table."""
    if table_name is None:
        table_name = os.path.splitext(os.path.basename(file_path))[0]

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file_path)
    elif file_path.endswith(".json"):
        df = pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file type")

    df.to_sql(table_name, engine, if_exists="replace", index=False)
    schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
    return {"table": table_name, "rows": len(df), "schema": schema}

