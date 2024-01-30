from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, ChatTypeFilter
from data.config import ADMINS
from loader import dp
from filters.admin_filter import AdminFilter


@dp.message_handler(CommandHelp(), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/menu - Начать диалог",
            "/help - Получить справку",
            "/admin - админстраторам"
            )

    await message.answer("\n".join(text))
