import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
from loader import sql_object, dp


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


def edit_like_dislike(heard, like, dislike):
    if heard == 0:
        heard = ''
    if like == 0:
        like = ''
    if dislike == 0:
        dislike = ''
    ikm = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(emojize(':red_heart:') + f'{heard}', callback_data='emo red heart')
    btn2 = InlineKeyboardButton(emojize(':thumbs_up:') + f'{like}', callback_data="emo humbs up")
    btn3 = InlineKeyboardButton(emojize(':thumbs_down:') + f'{dislike}', callback_data='emo thumbs down')
    return ikm.add(btn1, btn2, btn3)
