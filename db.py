import psycopg2

# PostgreSQLの接続情報
DB_NAME = "dx_data"
DB_USER = "matsuokaryo"  # Macのログインユーザーと同じ
DB_PASSWORD = ""  # 通常、ローカル環境なら空でOK
DB_HOST = "localhost"
DB_PORT = "5432"

# データベース接続
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("✅ PostgreSQLに接続成功！")
        return conn
    except Exception as e:
        print("❌ データベース接続エラー:", e)
        return None

# 接続テスト
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        conn.close()
