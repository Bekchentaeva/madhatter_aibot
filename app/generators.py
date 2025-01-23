import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('AI_TOKEN'))

async def gpt4(question, timeout=20):
    try:
        response = await asyncio.wait_for(
            client.chat.completions.create(
                messages=[{"role": "user", "content": str(question)}],
                model="gpt-4o"
            ),
            timeout=timeout  # Устанавливаем таймаут в секундах
        )
        return response
    except asyncio.TimeoutError:
        raise Exception("Запрос превысил время ожидания.")
