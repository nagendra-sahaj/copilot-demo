import duckdb
import pandas as pd
from shared.config import DB_PATH


def execute_sql(sql: str) -> tuple[pd.DataFrame, str | None]:
    stripped = sql.strip()
    if not stripped.upper().startswith("SELECT"):
        raise ValueError("Only SELECT statements are permitted.")

    conn = None
    try:
        conn = duckdb.connect(DB_PATH, read_only=True)
        df = conn.execute(sql).df()
        return df, None
    except Exception as exc:
        return pd.DataFrame(), str(exc)
    finally:
        if conn is not None:
            conn.close()
