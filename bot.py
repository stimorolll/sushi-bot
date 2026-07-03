from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)

# === ЗМІННІ СЕРЕДОВИЩА (для Render) ===
TOKEN = os.getenv("8948678531:AAGPocItVNaxhjcSLl9TuC_mCJ9tzHaKMkw")
ADMIN_ID = int(os.getenv("740442241", 0))   # Якщо не вказано — 0

if not TOKEN:
    raise ValueError("BOT_TOKEN не знайдено в змінних середовища!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ====================== КОНТЕНТ ======================
content = {
    "kasir_complaints": {"text": "ЖАЛОБИ GOOGLE CHOICE\n\nТекст відсутній", "photo": None},
    "kasir_duties": {"text": "ОБОВ'ЯЗКИ\n\nТекст відсутній", "photo": None},
    "kasir_poster": {"text": "ПОСТЕР\n\nТекст відсутній", "photo": None},
    "kasir_orders": {"text": "ПРИЙОМ ЗАМОВЛЕНЬ\n\nТекст відсутній", "photo": None},
    "courier": {"text": "КУР'ЄРИ\n\nТекст відсутній", "photo": None},
    "logist": {"text": "ЛОГІСТ\n\nТекст відсутній", "photo": None},
    "sushi_instruction": {"text": "ІНСТРУКЦІЯ\n\nТекст відсутній", "photo": None},
    "sushi_internship": {"text": "СТАЖИРОВКА\n\nТекст відсутній", "photo": None},
    "manager_gen_cleaning": {"text": "ГЕНЕРАЛЬНЕ ПРИБИРАННЯ\n\nТекст відсутній", "photo": None},
    "manager_complaints": {"text": "ЖАЛОБИ\n\nТекст відсутній", "photo": None},
    "manager_instruction": {"text": "ІНСТРУКЦІЯ\n\nТекст відсутній", "photo": None},
    "manager_emergency": {"text": "НЕШТАТНІ СИТУАЦІЇ\n\nТекст відсутній", "photo": None},
    "manager_internship": {"text": "СТАЖИРОВКА\n\nТекст відсутній", "photo": None},
}

user_state = {}

# ====================== МЕНЮ ======================
def main_menu():
    kb = [
        [InlineKeyboardButton(text="👨‍💼 Касир", callback_data="role_kasir")],
        [InlineKeyboardButton(text="🚴 Кур'єри", callback_data="role_courier")],
        [InlineKeyboardButton(text="📦 Логіст", callback_data="role_logist")],
        [InlineKeyboardButton(text="🍣 Сушіст", callback_data="role_sushi")],
        [InlineKeyboardButton(text="👔 Управляючий", callback_data="role_manager")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👑 Адмін-панель активована", reply_markup=main_menu())
    else:
        await message.answer("👋 Ласкаво просимо!\nОберіть свою роль:", reply_markup=main_menu())

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    data = callback.data
    user_id = callback.from_user.id

    if data in ["role_kasir", "role_sushi", "role_manager"]:
        role = data.split("_")[1]
        user_state[user_id] = {"step": "password", "role": role}
        await callback.message.edit_text(f"🔐 Введіть пароль для доступу до **{role.upper()}**:")
        return

    if data in content:
        item = content[data]
        if item.get("photo"):
            await callback.message.answer_photo(item["photo"], caption=item["text"])
        else:
            await callback.message.answer(item["text"])

@dp.message()
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_state or user_state[user_id].get("step") != "password":
        return

    # Тимчасова перевірка пароля (можна розширити)
    await message.answer("✅ Доступ дозволено (тимчасово)")
    user_state.pop(user_id, None)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("🤖 Бот запущений на Webhook...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
