import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_article_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
        "Connection": "close",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30,
            verify=False
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(" ", strip=True)

    except Exception as e:
        print(f"기사 본문 가져오기 실패: {e}")
        return ""