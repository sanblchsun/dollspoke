import asyncio
import json
import logging

from emoji import emojize

from functions import defs
from states.state_form import AdminStates, AdminInfoStates
from loader import dp, bot, sql_object
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text, ChatTypeFilter
from keyboards.reply.buttons import menu_start_for_admin, menu_out_admin
from keyboards.inline.buttons import del_product, pass_step
from filters.admin_filter import AdminFilter
from aiogram.types import ReplyKeyboardRemove
from typing import List



# ==================================Регистрируем в фильтре AdminFilter id группы
@dp.message_handler(commands=["admin"], is_chat_admin=True)
async def definition_admins(message: types.Message):
    obj = AdminFilter(is_admin=True)
    await obj.my_chat_id_data(message.chat.id)
    await bot.send_message(message.from_user.id, emojize(':yarn:'))
    await bot.send_message(message.from_user.id, '<b><i>Регистрация администратора: </i></b>'
                                                 f'<pre>{message.from_user.full_name}</pre>'
                                                 '<b><i>'
                                                 'вам доступно управление номенклатурой, выбирайте ваше действия'
                                                 '</i></b>',
                           reply_markup=menu_start_for_admin())
    await message.delete()


# ===================================================================================


# ================================== Реакция на Reply кнопки
@dp.message_handler(AdminFilter(is_admin=True),
                    Text(equals='Новый товар'),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_btn_new_product(message: types.Message):
    await message.answer(emojize(':yarn:'))
    await AdminStates.photo.set()
    await message.answer('<b><i><u>Загрузите фото товара</u></i></b>', reply_markup=menu_out_admin())


@dp.message_handler(AdminFilter(is_admin=True),
                    Text(equals='инфо'),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE), state=None)
async def action_btn_info(message: types.Message):
    await message.answer(emojize(':yarn:'))
    await AdminInfoStates.tlf.set()
    await message.answer('<b><i><u>Вы в стадии изменения инфомации о компании.\n'
                         'Введенное поле сохраняеться в базе в конце, когда выйдет сообщение.</u></i></b>',
                         reply_markup=menu_out_admin())
    await message.answer('<b><i><u>Укажите телефон</u></i></b>', reply_markup=pass_step())


