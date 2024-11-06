from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, ConversationHandler
from telegram.ext import ContextTypes
import logging
from uuid import uuid4

# Setting up basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
REGISTER, PREFERENCES, FEEDBACK = range(3)

# Пародия ДБ
users = {}
lunch_matches = {}

# Регистрация [comand='start'] 
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Добро пожаловать в LunchBot! Время зарегистрироваться!")
    return REGISTER

# Сбор предпочтений
async def register(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    users[user_id] = {"username": update.message.from_user.username}
    await update.message.reply_text("Расскажите о своих предпочтениях:")
    return PREFERENCES

async def save_preferences(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    users[user_id]["preferences"] = update.message.text
    qr_code = uuid4()  # генерит qr
    users[user_id]["qr_code"] = qr_code
    await update.message.reply_text(f"Вы зарегистрированы! Ваш Qr-код: {qr_code}")
    return ConversationHandler.END

# Мэтчинг
def find_lunch_match(user_id):
    user_pref = users[user_id].get("preferences")
    for uid, data in users.items():
        if uid != user_id and user_pref in data.get("preferences", ""):
            return uid
    return None

# Команда для мэтчинга
async def find_buddy(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    match_id = find_lunch_match(user_id)
    if match_id:
        lunch_matches[user_id] = match_id
        lunch_matches[match_id] = user_id
        await context.bot.send_message(chat_id=user_id, text=f"Есть предложение для обеда: @{users[match_id]['username']}")
        await context.bot.send_message(chat_id=match_id, text=f"Есть предложение для обеда: @{users[user_id]['username']}")
    else:
        await update.message.reply_text("К сожалению, пока у Вас ни с кем не будет обэда! Попробуйте попозже")

# Напоминания
async def remind(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    match_id = lunch_matches.get(user_id)
    if match_id:
        await context.bot.send_message(chat_id=user_id, text=f"Напоминаем: у Вас запланирован обэд @{users[match_id]['username']}!")
    else:
        await update.message.reply_text("Нет запланированных обэдов")

# Фидбэк
async def feedback(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Оцените Ваш обэд:")
    return FEEDBACK

async def save_feedback(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    users[user_id]["feedback"] = update.message.text
    await update.message.reply_text("Спасибо за оценку обэда!")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token("7700731666:AAESsLAY8Bu_KNNYBm3KCAL4ugKZWGVzbGw").build()

    # Регистрация, мэтчинг, фидбек и тд
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            REGISTER: [MessageHandler(filters.TEXT, register)],
            PREFERENCES: [MessageHandler(filters.TEXT, save_preferences)],
            FEEDBACK: [MessageHandler(filters.TEXT, save_feedback)],
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("find_buddy", find_buddy))
    application.add_handler(CommandHandler("remind", remind))
    application.add_handler(CommandHandler("feedback", feedback))

    # ланч
    application.run_polling()

if __name__ == "__main__":
    main()
