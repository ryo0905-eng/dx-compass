import psycopg2
from db import connect_db

def fetch_dx_cases():
    conn = connect_db()
    if conn is None:
        return

    cur = conn.cursor()
    cur.execute("SELECT id, title, industry, technology, company_name FROM dx_cases;")
    cases = cur.fetchall()

    print("📌 DX事例一覧")
    for case in cases:
        print(f"🔹 {case[1]}（業界: {case[2]}, 技術: {case[3]}, 企業: {case[4]})")

    cur.close()
    conn.close()

# 実行
if __name__ == "__main__":
    fetch_dx_cases()
