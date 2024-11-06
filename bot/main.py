from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, ConversationHandler, filters
from data.user import User, UserSex
import logging
from uuid import uuid4

# Логгинг
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# КХ
REGISTER, GET_NAME, GET_SEX, GET_PARTNER_PREFERENCE, GET_LUNCH_TIME, PREFERENCES, FEEDBACK = range(7)

# Пародия на БД
users = {}
lunch_matches = {}
feedbacks = {}

# Рега
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Привет! 👋 \nТы попал в LunchBuddy – бота, который поможет тебе найти классную компанию для обеда!\n"
        "Чтобы найти тебе идеальных сотрапезников, ответь на пару вопросов о себе и заполни короткую анкету.\n"
        "Поехали! 🚀\n\nВведите Имя (или псевдоним):"
    )
    return GET_NAME

# Имя
async def get_name(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    name = update.message.text
    users[user_id] = {"username": update.message.from_user.username, "name": name}
    await update.message.reply_text("Пол:", reply_markup=ReplyKeyboardMarkup([["Мужской", "Женский"]], one_time_keyboard=True))
    return GET_SEX

# Пол
async def get_sex(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    sex = UserSex.MALE if update.message.text == "Мужской" else UserSex.FEMALE
    users[user_id]["sex"] = sex
    await update.message.reply_text(
        "Выберите, с кем Вам было бы комфортно обедать?", 
        reply_markup=ReplyKeyboardMarkup([["Девушка", "Парень", "Компания", "Неважно"]], one_time_keyboard=True)
    )
    return GET_PARTNER_PREFERENCE

# Префы
async def get_partner_preference(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    users[user_id]["partner_preference"] = update.message.text
    await update.message.reply_text(
        "Желаемое время обеда:", 
        reply_markup=ReplyKeyboardMarkup(
            [["12:00-13:00", "13:00-14:00", "14:00-15:00"], ["15:00-16:00", "16:00-17:00"]],
            one_time_keyboard=True
        )
    )
    return GET_LUNCH_TIME

# Время
async def get_lunch_time(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    users[user_id]["lunch_time"] = update.message.text
    qr_code = uuid4()
    users[user_id]["qr_code"] = qr_code
    await update.message.reply_text(f"Вы успешно зарегистрированы! Ваш Qr-код: {qr_code}")
    return ConversationHandler.END

# Функция для регистрации предпочтений (опционально, пока пох я думаю)
async def save_preferences(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    users[user_id]["preferences"] = update.message.text
    await update.message.reply_text("Ваши предпочтения сохранены.")
    return ConversationHandler.END

# Мэтчинг
async def find_buddy(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_pref = users[user_id].get("partner_preference")
    user_lunch_time = users[user_id].get("lunch_time")
    
    for uid, data in users.items():
        # Мэтч
        if uid != user_id and data.get("partner_preference") == user_pref and data.get("lunch_time") == user_lunch_time:
            lunch_matches[user_id] = uid
            lunch_matches[uid] = user_id
            await context.bot.send_message(chat_id=user_id, text=f"Для обеда подходит: @{users[uid]['username']}")
            await context.bot.send_message(chat_id=uid, text=f"Для обеда подходит: @{users[user_id]['username']}")
            return
    
    await update.message.reply_text("Пока не удалось найти подходящего напарника для обеда. Попробуйте, пожалуйста, позже.")

# Ремайндер
async def remind(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    match_id = lunch_matches.get(user_id)
    
    if match_id:
        await context.bot.send_message(
            chat_id=user_id, 
            text=f"Напоминаем: у Вас запланирован обед с @{users[match_id]['username']}!"
        )
    else:
        await update.message.reply_text("У Вас нет запланированных встреч на обед.")

# Получение фидбека
async def feedback(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Оцените Ваш обед от 1 до 5 и оставьте отзыв о своём опыте:")
    return FEEDBACK

# Сохранение фидбека
async def save_feedback(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    score, *review = update.message.text.split(maxsplit=1)
    score = float(score)
    review = review[0] if review else ""
    
    if user_id in lunch_matches:
        partner_id = lunch_matches[user_id]
        
        # Обновление рейтинга (возможно это нахрен не надо, обсудите и удалите если что)
        if "rating" in users[partner_id]:
            users[partner_id]["rating"] = (users[partner_id]["rating"] + score) / 2
        else:
            users[partner_id]["rating"] = score
        
        # Сохранение отзыва
        feedbacks[user_id] = {"partner_id": partner_id, "score": score, "review": review}
        await update.message.reply_text("Спасибо за отзыв! Ваш отзыв был сохранён.")
    else:
        await update.message.reply_text("Обед не состоялся, оставить отзыв нельзя.")
    
    return ConversationHandler.END

# КХ
def main() -> None:
    application = Application.builder().token("7700731666:AAESsLAY8Bu_KNNYBm3KCAL4ugKZWGVzbGw").build()

    # рег
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GET_NAME: [MessageHandler(filters.TEXT, get_name)],
            GET_SEX: [MessageHandler(filters.TEXT, get_sex)],
            GET_PARTNER_PREFERENCE: [MessageHandler(filters.TEXT, get_partner_preference)],
            GET_LUNCH_TIME: [MessageHandler(filters.TEXT, get_lunch_time)],
            PREFERENCES: [MessageHandler(filters.TEXT, save_preferences)],
            FEEDBACK: [MessageHandler(filters.TEXT, save_feedback)],
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler)

    # Другие комманды
    application.add_handler(CommandHandler("find_buddy", find_buddy))
    application.add_handler(CommandHandler("remind", remind))
    application.add_handler(CommandHandler("feedback", feedback))

    # Ланч
    application.run_polling()

if __name__ == "__main__":
    main()
