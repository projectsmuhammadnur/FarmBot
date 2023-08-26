from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import settings_menu_button
from bot.buttons.reply_buttons import back_admin_menu
from bot.buttons.text import settings
from bot.dispatcher import dp
from bot.handlers.variables import edit


@dp.message_handler(Text(settings))
async def settinngs_menu(msg: types.Message):
    await msg.answer(text=f"<b>⚙️ Malumotlarni o'zgartirish</b>", parse_mode="HTML",
                     reply_markup=await settings_menu_button())


@dp.callback_query_handler(Text(
    ["current", "referal_%", "sub_egg", "min_sub_egg", "exchange_%", "bot_username", "contact", "payment_channel",
     "credit_%", "grain_price", "mutation_price", "vitamin_price"]))
async def edit_setings(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        data['key'] = call.data
    await state.set_state('new_value')
    await call.message.answer(text=f"<b>Yangi qiymatni kiriting</b>", parse_mode="HTML",
                              reply_markup=await back_admin_menu())


@dp.message_handler(state='new_value')
async def new_value(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    msg.text = int(msg.text)
    await edit(key=data['key'], value=msg.text)
    await state.finish()
    await msg.answer(text=f"<b>✅ Malumot o'zgartirildi</b>", parse_mode="HTML",
                     reply_markup=await settings_menu_button())
