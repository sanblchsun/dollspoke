import asyncio

from emoji import emojize
from aiogram import types

import loader
from loader import dp, sql_object, bot
from aiogram.dispatcher.filters.builtin import Text, ChatTypeFilter
from functions import defs
from keyboards.inline.buttons import edit_like_dislike_and_buy
# from keyboards.reply.buttons import reply_button

PRICES = [
    types.LabeledPrice(label='Ноутбук', amount=1000),
    types.LabeledPrice(label='Прочная упаковка', amount=1000)
]


@dp.message_handler(Text(equals='Показать товар'), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['product'])
async def action_user_echo(message: types.Message):
    await message.answer(emojize(':yarn:') + emojize(':yarn:') + emojize(':yarn:'))
    res = await defs.viewer_product_caption_media_group(message.from_user.id)
    if not res:
        await message.answer("<b><i><u>Товара пока нет</u></i></B>")
        return
    # get_cart = await sql_object.sql_get_cart_count_customer(message.from_user.id)
    # cart_current_user = 0
    # for item in get_cart:
    #     cart_current_user = item["count"]
    # await bot.send_message(message.from_user.id, 'Нажмите, что бы добавить в корзину.',
    #                        reply_markup=reply_button(cart_current_user))


@dp.message_handler(Text(equals='Контакты'), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_user_contact(message: types.Message):
    await message.answer(emojize(':yarn:'))
    res_sql_telefon = await sql_object.sql_get_info()
    for itr in res_sql_telefon:
        if itr["telefon"] != 'None':
            await message.reply(f'<b><i><u>{itr["telefon"]}</u></i></b>')
        if itr["full_name"] != 'None':
            await message.answer(f'<b><i><u>{itr["full_name"]}</u></i></b>')
        if itr["telefon"] == 'None' and itr["full_name"] == 'None':
            await message.reply('<b><i><u>Контактов пока нет</u></i></b>')


@dp.message_handler(Text(equals='Режим работы'), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_user_schedule(message: types.Message):
    await message.answer(emojize(':yarn:'))
    res_sql_operating_mode = await sql_object.sql_get_info()
    for itr in res_sql_operating_mode:
        if itr["operating_mode"] != 'None':
            await message.reply(f'<b><i><u>{itr["operating_mode"]}</u></i></b>')
        else:
            await message.reply('<b><i><u>Режима работы пока нет</u></i></b>')


@dp.message_handler(Text(equals='Доставка'), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_user_schedule(message: types.Message):
    await message.answer(emojize(':yarn:'))
    res_sql_delivery = await sql_object.sql_get_info()
    for itr in res_sql_delivery:
        if itr["delivery"] != 'None':
            await message.reply(f'<b><i><u>{itr["delivery"]}</u></i></b>')
        else:
            await message.reply('<b><i><u>Информации о доставке пока нет</u></i></b>')


@dp.callback_query_handler(lambda c: c.data.startswith(('emo red heart', 'emo humbs up', 'emo thumbs down')))
async def action_emo_red_heart(callback_query: types.CallbackQuery):
    id_product = callback_query.message.text.split("\n")[0].replace("Код товара: ", "")
    callback_data = callback_query.data
    res_sql_like = await sql_object.sql_get_like(id_product=id_product)
    heard, like, dislike = 0, 0, 0
    for itr in res_sql_like:
        heard, like, dislike = itr["heard"], itr["like"], itr["dislike"]
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
            reply_markup=edit_like_dislike_and_buy(heard=heard, like=like, dislike=dislike))
    except Exception as e:
        print(f" Ошибка изменения кнопки \n {e}")
    await asyncio.sleep(1)


@dp.callback_query_handler(lambda c: c.data == "3143 add one product in cart")
async def action_add_to_cart(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    get_cart = await sql_object.sql_get_cart_count_customer(callback_query.message.from_user.id)
    cart_count_user = 0
    for item in get_cart:
        cart_count_user = item["count"]
    if cart_count_user == 0:
        cart_count_user += 1
        await sql_object.sql_add_cart_and_customer(id_customer=callback_query.message.from_user.id,
                                                   id_product=callback_query.message.text.split("\n")[0].replace(
                                                       'Код товара: ', ''))
    else:
        await sql_object.sql_add_cart_only(id_customer=callback_query.message.from_user.id,
                                           id_product=callback_query.message.text.split("\n")[0].replace('Код товара: ',
                                                                                                         ''))

    await callback_query.message.answer("Вы добавили товар в корзину", reply_markup=reply_button(cart_count_user))


@dp.message_handler(content_types='web_app_data')
async def buy_process(message: types.Message):
    await message.answer(message.web_app_data.data)
    # await bot.send_invoice(message.chat.id,
    #                        title='Какой-то товар',
    #                        description='Описание какого-то товара',
    #                        provider_token=loader.payments_token,
    #                        currency='rub',
    #                        photo_url='https://images.unsplash.com/photo-1603302576837-37561b2e2302?ixlib=rb-1.2.1&ixid='
    #                                  'MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1468&q=80',
    #                        photo_height=512,
    #                        photo_width=512,
    #                        photo_size=512,
    #                        need_email=True,
    #                        need_phone_number=True,
    #                        is_flexible=True,
    #                        prices=PRICES,
    #                        start_parameter='example',
    #                        payload='some_invoice')

# @dp.pre_checkout_query_handler(lambda q: True)
# async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
#
# @dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
# async def successful_payment_handler(message: types.Message) -> None:
#     await message.answer("Платеж прошел успешно")
