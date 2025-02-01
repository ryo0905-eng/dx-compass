import requests
from bs4 import BeautifulSoup
from save_data import insert_dx_case

# PR TIMESのDX関連ニュースURL
PR_TIMES_URL = "https://prtimes.jp/main/action.php?run=html&page=searchkey&search_word=DX%E4%BA%8B%E4%BE%8B"

def scrape_pr_times():
    print("🔍 PR TIMESからデータを取得開始...")
    response = requests.get(PR_TIMES_URL)

    if response.status_code != 200:
        print(f"❌ PR TIMESからデータを取得できませんでした。（ステータスコード: {response.status_code}）")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="release-card_article__No7uQ")

    print(f"📝 {len(articles)} 件のDX事例を取得")

    for article in articles[:5]:
        title = article.find("h3").get_text(strip=True) if article.find("h3") else "タイトルなし"
        url = article.find("a")["href"] if article.find("a") else "URLなし"
        summary = article.find("p").get_text(strip=True) if article.find("p") else "概要なし"

        print(f"✅ データ取得: {title} ({url})")
        insert_dx_case(title, url, summary, "未分類", "未分類", "不明")

if __name__ == "__main__":
    scrape_pr_times()
