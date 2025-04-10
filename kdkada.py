from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Токен вашего бота
TOKEN = "ВАШ_ТОКЕН"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот. Напиши мне что-нибудь.")

# Основная функция для запуска бота
def main():
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Регистрируем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Запускаем бота
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
