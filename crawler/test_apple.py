from apple import get_apple_articles

devices = get_apple_articles()

print(f"\n총 {len(devices)}개 발견\n")

for device in devices:
    print("=" * 50)
    print(f"모델 : {device['model']}")
    print(f"제목 : {device['title']}")
    print(f"링크 : {device['link']}")