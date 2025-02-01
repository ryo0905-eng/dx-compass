import psycopg2
from db import connect_db

def insert_dx_case(title, url, summary, industry, technology, company_name):
    conn = connect_db()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO dx_cases (title, url, summary, industry, technology, company_name)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING;
        """, (title, url, summary, industry, technology, company_name))
        
        conn.commit()
        print(f"✅ データ保存成功: {title}")
    except Exception as e:
        print("❌ データ保存エラー:", e)
    finally:
        cur.close()
        conn.close()

# テスト用
if __name__ == "__main__":
    insert_dx_case(
        "製造業X社のDX成功事例",
        "https://example.com/dx-case",
        "製造業の生産効率向上のためのDX導入事例。",
        "製造業",
        "AI, IoT",
        "X社"
    )
