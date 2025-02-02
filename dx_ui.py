import streamlit as st
import requests

API_URL = "https://dx-compass.onrender.com"

st.title("🔍 DX事例検索")

industry = st.selectbox("業界を選択", ["", "製造業", "小売", "金融"])
technology = st.text_input("技術を入力（例: AI, RPA, IoT）")

if st.button("検索"):
    params = {}
    if industry:
        params["industry"] = industry
    if technology:
        params["technology"] = technology

    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()
        if results:
            for case in results:
                st.markdown(f"### [{case['title']}]({case['url']})")
                st.write(f"📌 **業界:** {case['industry']} | **技術:** {case['technology']} | **企業:** {case['company']}")
                st.write("---")
        else:
            st.warning("🔍 事例が見つかりませんでした。")
    else:
        st.error("❌ 検索エラーが発生しました。")

