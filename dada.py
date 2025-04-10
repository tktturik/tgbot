from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
from config import BOT_TOKEN
from handlers.commands import start_command, help_command
from handlers.messages import echo_message

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    print("Бот работает 🚀")
    await app.run_polling()

# Запуск
if __name__ == '__main__':
    main()
