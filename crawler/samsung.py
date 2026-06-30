import re
import requests
from bs4 import BeautifulSoup
from datetime import date
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_test_devices():
    today = date.today().isoformat()

    return [
        {
            "brand": "삼성",
            "type": "태블릿",
            "model": "Galaxy Tab S11",
            "status": "출시 예정",
            "releaseDate": "2026-07-15",
            "link": "https://news.samsung.com/kr",
            "lastChecked": today,
            "createdAt": today,
            "updatedAt": today
        },
        {
            "brand": "삼성",
            "type": "모바일",
            "model": "Galaxy S26",
            "status": "출시 예정",
            "releaseDate": "2026-08-01",
            "link": "https://news.samsung.com/kr",
            "lastChecked": today,
            "createdAt": today,
            "updatedAt": today
        }
    ]

def test_html():
    url = "https://news.samsung.com/global/feed"

    response = requests.get(url, verify=False)

    print(response.status_code)

    soup = BeautifulSoup(response.text, "xml")

    print(soup.title.text)

    items = soup.find_all("item")

    print(len(items))

    first_item = items[0]

    print(first_item.find("title").text)
    print(first_item)


def get_samsung_articles():
    url = "https://news.samsung.com/global/feed"

    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, "xml")

    items = soup.find_all("item")

    devices = []

    keywords = [
        "Galaxy A",
        "Galaxy Z",
        "Galaxy Tab",
        "Fold",
        "Flip"
        ]

    exclude_keywords = [
        "One UI",
        "Beta",
        "Watch",
        "Buds",
        "XR"
    ]

    for item in items:
        title = item.find("title").text

        if any(keyword.lower() in title.lower() for keyword in keywords):

            model = extract_model_name(title)
            if model is None:
                continue

            guid = item.find("guid")

            article_id = guid.text if guid else ""

            pub_date = item.find("pubDate").text

            description = item.find("description").text if item.find("description") else ""

            is_new_release = is_release_candidate(title, description)

            device = {
                "brand": "Samsung",
                "type": "Mobile",
                "model": model,
                "title": title,
                "status": "출시 예정" if is_new_release else "후보",
                "releaseDate": "",
                "link": guid.text if guid else "",
                "source": "Samsung RSS",
                "publishedAt": pub_date,
                "description": description,
                "articleId": article_id,
                "lastChecked": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

            devices.append(device)

    return devices

def extract_model_name(title):
    pattern = r"Galaxy\s+(A|S)\d+"

    match = re.search(pattern, title)

    if match:
        return match.group()

    return None

def is_release_candidate(title, description):
    text = f"{title} {description}".lower()

    include_words = [
        "announced",
        "introduces",
        "launches",
        "brings"
    ]

    exclude_words = [
        "one ui",
        "beta",
        "watch",
        "buds",
        "xr",
        "study",
        "research"
    ]

    has_include = any(word in text for word in include_words)
    matched_excludes = [word for word in exclude_words if word in text]

    print("matched exclude:", matched_excludes)

    has_exclude = len(matched_excludes) > 0

    return has_include and not has_exclude