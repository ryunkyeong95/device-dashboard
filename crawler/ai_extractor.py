import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_device_info_with_ai(article_text):
    prompt = f"""
아래 삼성 뉴스룸 기사 본문에서 신규 단말 정보를 추출해줘.

반드시 JSON만 반환해.
모르면 빈 문자열("")로 반환해.

필드:
- releaseDate: 출시일. 형식은 YYYY, YYYY-MM, YYYY-MM-DD 중 하나
- os: 운영체제. 예: Android 16
- screen: 화면 크기. 예: 6.7-inch
- type: Mobile 또는 Tablet

기사 본문:
{article_text[:8000]}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    text = response.output_text.strip()

    print("AI 원본 응답:")
    print(text)

    # ```json 제거
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)