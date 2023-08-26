from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text

from bot.buttons.inline_buttons import member_buttons
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import back
from bot.dispatcher import dp, bot
from bot.handlers.variables import get_member_channel, admins, variable
from db.model import User, Farm, Dayuser, Eggs


@dp.message_handler(commands='cancel', state="*")
async def back_command(msg: types.Message, state: FSMContext):
    fuser = await Farm.get(str(msg.from_user.id))
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
            fuser[0].bird7
    await msg.answer_photo(photo=open('images/start.jpg', 'rb'), caption=f"""<b>
🇺🇿 Assalomu alaykum {msg.from_user.first_name}

📝 Fermamizning qoidalari:
├─Do'stlaringizni botga taklif qiling,
├─Qushlarimizni sotib oling,
├─Tuxumlarini yig'ing va soting,
└─Pulni hamyonga yechib oling
        </b>""", parse_mode="HTML", reply_markup=await main_menu_buttons(count))
    await state.finish()


@dp.message_handler(Text(back), state="*")
async def back_msg(msg: types.Message, state: FSMContext):
    fuser = await Farm.get(str(msg.from_user.id))
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
            fuser[0].bird7
    await msg.answer_photo(photo=open('images/start.jpg', 'rb'), caption=f"""<b>
🇺🇿 Assalomu alaykum {msg.from_user.first_name}

📝 Fermamizning qoidalari:
├─Do'stlaringizni botga taklif qiling,
├─Qushlarimizni sotib oling,
├─Tuxumlarini yig'ing va soting,
└─Pulni hamyonga yechib oling
        </b>""", parse_mode="HTML", reply_markup=await main_menu_buttons(count))
    await state.finish()


@dp.message_handler(CommandStart())
async def start(msg: types.Message, state: FSMContext):
    try:
        fuser = await Farm.get(str(msg.from_user.id))
        count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
                fuser[0].bird7
    except TypeError:
        count = 0
    s = 0
    channel = await get_member_channel(msg.from_user.id)
    if channel == 0:
        await state.set_state('member')
        await msg.answer(text=f"<b>Bizning kanallarga obuna bo'lmagansiz❌</b>", parse_mode="HTML",
                         reply_markup=await member_buttons())
        s += 1
    else:
        await msg.answer_photo(photo=open('images/start.jpg', 'rb'), caption=f"""<b>
🇺🇿 Assalomu alaykum {msg.from_user.first_name}

📝 Fermamizning qoidalari:
├─Do'stlaringizni botga taklif qiling,
├─Qushlarimizni sotib oling,
├─Tuxumlarini yig'ing va soting,
└─Pulni hamyonga yechib oling
    </b>""", parse_mode="HTML", reply_markup=await main_menu_buttons(count))
    user = await User.get(str(msg.from_user.id))
    if user is None:
        await Eggs.create(chat_id=str(msg.from_user.id))
        await User.create(chat_id=str(msg.from_user.id), username=msg.from_user.username,
                          full_name=msg.from_user.full_name)
        await Farm.create(chat_id=str(msg.from_user.id))
        await Dayuser.create(chat_id=str(msg.from_user.id))
        for i in await admins():
            await bot.send_message(chat_id=i,
                                   text=f"<b>Yangi user🆕\nID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>\nIsm-Familiya: {msg.from_user.full_name}\nUsername: @{msg.from_user.username}\n</b>",
                                   parse_mode='HTML')
        if msg.get_args() != '':
            user = await User.get(msg.get_args())
            if user:
                if s == 1:
                    async with state.proxy() as data:
                        data['id'] = msg.get_args()
                    await bot.send_message(chat_id=int(msg.get_args()), text="""<b>
📳 Sizda yangi taklif mavjud!
    
Do'stingiz to'liq ro'yxatdan o'tmagunicha sizga referal pul berilmaydi</b>""", parse_mode="HTML")
                    await User.update(msg.get_args(), added_user=user[0].added_user + 1)
                    await User.update(str(msg.from_user.id), add_user=msg.get_args())
                else:
                    val = await variable("current")
                    await bot.send_message(chat_id=int(msg.get_args()), text=f"<b>Hisobingizga 1 {val} qo'shildi!</b>",
                                           parse_mode="HTML")
                    await User.update(msg.get_args(), added_user=user[0].added_user + 1,
                                      member_user=user[0].member_user + 1)
                    fuser = await Farm.get(msg.get_args())
                    await Farm.update(msg.get_args(), purchase=fuser[0].purchase + 1)
                    await User.update(str(msg.from_user.id), add_user=msg.get_args())


@dp.callback_query_handler(state='member')
async def member(call: types.CallbackQuery, state: FSMContext):
    fuser = await Farm.get(str(call.from_user.id))
    count = fuser[0].bird1 + fuser[0].bird2 + fuser[0].bird3 + fuser[0].bird4 + fuser[0].bird5 + fuser[0].bird6 + \
            fuser[0].bird7
    async with state.proxy() as data:
        pass
    s = 0
    channel = await get_member_channel(call.from_user.id)
    if channel == 0:
        await state.set_state('member')
        await call.answer(text=f"Bizning kanallarga obuna bo'lmagansiz", show_alert=True)
        s += 1
    else:
        await call.message.delete()
        await call.message.answer_photo(photo=open('images/start.jpg', 'rb'), caption=f"""<b>
🇺🇿 Assalomu alaykum {call.from_user.first_name}

📝 Fermamizning qoidalari:
├─Do'stlaringizni botga taklif qiling,
├─Qushlarimizni sotib oling,
├─Tuxumlarini yig'ing va soting,
└─Pulni hamyonga yechib oling
    </b>""", parse_mode="HTML", reply_markup=await main_menu_buttons(count))
        try:
            user = await User.get(data['id'])
            fuser = await Farm.get(data['id'])
            val = await variable("current")
            await bot.send_message(chat_id=int(data['id']), text=f"<b>Hisobingizga 1 {val} qo'shildi!</b>",
                                   parse_mode="HTML")
            await User.update(data['id'], member_user=user[0].member_user + 1)
            await Farm.update(data['id'], purchase=fuser[0].purchase + 1)
        except KeyError:
            pass
