import telebot
from telebot import types

TOKEN = '8948678531:AAGPocItVNaxhjcSLl9TuC_mCJ9tzHaKMkw'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 740442241   # ← ЗАМІНИ НА СВІЙ TELEGRAM ID

# Контент усіх розділів
content = {
    "kasir_complaints": {"text": "ЖАЛОБИ GOOGLE CHOICE\n\nТекст відсутній", "photo": None, "video": None},
    "kasir_duties": {"text": "ОБОВ'ЯЗКИ КАСИРА\n\nТекст відсутній", "photo": None, "video": None},
    "kasir_poster": {"text": "ПОСТЕР\n\nТекст відсутній", "photo": None, "video": None},
    "kasir_orders": {"text": "ПРИЙОМ ЗАМОВЛЕНЬ\n\nТекст відсутній", "photo": None, "video": None},
    
    "courier": {"text": "КУР'ЄРИ\n\nТекст відсутній", "photo": None, "video": None},
    "logist": {"text": "ЛОГІСТ\n\nТекст відсутній", "photo": None, "video": None},
    
    "sushi_instruction": {"text": "ІНСТРУКЦІЯ\n\nТекст відсутній", "photo": None, "video": None},
    "sushi_internship": {"text": "СТАЖИРОВКА\n\nТекст відсутній", "photo": None, "video": None},
    
    "manager_gen_cleaning": {"text": "ГЕНЕРАЛЬНЕ ПРИБИРАННЯ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_complaints": {"text": "ЖАЛОБИ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_instruction": {"text": "ІНСТРУКЦІЯ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_emergency": {"text": "НЕШТАТНІ СИТУАЦІЇ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_internship": {"text": "СТАЖИРОВКА\n\nТекст відсутній", "photo": None, "video": None},
}

user_state = {}

ROLES = {
    "kasir": {"name": "Касир", "password": "1111"},
    "sushi": {"name": "Сушіст", "password": "2222"},
    "manager": {"name": "Управляючий", "password": "1212"}
}

# Назви розділів для адміна
sections = {
    "kasir_complaints": "Касир → Жалобы Google Choice",
    "kasir_duties": "Касир → Обов'язки",
    "kasir_poster": "Касир → Постер",
    "kasir_orders": "Касир → Прийом замовлень",
    "courier": "Кур'єри",
    "logist": "Логіст",
    "sushi_instruction": "Сушіст → Інструкція",
    "sushi_internship": "Сушіст → Стажировка",
    "manager_gen_cleaning": "Управляючий → Ген. Уборка",
    "manager_complaints": "Управляючий → Жалобы",
    "manager_instruction": "Управляючий → Інструкція",
    "manager_emergency": "Управляючий → Нештатні ситуації",
    "manager_internship": "Управляючий → Стажировка"
}

# ==================== МЕНЮ ====================
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("👨‍💼 Касир", callback_data="role_kasir"))
    markup.add(types.InlineKeyboardButton("🚴 Кур'єри", callback_data="role_courier"))
    markup.add(types.InlineKeyboardButton("📦 Логіст", callback_data="role_logist"))
    markup.add(types.InlineKeyboardButton("🍣 Сушіст", callback_data="role_sushi"))
    markup.add(types.InlineKeyboardButton("👔 Управляючий", callback_data="role_manager"))
    return markup

def kasir_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Жалобы Google Choice", callback_data="kasir_complaints"))
    markup.add(types.InlineKeyboardButton("Обов'язки", callback_data="kasir_duties"))
    markup.add(types.InlineKeyboardButton("Постер", callback_data="kasir_poster"))
    markup.add(types.InlineKeyboardButton("Прийом замовлень", callback_data="kasir_orders"))
    markup.add(types.InlineKeyboardButton("🏠 На головну", callback_data="main_menu"))
    return markup

def sushi_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Інструкція", callback_data="sushi_instruction"))
    markup.add(types.InlineKeyboardButton("Стажировка", callback_data="sushi_internship"))
    markup.add(types.InlineKeyboardButton("🏠 На головну", callback_data="main_menu"))
    return markup

def manager_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Ген. Уборка", callback_data="manager_gen_cleaning"))
    markup.add(types.InlineKeyboardButton("Жалобы", callback_data="manager_complaints"))
    markup.add(types.InlineKeyboardButton("Інструкція", callback_data="manager_instruction"))
    markup.add(types.InlineKeyboardButton("Нештатні ситуації", callback_data="manager_emergency"))
    markup.add(types.InlineKeyboardButton("Стажировка", callback_data="manager_internship"))
    markup.add(types.InlineKeyboardButton("🏠 На головну", callback_data="main_menu"))
    return markup

def admin_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("✏️ Редагувати контент", callback_data="admin_edit_content"))
    markup.add(types.InlineKeyboardButton("🏠 Головне меню", callback_data="main_menu"))
    return markup

# ==================== START ====================
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👑 **АДМІН ПАНЕЛЬ**", parse_mode='Markdown')
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=admin_main_menu())
    else:
        bot.send_message(message.chat.id, "👋 Ласкаво просимо!\n\nОберіть свою роль:", reply_markup=main_menu())

# ==================== CALLBACK ====================
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

    # Адмін панель
    if user_id == ADMIN_ID and data == "admin_edit_content":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, name in sections.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=f"edit_{key}"))
        bot.edit_message_text("Оберіть розділ для редагування:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        return

    # Адмін обрав розділ
    if user_id == ADMIN_ID and data.startswith("edit_"):
        section = data[5:]
        user_state[user_id] = {"action": "edit_section", "section": section}
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Змінити текст", callback_data="change_text"))
        markup.add(types.InlineKeyboardButton("Завантажити фото", callback_data="change_photo"))
        markup.add(types.InlineKeyboardButton("Завантажити відео", callback_data="change_video"))
        markup.add(types.InlineKeyboardButton("Назад", callback_data="admin_edit_content"))
        bot.edit_message_text(f"Редагуємо:\n**{sections[section]}**", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        bot.send_message(call.message.chat.id, "Що хочете зробити?", reply_markup=markup)
        return

    # Режим редагування
    if user_id == ADMIN_ID and data in ["change_text", "change_photo", "change_video"]:
        user_state[user_id]["sub_action"] = data
        if data == "change_text":
            bot.send_message(call.message.chat.id, "Надішліть новий текст:")
        elif data == "change_photo":
            bot.send_message(call.message.chat.id, "Надішліть нове фото:")
        elif data == "change_video":
            bot.send_message(call.message.chat.id, "Надішліть нове відео:")
        return

    # Відображення контенту
    if data in content:
        item = content[data]
        text = item["text"]
        if item["photo"]:
            bot.send_photo(call.message.chat.id, item["photo"], caption=text, parse_mode='Markdown')
        elif item["video"]:
            bot.send_video(call.message.chat.id, item["video"], caption=text, parse_mode='Markdown')
        else:
            bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    # Ролі без пароля
    if data == "role_courier":
        bot.send_message(call.message.chat.id, "🚴 **КУР'ЄРИ**", parse_mode='Markdown')
        bot.send_message(call.message.chat.id, content["courier"]["text"])
    if data == "role_logist":
        bot.send_message(call.message.chat.id, "📦 **ЛОГІСТ**", parse_mode='Markdown')
        bot.send_message(call.message.chat.id, content["logist"]["text"])

# ==================== ОБРОБКА ПОВІДОМЛЕНЬ ====================
@bot.message_handler(content_types=['text', 'photo', 'video'])
def handle_content(message):
    user_id = message.from_user.id
    if user_id not in user_state or "sub_action" not in user_state[user_id]:
        return

    state = user_state[user_id]
    section = state["section"]

    if state["sub_action"] == "change_text":
        content[section]["text"] = message.text
        bot.send_message(message.chat.id, "✅ Текст оновлено!")
    elif state["sub_action"] == "change_photo" and message.photo:
        content[section]["photo"] = message.photo[-1].file_id
        content[section]["video"] = None
        bot.send_message(message.chat.id, "✅ Фото завантажено!")
    elif state["sub_action"] == "change_video" and message.video:
        content[section]["video"] = message.video.file_id
        content[section]["photo"] = None
        bot.send_message(message.chat.id, "✅ Відео завантажено!")

    # Повернення в меню редагування
    user_state[user_id] = {"action": "edit_section", "section": section}

# Обробка пароля
@bot.message_handler(func=lambda message: True)
def handle_password(message):
    user_id = message.from_user.id
    if user_id not in user_state or user_state[user_id].get("step") != "waiting_password":
        return

    role = user_state[user_id]["role"]
    if message.text.strip() == ROLES[role]["password"]:
        bot.send_message(message.chat.id, f"✅ Доступ дозволено!\n**{ROLES[role]['name']}**", parse_mode='Markdown')
        if role == "kasir":
            bot.send_message(message.chat.id, "Оберіть розділ:", reply_markup=kasir_menu())
        elif role == "sushi":
            bot.send_message(message.chat.id, "Оберіть розділ:", reply_markup=sushi_menu())
        elif role == "manager":
            bot.send_message(message.chat.id, "Оберіть розділ:", reply_markup=manager_menu())
    else:
        bot.send_message(message.chat.id, "❌ Неправильний пароль.")

print("🤖 Бот з адмін-панеллю запущений...")
bot.infinity_polling()