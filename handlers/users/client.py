from emoji import emojize
from aiogram import types
from loader import dp, sql_object
from aiogram.dispatcher.filters.builtin import Text, ChatTypeFilter
from functions import defs


@dp.message_handler(Text(equals='Куклы'), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_user_echo(message: types.Message):
    await message.answer(emojize(':yarn:') + emojize(':yarn:') + emojize(':yarn:'))
    await defs.viewer_product_caption(message.from_user.id)


@dp.message_handler(Text(equals='Контакты'), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_user_contact(message: types.Message):
    await message.answer(emojize(':yarn:'))
    res = await sql_object.sql_get_info()
    if res["telefon"] != 'None':
        await message.reply(f'<b><i><u>{res["telefon"]}</u></i></b>')
    if res["full_name"] != 'None':
        await message.answer(f'<b><i><u>{res["full_name"]}</u></i></b>')
    if res["telefon"] == 'None' and res["full_name"] == 'None':
        await message.reply('<b><i><u>Контактов пока нет</u></i></b>')


@dp.message_handler(Text(equals='Режим работы'), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_user_schedule(message: types.Message):
    await message.answer(emojize(':yarn:'))
    res = await sql_object.sql_get_info()
    if res["operating_mode"] != 'None':
        await message.reply(f'<b><i><u>{res["operating_mode"]}</u></i></b>')
    else:
        await message.reply('<b><i><u>Режима работы пока нет</u></i></b>')


@dp.message_handler(Text(equals='Доставка'), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_user_schedule(message: types.Message):
    await message.answer(emojize(':yarn:'))
    res = await sql_object.sql_get_info()
    if res["delivery"] != 'None':
        await message.reply(f'<b><i><u>{res["delivery"]}</u></i></b>')
    else:
        await message.reply('<b><i><u>Информации о доставке пока нет</u></i></b>')
