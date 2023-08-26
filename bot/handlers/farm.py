import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import vitamon_grain_button
from bot.buttons.reply_buttons import farm_buttons, back_farm_menu
from bot.buttons.text import farm, coop, grain, back_purchase, vitamin, mutant
from bot.dispatcher import dp
from bot.handlers.variables import variable
from db.model import Farm, Birds


@dp.message_handler(Text(back_purchase), state='*')
async def info_call(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=f"<b>{msg.text} bo'limidasiz</b>", parse_mode="HTML", reply_markup=await farm_buttons())


@dp.message_handler(Text(farm))
async def farm(msg: types.Message):
    await msg.answer(text=f"<b>{msg.text} bo'limidasiz</b>", parse_mode="HTML", reply_markup=await farm_buttons())


@dp.message_handler(Text(coop))
async def coop(msg: types.Message):
    await msg.answer(text=f"<b>✅ Katak tozalandi</b>", parse_mode="HTML")
    await Farm.update(str(msg.from_user.id), coop=datetime.datetime.now())


@dp.message_handler(Text(grain))
async def grain(msg: types.Message, state: FSMContext):
    val = await variable("current")
    grain_price = await variable('grain_price')
    await state.set_state('grain')
    await msg.answer(text=f"<b>🌾 Don qiymatini kiriting:\n\n1 kg don {grain_price} {val}</b>", parse_mode="HTML",
                     reply_markup=await back_farm_menu())


@dp.message_handler(state='grain')
async def grain_msg(msg: types.Message, state: FSMContext):
    val = await variable("current")
    grain_price = await variable('grain_price')
    fuser = await Farm.get(str(msg.from_user.id))
    try:
        if int(msg.text) <= 0:
            await msg.answer(
                text=f"<b>⚠️ Noto'g'ri qiymat❗️\n\n🌾 Don qiymatini kiriting:\n\n1 kg don {grain_price} {val}</b>",
                parse_mode="HTML",
                reply_markup=await back_farm_menu())
        elif int(msg.text) * grain_price > fuser[0].purchase:
            await msg.answer(
                text=f"<b>⚠️ Mablag' yetarli emas❗️\n\n🌾 Don qiymatini kiriting:\n\n1 kg don {grain_price} {val}</b>",
                parse_mode="HTML",
                reply_markup=await back_farm_menu())
        else:
            await state.set_state()
            await msg.answer(text=f"<b>✅ Don sotib olindi</b>", parse_mode="HTML", reply_markup=await farm_buttons())
            await Farm.update(str(msg.from_user.id), grain=int(msg.text),
                              purchase=fuser[0].purchase - int(msg.text) * grain_price)
    except ValueError:
        await msg.answer(
            text=f"<b>⚠️ Noto'g'ri qiymat❗️\n\n🌾 Don qiymatini kiriting:\n\n1 kg don {grain_price} {val}</b>",
            parse_mode="HTML",
            reply_markup=await back_farm_menu())


@dp.message_handler(Text(vitamin))
async def vitamin_add(msg: types.Message, state: FSMContext):
    await msg.answer(text=msg.text, reply_markup=await back_farm_menu())
    await state.set_state('vitamin')
    await msg.answer(text=f"<b>🦜 Qaysi darajali qushingizga vitamin berasiz</b>", parse_mode="HTML",
                     reply_markup=await vitamon_grain_button(msg.from_user.id))


@dp.message_handler(Text(vitamin))
async def vitamin_add(msg: types.Message, state: FSMContext):
    await msg.answer(text=msg.text, reply_markup=await back_farm_menu())
    await state.set_state('vitamin')
    await msg.answer(text=f"<b>🦜 Qaysi darajali qushingizga vitamin berasiz</b>", parse_mode="HTML",
                     reply_markup=await vitamon_grain_button(msg.from_user.id))


@dp.callback_query_handler(Text(endswith="-Darajali qush"), state='vitamin')
async def vitamin_msg(call: types.CallbackQuery):
    num, txt = call.data.split("-")
    vitamin_price = await variable('vitamin_price')
    fuser = await Farm.get(str(call.from_user.id))
    if fuser[0].purchase < vitamin_price:
        await call.answer(text="⚠️ Mablag' yetarli emas❗️", show_alert=True)
    else:
        await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase - vitamin_price)
        await Birds.update_bird(id_=str(call.from_user.id), type_=int(num),
                                vitamin=datetime.datetime.now() + datetime.timedelta(days=7))
        await call.answer(text=f"✅ {call.data}ga vitamin berildi", show_alert=True)
        await call.message.edit_text(text=f"<b>🦜 Qaysi darajali qushingizga vitamin berasiz</b>", parse_mode="HTML",
                                     reply_markup=await vitamon_grain_button(call.from_user.id))


@dp.message_handler(Text(mutant))
async def mutant_add(msg: types.Message, state: FSMContext):
    await msg.answer(text=msg.text, reply_markup=await back_farm_menu())
    await state.set_state('mutant')
    await msg.answer(text=f"<b>🦜 Qaysi darajali qushingizni mutatsiya qilasiz</b>", parse_mode="HTML",
                     reply_markup=await vitamon_grain_button(msg.from_user.id))


@dp.callback_query_handler(Text(endswith="-Darajali qush"), state='mutant')
async def vitamin_msg(call: types.CallbackQuery):
    num, txt = call.data.split("-")
    mutation_price = await variable('mutation_price')
    fuser = await Farm.get(str(call.from_user.id))
    if fuser[0].purchase < mutation_price:
        await call.answer(text="⚠️ Mablag' yetarli emas❗️", show_alert=True)
    else:
        await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase - mutation_price)
        await Birds.update_bird(id_=str(call.from_user.id), type_=int(num),
                                mutation=datetime.datetime.now() + datetime.timedelta(days=7))
        await call.answer(text=f"✅ {call.data} mutatsiyalantirildi", show_alert=True)
        await call.message.edit_text(text=f"<b>🦜 Qaysi darajali qushingizga vitamin berasiz</b>", parse_mode="HTML",
                                     reply_markup=await vitamon_grain_button(call.from_user.id))
