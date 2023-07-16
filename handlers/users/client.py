import asyncio

from emoji import emojize
from aiogram import types
from loader import dp, sql_object, bot
from aiogram.dispatcher.filters.builtin import Text, ChatTypeFilter
from functions import defs
from keyboards.inline.buttons import edit_like_dislike


@dp.message_handler(Text(equals='Куклы'), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_user_echo(message: types.Message):
    await message.answer(emojize(':yarn:') + emojize(':yarn:') + emojize(':yarn:'))
    res = await defs.viewer_product_caption_media_group(message.from_user.id)
    if not res:
        await message.answer("<b><i><u>Товара пока нет</u></i></B>")


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


@dp.callback_query_handler(lambda c: c.data.startswith(('emo red heart', 'emo humbs up', 'emo thumbs down')))
async def action_emo_red_heart(callback_query: types.CallbackQuery):
    id_product = callback_query.message.text.split("\n")[0].replace("Код товара: ", "")
    callback_data = callback_query.data
    res_sql_like = await sql_object.sql_get_like(id_product=id_product)
    heard, like, dislike = 0, 0, 0
    for itr in res_sql_like:
        heard, like, dislike =  itr["heard"], itr["like"], itr["dislike"]
        if callback_data == 'emo red heart':
            heard += 1
        if callback_data == 'emo humbs up':
            like += 1
        if callback_data == 'emo thumbs down':
            dislike += 1
        await sql_object.sql_set_new_like(id_product, heard=heard, like=like, dislike=dislike)
    try:
        await bot.edit_message_reply_markup(
            callback_query.message.chat.id,
            callback_query.message.message_id,
            reply_markup=edit_like_dislike(heard=heard, like=like, dislike=dislike))
    except Exception as e:
        print(f" Ошибка изменения кнопки \n {e}")
    await asyncio.sleep(1)

