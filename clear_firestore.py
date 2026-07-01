import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("crawler/serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

docs = db.collection("devices").stream()

count = 0

for doc in docs:
    print(f"삭제 : {doc.id}")
    doc.reference.delete()
    count += 1

print(f"\n총 {count}개 삭제 완료!")