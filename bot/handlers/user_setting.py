from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import user_settings_button
from bot.buttons.reply_buttons import back_admin_menu, admin_buttons
from bot.buttons.text import user_settings, ban_user, user_balance, unban_user
from bot.dispatcher import dp, bot
from bot.handlers.variables import variable
from db.model import User, Farm, Ban


@dp.message_handler(Text(user_settings))
async def user_settings_id(msg: types.Message, state: FSMContext):
    await state.set_state("settings_user_id")
    await msg.answer(text=f"<b>👤 Foydalanuvchi ID raqamini yuboring:</b>", parse_mode="HTML",
                     reply_markup=await back_admin_menu())


@dp.message_handler(state='settings_user_id')
async def send_user_txt(msg: types.Message, state: FSMContext):
    user = await User.get(msg.text)
    if user:
        fuser = await Farm.get(str(msg.text))
        val = await variable("current")
        if user[0].add_user:
            auser = f"<a href='tg://user?id={user[0].add_user}'>{user[0].add_user}</a>"
        else:
            auser = "Hech kim"
        await msg.answer(text=f"""<b>
┌🏛 Userning botdagi kabineti
├
├ID raqami: <code>{user[0].chat_id}</code>
├Xaridlar balansi: {fuser[0].purchase} {val}
├Yechish balansi: {fuser[0].take} {val}
├
├Do'stlari soni: {user[0].added_user} ta
├Taklif qildi: {auser}
├
├Sarmoyasi: {fuser[0].invest} {val}
└Daromadi: {fuser[0].income} {val}
</b>""", parse_mode="HTML", reply_markup=await user_settings_button(msg.text))
        await state.finish()
    else:
        await msg.answer(text=f"<b>❗️ Foydalanuvchi topilmadi\n👤 Foydalanuvchi ID raqamini yuboring:</b>",
                         parse_mode="HTML")


@dp.callback_query_handler(Text(startswith=ban_user))
async def ban_user_handler(call: types.CallbackQuery):
    txt, id_ = call.data.split("_")
    await Ban.create(chat_id=id_)
    await call.answer(text="🔕 Foydalanuvchi ban oldi", show_alert=True)
    await call.message.edit_text(text=call.message.text, parse_mode="HTML",
                                 reply_markup=await user_settings_button(id_))


@dp.callback_query_handler(Text(startswith=unban_user))
async def ban_user_handler(call: types.CallbackQuery):
    txt, id_ = call.data.split("_")
    await Ban.delete(id_)
    await call.answer(text="🔔 Foydalanuvchi bandan olindi", show_alert=True)
    await call.message.edit_text(text=call.message.text, parse_mode="HTML",
                                 reply_markup=await user_settings_button(id_))


@dp.callback_query_handler(Text(startswith=user_balance))
async def user_balance(call: types.CallbackQuery, state: FSMContext):
    txt, id_ = call.data.split("_")
    await call.message.delete()
    async with state.proxy() as data:
        data['id'] = id_
    await state.set_state('user_balance')
    await call.message.answer(text=f"<b>💰 Balansini qancha qilasiz</b>", parse_mode="HTML",
                              reply_markup=await back_admin_menu())


@dp.message_handler(state='user_balance')
async def balance_add(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    await Farm.update(data['id'], purchase=float(msg.text))
    await bot.send_message(chat_id=int(data['id']), text=f"<b>💰 Balansingiz {msg.text} ga o'zgartirildi</b>",
                           parse_mode="HTML")
    await msg.answer(text=f"<b>✅ Balans o'zgartirildi</b>", parse_mode="HTML", reply_markup=await admin_buttons())
    await state.finish()
