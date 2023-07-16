import json
import string
from aiogram import types
from emoji import emojize
from loader import dp, bot
from aiogram.types import ReplyKeyboardRemove



# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler()
async def bot_echo(message: types.Message):
    # Фильтр мата
    # if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
    #         .intersection(set(json.load(open('senz.json')))) != set():
    #     await bot.send_message(message.from_user.id, emojize(':squinting_face_with_tongue:'))
    #     await bot.send_message(message.from_user.id, "<b><i><u>Маты запрещены</u></i></b>", reply_markup=ReplyKeyboardRemove())
    #     await message.delete()
    await message.reply(emojize(':eye:'))
    await message.reply(text='<b><i><u>не верная команда</u></i></b>', reply_markup=ReplyKeyboardRemove())
        # await message.reply('<b>жирный</b>, <strong>жирный</strong>'
        #                     '<i>курсив</i>, <em>курсив</em>'
        #                     '<u>подчеркивание</u>, <ins>подчеркивание</ins>'
        #                     '<s>зачеркнуто</s>, <strike>зачеркнуто</strike>, <del>зачеркнуто</del>'
        #                     '<span class="tg-spoiler">скрытый текст</span>, <tg-spoiler>скрытый текст</tg-spoiler>')
        # await message.answer('<b>'
        #                      'bold '
        #                      '<i>'
        #                      'italic bold '
        #                      '<s>'
        #                      'italic bold strikethrough'
        #                      '<span class="tg-spoiler">'
        #                      'italic bold strikethrough spoiler'
        #                      '</span>'
        #                      '</s>'
        #                      '<u>'
        #                      'underline italic bold'
        #                      '</u>'
        #                      '</i>'
        #                      ' bold'
        #                      '</b>')
        # await message.answer('<a href="http://www.example.com/">встроенный URL-адрес</a>'
        #                      '<a href="tg://user?id=123456789">встроенное упоминание пользователя</a>'
        #                      '<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>'
        #                      '<code>встроенный код фиксированной ширины</code>'
        #                      '<pre>предварительно отформатированный блок кода фиксированной ширины</pre>')
        # await message.answer('<pre>'
        #                      '<code class="language-python">'
        #                      'предварительно отформатированный блок кода фиксированной ширины,'
        #                      'написанный на языке программирования Python'
        #                      '</code>'
        #                      '</pre>')
