from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import eggs_buttons
from bot.buttons.text import eggs, sub_eggs
from bot.dispatcher import dp
from bot.handlers.variables import variable
from db.model import Farm


@dp.message_handler(Text(eggs))
async def eggs(msg: types.Message):
    fuser = await Farm.get(str(msg.from_user.id))
    min_sub = await variable('min_sub_egg')
    sub = await variable('sub_egg')
    await msg.answer(f"""<b>
🏦 Barcha yig'ilgan tuxumlarni shu yerda sotishingiz mumkin!

📊 Tuxum valyuta kursi:
{sub} tuxum - 1 ₽

Tuxumlarni sotiganingizdan so'ng 50% miqdori Xaridlar balansiga 50% miqdori esa Yechish balansiga o'tkaziladi

🥚 Sizdagi tuxumlar soni: {fuser[0].eggs} ta
🛒 Minimal sotish miqdori: {min_sub} ta tuxum
</b>""", parse_mode="HTML", reply_markup=await eggs_buttons())


@dp.callback_query_handler(Text(sub_eggs))
async def sub_eggs(call: types.CallbackQuery):
    min_sub = await variable('min_sub_egg')
    sub = await variable('sub_egg')
    fuser = await Farm.get(str(call.from_user.id))
    if fuser[0].eggs < min_sub:
        await call.answer(text=f"⚠️ Minimal sotish miqdori {min_sub} ta tuxum", show_alert=True)
    else:
        val_ = fuser[0].eggs / sub
        val = val_ / 2
        await call.answer(text=f"💰 {fuser[0].eggs} ta tuxumni {val_} ₽ ga sotdingiz", show_alert=True)
        await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase + val, take=fuser[0].take + val, eggs=0)
        val = await variable("current")
        await call.message.edit_text(f"""<b>
🏦 Barcha yig'ilgan tuxumlarni shu yerda sotishingiz mumkin!

📊 Tuxum valyuta kursi:
{sub} tuxum - 1 {val}

Tuxumlarni sotiganingizdan so'ng 50% miqdori Xaridlar balansiga 50% miqdori esa Yechish balansiga o'tkaziladi

🥚 Sizdagi tuxumlar soni: {fuser[0].eggs} ta
🛒 Minimal sotish miqdori: {min_sub} ta tuxum
</b>""", parse_mode="HTML", reply_markup=await eggs_buttons())
