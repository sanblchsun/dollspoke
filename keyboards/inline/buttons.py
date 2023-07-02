from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def del_product():
    ikm = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('Удалить', callback_data='delete product from base (kod 9087876)')
    ikm.add(btn)
    return ikm

def pass_step():
    ikm = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('Пропустить', callback_data='pass step (kod 907554376)')
    ikm.add(btn)
    return ikm