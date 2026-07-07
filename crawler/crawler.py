from samsung import get_samsung_articles
from device_processor import process_device

devices = get_samsung_articles()

for device in devices:
    process_device(device)

print("삼성 RSS 수집 및 Firestore 저장 완료")