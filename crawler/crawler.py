from samsung import get_samsung_articles
from firebase_service import upsert_device

devices = get_samsung_articles()

for device in devices:
    upsert_device(device)

print("삼성 RSS 수집 및 Firestore 저장 완료")