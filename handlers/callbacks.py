from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
#from keyboards.inline import 


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  

    if query.data == "button1":
        await query.edit_message_text("Вы нажали Кнопку 1")
    elif query.data == "button2":
        await query.edit_message_text("Вы нажали Кнопку 2")
    elif query.data == "button3":
        await query.edit_message_text("Вы нажали Кнопку 3")

callback_handler = CallbackQueryHandler(button_handler)