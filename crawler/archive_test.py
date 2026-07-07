import requests
from bs4 import BeautifulSoup

url = "https://www.apple.com/newsroom/archive/iphone/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("상태코드:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

articles = soup.select("a")

print("링크 개수:", len(articles))

count = 0

for article in articles:
    text = article.get_text(" ", strip=True)

    if "iPhone" in text:
        print("=" * 50)
        print(text)
        print(article.get("href"))
        count += 1

print(f"\niPhone 기사 {count}개 발견")