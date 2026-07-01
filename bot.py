import telebot
from telebot import types

TOKEN = '8948678531:AAGPocItVNaxhjcSLl9TuC_mCJ9tzHaKMkw'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 740442241   # ← ЗАМІНИ НА СВІЙ TELEGRAM ID

# Зберігання контенту
content = {
    "kasir_complaints": {"text": "ЖАЛОБИ GOOGLE CHOICE\n\nТекст відсутній", "photo": None, "video": None},
    "kasir_duties": {"text": "ОБОВ'ЯЗКИ КАСИРА\n\nТекст відсутній", "photo": None, "video": None},
    "kasir_poster": {"text": "ПОСТЕР\n\nТекст відсутній", "photo": None, "video": None},
    "kasir_orders": {"text": "ПРИЙОМ ЗАМОВЛЕНЬ\n\nТекст відсутній", "photo": None, "video": None},
    
    "courier": {"text": "КУР'ЄРИ\n\nТекст відсутній", "photo": None, "video": None},
    "logist": {"text": "ЛОГІСТ\n\nТекст відсутній", "photo": None, "video": None},
    
    "sushi_instruction": {"text": "ІНСТРУКЦІЯ СУШІСТА\n\nТекст відсутній", "photo": None, "video": None},
    "sushi_internship": {"text": "СТАЖИРОВКА СУШІСТА\n\nТекст відсутній", "photo": None, "video": None},
    
    "manager_gen_cleaning": {"text": "ГЕНЕРАЛЬНЕ ПРИБИРАННЯ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_complaints": {"text": "ЖАЛОБИ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_instruction": {"text": "ІНСТРУКЦІЯ КЕРІВНИКА\n\nТекст відсутній", "photo": None, "video": None},
    "manager_emergency": {"text": "НЕШТАТНІ СИТУАЦІЇ\n\nТекст відсутній", "photo": None, "video": None},
    "manager_internship": {"text": "СТАЖИРОВКА КЕРІВНИКА\n\nТекст відсутній", "photo": None, "video": None},
}

user_state = {}

ROLES = {
    "kasir": {"name": "Касир", "password": "1111"},
    "sushi": {"name": "Сушіст", "password": "2222"},
    "manager": {"name": "Управляючий", "password": "1212"}
}

# Головне меню
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("👨‍💼 Касир", callback_data="role_kasir"))
    markup.add(types.InlineKeyboardButton("🚴 Кур'єри", callback_data="role_courier"))
    markup.add(types.InlineKeyboardButton("📦 Логіст", callback_data="role_logist"))
    markup.add(types.InlineKeyboardButton("🍣 Сушіст", callback_data="role_sushi"))
    markup.add(types.InlineKeyboardButton("👔 Управляючий", callback_data="role_manager"))
    return markup

# Меню для кожної ролі
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

# Адмін меню (залишається)
def admin_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("✏️ Редагувати контент", callback_data="admin_edit_content"))
    markup.add(types.InlineKeyboardButton("🏠 Головне меню", callback_data="main_menu"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👑 **АДМІН ПАНЕЛЬ**", parse_mode='Markdown')
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=admin_main_menu())
    else:
        bot.send_message(message.chat.id, "👋 Ласкаво просимо!\n\nОберіть свою роль:", reply_markup=main_menu())

# Обробка кнопок (скорочена для зручності)
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

    # Ролі
    if data.startswith("role_"):
        role = data.split("_")[1]
        if role in ["kasir", "sushi", "manager"]:
            bot.edit_message_text(f"🔐 Введіть пароль для **{ROLES[role]['name']}**:", 
                                call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            user_state[user_id] = {"step": "waiting_password", "role": role}
        elif role == "courier":
            bot.send_message(call.message.chat.id, "🚴 **КУР'ЄРИ**", parse_mode='Markdown')
            bot.send_message(call.message.chat.id, content["courier"]["text"])
        elif role == "logist":
            bot.send_message(call.message.chat.id, "📦 **ЛОГІСТ**", parse_mode='Markdown')
            bot.send_message(call.message.chat.id, content["logist"]["text"])
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

# Обробка пароля
@bot.message_handler(func=lambda message: True)
def handle_password(message):
    user_id = message.from_user.id
    if user_id not in user_state or user_state[user_id].get("step") != "waiting_password":
        return

    role = user_state[user_id]["role"]
    if message.text.strip() == ROLES[role]["password"]:
        bot.send_message(message.chat.id, f"✅ Доступ дозволено! **{ROLES[role]['name']}**", parse_mode='Markdown')
        if role == "kasir":
            bot.send_message(message.chat.id, "Оберіть розділ:", reply_markup=kasir_menu())
        elif role == "sushi":
            bot.send_message(message.chat.id, "Оберіть розділ:", reply_markup=sushi_menu())
        elif role == "manager":
            bot.send_message(message.chat.id, "Оберіть розділ:", reply_markup=manager_menu())
    else:
        bot.send_message(message.chat.id, "❌ Неправильний пароль.")

print("🤖 Бот запущений...")
bot.infinity_polling()