import datetime

from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import purchase_buttons, purchase_bird_buttons, add_eggs_buttons
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import purchase, purchase_bird, back_purchase, purchase_bird_txt, my_bird, add_eggs, add_eggs_txt
from bot.dispatcher import dp
from bot.handlers.variables import bird_types, bird_infos, variable
from db.model import Farm, Eggs, Birds


@dp.callback_query_handler(Text(back_purchase))
async def info_call(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer_photo(photo=open('images/purchase.jpg', 'rb'), caption=f"""<b>
💵 Sotib olish - bo'limidasiz
Siz bu yerda turli qushlarni sotib olishingiz,
tuxumlarni yi'g'ib olishingiz va qushlaringizni ko'rishingiz mumkin!

⬇️ Quyidagilardan birini tanlang:
    </b>""", parse_mode="HTML", reply_markup=await purchase_buttons())


@dp.message_handler(Text(purchase))
async def purchase_menu(msg: types.Message):
    await msg.answer_photo(photo=open('images/purchase.jpg', 'rb'), caption=f"""<b>
💵 Sotib olish - bo'limidasiz
Siz bu yerda turli qushlarni sotib olishingiz,
tuxumlarni yi'g'ib olishingiz va qushlaringizni ko'rishingiz mumkin!

⬇️ Quyidagilardan birini tanlang:
</b>""", parse_mode="HTML", reply_markup=await purchase_buttons())


@dp.callback_query_handler(Text(purchase_bird))
async def purchase_bird(call: types.CallbackQuery):
    await call.message.delete()
    val = await variable("current")
    await call.message.answer_photo(open('images/bird1.jpg', 'rb'), caption=f"""<b>
1-Darajali qush

💶 Qush narxi: 10 {val}
🥚 Soatiga tuxumlar: 5 ta
</b>""", parse_mode="HTML", reply_markup=await purchase_bird_buttons(1))


@dp.callback_query_handler(Text(bird_types))
async def birds_types(call: types.CallbackQuery):
    ind = bird_types.index(call.data)
    amout, egg = bird_infos[ind].split('_')
    val = await variable("current")
    await call.message.delete()
    await call.message.answer_photo(open(f'images/bird{ind + 1}.jpg', 'rb'), caption=f"""<b>
{ind + 1}-Darajali qush

💶 Qush narxi: {amout} {val}
🥚 Soatiga tuxumlar: {egg} ta
    </b>""", parse_mode="HTML", reply_markup=await purchase_bird_buttons(ind + 1))


@dp.callback_query_handler(Text("✅"))
async def out_bird(call: types.CallbackQuery):
    await call.answer(text=f"⚠️ Siz shu qushni tanlagansiz!", show_alert=True)


@dp.callback_query_handler(Text(startswith=purchase_bird_txt))
async def purchase_bird(call: types.CallbackQuery):
    txt, id_ = call.data.split("_")
    amout, egg = bird_infos[int(id_) - 1].split("_")
    fuser = await Farm.get(str(call.from_user.id))
    if float(amout) > fuser[0].purchase:
        await call.answer(text="⚠️ Hisobingizda mablag' yetarli emas!", show_alert=True)
    else:
        id_ = int(id_)
        await Birds.create(chat_id=str(call.from_user.id), type=id_,
                           vitamin=datetime.datetime.now() - datetime.timedelta(days=1))
        if id_ == 1:
            await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase - float(amout),
                              bird1=fuser[0].bird1 + 1)
        elif id_ == 2:
            await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase - float(amout),
                              bird2=fuser[0].bird2 + 1)
        elif id_ == 3:
            await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase - float(amout),
                              bird3=fuser[0].bird3 + 1)
        elif id_ == 4:
            await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase - float(amout),
                              bird4=fuser[0].bird4 + 1)
        elif id_ == 5:
            await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase - float(amout),
                              bird5=fuser[0].bird5 + 1)
        elif id_ == 6:
            await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase - float(amout),
                              bird6=fuser[0].bird6 + 1)
        else:
            await Farm.update(str(call.from_user.id), purchase=fuser[0].purchase - float(amout),
                              bird7=fuser[0].bird7 + 1)
        await call.answer(text=f"✅ {id_}-darajali qush sotib olindi", show_alert=True)
        count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
                fuser[0].bird7
        await call.message.answer(text=f"<b>✅ {id_}-darajali qush sotib olindi</b>",
                                  reply_markup=await main_menu_buttons(count), parse_mode="HTML")


@dp.callback_query_handler(Text(my_bird))
async def my_bird(call: types.CallbackQuery):
    fuser = await Farm.get(str(call.from_user.id))
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + fuser[
        0].bird7
    await call.answer(text=f"🦜 Sizdagi qushlar soni {count} ta", show_alert=True)


@dp.callback_query_handler(Text(add_eggs))
async def add_eggs(call: types.CallbackQuery):
    await call.message.delete()
    euser = await Eggs.get(str(call.from_user.id))
    fuser = await Farm.get(str(call.from_user.id))
    day_user = fuser[0].bird1 * 5 + fuser[0].bird2 * 30 + fuser[0].bird3 * 65 + fuser[0].bird4 * 130 + fuser[
        0].bird5 * 315 + fuser[0].bird6 * 630 + fuser[
                   0].bird7 * 1500
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + fuser[
        0].bird7
    await call.message.answer_photo(photo=open('images/add_eggs.jpg', 'rb'), caption=f"""<b>
Sizning daromad ma'lumotlaringiz:

🦜 Barcha qushlar: {count} ta
🥚 Kunlik tuxumlar: {day_user} ta
</b>""", parse_mode="HTML", reply_markup=await add_eggs_buttons(num=euser[0].eggs))


@dp.callback_query_handler(Text(add_eggs_txt))
async def add_egg(call: types.CallbackQuery):
    euser = await Eggs.get(str(call.from_user.id))
    fuser = await Farm.get(str(call.from_user.id))
    await Farm.update(str(call.from_user.id), eggs=fuser[0].eggs + euser[0].eggs)
    await Eggs.update(str(call.from_user.id), eggs=0)
    await call.answer(text=f"🥚 Siz {euser[0].eggs} ta tuxumni yi'g'ib oldingiz", show_alert=True)
