import os
import psycopg2

# Render の環境変数 `DATABASE_URL` を取得
DATABASE_URL = os.getenv("DATABASE_URL")

# データベース接続
def connect_db():
    if not DATABASE_URL:
        raise ValueError("❌ 環境変数 `DATABASE_URL` が設定されていません！")

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")  # ✅ SSLモードを有効化
        print("✅ PostgreSQL に接続成功！")
        return conn
    except Exception as e:
        print("❌ データベース接続エラー:", e)
        return None

# 接続テスト
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        conn.close()
