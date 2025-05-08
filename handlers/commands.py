from telegram import Update
from telegram.ext import CommandHandler,ContextTypes
import requests
from dotenv import load_dotenv
import os
from keyboards.reply import darsik_menu, request_contact_button
from utils.path_config import MediaPath
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.crud.user import get_user_by_chatid
from utils.auth import checkAuth


load_dotenv()
url = os.getenv('URL_CATS_FACTS')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE,):
    
    chat_id = update.message.chat_id
    user = await checkAuth(chat_id=chat_id)
    
    if user:
        await update.message.reply_text(f"С возвращением! {update.message.from_user.full_name}")
    else:
        await update.message.reply_text("Номер на базу", reply_markup=request_contact_button())

start_handler = CommandHandler("start",start)

async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["back_comm"] = "gift"

    response = requests.get(url)
    data = response.json()
    fact = data['fact']
    await update.message.reply_text(fact)

gift_handler = CommandHandler("gift",gift)

async def darsik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите кнопку:", reply_markup=darsik_menu())

but_handler = CommandHandler("dora",darsik)

async def request_contact_menu(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите кнопку:", reply_markup=request_contact_button())

request_contact_handler = CommandHandler("aaa",request_contact_menu)