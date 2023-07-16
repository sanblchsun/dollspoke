from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, ChatTypeFilter
from data.config import ADMINS
from loader import dp


@dp.message_handler(CommandHelp(), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def bot_help(message: types.Message):
    usr_id = message.from_user.id
    usr_id_str = str(usr_id)
    if usr_id_str in ADMINS:
        text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/admin - админстраторам"
                )
    else:
        text = ("Список команд: ",
                "/start - Начать диалог",
                "/help - Получить справку")

    await message.answer("\n".join(text))
