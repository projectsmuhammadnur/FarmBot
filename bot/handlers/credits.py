from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_buttons import back_main_menu, main_menu_buttons
from bot.buttons.text import credit
from bot.dispatcher import dp
from db.model import Credits, Farm


@dp.message_handler(Text(credit))
async def credit_handler(msg: types.Message, state: FSMContext):
    await state.set_state('credit')
    await msg.answer(text=f"""<b>
📝 Kredit miqdorini kiriting:
</b>""", parse_mode="HTML", reply_markup=await back_main_menu())


@dp.message_handler(state='credit')
async def credit_msg(msg: types.Message, state: FSMContext):
    try:
        fuser = await Farm.get(str(msg.from_user.id))
        count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
                fuser[0].bird7
        if float(msg.text) <= 0:
            await msg.answer(text=f"<b>⚠️ Noto'g'ri qiymat❗️\n\n📝 Kredit miqdorini kiriting:</b>", parse_mode="HTML")
        else:
            await msg.answer(text=f"<b>✅ Kredit olindi</b>", parse_mode="HTML",
                             reply_markup=await main_menu_buttons(count))
            await state.finish()
            fuser = await Farm.get(str(msg.from_user.id))
            await Farm.update(id_=str(msg.from_user.id), purchase=fuser[0].purchase + float(msg.text))
            cuser = await Credits.get(str(msg.from_user.id))
            if cuser:
                await Credits.update(id_=str(msg.from_user.id), price=cuser[0].price + float(msg.text))
            else:
                await Credits.create(chat_id=str(msg.from_user.id), price=float(msg.text))
    except ValueError:
        await msg.answer(text=f"<b>⚠️ Noto'g'ri qiymat❗️\n\n📝 Kredit miqdorini kiriting:</b>", parse_mode="HTML")
