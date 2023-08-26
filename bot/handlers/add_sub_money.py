import datetime
import os
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from bot.buttons.inline_buttons import credits_button, cabinet_button, yes_or_no_admin_button, yes_or_no_user_button
from bot.buttons.reply_buttons import back_main_menu, main_menu_buttons, back_admin_menu
from bot.buttons.text import add_money, sub_money, credit_pay
from bot.dispatcher import dp, bot
from bot.handlers.variables import variable, admins
from db.model import Credits, Farm, User


@dp.callback_query_handler(Text(add_money))
async def add_money_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text=f"""<b>
To'l'ov uchun kartalar✅

💳UZKARD : <code>8600 1309 2432 6459</code>
👆ISM : ISMATOV NIGMATILLA
</b>""", parse_mode="HTML", reply_markup=await back_main_menu())
    await call.message.answer(
        text=f"<b>🖼 Tolov qilib chek rasmini yuboring❗️\n\nAdmin chekni tekshirib balansingizni to'ldiradi✅</b>",
        parse_mode="HTML")
    await state.set_state('chek_photo')


@dp.message_handler(content_types='photo', state='chek_photo')
async def chek_photo_handler(msg: types.Message, state: FSMContext):
    rand = str(random.randint(100000000, 999999999999))
    await msg.photo[-1].download(rand)
    for i in await admins():
        await bot.send_photo(i, photo=open(rand, 'rb'),
                             caption=f"""<b>
Yangi donat🆕

🆔User ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>

Pulni qabul qildingizmi?
</b>""", parse_mode="HTMl", reply_markup=await yes_or_no_user_button(msg.from_user.id, ))
    fuser = await Farm.get(str(msg.from_user.id))
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
            fuser[0].bird7
    await msg.answer(text=f"<b>✅ Malumot adminga yetib bordi</b>", parse_mode="HTML",
                     reply_markup=await main_menu_buttons(count))
    os.remove(rand)
    await state.finish()


@dp.callback_query_handler(Text(sub_money))
async def sub_money_handler(call: types.CallbackQuery, state: FSMContext):
    cuser = await Credits.get(str(call.from_user.id))
    cur = await variable("current")
    if cuser and cuser[0].days == -1:
        days = cuser[0].created_at
        val = await variable("credit_%")
        s = cuser[0].price + (datetime.datetime.now() - days).days * val / 30
        await call.message.edit_text(text=f"<b>❗️ Sizda {s} {cur} kredit mavjud. Avval kreditni tolang</b>",
                                     parse_mode="HTML",
                                     reply_markup=await credits_button())
    else:
        fuser = await Farm.get(str(call.from_user.id))
        mn = await variable('min_take')
        if fuser[0].take < mn:
            await call.answer(text=f"❌ Mablag' yetarli emas\n\nEng kam pul chiqarish {mn} {cur}", show_alert=True)
        else:
            async with state.proxy() as data:
                data['sum'] = fuser[0].take
            await state.set_state('card')
            await call.message.delete()
            await call.message.answer(text=f"<b>💳 Karta raqamingizni kiriting</b>", parse_mode="HTML",
                                      reply_markup=await back_main_menu())


@dp.message_handler(state='card')
async def card_purchase(msg: types.Message, state: FSMContext):
    fuser = await Farm.get(str(msg.from_user.id))
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
            fuser[0].bird7
    async with state.proxy() as data:
        pass
    await msg.answer(text=f"<b>✅ Malumot adminga yetib bordi</b>", parse_mode="HTML",
                     reply_markup=await main_menu_buttons(count))
    val = await variable("current")
    for i in await admins():
        await bot.send_message(chat_id=i, text=f"""<b>
🆕 Yangi pul chiqarish

🆔User ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
💳 Karta raqami: {msg.text}
💰 Miqdor: {data['sum']} {val}

Pul tushirib berdingizmi?
</b>""", parse_mode="HTML", reply_markup=await yes_or_no_admin_button(id_=msg.from_user.id))
    await state.finish()
    await Farm.update(id_=str(msg.from_user.id), take=0, income=fuser[0].take)


