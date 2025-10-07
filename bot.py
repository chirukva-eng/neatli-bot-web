import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fastapi import FastAPI, Request
import uvicorn
from dotenv import load_dotenv

# Загружаем переменные окружения (BOT_TOKEN, WEBHOOK_URL)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN:
    raise ValueError("❌ Переменная BOT_TOKEN не установлена в окружении!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

app = FastAPI()

# --- Хэндлер команды /start ---
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    neatli_button = InlineKeyboardButton(
        text="💬 Задать вопрос",
        url="https://neatli.com/tochka1084"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[neatli_button]])

    await message.answer(
        "👋 Привет! Я бот Neatli.\n\n"
        "Ты можешь задать мне вопрос, и я помогу тебе найти ответ.\n"
        "Нажми кнопку ниже, чтобы открыть чат на Neatli 👇",
        reply_markup=keyboard
    )

# --- Webhook обработчик ---
@app.post("/webhook")
async def process_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

# --- Установка вебхука при запуске ---
@app.on_event("startup")
async def on_startup():
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Webhook установлен: {WEBHOOK_URL}")
    else:
        print("⚠️ WEBHOOK_URL не задан — бот не сможет получать обновления.")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("bot:app", host="0.0.0.0", port=port)