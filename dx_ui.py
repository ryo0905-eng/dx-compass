import streamlit as st
import requests

API_URL = "https://dx-compass.onrender.com/search"

st.title("🔍 DX事例検索")

industry = st.selectbox("業界を選択", ["", "製造業", "小売", "金融"])
technology = st.text_input("技術を入力（例: AI, RPA, IoT）")

if st.button("検索"):
    params = {}
    if industry:
        params["industry"] = industry
    if technology:
        params["technology"] = technology

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # ✅ HTTPエラーをキャッチ

        if response.status_code == 200:
            try:
                results = response.json()
                if "error" in results:
                    st.error(f"❌ APIエラー: {results['error']}")
                elif "message" in results:
                    st.warning("⚠️ データがありません")
                else:
                    for case in results:
                        st.markdown(f"### [{case['title']}]({case['url']})")
                        st.write(f"📌 **業界:** {case['industry']} | **技術:** {case['technology']} | **企業:** {case['company']}")
                        st.write("---")
            except requests.exceptions.JSONDecodeError:
                st.error("❌ APIのレスポンスが不正です")
        else:
            st.error(f"❌ APIエラー: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ ネットワークエラー: {e}")
