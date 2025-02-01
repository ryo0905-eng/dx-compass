import time
import logging
from scrape_dx_news import scrape_pr_times

# ログの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def update_data():
    logging.info("🔄 DX事例のデータ更新を開始...")
    scrape_pr_times()
    logging.info("✅ DX事例のデータ更新が完了しました！")

if __name__ == "__main__":
    update_data()
