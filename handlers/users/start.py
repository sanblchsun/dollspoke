from aiogram import types
from emoji import emojize

from loader import dp, bot
from keyboards.reply.buttons import menu_clients_start
from aiogram.dispatcher import FSMContext


@dp.message_handler(state='*', commands=['start', 'menu'])
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(emojize(':yarn:'))
    current_state = await state.get_state()
    if current_state is not None:
        await message.reply(f'<pre>{message.from_user.full_name}</pre> '
                            '\n<b><i>'
                            'вы сейчас находитесь в стадии админстрирования, что бы выйти из этого состояния, нажмине'
                            '</i></b>'
                            ' /cancel')
    else:
        await message.answer("<b><i>"
                             "Привет"
                             "</i></b>"
                             " <pre>"
                             f"{message.from_user.full_name}"
                             "</pre>\n "
                             "<b><i>"
                             "это бот для продажи вязаных кукол, ручной работы."
                             "</i></b>\n"
                             "<b><i>"
                             "Нажмите /product"
                             "</i></b>",
                             reply_markup=menu_clients_start())
