import psycopg
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def connect():
    conn = psycopg.connect(
        dbname="suppliers_db",
        user="kumarkyzyajdana",
        password="0115",
        host="localhost",
        port=5432
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