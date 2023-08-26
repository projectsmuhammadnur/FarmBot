import datetime

from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import info_buttons, back_info_button
from bot.buttons.text import info, top_deposit, back, top_income, top_referal
from bot.dispatcher import dp
from bot.handlers.variables import variable
from db.model import User, Dayuser, Farm

created_time = datetime.datetime.now()


@dp.callback_query_handler(Text(back))
async def info_call(call: types.CallbackQuery):
    username = await variable('bot_username')
    users = await User.get_all()
    dusers = await Dayuser.get_all()
    day_later = (created_time.day - datetime.datetime.now().day)
    await call.message.edit_text(text=f"""<b>
@{username} - Loyiha statistikasi:

👥 Aktiv foydalanuvchilar: {len(users)} ta
👥 Bugun kirgan odamlar: {len(dusers)} ta

📆 Botimiz ishlamoqda: {day_later + 1} kun
</b>""", parse_mode="HTML", reply_markup=await info_buttons())


@dp.message_handler(Text(info))
async def info_msg(msg: types.Message):
    username = await variable('bot_username')
    users = await User.get_all()
    dusers = await Dayuser.get_all()
    day_later = (created_time.day - datetime.datetime.now().day)
    await msg.answer(text=f"""<b>
@{username} - Loyiha statistikasi:

👥 Aktiv foydalanuvchilar: {len(users)} ta
👥 Bugun kirgan odamlar: {len(dusers)} ta

📆 Botimiz ishlamoqda: {day_later + 1} kun
</b>""", parse_mode="HTML", reply_markup=await info_buttons())


@dp.callback_query_handler(Text(top_deposit))
async def top_deposit(call: types.CallbackQuery):
    users = await Farm.get_top('invest')
    reply = "<b>🏆 TOP 10 Pul kititganlar:\n\n"
    val = await variable("current")
    for i in range(len(users)):
        reply += f"{i + 1}. <a href='tg://user?id={users[i][0].chat_id}'>{users[i][0].chat_id}</a> - {users[i][0].invest} {val}\n"
    reply += '</b>'
    await call.message.edit_text(text=reply, parse_mode="HTML", reply_markup=await back_info_button())


@dp.callback_query_handler(Text(top_income))
async def top_deposit(call: types.CallbackQuery):
    users = await Farm.get_top('income')
    reply = "<b>🏆 TOP 10 Pul yechganlar:\n\n"
    val = await variable("current")
    for i in range(len(users)):
        reply += f"{i + 1}. <a href='tg://user?id={users[i][0].chat_id}'>{users[i][0].chat_id}</a> - {users[i][0].income} {val}\n"
    reply += '</b>'
    await call.message.edit_text(text=reply, parse_mode="HTML", reply_markup=await back_info_button())


@dp.callback_query_handler(Text(top_referal))
async def top_deposit(call: types.CallbackQuery):
    users = await User.get_top('member_user')
    reply = "<b>🏆 TOP 10 Pul Referallar:\n\n"
    for i in range(len(users)):
        reply += f"{i + 1}. <a href='tg://user?id={users[i][0].chat_id}'>{users[i][0].chat_id}</a> - {users[i][0].member_user} ta\n"
    reply += '</b>'
    await call.message.edit_text(text=reply, parse_mode="HTML", reply_markup=await back_info_button())
