import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

cred = credentials.Certificate(BASE_DIR / "serviceAccountKey.json")

firebase_admin.initialize_app(cred)

db = firestore.client()

print("Firebase 연결 성공!")


def get_device(model):
    return db.collection("devices").document(model).get()

def save_device(device):
    model = device["model"]
    db.collection("devices").document(model).set(device)
    print(f"{model} 저장 완료")

def upsert_device(device):
    model = device["model"]
    existing = get_device(model)

    if existing.exists:
        db.collection("devices").document(model).update({
            "os": device.get("os", ""),
            "screen": device.get("screen", ""),
            "type": device.get("type", ""),
            "releaseDate": device["releaseDate"],
            "status": device["status"],
            "link": device["link"],
            "lastChecked": device["lastChecked"],
            "source": device["source"],
            "publishedAt": device["publishedAt"],
            "description": device["description"],
            "articleId": device["articleId"],
            "updatedAt": device["updatedAt"]
        })
        print(f"{model} 업데이트 완료")
    else:
        save_device(device)