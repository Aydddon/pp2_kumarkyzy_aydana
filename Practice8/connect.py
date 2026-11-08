
from pathlib import Path

import psycopg
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def connect():
    conn = psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    print("Connected successfully!")
    return conn


def create_table():
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) UNIQUE NOT NULL
            );
        """)
        conn.commit()
        print("Contacts table is ready!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def install_sql_objects():
    """Create/update the functions and procedures stored beside this file."""
    base_dir = Path(__file__).resolve().parent
    conn = connect()
    cur = conn.cursor()
    try:
        for filename in ("functions.sql", "procedures.sql"):
            sql = (base_dir / filename).read_text(encoding="utf-8")
            cur.execute(sql, prepare=False)
        conn.commit()
        print("SQL functions and procedures are ready!")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
