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