from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("cancel", "Завершить заявку"),
            types.BotCommand("info", "Вывести информацию о боте"),
            types.BotCommand("menu", "Вывести меню"),
            types.BotCommand("timeline", "Режим работы"),
            types.BotCommand("contacts", "Контакты"),
            types.BotCommand("delivery", "Доставка"),
            types.BotCommand("help", "помошь")
        ]
    )
