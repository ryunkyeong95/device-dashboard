import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred)

db = firestore.client()

print("Firebase 연결 성공!")

doc = {
    "brand": "삼성",
    "type": "태블릿",
    "model": "Galaxy Tab S11",
    "status": "출시 예정",
    "releaseDate": "2026-07-15",
    "link": "https://news.samsung.com/kr",
    "lastChecked": "2026-06-26",
    "createdAt": "2026-06-26",
    "updatedAt": "2026-06-26"
}

db.collection("devices").document("Galaxy Tab S11").set(doc)

print("Firestore 저장 성공!")

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