import os
import threading
from flask import Flask
import telebot
from telebot import types
from supabase import create_client, Client

# === ФЕЙКОВЫЙ ВЕБ-СЕРВЕР ДЛЯ RENDER ===
app = Flask('')

@app.route('/')
def home():
    return "Бот запущен и Supabase подключен!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# === НАСТРОЙКА БОТА И SUPABASE ===
TOKEN = os.environ.get('BOT_TOKEN')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not TOKEN:
    raise ValueError("ОШИБКА: Переменная BOT_TOKEN не задана!")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("ОШИБКА: Переменные SUPABASE_URL или SUPABASE_KEY не заданы!")

bot = telebot.TeleBot(TOKEN)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_ID = 740442241   # Твой ID

# --- РАБОТА С SUPABASE ---
def init_db():
    """Проверяет базу и заполняет дефолтными значениями, если пустая"""
    default_content = {
        "kasir_complaints": "ЖАЛОБИ GOOGLE CHOICE\n\nТекст відсутній",
        "kasir_duties": "ОБОВ'ЯЗКИ КАСИРА\n\nТекст відсутній",
        "kasir_poster": "ПОСТЕР\n\nТекст відсутній",
        "kasir_orders": "ПРИЙОМ ЗАМОВЛЕНЬ\n\nТекст відсутній",
        "courier": "КУР'ЄРИ\n\nТекст відсутній",
        "logist": "ЛОГІСТ\n\nТекст відсутній",
        "sushi_instruction": "ІНСТРУКЦІЯ\n\nТекст відсутній",
        "sushi_internship": "СТАЖИРОВКА\n\nТекст відсутній",
        "manager_gen_cleaning": "ГЕНЕРАЛЬНЕ ПРИБИРАННЯ\n\nТекст відсутній",
        "manager_complaints": "ЖАЛОБИ\n\nТекст відсутній",
        "manager_instruction": "ІНСТРУКЦІЯ\n\nТекст відсутній",
        "manager_emergency": "НЕШТАТНІ СИТУАЦІЇ\n\nТекст відсутній",
        "manager_internship": "СТАЖИРОВКА\n\nТекст відсутній"
    }
    
    try:
        response = supabase.table("bot_content").select("count", count="exact").execute()
        if response.count == 0:
            for key, text in default_content.items():
                supabase.table("bot_content").insert({
                    "section_key": key, "text": text, "photo": None, "video": None
                }).execute()
            print("База данных Supabase успешно инициализирована базовыми текстами.")
    except Exception as e:
        print(f"⚠️ Ошибка инициализации (убедись, что таблица создана через SQL Editor): {e}")

def load_content(key):
    """Загружает контент секции из Supabase"""
    try:
        response = supabase.table("bot_content").select("text, photo, video").eq("section_key", key).execute()
        if response.data:
            row = response.data[0]
            return {"text": row["text"], "photo": row["photo"], "video": row["video"]}
    except Exception as e:
        print(f"Ошибка загрузки секции {key}: {e}")
    return {"text": "Текст відсутній", "photo": None, "video": None}

def update_content(key, text=None, photo=None, video=None):
    """Обновляет данные в Supabase"""
    update_data = {}
    if text is not None:
        update_data["text"] = text
    elif photo is not None:
        update_data["photo"] = photo
        update_data["video"] = None
    elif video is not None:
        update_data["video"] = video
        update_data["photo"] = None
        
    try:
        supabase.table("bot_content").update(update_data).eq("section_key", key).execute()
    except Exception as e:
        print(f"Ошибка обновления базы данных: {e}")

# --- СТРУКТУРА ДАННЫХ И МЕНЮ ---
user_state = {}
ROLES = {
    "kasir": {"name": "Касир", "password": "1111"},
    "sushi": {"name": "Сушіст", "password": "2222"},
    "manager": {"name": "Управляючий", "password": "1212"}
}
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

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("👨‍💼 Касир", callback_data="role_kasir"),
               types.InlineKeyboardButton("🚴 Кур'єри", callback_data="role_courier"),
               types.InlineKeyboardButton("📦 Логіст", callback_data="role_logist"),
               types.InlineKeyboardButton("🍣 Сушіст", callback_data="role_sushi"),
               types.InlineKeyboardButton("👔 Управляючий", callback_data="role_manager"))
    return markup

def kasir_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Жалобы Google Choice", callback_data="kasir_complaints"),
               types.InlineKeyboardButton("Обов'язки", callback_data="kasir_duties"),
               types.InlineKeyboardButton("Постер", callback_data="kasir_poster"),
               types.InlineKeyboardButton("Прийом замовлень", callback_data="kasir_orders"),
               types.InlineKeyboardButton("🏠 На головну", callback_data="main_menu"))
    return markup

def sushi_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Інструкція", callback_data="sushi_instruction"),
               types.InlineKeyboardButton("Стажировка", callback_data="sushi_internship"),
               types.InlineKeyboardButton("🏠 На головну", callback_data="main_menu"))
    return markup

