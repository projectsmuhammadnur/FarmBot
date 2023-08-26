from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_buttons import back_main_menu, main_menu_buttons
from bot.buttons.text import exchange
from bot.dispatcher import dp
from bot.handlers.variables import variable
from db.model import Farm


@dp.message_handler(Text(exchange))
async def exchange(msg: types.Message, state: FSMContext):
    ex = await variable('exchange_%')
    await state.set_state('exchange')
    await msg.answer(text=f"""<b>
♻️ Siz bu bo'limda balansingizdagi pullarni almashtirishingiz mumkin!

Yechish balansidagi pullarni Xaridlar balansiga o'tkaza olasiz va siz bu o'tkazmadan qo'shimcha {ex}% bonus olasiz

📝 Pul miqdorini kiriting:
</b>""", parse_mode="HTML", reply_markup=await back_main_menu())


@dp.message_handler(state='exchange')
async def exchange_msg(msg: types.Message, state: FSMContext):
    fuser = await Farm.get(str(msg.from_user.id))
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
            fuser[0].bird7
    ex = await variable('exchange_%')
    try:
        if int(msg.text) <= 0:
            await msg.answer(text=f"<b>⚠️ Noto'g'ri qiymat❗️\n\n📝 Pul miqdorini kiriting:</b>", parse_mode="HTML")
        elif fuser[0].take < int(msg.text):
            await msg.answer(text="<b>⚠️ Mablag' yetarli emas❗️\n\n📝 Pul miqdorini kiriting:</b>", parse_mode="HTML")
        else:
            await state.finish()
            await msg.answer(text="<b>✅ Almashtirildi</b>", parse_mode="HTML",
                             reply_markup=await main_menu_buttons(count))
            await Farm.update(str(msg.from_user.id), purchase=fuser[0].purchase + int(msg.text) + (int(msg.text) / ex),
                              take=fuser[0].take - int(msg.text))
    except ValueError:
        await msg.answer(text=f"<b>⚠️ Noto'g'ri qiymat❗️\n\n📝 Pul miqdorini kiriting:</b>", parse_mode="HTML")
