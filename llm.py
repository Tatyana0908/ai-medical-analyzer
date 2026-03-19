import os
import json
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

MODEL = os.getenv("MODEL")

# Функция генерации промта. Задаем ограничения.
def build_prompt(data: dict) -> str:
    return f"""
Ты медицинский AI-ассистент.
Ты можешь только анализировать показатели и не можешь ставить диагнозы.

Данные анализа:
{json.dumps(data, ensure_ascii=False)}

Верни строго JSON:

{{
  "summary": "краткое описание",
  "abnormal_values": [
    {{
      "name": "показатель",
      "status": "low/high/normal",
      "possible_reasons": ["причина 1", "причина 2"]
    }}
  ],
  "recommendations": ["рекомендация"]
}}

Никакого текста вне JSON.
"""


def analyze_lab(data: dict, temperature: float):
    prompt = build_prompt(data)

    response = client.chat.completions.create(
        model=MODEL,
        temperature=temperature,
        max_tokens=500,
        extra_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Medical Analyzer"
        },
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    # попытка безопасного парсинга JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        import re
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("Модель не вернула валидный JSON")