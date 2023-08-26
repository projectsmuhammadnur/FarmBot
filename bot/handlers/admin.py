from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import ChatNotFound

from bot.buttons.inline_buttons import channel_butotns, sub_channel_button, admins_butotns, sub_admins_button
from bot.buttons.reply_buttons import admin_buttons, back_admin_menu
from bot.buttons.text import statistic, channels, add_channel, admin_menu, sub_channel, admins_txt, add_admins, \
    sub_admins
from bot.dispatcher import dp, bot
from bot.handlers.variables import admins, get_channels, add_channels, sub_channels, get_admins, sub_admin, add_admin
from db.model import User, Dayuser


@dp.message_handler(Text(admin_menu), state='*')
async def admin(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=f"<b>👨‍💻 Admin paneliga xush kelibsiz!</b>", parse_mode="HTML",
                     reply_markup=await admin_buttons())


@dp.message_handler(commands='admin')
async def admin(msg: types.Message):
    if msg.from_user.id in await admins():
        await msg.answer(text=f"<b>👨‍💻 Admin paneliga xush kelibsiz!</b>", parse_mode="HTML",
                         reply_markup=await admin_buttons())


@dp.message_handler(Text(statistic))
async def statistic(msg: types.Message):
    fuser = await User.get_all()
    dusers = await Dayuser.get_all()
    await msg.answer(f"<b>👥 Foydalanuvchilar: {len(fuser)} ta\n👥 Bugun kirgan odamlar: {len(dusers)} ta</b>",
                     parse_mode="HTML")


@dp.message_handler(Text(channels))
async def channels_handler(msg: types.Message):
    ch = await get_channels()
    reply = f"<b>📢 Ulangan kanallar soni {len(ch)}\n\n"
    k = 0
    for i in ch.values():
        k += 1
        reply += f"🆔 {k}-kanal ID si) <code>{i}</code>\n"
    reply += "</b>"
    await msg.answer(text=reply, parse_mode="HTML", reply_markup=await channel_butotns())


@dp.callback_query_handler(Text(add_channel))
async def channel_add(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state('channel_id')
    await call.message.answer(text=f"<b>🆔 Kanal ID sini yuboring ❗️ Bot kanalga admin bo'lishi zarur</b>",
                              parse_mode="HTML", reply_markup=await back_admin_menu())


@dp.message_handler(state='channel_id')
async def channel_id(msg: types.Message, state: FSMContext):
    try:
        user = await bot.get_chat_member(chat_id=msg.text, user_id=msg.from_user.id)
        await add_channels(id_=msg.text)
        await msg.answer(text=f"<b>✅ Kanal ulandi</b>", parse_mode="HTML", reply_markup=await admin_buttons())
        await state.finish()
    except ChatNotFound:
        await msg.answer(text=f"<b>❗️ Bunday kanal mavjud emas yoki bot amdin emas\n🆔 Kanal ID sini yuboring</b>",
                         parse_mode="HTML")


@dp.callback_query_handler(Text(sub_channel))
async def channel_sub(call: types.CallbackQuery):
    await call.message.edit_text(text=f"<b>🪓 Qaysi kanalni o'chirasiz</b>", parse_mode="HTML",
                                 reply_markup=await sub_channel_button())


@dp.callback_query_handler(Text(startswith='-'))
async def channel_sub_id(call: types.CallbackQuery):
    await sub_channels(int(call.data))
    await call.answer(text="✅ Kanal o'chirib tashlandi")
    await call.message.edit_text(text=f"<b>🪓 Qaysi kanalni o'chirasiz</b>", parse_mode="HTML",
                                 reply_markup=await sub_channel_button())


@dp.message_handler(Text(admins_txt))
async def admin_msg(msg: types.Message):
    ch = await get_admins()
    reply = f"<b>🧑‍💻 Adminlar soni {len(ch)}\n\n"
    k = 0
    for i in ch.values():
        k += 1
        reply += f"🆔 {k}-admin ID si) <a href='tg://user?id={i}'>{i}</a>\n"
    reply += "</b>"
    await msg.answer(text=reply, parse_mode="HTML", reply_markup=await admins_butotns())


@dp.callback_query_handler(Text(add_admins))
async def channel_add(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state('admin_id')
    await call.message.answer(text=f"<b>🆔 User ID sini yuboring ❗️ User botni ishlatgan bo'lishi zarur</b>",
                              parse_mode="HTML", reply_markup=await back_admin_menu())


@dp.message_handler(state='admin_id')
async def channel_id(msg: types.Message, state: FSMContext):
    user = await User.get(str(msg.text))
    if user:
        await add_admin(id_=msg.text)
        await msg.answer(text=f"<b>✅ Admin qo'shildi</b>", parse_mode="HTML", reply_markup=await admin_buttons())
        await state.finish()
    else:
        await msg.answer(text=f"<b>❗️ Bu user botni ishlatmagan\n🆔 User ID sini yuboring</b>",
                         parse_mode="HTML")


@dp.callback_query_handler(Text(sub_admins))
async def channel_sub(call: types.CallbackQuery):
    await call.message.edit_text(text=f"<b>🪓 Qaysi adminni o'chirasiz</b>", parse_mode="HTML",
                                 reply_markup=await sub_admins_button())


@dp.callback_query_handler(Text(startswith='admin'))
async def channel_sub_id(call: types.CallbackQuery):
    await sub_admin(int(call.data.split("_")[1]))
    await call.answer(text="✅ Admin o'chirib tashlandi")
    await call.message.edit_text(text=f"<b>🪓 Qaysi adminni o'chirasiz</b>", parse_mode="HTML",
                                 reply_markup=await sub_admins_button())
    