import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import json

class Database:
    def __init__(self, db_path: str = "document_analyzer.db"):
        self.conn = sqlite3.connect(db_path)
        self.engine = create_engine(f"sqlite:///{db_path}")

    def load_csv(self, csv_path: str, table_name: str):
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, self.engine, if_exists="replace", index=False)

    def create_table_dynamic(self, df: pd.DataFrame, table_name: str):
        """
        JSON-serialize any list/dict columns, then write to SQLite.
        """
        df2 = df.copy()
        for col in df2.columns:
            df2[col] = df2[col].apply(
                lambda v: json.dumps(v) if isinstance(v, (list, dict)) else v
            )
        df2.to_sql(table_name, self.engine, if_exists="replace", index=False)

    def handle_schema_conflict(self, table_name: str) -> pd.DataFrame:
        """Inspect an existing table’s schema (if any)."""
        return pd.read_sql(f"PRAGMA table_info({table_name})", self.conn)

    def execute_query(self, query: str) -> pd.DataFrame:
        return pd.read_sql(query, self.conn)