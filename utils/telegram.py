import httpx

BOT_TOKEN = "7029428302:AAGa9ZRQzunA29-CGsTtH8hFo7ZxwUMP46s"
CHAT_ID = "5846405605"

async def send_to_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    async with httpx.AsyncClient() as client:
        await client.post(url, data=payload)
