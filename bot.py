import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# ====================== SETTINGS ======================
TOKEN = "9209359401:AAFKFvJmHbdQHcM-0aYjNIwqlsYIFH6bvoY"
WEBAPP_URL = "https://quiet-kitten-3e5b18.netlify.app"
# ======================================================

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔍 Open Analyzer",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]
    ])

    await message.answer(
        "👑 <b>King Thimbles Analyzer</b>\n\n"
        "Press the button below to open the mini application.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())