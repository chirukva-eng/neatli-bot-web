import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import asyncio
import uvicorn

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://neatli-bot-web.onrender.com/webhook")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()


# === Вебхуки ===
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
    data = await request.json()
    update = types.Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}


@app.get("/")
async def root():
    return {"status": "running"}


# === Хэндлеры ===
@dp.message()
async def start_handler(message: types.Message):
    # Создаём кнопку с ссылкой на профиль Neatli
    neatli_button = InlineKeyboardButton(
        text="💬 Задать вопрос", url="https://neatli.com/tochka1084"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[neatli_button]])

    # Приветственное сообщение
    await message.answer(
        "👋 Привет! Я бот Neatli.\n\n"
        "Ты можешь задать мне вопрос, и я помогу тебе найти ответ.\n"
        "Нажми кнопку ниже, чтобы открыть чат на Neatli 👇",
        reply_markup=keyboard
    )


# === Точка входа ===
if __name__ == "__main__":
    print("🚀 Starting server on port 10000...")
    uvicorn.run("bot:app", host="0.0.0.0", port=10000)