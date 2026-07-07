from datetime import datetime

from article_parser import get_article_text
from ai_extractor import extract_device_info_with_ai
from firebase_service import upsert_device


def process_device(device):
    """
    기사 본문 추출 → AI 분석 → 상태 계산 → Firestore 저장
    """

    print(f"\n기사 링크: {device['link']}")

    # 기사 본문 가져오기
    article_text = get_article_text(device["link"])

    # AI 분석
    ai_info = extract_device_info_with_ai(article_text)

    print("AI 추출 결과:", ai_info)

    # AI 결과 저장
    device["releaseDate"] = ai_info.get("releaseDate", "")
    device["os"] = ai_info.get("os", "")
    device["screen"] = ai_info.get("screen", "")

    if ai_info.get("type"):
        device["type"] = ai_info.get("type")

    # 출시 상태 계산
    release_date = device.get("releaseDate", "")

    if release_date:
        try:
            release = datetime.strptime(release_date, "%Y-%m-%d").date()

            if release > datetime.today().date():
                device["status"] = "Upcoming"
            else:
                device["status"] = "Released"

        except Exception:
            device["status"] = "Unknown"
    else:
        device["status"] = "Unknown"

    # Firestore 저장
    upsert_device(device)