from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os
from utils.path_config import MediaPath
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.schemas.user import UserCreate
from backend.crud.user import create_user

load_dotenv()
DARSIK_ID = os.getenv("DARSIK_ID")
ROOT_ID = os.getenv("ROOT_ID")

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone_number = contact.phone_number
    chat_id = update.message.chat_id
    context.user_data["phone_number"] = phone_number

    db: Session = SessionLocal()

    try:
        new_user = UserCreate(phone_number=phone_number, chat_id=chat_id)
        create_user(db, new_user)
        await update.message.reply_text("Вы успешно зарегистрированы!")
    finally:
        db.close()


contact_handler = MessageHandler(filters.CONTACT, handle_contact)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()  
    user_name = update.message.from_user.full_name
    if update.message.chat_id == DARSIK_ID:
        await context.send_message(chat_id=ROOT_ID,text=update.message.text+f"from {user_name}")
    if "катька" in text:
        await update.message.reply_text("дура")
    elif "беру" in text:
        prev_con = context.user_data.get("back_comm","bad")
        if prev_con == "start":
            await update.message.reply_text(f"Сосиска в тесте заказана для {user_name}")
    elif "бегемот" in text:
        await update.message.reply_animation("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTh2OTgxbmJsM2xqMGhyNWhlYmk2emFudnBka3hpbWNiajh0cmxhcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7kn27lnYSAE9O/giphy.gif")
    else:
        await update.message.reply_text("Я не понимаю :(")
messages_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

async def darsik_menu_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.full_name
    text = update.message.text
    if text in "сосиска виорд":
        await update.message.reply_photo(MediaPath.getImagePath("img.png"))
    elif text in "Хочу сосиску в тесте":
        await update.message.reply_text(f"Будет сосиска из виорда для {user_name}")
    elif text in "чозабретта":
        await update.message.reply_photo(MediaPath.getImagePath("sobaka.png"))
    elif text in "уебище":
        await update.message.reply_animation(MediaPath.getVideoPath("yebishe.mp4"))
    elif text in "бам":
        await context.bot.send_video(chat_id=ROOT_ID,video=MediaPath.getVideoPath("video.mp4"))
    

darsik_messages_handler = MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex("сосиска виорд|Хочу сосиску в тесте|чозабретта|уебище|бам"),darsik_menu_messages)