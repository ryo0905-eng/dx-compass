from flask import Flask, request, jsonify
import psycopg2
from db import connect_db
import threading
from update_data import update_data

import os

app = Flask(__name__)

# DX事例を検索するAPI
@app.route("/search", methods=["GET"])
def search_dx_cases():
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

    results = [{"title": c[0], "industry": c[1], "technology": c[2], "company": c[3], "url": c[4]} for c in cases]

    cur.close()
    conn.close()

    return jsonify(results)


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

