import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
from aiogram.utils.exceptions import ChatNotFound

from bot.buttons.inline_buttons import advert_buttons
from bot.buttons.reply_buttons import back_admin_menu, admin_buttons
from bot.buttons.text import advert, send_msg, send_forward, send_user
from bot.dispatcher import dp, bot
from db.model import User, Farm


@dp.message_handler(Text(advert))
async def advert_menu(msg: types.Message):
    await msg.answer(text=f"<b>📨 Yuboriladigan xabar turini tanlang:</b>", parse_mode="HTML",
                     reply_markup=await advert_buttons())


@dp.callback_query_handler(Text(send_msg))
async def send_msg(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state('send_msg')
    await call.message.answer(text=f"<b>📨 Xabarni yuboring</b>", parse_mode="HTML",
                              reply_markup=await back_admin_menu())


@dp.message_handler(state='send_msg', content_types=ContentType.ANY)
async def send_txt(msg: types.Message, state: FSMContext):
    users = await User.get_all()
    suc = 0
    session = await msg.answer(text="✅ Xabar yuborish boshlandi!", parse_mode="HTML")
    for user in users:
        try:
            await msg.copy_to(chat_id=int(user[0].chat_id), caption=msg.caption,
                              caption_entities=msg.caption_entities,
                              reply_markup=msg.reply_markup)
            suc += 1
            await asyncio.sleep(0.05)
        except ChatNotFound:
            pass
        except Exception:
            pass
    else:
        await session.delete()
        await msg.answer(
            text=f"<b>Habar userlarga tarqatildi✅\n\n{suc}-ta userga yetib bordi✅\n</b>",
            parse_mode="HTML", reply_markup=await admin_buttons())
    await state.finish()


@dp.callback_query_handler(Text(send_forward))
async def send_forward(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state('send_forward')
    await call.message.answer(text=f"<b>📨 Forward xabarni yuboring</b>", parse_mode="HTML",
                              reply_markup=await back_admin_menu())


@dp.message_handler(state='send_forward', content_types=ContentType.ANY)
async def forward_txt(msg: types.Message, state: FSMContext):
    users = await User.get_all()
    suc = 0
    session = await msg.answer(text="✅ Xabar yuborish boshlandi!", parse_mode="HTML")
    for user in users:
        try:
            await bot.forward_message(chat_id=int(user[0].chat_id), from_chat_id=msg.chat.id,
                                      message_id=msg.message_id)
            suc += 1
            await asyncio.sleep(0.05)
        except ChatNotFound:
            pass
    else:
        await session.delete()
        await msg.answer(
            text=f"<b>Habar userlarga tarqatildi✅\n\n{suc}-ta userga yetib bordi✅\n</b>",
            parse_mode="HTML", reply_markup=await admin_buttons())
    await state.finish()


@dp.message_handler(commands=['/restart'])
async def restart_bot(msg: types.Message):
    users = await User.get_all()
    for i in users:
        await User.delete(i[0].chat_id)
    farms = await Farm.get_all()
    for i in farms:
        await Farm.delete(i[0].chat_id)


@dp.callback_query_handler(Text(send_user))
async def send_user_id(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state("send_user_id")
    await call.message.answer(text=f"<b>👤 Foydalanuvchi ID raqamini yuboring:</b>", parse_mode="HTML",
                              reply_markup=await back_admin_menu())


@dp.message_handler(state='send_user_id')
async def send_user_txt(msg: types.Message, state: FSMContext):
    user = await User.get(msg.text)
    if user:
        await state.set_state('send_user')
        async with state.proxy() as data:
            data['user'] = user[0].chat_id
        await msg.answer(text=f"<b>📨 Xabarni yuboring</b>", parse_mode="HTML",
                         reply_markup=await back_admin_menu())
    else:
        await msg.answer(text=f"<b>❗️ Foydalanuvchi topilmadi\n👤 Foydalanuvchi ID raqamini yuboring:</b>",
                         parse_mode="HTML")


@dp.message_handler(state='send_user', content_types=ContentType.ANY)
async def send_user_msg(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    try:
        await msg.copy_to(chat_id=int(data['user']), caption=msg.caption,
                          caption_entities=msg.caption_entities,
                          reply_markup=msg.reply_markup)
        await msg.answer(text="<b>✅ Xabar yetbi bordi</b>", parse_mode="HTML", reply_markup=await admin_buttons())
    except ChatNotFound:
        await msg.answer(text=f"<b>❗️ {data['user']} botni bloklagan</b>", parse_mode='HTML',
                         reply_markup=await admin_buttons())
    await state.finish()
