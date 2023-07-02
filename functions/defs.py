import asyncio
import json

from aiogram import types

from loader import sql_object, bot


async def viewer_product_caption(my_id, last=False):
    res_get = await sql_object.sql_get_product(last=last)
    if res_get:
        for item in res_get:
            my_str = f'\n<b><i><u>Код товара: </u></i></b><code>{item["id"]}</code>\n' \
                     f'<b><i><u>Наименование: </u></i></b><code>{item["name"]}</code>\n' \
                     f'<b><i><u>Описание: </u></i></b><code>{item["description"]}</code>\n' \
                     f'<b><i><u>Цена (руб): </u></i></b><code>{item["price"]}</code>\n'
            ii = json.loads(item['img'])
            try:
                ii[0]["caption"] += my_str
            except KeyError:
                ii[0].update(caption=my_str)
            media_group = types.MediaGroup(medias=ii)
            await bot.send_media_group(my_id, media_group)
            await asyncio.sleep(0.3)
    else:
        await bot.send_message(my_id, "<b><i><u>Товара пока нет</u></i></B>")
