from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import referal_button
from bot.buttons.text import referal
from bot.dispatcher import dp
from bot.handlers.variables import variable
from db.model import User


@dp.message_handler(Text(referal))
async def referal(msg: types.Message):
    user = await User.get(str(msg.from_user.id))
    val = await variable('referal_%')
    v = await variable("current")
    link = await variable("bot_username")
    await msg.answer(text=f"""<b>
👥 Hamkorlik dasturi orqali pul ishlash:

💳 Siz hamkorlar orqali quydagilarni olasiz:
1️⃣ Xar bir do'stingiz uchun 1 {v} beriladi,
2️⃣ Do'stingizni depozitidan {val}% miqdorda bonus beriladi

🔗 Sizning referal havolangiz:
<code>https://t.me/{link}?start={msg.from_user.id}</code>

👥 Sizning do'stlaringiz soni: {user[0].added_user} ta
</b>""", parse_mode="HTML", reply_markup=await referal_button(msg.from_user.id))
