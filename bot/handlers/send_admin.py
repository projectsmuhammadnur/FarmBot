from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from bot.buttons.inline_buttons import send_admin_button
from bot.buttons.reply_buttons import back_main_menu, main_menu_buttons
from bot.buttons.text import send_admin, reply_back
from bot.dispatcher import dp, bot
from bot.handlers.variables import admins
from db.model import Farm


@dp.message_handler(Text(send_admin))
async def send_admin(msg: types.Message, state: FSMContext):
    await state.set_state('send_admin')
    await msg.answer(text="<b>📝 Bot haqida biron bir savolingiz bo'lsa yozib qoldiring:</b>", parse_mode="HTML",
                     reply_markup=await back_main_menu())


@dp.message_handler(state='send_admin', content_types=ContentType.ANY)
async def get_user_id_for_send_to_user(msg: types.Message, state: FSMContext):
    fuser = await Farm.get(str(msg.from_user.id))
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
            fuser[0].bird7
    for i in await admins():
        await msg.copy_to(chat_id=int(i),
                          caption=f"<b>Yangi habar🆕\n\nID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>\nIsm-Familia: {msg.from_user.full_name}\n@Username: {msg.from_user.username}\n\n{msg.caption}</b>",
                          caption_entities=msg.caption_entities,
                          reply_markup=await send_admin_button(msg.reply_markup, str(msg.from_user.id)),
                          parse_mode="HTML")
    await msg.answer(text=f"<b>✅ Murojaatingiz yuborildi\n\nTez orada javob qaytaramiz!</b>", parse_mode="HTML",
                     reply_markup=await main_menu_buttons(count))
    await state.finish()


@dp.callback_query_handler(Text(startswith=reply_back))
async def reply_back(call: types.CallbackQuery, state: FSMContext):
    text, id_ = call.data.split("_")
    async with state.proxy() as data:
        data['id'] = id_
    await state.set_state('reply_back')
    await call.message.answer(text="<b>Habaringizni yozib qoldiring:</b>", parse_mode="HTML",
                              reply_markup=await back_main_menu())


@dp.message_handler(state='reply_back')
async def reply_back_msg(msg: types.Message, state: FSMContext):
    fuser = await Farm.get(str(msg.from_user.id))
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
            fuser[0].bird7
    async with state.proxy() as data:
        pass
    await bot.send_message(chat_id=int(data['id']), text=f"<b>📨Admin javobi: {msg.text}</b>", parse_mode="HTML")
    await msg.answer(text="<b>Habar yetib bordi✅</b>", parse_mode="HTML", reply_markup=await main_menu_buttons(count))
    await state.finish()
