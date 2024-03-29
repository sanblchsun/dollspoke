from aiogram.utils import executor
from loader import dp, sql_object
from utils import on_startup_notify, set_default_commands
import handlers, filters


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await  set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    sql_object.start()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
