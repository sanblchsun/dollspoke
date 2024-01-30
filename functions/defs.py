import asyncio
import json
from keyboards.inline.buttons import edit_like_dislike_and_buy
from aiogram import types

from loader import sql_object, bot


async def viewer_product_caption_media_group(my_id, last=False):
    res_get = await sql_object.sql_get_product(last=last)
    res = False
    for item in res_get:
        my_str = f'<b><i><u>Код товара: </u></i></b><code>{item["id"]}</code>\n' \
                 f'<b><i><u>Наименование: </u></i></b><code>{item["name"]}</code>\n' \
                 f'<b><i><u>Описание: </u></i></b><code>{item["description"]}</code>\n' \
                 f'<b><i><u>Цена (руб): </u></i></b><code>{item["price"]}</code>\n' \
                 f'<b><i><u>Количество: </u></i></b><code>{item["count"]}</code>'
        ii = json.loads(item['img'])
        for i in ii:
            i.update(caption=f'<b><i><u>Код товара: </u></i></b><code>{item["id"]}</code>\n' \
                             f'<b><i><u>Наименование: </u></i></b><code>{item["name"]}</code>')

        media_group = types.MediaGroup(medias=ii)
        await bot.send_media_group(my_id, media_group)
        await bot.send_message(my_id, my_str, reply_markup=edit_like_dislike_and_buy(heard=item['heard'],
                                                                                     like=item['like'],
                                                                                     dislike=item['dislike']))
        await asyncio.sleep(0.3)
        res = True
    return res


async def viewer_product_caption_photo(my_id, keyboard=None):
    res_get = await sql_object.sql_get_product()
    res = False
    for item in res_get:
        my_str = f'<b><i><u>Код товара: </u></i></b><code>{item["id"]}</code>\n' \
                 f'<b><i><u>Наименование: </u></i></b><code>{item["name"]}</code>\n' \
                 f'<b><i><u>Описание: </u></i></b><code>{item["description"]}</code>\n' \
                 f'<b><i><u>Цена (руб): </u></i></b><code>{item["price"]}</code>\n' \
                 f'<b><i><u>Количество: </u></i></b><code>{item["count"]}</code>'
        photo_id = json.loads(item['img'])[0]['media']
        await bot.send_photo(my_id, photo=photo_id, reply_markup=keyboard, caption=my_str)
        await asyncio.sleep(0.3)
        res = True
    return res

