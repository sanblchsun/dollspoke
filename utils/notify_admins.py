import logging
from loader import Dispatcher
from aiogram.utils.exceptions import ChatNotFound
from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")
        except ChatNotFound as err:
            logging.exception(f'Указан администратор бота с не существующим ID\n {err}')

