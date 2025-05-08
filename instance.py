from telegram.ext import Application
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("Не удалось загрузить BOT_TOKEN из .env файла")

app = Application.builder().token(BOT_TOKEN).build()
