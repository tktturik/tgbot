from telegram import ReplyKeyboardMarkup, KeyboardButton

def request_contact_button():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Поделиться номером", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )
def darsik_menu():
    return ReplyKeyboardMarkup(
       [
        ["сосиска виорд"],  
        ["Хочу сосиску в тесте"],
        ["чозабретта"],
        ["уебище"],
        ["бам"]],
        resize_keyboard=True
    )