from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from loader import bot


# class AdminFilter(BoundFilter):
#     key = 'is_admin'
#     ADMINS = []
#
#     def __init__(self, is_admin):
#         self.is_admin = is_admin
#
#     async def check(self, message: types.Message) -> bool:
#         user = message.from_user
#         return user.id in self.ADMINS
#
#     async def add_chat_id(self, id_add):
#         self.ADMINS.append(id_add)
#
#     async def clradm(self):
#         self.ADMINS.clear()


class AdminFilter(BoundFilter):
    key = 'is_admin'
    my_chat_id = []

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        try:
            res = await bot.get_chat_administrators(chat_id=self.my_chat_id[0])
        except Exception as e:
            return False
        for i in res:
            if message.from_user.id == i['user']['id']:
                return True
        return False

    async def my_chat_id_data(self, my_chat_id):
        self.my_chat_id.append(my_chat_id)

    async def clradm(self):
        self.my_chat_id.clear()
