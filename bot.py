import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from fastapi import FastAPI, Request
import uvicorn

# Загружаем токен из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI()

# === Основная логика бота ===
@dp.message()
async def start(message: Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Задать вопрос", url="https://t.me/neatli_support")]
    ])
    await message.answer(
        "Здравствуйте! Нам очень приятно, что вы приобрели продукцию Neatli.\n\n"
        "Если у вас возникли вопросы, мы с радостью поможем их решить.\n"
        "Выберите интересующий вас вопрос из списка или напишите нам в канал поддержки.",
        reply_markup=keyboard
    )

# === FastAPI часть для webhook ===
@app.on_event("startup")
async def on_startup():
    # Укажи сюда URL, который Render выдаст (он будет вида https://<имя>.onrender.com)
    webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/webhook"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")

@app.post("/webhook")
async def process_webhook(request: Request):
    update = await request.json()
    await dp.feed_update(bot, update)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))