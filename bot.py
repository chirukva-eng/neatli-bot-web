import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://neatli-bot-web.onrender.com/webhook")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook установлен: {WEBHOOK_URL}")


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    print("🛑 Webhook удалён и сессия закрыта.")


@app.post("/webhook")
async def process_webhook(request: Request):
    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp._process_update(update)
    return {"ok": True}


@app.get("/")
async def root():
    return {"status": "running"}


# Пример простой команды
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Привет! Ты написал: {message.text}")


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting server on port 10000...")
    uvicorn.run("bot:app", host="0.0.0.0", port=10000)