from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def menu_clients_start():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    bt2 = KeyboardButton('Контакты')
    bt1 = KeyboardButton('Режим работы')
    bt3 = KeyboardButton('Куклы')
    bt4 = KeyboardButton('Доставка')
    rkm.add(bt1,bt2).add(bt3,bt4)
    return rkm

def menu_start_for_admin():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = KeyboardButton('Новый товар')
    bt2 = KeyboardButton('Удалить товар')
    bt3 = KeyboardButton('инфо')
    rkm.add(bt1, bt2).add(bt3)
    return rkm

def menu_out_admin():
    rkm = ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = KeyboardButton('выйти из админа')
    rkm.add(bt1)
    return rkm



