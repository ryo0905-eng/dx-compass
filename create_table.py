import psycopg2
from db import connect_db

def create_table():
    conn = connect_db()
    if conn is None:
        return

    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dx_cases (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            summary TEXT,
            industry TEXT,  -- 製造業、小売業など
            technology TEXT,  -- AI, RPA, IoTなど
            company_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ テーブル作成完了！")

if __name__ == "__main__":
    create_table()
