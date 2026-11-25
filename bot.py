import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus

TOKEN = os.getenv("TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def subscribe_keyboard():
    channel_username = CHANNEL_ID.replace("@", "") if CHANNEL_ID.startswith("@") else None
    buttons = []
    
    if channel_username:
        buttons.append([
            InlineKeyboardButton(
                text="📢 Subscribe to Channel",
                url=f"https://t.me/{channel_username}"
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(
            text="✅ I Subscribed",
            callback_data="check_sub"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def analyzer_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔍 Open Analyzer",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]
    ])

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
    except Exception:
        return False

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    if await is_subscribed(message.from_user.id):
        await message.answer(
            "👑 <b>King Thimbles Analyzer</b>\n\n"
            "You are subscribed. Press the button below to open the analyzer.",
            reply_markup=analyzer_keyboard(),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "🔒 <b>Access Restricted</b>\n\n"
            "To use the analyzer, you must subscribe to our channel first.",
            reply_markup=subscribe_keyboard(),
            parse_mode="HTML"
        )

@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id):
        await callback.message.edit_text(
            "👑 <b>King Thimbles Analyzer</b>\n\n"
            "✅ Subscription confirmed!\n\n"
            "Press the button below to open the analyzer.",
            reply_markup=analyzer_keyboard(),
            parse_mode="HTML"
        )
    else:
        await callback.answer("You are not subscribed yet!", show_alert=True)

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())