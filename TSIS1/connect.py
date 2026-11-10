from pathlib import Path

import psycopg
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

BASE_DIR = Path(__file__).resolve().parent

def connect():
    return psycopg.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    )

def initialize_database():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute((BASE_DIR / "schema.sql").read_text(encoding="utf-8"), prepare=False)
        for filename in ("functions.sql", "procedures.sql"):
            cur.execute((BASE_DIR / filename).read_text(encoding="utf-8"), prepare=False)
        conn.commit()
        print("TSIS 1 database schema and SQL objects are ready.")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

# Compatibility names used by the inherited Practice 8 menu.
def create_table():
    initialize_database()

def install_sql_objects():
    initialize_database()
