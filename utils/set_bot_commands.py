from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("product", "Показать товар"),
            types.BotCommand("cancel", "Завершить заявку"),
            types.BotCommand("menu", "Вывести меню"),
            types.BotCommand("help", "помошь")
        ]
    )
