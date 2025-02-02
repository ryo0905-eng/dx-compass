from flask import Flask, request, jsonify
import psycopg2
from db import connect_db
import threading
from flask_cors import CORS

from update_data import update_data

import os


app = Flask(__name__)

CORS(app)  # すべてのリクエストを許可
DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    if not DATABASE_URL:
        raise ValueError("❌ DATABASE_URL が設定されていません！")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ PostgreSQL に接続成功")
        return conn
    except Exception as e:
        print(f"❌ データベース接続エラー: {e}")
        return None


def create_table():
    """テーブルがない場合に `dx_cases` を作成する"""
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
            industry TEXT,
            technology TEXT,
            company_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ `dx_cases` テーブルを作成または確認しました")

# アプリ起動時に `dx_cases` を作成
create_table()


# DX事例を検索するAPI
@app.route("/search", methods=["GET"])
def search_dx_cases():
    try:
        industry = request.args.get("industry", "")
        technology = request.args.get("technology", "")

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "データベース接続エラー"}), 500

        cur = conn.cursor()
        query = "SELECT title, industry, technology, company_name, url FROM dx_cases WHERE 1=1"
        params = []

        if industry:
            query += " AND industry = %s"
            params.append(industry)
        if technology:
            query += " AND technology LIKE %s"
            params.append(f"%{technology}%")

        cur.execute(query, tuple(params))
        cases = cur.fetchall()
        cur.close()
        conn.close()

        if not cases:
            return jsonify({"message": "データがありません"}), 200  # ✅ データがない場合の処理

        results = [{"title": c[0], "industry": c[1], "technology": c[2], "company": c[3], "url": c[4]} for c in cases]
        return jsonify(results)

    except Exception as e:
        print(f"❌ APIエラー: {e}")
        return jsonify({"error": "内部エラー", "details": str(e)}), 500  # ✅ エラーを JSON で返す



@app.route("/update", methods=["POST"])
def trigger_update():
    thread = threading.Thread(target=update_data)
    thread.start()
    return jsonify({"message": "データ更新が開始されました。"}), 202


@app.route("/")
def home():
    return "DX事例検索API is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderのポートを取得
    app.run(host="0.0.0.0", port=port, debug=False)  # 0.0.0.0 にバインド

