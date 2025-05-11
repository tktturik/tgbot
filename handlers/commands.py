from telegram import Update
from telegram.ext import CommandHandler,ContextTypes
import requests
from dotenv import load_dotenv
import os
from keyboards.reply import darsik_menu, request_contact_button
from utils.path_config import MediaPath
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.crud.user import get_user_by_chatid, add_new_user
from utils.auth import checkAuth



load_dotenv()
url = os.getenv('URL_CATS_FACTS')
API_KEY = os.getenv('API_KEY')

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


async def create_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 4:
        await update.message.reply_text("❗ Формат: /create_user Имя Фамилия Отчество Телефон")
        return

    first_name, last_name, middle_name, phone_number = args[:4]

    db: Session = SessionLocal()

    try:
        user = add_new_user(
            db=db,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name
        )
        await update.message.reply_text(f"✅ Пользователь {first_name} {last_name} создан.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        db.close()

create_user_handler = CommandHandler("create_user", create_user)


async def set_city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    city = " ".join(context.args)
    context.user_data["city"] = city  
    await update.message.reply_text(f"✅ Город по умолчанию установлен: {city}")
set_city_handler = CommandHandler("set_city",set_city)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if context.args:
        city = " ".join(context.args)
    elif "city" in context.user_data:
        city = context.user_data["city"]
    else:
        await update.message.reply_text(
            "Укажите город (/weather Москва) или установите город по умолчанию (/setcity Москва)"
        )
        return    

    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3&lang=ru"

    response = requests.get(url)
    response.raise_for_status()  

    data = response.json()
    print(data)
    location = data['location']['name']
    temp_c = data['current']['temp_c']
    condition = data['current']['condition']['text']
    feelslike = data['current']['feelslike_c']
    humidity = data['current']['humidity']

    image_url = "https:" + data['current']['condition']['icon']

    weather_info = (
        f"Погода в {location}:\n"
        f"🌡 Температура: {temp_c}°C (ощущается как {feelslike}°C)\n"
        f"☁ Состояние: {condition}\n"
        f"💧 Влажность: {humidity}%"
    )
    await update.message.reply_text(weather_info)
    await update.message.reply_photo(image_url)

weather_handler = CommandHandler("weather",weather)
