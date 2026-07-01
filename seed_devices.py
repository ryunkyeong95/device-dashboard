import re
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# crawler.py에서 쓰는 json 파일명과 같게 맞춰줘
cred = credentials.Certificate("crawler/serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

TODAY = datetime.now().strftime("%Y-%m-%d")


def make_doc_id(brand, model):
    text = f"{brand}_{model}".lower()
    text = re.sub(r"[^a-z0-9가-힣]+", "_", text)
    return text.strip("_")


def get_status(release_date):
    if release_date >= TODAY:
        return "출시예정"
    return "출시완료"


devices = [
    # Samsung
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy S25", "releaseDate": "2025-02-07"},
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy S25+", "releaseDate": "2025-02-07"},
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy S25 Ultra", "releaseDate": "2025-02-07"},
    {"brand": "Samsung", "type": "Tablet", "model": "Galaxy Tab S10 FE / FE+", "releaseDate": "2025-04-02"},
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy S25 Edge", "releaseDate": "2025-05-30"},
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy Z Fold7", "releaseDate": "2025-07-25"},
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy Z Flip7", "releaseDate": "2025-07-25"},
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy Z Flip7 FE", "releaseDate": "2025-07-25"},
    {"brand": "Samsung", "type": "Tablet", "model": "Galaxy Tab S11 Series", "releaseDate": "2025-09-04"},
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy S25 FE", "releaseDate": "2025-09-19"},
    {"brand": "Samsung", "type": "Tablet", "model": "Galaxy Tab A11+", "releaseDate": "2025-09-30"},
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy A17 5G", "releaseDate": "2025-12-30"},
    {"brand": "Samsung", "type": "Tablet", "model": "Galaxy Tab A11", "releaseDate": "2025-12-30"},
    {"brand": "Samsung", "type": "Mobile", "model": "Galaxy Z TriFold", "releaseDate": "2025-12-12"},
    {"brand": "Samsung", "type": "Tablet", "model": "Galaxy Tab S10 Lite", "releaseDate": "2025"},

    # Apple
    {"brand": "Apple", "type": "Tablet", "model": "iPad 11th generation", "releaseDate": "2025-03-12"},
    {"brand": "Apple", "type": "Mobile", "model": "iPhone 17", "releaseDate": "2025-09-19"},
    {"brand": "Apple", "type": "Mobile", "model": "iPhone 17 Pro", "releaseDate": "2025-09-19"},
    {"brand": "Apple", "type": "Mobile", "model": "iPhone 17 Pro Max", "releaseDate": "2025-09-19"},
    {"brand": "Apple", "type": "Mobile", "model": "iPhone Air", "releaseDate": "2025-09-19"},
    {"brand": "Apple", "type": "Tablet", "model": "iPad Pro M5", "releaseDate": "2025-10-15"},
    {"brand": "Apple", "type": "Tablet", "model": "iPad Air M4", "releaseDate": "2026-03-02"},
    {"brand": "Apple", "type": "Tablet", "model": "iPad Air M3", "releaseDate": "2025-03-12"},

    # Lenovo
    {"brand": "Lenovo", "type": "Tablet", "model": "Legion Y700 2025", "releaseDate": "2025"},
    {"brand": "Lenovo", "type": "Mobile", "model": "Legion Y70", "releaseDate": "2026-05-19"},
    {"brand": "Lenovo", "type": "Tablet", "model": "Legion Y900 2026 Edition", "releaseDate": "2026-05-19"},
    {"brand": "Lenovo", "type": "Tablet", "model": "Lenovo Tab Plus Gen 2", "releaseDate": "2026-06-16"},
    {"brand": "Lenovo", "type": "Tablet", "model": "Legion Y700 Gen 5", "releaseDate": "2026-06"},
]


for device in devices:
    doc_id = make_doc_id(device["brand"], device["model"])

    data = {
        **device,
        "title": device["model"],
        "status": get_status(device["releaseDate"]),
        "link": "",
        "source": "manual_seed",
        "publishedAt": "",
        "description": "",
        "articleId": doc_id,
        "lastChecked": TODAY,
        "updatedAt": TODAY,
    }

    db.collection("devices").document(doc_id).set(data, merge=True)
    print(f"저장 완료: {device['brand']} / {device['model']}")

print("seed 데이터 입력 완료")