@dp.message_handler(AdminFilter(is_admin=True),
                    Text(equals='Удалить товар'),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def action_btn_del(message: types.Message):
    await message.answer(emojize(':yarn:') + emojize(':yarn:') + emojize(':yarn:'))
    res = await defs.viewer_product_caption_photo(message.from_user.id, keyboard=del_product())
    if not res:
        await message.answer("<b><i><u>Товара пока нет</u></i></B>")


# ==========================================================

# ======================отменяем все действия администратора и выходим из режима админа
@dp.message_handler(AdminFilter(is_admin=True),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    commands=['cancel'],
                    state='*')
@dp.message_handler(AdminFilter(is_admin=True),
                    Text(equals='выйти из админа'),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    state='*')
async def action_del_user_data(message: types.Message, state: FSMContext):
    await message.answer("<b><i><u>Вы отменили все свои действия и вышли из режима администратора.</u></i></b>",
                         reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await AdminFilter(is_admin=True).clradm()


# ====================================================================================

# =========================================== Раздел где добавить товар
# @dp.message_handler(AdminFilter(is_admin=True),
#                     ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
#                     content_types=['photo'],
#                     state=AdminStates.photo)
@dp.message_handler(
                    AdminFilter(is_admin=True),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    is_media_group=True,
                    content_types=types.ContentType.ANY,
                    state=AdminStates.photo
                    )
# async def end_action_load(message: types.Message, state: FSMContext):
async def handle_albums(message: types.Message, album: List[types.Message], state: FSMContext):
    await message.answer(emojize(':yarn:'))
    # --------------------------------------------------------------------
    """This handler will receive a complete album of any type."""
    media_group = types.MediaGroup()
    i = 0
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            if i == 0:
                media_group.attach({"caption": message.caption,
                                    "media": file_id, "type": obj.content_type})
            else:
                media_group.attach({"media": file_id, "type": obj.content_type})
            i += 1
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")
    # -------------------------------------------------------------------------
    await state.update_data(photo=media_group)
    await AdminStates.name.set()
    await message.answer('<b><i><u>Введите название для товара с фото</u></i></b>', reply_markup=menu_out_admin())


@dp.message_handler(AdminFilter(is_admin=True),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    content_types=['text'],
                    state=AdminStates.name)
async def action_name(message: types.Message, state: FSMContext):
    await message.answer(emojize(':yarn:'))
    await state.update_data(name=message.text)
    await AdminStates.description.set()
    await message.reply('<b><i><u>Введите описание для товара с фото</u></i></b>', reply_markup=menu_out_admin())


@dp.message_handler(AdminFilter(is_admin=True),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    content_types=['text'],
                    state=AdminStates.description)
async def action_desc(message: types.Message, state: FSMContext):
    await message.answer(emojize(':yarn:'))
    await state.update_data(description=message.text)
    await AdminStates.price.set()
    await message.reply('<b><i><u>Укажите цену для товара с фото</u></i></b>', reply_markup=menu_out_admin())



@dp.message_handler(AdminFilter(is_admin=True),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    content_types=['text'],
                    state=AdminStates.price)
async def action_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        await state.update_data(price=float(price))
    except ValueError as e:
        await message.answer(emojize(':prohibited:'))
        await message.reply('<b><i><u>Введите цену в формате число</u></i></b>', reply_markup=menu_out_admin())
        return

    await message.answer(emojize(':yarn:'))
    await message.reply('<b><i><u>Вы создали единицу номенклатуры в базе</u></i></b>',
                        reply_markup=ReplyKeyboardRemove())
    media_group = (await state.get_data()).get('photo')
    data_name = (await state.get_data()).get('name')
    data_description = (await state.get_data()).get('description')
    data_price = (await state.get_data()).get('price')
    json_func = media_group.as_json()
    await sql_object.sql_add_product(json_func, data_name, data_description, data_price)
    await asyncio.sleep(2)
    await defs.viewer_product_caption_media_group(my_id=message.from_user.id, last=True)
    await state.finish()
    await AdminFilter(is_admin=True).clradm()


# =============================================================================================

# ==========================================Раздел где удаляют товар
@dp.callback_query_handler(AdminFilter(is_admin=True), lambda c: c.data == 'delete product from base (kod 9087876)')
async def action_delete_product(callback_query: types.CallbackQuery):
    res = callback_query.message.values
    res0 = res['caption'].split('\n')[0].replace("Код товара: ", '')
    await sql_object.sql_del_product(int(res0))
    await bot.answer_callback_query(callback_query_id=callback_query.id,
                                    text=f'Товар с кодом: {res0} был удален.',
                                    show_alert=True)
    await callback_query.message.delete()
    res_get = await sql_object.sql_get_product()
    if not res_get:
        await callback_query.message.answer('<b><i><u>Удален весь товар из базы</u></i></b>')
    await callback_query.message.answer(emojize(':yarn:') + "что то было удалено")


@dp.callback_query_handler(lambda c: c.data == 'delete product from base (kod 9087876)')
async def action_delete_product(callback_query: types.CallbackQuery):
    await callback_query.message.answer(emojize(':yarn:'))
    await callback_query.message.answer('<b><i><u>Вы сейчас не в статусе администратора</u></i></b>',
                                        reply_markup=ReplyKeyboardRemove())


# ===========================================================================================


# =================================================== Раздел info, где редактируют ФИО, телефон, режим работы, доставка
@dp.message_handler(AdminFilter(is_admin=True),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    content_types=['text'],
                    state=AdminInfoStates.tlf)
async def end_action_tlf(message: types.Message, state: FSMContext):
    await message.answer(emojize(':yarn:'))
    await state.update_data(telefon=message.text)
    await AdminInfoStates.next()
    await message.answer('<b><i><u>Введите Ф.И.О.</u></i></b>', reply_markup=pass_step())


@dp.message_handler(AdminFilter(is_admin=True),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    content_types=['text'],
                    state=AdminInfoStates.FIO)
async def end_action_fio(message: types.Message, state: FSMContext):
    await message.answer(emojize(':yarn:'))
    await state.update_data(fio=message.text)
    await AdminInfoStates.next()
    await message.answer('<b><i><u>Введите режим работы.</u></i></b>', reply_markup=pass_step())


@dp.message_handler(AdminFilter(is_admin=True),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    content_types=['text'],
                    state=AdminInfoStates.operating_mode)
async def end_action_operation_mode(message: types.Message, state: FSMContext):
    await message.answer(emojize(':yarn:'))
    await state.update_data(operating_mode=message.text)
    await AdminInfoStates.next()
    await message.answer('<b><i><u>Введите информацию о доставке товара</u></i></b>', reply_markup=pass_step())


@dp.message_handler(AdminFilter(is_admin=True),
                    ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
                    content_types=['text'],
                    state=AdminInfoStates.delivery)
async def end_action_delivery(message: types.Message, state: FSMContext):
    await message.answer(emojize(':yarn:'))
    await state.update_data(delivery=message.text)
    await message.answer('<b><i><u>Конец формы инфо, данные записаны</u></i></b>')
    data = await state.get_data()
    tlf = data.get('telefon')
    full_name = data.get('fio')
    operating_mode = data.get('operating_mode')
    delivery = data.get('delivery')
    await state.finish()
    res0 = await sql_object.sql_get_info()
    # Защитим от перезаписи не пустое значение поля таблицы, значением None.
    # в базу пишется только одна строка (запись), когда создаеться таблица,
    # и дальше эта строка только перезаписываеться.
    # если данные (data.get()) None и в поле таблицы не None,
    # тогда данные (data.get()) поменять на значение из поля таблицы.

    if res0["telefon"] != "None" and tlf == 'None':
        tlf = res0["telefon"]
    if res0["full_name"] != "None" and full_name == 'None':
        full_name = res0["full_name"]
    if res0["operating_mode"] != "None" and operating_mode == 'None':
        operating_mode = res0["operating_mode"]
    if res0["delivery"] != "None" and delivery == 'None':
        delivery = res0["delivery"]

    await sql_object.sql_set_info(tlf=tlf, full_name=full_name, operating_mode=operating_mode, delivery=delivery)
    await asyncio.sleep(1)
    res = await sql_object.sql_get_info()
    await message.answer(
        f'<b><i><u>Телефон: </u></i></b><code>{res["telefon"]}</code>\n'
        f'<b><i><u>ФИО: </u></i></b><code>{res["full_name"]}</code>\n'
        f'<b><i><u>Режим работы: </u></i></b><code>{res["operating_mode"]}</code>\n'
        f'<b><i><u>Доставка: </u></i></b><code>{res["delivery"]}</code>\n'
    )
    await state.finish()


# ======================================================================================================

# =======================================тут мы пропускаем шаг и переходим на следующую стадию заполнения info
@dp.callback_query_handler(AdminFilter(is_admin=True), lambda c: c.data == 'pass step (kod 907554376)', state='*')
async def action_delete_product(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(emojize(':yarn:'))
    await callback_query.message.answer(f'вы отказалисль от ввода и перешли дальше. ')
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    current_state = await state.get_state()
    if current_state == 'AdminInfoStates:tlf':
        callback_query.message.text = "None"
        await end_action_tlf(message=callback_query.message, state=state)
    elif current_state == 'AdminInfoStates:FIO':
        callback_query.message.text = "None"
        await end_action_fio(message=callback_query.message, state=state)
    elif current_state == 'AdminInfoStates:operating_mode':
        callback_query.message.text = "None"
        await end_action_operation_mode(message=callback_query.message, state=state)
    elif current_state == 'AdminInfoStates:delivery':
        callback_query.message.text = "None"
        await end_action_delivery(message=callback_query.message, state=state)
    else:
        logging.info('что то пошло не так')


# ===========================================================================================


@dp.message_handler(commands=["admin"])
async def delete_text_admins(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, "<b><i><u>Ты не админ</u></i></b>")
