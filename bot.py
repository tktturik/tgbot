from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Bot, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import requests

# Токен вашего бота
TOKEN = "7693189579:AAEdz8QnX1uZlpo14ZMqhcJ1l_PQy86_4J4"
url = "https://catfact.ninja/fact"
bot = Bot(token=TOKEN)
darsik_id = 1492493203

async  def but2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("Поделиться номером", request_contact=True)
    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Выберите кнопку:", reply_markup=reply_markup)


# Обработчик команды /start
async def but(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем инлайн-кнопки
    context.user_data["back_comm"] = "menu"
    keyboard = [
        ["Хочу сосиску в тесте"],
        ["чозабретта"],
        ["уебище"],
        ["бам"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите кнопку:", reply_markup=reply_markup)
# Обработчик нажатия на кнопку
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем контактные данные
    contact = update.message.contact
    phone_number = contact.phone_number  # Номер телефона
    user_id = contact.user_id  # ID пользователя

    # Сохраняем номер телефона (например, в базу данных)

    # Отправляем подтверждение
    await update.message.reply_text(f"Спасибо! Ваш номер телефона: {phone_number}")
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Подтверждаем нажатие кнопки

    # Определяем, какая кнопка была нажата
    if query.data == "button1":
        await query.edit_message_text("Вы нажали Кнопку 1")
    elif query.data == "button2":
        await query.edit_message_text("Вы нажали Кнопку 2")
    elif query.data == "button3":
        await query.edit_message_text("Вы нажали Кнопку 3")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["back_comm"] = "start"
    await update.message.reply_photo("img.png")
    #await update.message.reply_text(update.message.from_user.first_name)

async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["back_comm"] = "gift"

    response = requests.get(url)
    data = response.json()
    fact = data['fact']
    await update.message.reply_text(fact)


# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()  # Приводим текст к нижнему регистру
    user_name = update.message.from_user.full_name
    if update.message.chat_id == darsik_id:
        await bot.send_message(chat_id=557160827,text=update.message.text+f"from {user_name}")
    if "катька" in text:
        await update.message.reply_text("дура")
    elif "хочу сосиску в тесте" in text:
        await update.message.reply_text(f"Будет сосиска из виорда для {user_name}")

        from telegram import Update
        from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("Привет! Я бот.")

        app = ApplicationBuilder().token("YOUR_TOKEN").build()
        app.add_handler(CommandHandler("start", start))
        app.run_polling()
    elif "чозабретта" in text:
        await update.message.reply_photo("sobaka.png")
    elif "уебище" in text:
        await update.message.reply_animation("yebishe.mp4")
    elif "виорд" in text:
        await update.message.reply_text("жесть")
    elif "бам" in text:
        chat_id = update.message.chat_id
        await bot.send_video(chat_id=darsik_id,video="video.mp4")
    elif "беру" in text:
        prev_con = context.user_data.get("back_comm","bad")
        if prev_con == "start":
            await update.message.reply_text(f"Сосиска в тесте заказана для {user_name}")
    elif "бегемот" in text:
        await update.message.reply_animation("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTh2OTgxbmJsM2xqMGhyNWhlYmk2emFudnBka3hpbWNiajh0cmxhcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7kn27lnYSAE9O/giphy.gif")

    else:
        await update.message.reply_text("Я не понимаю :(")

# Основная функция для запуска бота
def main():
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gift", gift))
    app.add_handler(CommandHandler("menu", but))
    app.add_handler(CommandHandler("aaa", but2))

    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    # Запускаем бота
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()