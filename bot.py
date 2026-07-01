import telebot
from telebot import types
import os

TOKEN = '8948678531:AAGPocItVNaxhjcSLl9TuC_mCJ9tzHaKMkw'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 740442241   # ←←← ОБОВ'ЯЗКОВО ЗАМІНИ НА СВІЙ TELEGRAM ID

# Зберігання контенту
content = {
    "cashier_standards": {"text": "СТАНДАРТИ\n\nТекст відсутній", "photo": None, "video": None},
    "cashier_duties": {"text": "ОБОВ'ЯЗКИ\n\nТекст відсутній", "photo": None, "video": None},
    "sushi_standards": {"text": "СТАНДАРТИ\n\nТекст відсутній", "photo": None, "video": None},
    "sushi_duties": {"text": "ОБОВ'ЯЗКИ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_reports": {"text": "ЗВІТИ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_duties": {"text": "ОБОВ'ЯЗКИ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_responsibility": {"text": "ВІДПОВІДАЛЬНІСТЬ\n\nТекст відсутній", "photo": None, "video": None},
}

user_state = {}
ROLES = {
    "cashier": {"name": "Касир-пакувальник", "password": "1111"},
    "sushi": {"name": "Сушіст-заготовщик", "password": "2222"},
    "manager": {"name": "Керівний склад", "password": "1212"}
}

sections = {
    "cashier_standards": "Касир-пакувальник → Стандарти",
    "cashier_duties": "Касир-пакувальник → Обов'язки",
    "sushi_standards": "Сушіст-заготовщик → Стандарти",
    "sushi_duties": "Сушіст-заготовщик → Обов'язки",
    "manager_reports": "Керівний склад → Звіти",
    "manager_duties": "Керівний склад → Обов'язки",
    "manager_responsibility": "Керівний склад → Відповідальність"
}

# ====================== КЛАВІАТУРИ ======================
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("👨‍💼 Касир-пакувальник", callback_data="role_cashier"))
    markup.add(types.InlineKeyboardButton("🍣 Сушіст-заготовщик", callback_data="role_sushi"))
    markup.add(types.InlineKeyboardButton("👔 Керівний склад", callback_data="role_manager"))
    return markup

def admin_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("✏️ Редагувати контент", callback_data="admin_edit_content"))
    markup.add(types.InlineKeyboardButton("🏠 Головне меню", callback_data="main_menu"))
    return markup

def get_role_menu(role):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if role == "cashier":
        markup.add(types.InlineKeyboardButton("📋 Стандарти", callback_data="cashier_standards"))
        markup.add(types.InlineKeyboardButton("📋 Обов'язки", callback_data="cashier_duties"))
    elif role == "sushi":
        markup.add(types.InlineKeyboardButton("📋 Стандарти", callback_data="sushi_standards"))
        markup.add(types.InlineKeyboardButton("📋 Обов'язки", callback_data="sushi_duties"))
    elif role == "manager":
        markup.add(types.InlineKeyboardButton("📊 Звіти", callback_data="manager_reports"))
        markup.add(types.InlineKeyboardButton("📋 Обов'язки", callback_data="manager_duties"))
        markup.add(types.InlineKeyboardButton("⚖️ Відповідальність", callback_data="manager_responsibility"))
    markup.add(types.InlineKeyboardButton("🏠 На головну", callback_data="main_menu"))
    return markup

# ====================== START ======================
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👑 **АДМІН ПАНЕЛЬ**", parse_mode='Markdown')
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=admin_main_menu())
    else:
        bot.send_message(message.chat.id, "👋 Ласкаво просимо!\n\nОберіть свою роль:", reply_markup=main_menu())

# ====================== CALLBACK ======================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    data = call.data

    if data == "main_menu":
        if user_id == ADMIN_ID:
            bot.edit_message_text("Оберіть дію:", call.message.chat.id, call.message.message_id, reply_markup=admin_main_menu())
        else:
            bot.edit_message_text("Оберіть свою роль:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
        return

    # Адмін: вибір розділу для редагування
    if user_id == ADMIN_ID and data == "admin_edit_content":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, name in sections.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=f"edit_{key}"))
        bot.edit_message_text("Оберіть розділ для редагування:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        return

    # Адмін: вибрав розділ
    if user_id == ADMIN_ID and data.startswith("edit_"):
        section = data[5:]
        user_state[user_id] = {"action": "edit_section", "section": section}
        bot.edit_message_text(f"Редагуємо: **{sections[section]}**\n\nЩо хочете зробити?", 
                            call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Змінити текст", callback_data="change_text"))
        markup.add(types.InlineKeyboardButton("Завантажити фото", callback_data="change_photo"))
        markup.add(types.InlineKeyboardButton("Завантажити відео", callback_data="change_video"))
        markup.add(types.InlineKeyboardButton("Назад", callback_data="admin_edit_content"))
        bot.send_message(call.message.chat.id, "Оберіть дію:", reply_markup=markup)
        return

    # Режим редагування
    if user_id == ADMIN_ID and data in ["change_text", "change_photo", "change_video"]:
        section = user_state[user_id]["section"]
        user_state[user_id]["sub_action"] = data
        
        if data == "change_text":
            bot.send_message(call.message.chat.id, "Надішліть новий текст для цього розділу:")
        elif data == "change_photo":
            bot.send_message(call.message.chat.id, "Надішліть нове фото:")
        elif data == "change_video":
            bot.send_message(call.message.chat.id, "Надішліть нове відео:")
        return

    # Відображення контенту для звичайних користувачів
    if data in content:
        item = content[data]
        text = item["text"]
        
        try:
            if item["photo"]:
                bot.send_photo(call.message.chat.id, item["photo"], caption=text, parse_mode='Markdown')
            elif item["video"]:
                bot.send_video(call.message.chat.id, item["video"], caption=text, parse_mode='Markdown')
            else:
                bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        except:
            bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        
        role = user_state.get(user_id, {}).get("role")
        if role:
            bot.send_message(call.message.chat.id, "Оберіть дію:", reply_markup=get_role_menu(role))

# ====================== ОБРОБКА ПОВІДОМЛЕНЬ ======================
@bot.message_handler(content_types=['text', 'photo', 'video'])
def handle_content(message):
    user_id = message.from_user.id
    
    if user_id not in user_state:
        if user_id == ADMIN_ID:
            bot.send_message(message.chat.id, "Використовуйте кнопки адмін-панелі.")
        return

    state = user_state[user_id]

    if "sub_action" in state:
        section = state["section"]
        
        if state["sub_action"] == "change_text":
            content[section]["text"] = message.text
            bot.send_message(message.chat.id, "✅ Текст успішно оновлено!")
            
        elif state["sub_action"] == "change_photo" and message.photo:
            content[section]["photo"] = message.photo[-1].file_id
            content[section]["video"] = None
            bot.send_message(message.chat.id, "✅ Фото успішно завантажено!")
            
        elif state["sub_action"] == "change_video" and message.video:
            content[section]["video"] = message.video.file_id
            content[section]["photo"] = None
            bot.send_message(message.chat.id, "✅ Відео успішно завантажено!")
        
        # Повертаємо в меню редагування
        user_state[user_id] = {"action": "edit_section", "section": section}
        bot.send_message(message.chat.id, "Оберіть наступну дію:", reply_markup=types.InlineKeyboardMarkup())

# ====================== ЗАПУСК ======================
print("🤖 Бот з повною адмін-панеллю запущений...")
bot.infinity_polling()
