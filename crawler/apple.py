import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_apple_articles():
    url = "https://www.apple.com/newsroom/rss-feed.rss"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml")

    entries = soup.find_all("entry")

    devices = []

    for entry in entries:
        title = entry.find("title").text.strip()
        content = entry.find("content").text.strip() if entry.find("content") else ""

        if not is_apple_device_article(title, content):
            continue

        model = extract_apple_model_name(title, content)

        if model is None:
            continue

        link_tag = entry.find("link")
        article_link = link_tag.get("href") if link_tag else ""

        id_tag = entry.find("id")
        article_id = id_tag.text.strip() if id_tag else article_link

        updated = entry.find("updated").text.strip() if entry.find("updated") else ""

        device = {
            "brand": "Apple",
            "type": "Mobile",
            "model": model,
            "title": title,
            "status": "Candidate",
            "releaseDate": "",
            "link": article_link,
            "source": "Apple RSS",
            "publishedAt": updated,
            "description": content,
            "articleId": article_id,
            "lastChecked": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        devices.append(device)

    return devices


def is_apple_device_article(title, content):
    text = f"{title} {content}".lower()

    device_keywords = [
        "iphone",
        "ipad"
    ]

    release_keywords = [
        "introduces",
        "unveils",
        "announces",
        "launches",
        "available"
    ]

    exclude_keywords = [
        "apple tv",
        "apple intelligence",
        "app store",
        "apple arcade",
        "developer",
        "siri",
        "mlb",
        "sports",
        "podcast",
        "services"
    ]

    has_device = any(word in text for word in device_keywords)
    has_release = any(word in text for word in release_keywords)
    has_exclude = any(word in text for word in exclude_keywords)

    return has_device and has_release and not has_exclude


def extract_apple_model_name(title, content):
    text = f"{title} {content}"

    patterns = [
        r"iPhone\s+\d+\s+Pro\s+Max",
        r"iPhone\s+\d+\s+Pro",
        r"iPhone\s+\d+",
        r"iPad\s+Pro",
        r"iPad\s+Air",
        r"iPad\s+mini",
        r"iPad"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group()

    return None