@dp.callback_query_handler(Text(credit_pay))
async def credit_pay_handler(call: types.CallbackQuery):
    cuser = await Credits.get(str(call.from_user.id))
    fuser = await Farm.get(str(call.from_user.id))
    days = cuser[0].created_at
    val = await variable("credit_%")
    s = cuser[0].price + (datetime.datetime.now() - days).days * val / 30
    if fuser[0].take >= s:
        await Farm.update(str(call.from_user.id), take=fuser[0].take - s)
        await Credits.update(str(call.from_user.id), price=0, days=(datetime.datetime.now() - days).days)
        user = await User.get(str(call.from_user.id))
        if user[0].add_user:
            auser = f"<a href='tg://user?id={user[0].add_user}'>{user[0].add_user}</a>"
        else:
            val = await variable('current')
            auser = "Hech kim"
        await call.message.edit_text(f"""<b>
┌🏛 Sizning botdagi kabinetingiz
├
├ID raqamingiz: <code>{call.from_user.id}</code>
├Xaridlar balansi: {fuser[0].purchase} {val}
├Yechish balansi: {fuser[0].take} {val}
├
├Do'stlaringiz soni: {user[0].added_user} ta
├Sizni taklif qildi: {auser}
├
├Sarmoyalaringiz: {fuser[0].invest} {val}
└Daromadlaringiz: {fuser[0].income} {val}
        </b>""", parse_mode="HTML", reply_markup=await cabinet_button())
        await call.answer(text="✅ Kredit to'landi", show_alert=True)
    else:
        await call.answer(text="❌ Mablag' yetarli emas", show_alert=True)


@dp.callback_query_handler(Text(endswith="✅"))
async def yes_take(call: types.CallbackQuery):
    chat_id, txt = call.data.split('_')
    await call.answer(text=f"✅ To'lo'v bajarildi", show_alert=True)
    await bot.send_message(chat_id=chat_id, text=f"<b>✅ Pul chiqarish uchun sorovingiz bajarildi</b>",
                           parse_mode="HTML")
    await call.message.delete()


@dp.callback_query_handler(Text(endswith="❌"))
async def no_take(call: types.CallbackQuery):
    chat_id, txt = call.data.split('_')
    await call.answer(text=f"❌ To'lo'v bekor qilindi", show_alert=True)
    await bot.send_message(chat_id=chat_id, text=f"<b>❌ Pul chiqarish uchun sorovingiz bekor qilindi</b>",
                           parse_mode="HTML")
    await call.message.delete()


@dp.callback_query_handler(Text(startswith="✅_"))
async def yes_user(call: types.CallbackQuery, state: FSMContext):
    txt, chat_id = call.data.split('_')
    async with state.proxy() as data:
        data['chat_id'] = chat_id
    await state.set_state("amout")
    await call.message.answer(text=f"<b>❓ Qancha pul tashlangan</b>", parse_mode="HTML",
                              reply_markup=await back_admin_menu())


@dp.message_handler(state='amout')
async def amout_handler(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            pass
        fuser = await Farm.get(str(msg.from_user.id))
        count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
                fuser[0].bird7
        if float(msg.text) <= 0:
            await msg.answer(text=f"<b>⚠️ Noto'g'ri qiymat❗️\n\n❓ Qancha pul tashlangan</b>", parse_mode="HTML")
        else:
            await Farm.update(id_=data['chat_id'], take=float(msg.text) / 2, purchase=float(msg.text) / 2,
                              invest=float(msg.text))
            await bot.send_message(chat_id=data['chat_id'],
                                   text=f"<b>✅ Pul kiritish uchun sorovingiz bajarilid</b>",
                                   parse_mode="HTML")
            await msg.answer(text=f"<b>✅ Pul qo'shildi</b>", parse_mode="HTML",
                             reply_markup=await main_menu_buttons(count))
            await state.finish()
    except ValueError:
        await msg.answer(text=f"<b>⚠️ Noto'g'ri qiymat❗️\n\n❓ Qancha pul tashlangan</b>", parse_mode="HTML")


@dp.callback_query_handler(Text(startswith="❌_"))
async def no_user(call: types.CallbackQuery):
    txt, chat_id = call.data.split('_')
    await call.answer(text=f"❌ To'lo'v bekor qilindi", show_alert=True)
    await bot.send_message(chat_id=chat_id, text=f"<b>❌ Pul kiritish uchun sorovingiz bekor qilindi</b>",
                           parse_mode="HTML")
    await call.message.delete()
