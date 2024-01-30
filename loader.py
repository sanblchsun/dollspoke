from aiogram import Bot, Dispatcher, types
from data import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from base.sqlite_db import SQLighter
from middlewares import AlbumMiddleware

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(AlbumMiddleware(latency=0.3))
sql_object = SQLighter('base/db.db')
payments_token = config.PAYMENTS_TOKEN
