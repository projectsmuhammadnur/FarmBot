from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import cabinet_button
from bot.buttons.text import cabinet
from bot.dispatcher import dp
from bot.handlers.variables import variable
from db.model import Farm, User


@dp.message_handler(Text(cabinet))
async def cabinet(msg: types.Message):
    fuser = await Farm.get(str(msg.from_user.id))
    user = await User.get(str(msg.from_user.id))
    if user[0].add_user:
        auser = f"<a href='tg://user?id={user[0].add_user}'>{user[0].add_user}</a>"
    else:
        val = await variable('current')
        auser = "Hech kim"
    await msg.answer(f"""<b>
┌🏛 Sizning botdagi kabinetingiz
├
├ID raqamingiz: <code>{msg.from_user.id}</code>
├Xaridlar balansi: {fuser[0].purchase} {val}
├Yechish balansi: {fuser[0].take} {val}
├
├Do'stlaringiz soni: {user[0].added_user} ta
├Sizni taklif qildi: {auser}
├
├Sarmoyalaringiz: {fuser[0].invest} {val}
└Daromadlaringiz: {fuser[0].income} {val}
</b>""", parse_mode="HTML", reply_markup=await cabinet_button())