def manager_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Ген. Уборка", callback_data="manager_gen_cleaning"),
               types.InlineKeyboardButton("Жалобы", callback_data="manager_complaints"),
               types.InlineKeyboardButton("Інструкція", callback_data="manager_instruction"),
               types.InlineKeyboardButton("Нештатні ситуації", callback_data="manager_emergency"),
               types.InlineKeyboardButton("Стажировка", callback_data="manager_internship"),
               types.InlineKeyboardButton("🏠 На головну", callback_data="main_menu"))
    return markup

def admin_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("✏️ Редагувати контент", callback_data="admin_edit_content"),
               types.InlineKeyboardButton("🏠 Головне меню", callback_data="main_menu"))
    return markup

# --- ХЕНДЛЕРЫ БОТА ---
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👑 **АДМІН ПАНЕЛЬ**", parse_mode='Markdown')
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=admin_main_menu())
    else:
        bot.send_message(message.chat.id, "👋 Ласкаво просимо!\n\nОберіть свою роль:", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    data = call.data

    if data == "main_menu":
        if user_id == ADMIN_ID:
            bot.edit_message_text("Оберіть дію:", call.message.chat.id, call.message.message_id, reply_markup=admin_main_menu())
        else:
            bot.edit_message_text("Оберіть свою роль:", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
        user_state.pop(user_id, None)
        return

    if data in ["role_kasir", "role_sushi", "role_manager"]:
        role_key = data.split("_")[1]
        bot.edit_message_text(f"🔐 Введіть пароль для **{ROLES[role_key]['name']}**:", 
                            call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        user_state[user_id] = {"step": "waiting_password", "role": role_key}
        return

    if data in ["role_courier", "role_logist"]:
        key = "courier" if data == "role_courier" else "logist"
        item = load_content(key)
        if item.get("photo"):
            bot.send_photo(call.message.chat.id, item["photo"], caption=item["text"], parse_mode='Markdown')
        elif item.get("video"):
            bot.send_video(call.message.chat.id, item["video"], caption=item["text"], parse_mode='Markdown')
        else:
            bot.send_message(call.message.chat.id, item["text"], parse_mode='Markdown')
        return

    if user_id == ADMIN_ID and data == "admin_edit_content":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, name in sections.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=f"edit_{key}"))
        bot.edit_message_text("Оберіть розділ:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        return

    if user_id == ADMIN_ID and data.startswith("edit_"):
        section = data[5:]
        user_state[user_id] = {"action": "edit_section", "section": section}
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Змінити текст", callback_data="change_text"),
                   types.InlineKeyboardButton("Завантажити фото", callback_data="change_photo"),
                   types.InlineKeyboardButton("Завантажити відео", callback_data="change_video"),
                   types.InlineKeyboardButton("Назад", callback_data="admin_edit_content"))
        bot.edit_message_text(f"Редагуємо:\n**{sections[section]}**", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        bot.send_message(call.message.chat.id, "Оберіть дію:", reply_markup=markup)
        return

    if user_id == ADMIN_ID and data in ["change_text", "change_photo", "change_video"]:
        user_state[user_id]["sub_action"] = data
        if data == "change_text":
            bot.send_message(call.message.chat.id, "Надішліть новый текст:")
        elif data == "change_photo":
            bot.send_message(call.message.chat.id, "Надішліть нове фото:")
        elif data == "change_video":
            bot.send_message(call.message.chat.id, "Надішліть нове відео:")
        return

    if data in sections:
        item = load_content(data)
        text = item["text"] or "Текст відсутній"
        try:
            if item.get("photo"):
                bot.send_photo(call.message.chat.id, item["photo"], caption=text, parse_mode='Markdown')
            elif item.get("video"):
                bot.send_video(call.message.chat.id, item["video"], caption=text, parse_mode='Markdown')
            else:
                bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        except Exception as e:
            bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(content_types=['text', 'photo', 'video'])
def handle_input(message):
    user_id = message.from_user.id
    if user_id not in user_state:
        return

    state = user_state[user_id]

    if state.get("step") == "waiting_password":
        role = state["role"]
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
        return

    if "sub_action" in state:
        section = state["section"]
        if state["sub_action"] == "change_text" and message.text:
            update_content(section, text=message.text)
            bot.send_message(message.chat.id, "✅ Текст оновлено в Supabase!")
        elif state["sub_action"] == "change_photo" and message.photo:
            update_content(section, photo=message.photo[-1].file_id)
            bot.send_message(message.chat.id, "✅ Фото збережено в Supabase!")
        elif state["sub_action"] == "change_video" and message.video:
            update_content(section, video=message.video.file_id)
            bot.send_message(message.chat.id, "✅ Відео збережено в Supabase!")

        user_state[user_id] = {"action": "edit_section", "section": section}

# === ЗАПУСК ===
if __name__ == "__main__":
    init_db()
    threading.Thread(target=run_web_server, daemon=True).start()
    print("🤖 Бот запущен...")
    bot.infinity_polling()
