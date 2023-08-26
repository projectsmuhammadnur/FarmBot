from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from bot.buttons.text import member_yes, reply_back, share, add_money, sub_money, sub_eggs, top_deposit, top_income, \
    payments, contacts, back, top_referal, purchase_bird, add_eggs, my_bird, purchase_bird_txt, back_purchase, \
    add_channel, sub_channel, add_admins, sub_admins, send_msg, send_forward, send_user, user_balance, ban_user, \
    unban_user, credit_pay
from bot.dispatcher import bot
from bot.handlers.variables import variable, bird_types, get_channels, get_admins, pay_url, api_key, store_id
from db.model import Farm, Birds, Ban


async def member_buttons():
    chats = await get_channels()
    design = []
    for i in chats.values():
        values = await bot.get_chat(int(i))
        design.append([InlineKeyboardButton(text=values.full_name, url=f"https://t.me/{values.username}")])
    design.append([InlineKeyboardButton(text=member_yes, callback_data=member_yes)])
    return InlineKeyboardMarkup(inline_keyboard=design)


async def send_admin_button(msg: InlineKeyboardMarkup, id: str):
    try:
        return msg.add([InlineKeyboardButton(text=reply_back, callback_data=reply_back + "_" + id)])
    except AttributeError:
        design = [[InlineKeyboardButton(text=reply_back, callback_data=reply_back + "_" + id)]]
        return InlineKeyboardMarkup(inline_keyboard=design)


async def referal_button(id_: int):
    link = await variable("bot_username")
    design = [
        [InlineKeyboardButton(text=share, url=f"https://t.me/share/url?url=https://t.me/{link}?start={id_}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def cabinet_button():
    design = [
        [InlineKeyboardButton(text=add_money, callback_data=add_money),
         InlineKeyboardButton(text=sub_money, callback_data=sub_money)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def eggs_buttons():
    design = [
        [InlineKeyboardButton(text=sub_eggs, callback_data=sub_eggs)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def info_buttons():
    design = [
        [InlineKeyboardButton(text=top_deposit, callback_data=top_deposit),
         InlineKeyboardButton(text=top_income, callback_data=top_income)],
        [InlineKeyboardButton(text=payments, url=await variable("payment_channel")),
         InlineKeyboardButton(text=contacts, url=await variable("contact"))],
        [InlineKeyboardButton(text=top_referal, callback_data=top_referal)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def back_info_button():
    design = [[InlineKeyboardButton(text=back, callback_data=back)]]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def purchase_buttons():
    design = [
        [InlineKeyboardButton(text=purchase_bird, callback_data=purchase_bird),
         InlineKeyboardButton(text=add_eggs, callback_data=add_eggs)],
        [InlineKeyboardButton(text=my_bird, callback_data=my_bird)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def purchase_bird_buttons(id_: int):
    design = [[]]
    s = 0
    for i in range(len(bird_types)):
        if i % 3 == 0:
            if i == id_ - 1:
                design.append([InlineKeyboardButton(text="✅", callback_data="✅")])
            else:
                design.append([InlineKeyboardButton(text=bird_types[i], callback_data=bird_types[i])])
            s += 1
        else:
            if i == id_ - 1:
                design[s].append(InlineKeyboardButton(text="✅", callback_data="✅"))
            else:
                design[s].append(InlineKeyboardButton(text=bird_types[i], callback_data=bird_types[i]))
    design.append([InlineKeyboardButton(text=purchase_bird_txt, callback_data=f"{purchase_bird_txt}_{id_}")])
    design.append([InlineKeyboardButton(text=back_purchase, callback_data=back_purchase)])
    return InlineKeyboardMarkup(inline_keyboard=design)


async def add_eggs_buttons(num: float):
    design = [[InlineKeyboardButton(text=f"➕ {num} tuxumlarni yig'ish", callback_data=f"➕ tuxumlarni yig'ish")]]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def vitamon_grain_button(id_: int):
    buser = await Birds.get_birds(str(id_))
    one, two, three, four, five, six, seven = 0, 0, 0, 0, 0, 0, 0
    for i in range(len(buser)):
        if buser[i][0].type == 1:
            one += 1
        elif buser[i][0].type == 2:
            two += 1
        elif buser[i][0].type == 3:
            three += 1
        elif buser[i][0].type == 4:
            four += 1
        elif buser[i][0].type == 5:
            five += 1
        elif buser[i][0].type == 6:
            six += 1
        else:
            seven += 1
    fuser = await Farm.get(str(id_))
    design = [[]]
    if fuser[0].bird1 - one > 0:
        design[0].append(InlineKeyboardButton(text="1-Darajali qush", callback_data='1-Darajali qush'))
    if fuser[0].bird2 - two > 0:
        design[0].append(InlineKeyboardButton(text="2-Darajali qush", callback_data='2-Darajali qush'))
    if fuser[0].bird3 - three > 0:
        design[0].append(InlineKeyboardButton(text="3-Darajali qush", callback_data='3-Darajali qush'))
    if fuser[0].bird4 - four > 0:
        design[0].append(InlineKeyboardButton(text="4-Darajali qush", callback_data='4-Darajali qush'))
    if fuser[0].bird5 - five > 0:
        design[0].append(InlineKeyboardButton(text="5-Darajali qush", callback_data='5-Darajali qush'))
    if fuser[0].bird6 - six > 0:
        design[0].append(InlineKeyboardButton(text="6-Darajali qush", callback_data='6-Darajali qush'))
    if fuser[0].bird7 - seven > 0:
        design[0].append(InlineKeyboardButton(text="7-Darajali qush", callback_data='7-Darajali qush'))
    return InlineKeyboardMarkup(inline_keyboard=design, row_width=3)


async def channel_butotns():
    design = [
        [InlineKeyboardButton(text=add_channel, callback_data=add_channel)],
        [InlineKeyboardButton(text=sub_channel, callback_data=sub_channel)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def sub_channel_button():
    ch = await get_channels()
    deisgn = []
    for i in ch.keys():
        deisgn.append([InlineKeyboardButton(text=i, callback_data=i)])
    return InlineKeyboardMarkup(inline_keyboard=deisgn)


async def admins_butotns():
    design = [
        [InlineKeyboardButton(text=add_admins, callback_data=add_admins)],
        [InlineKeyboardButton(text=sub_admins, callback_data=sub_admins)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def sub_admins_button():
    ch = await get_admins()
    deisgn = []
    for i in ch.keys():
        deisgn.append([InlineKeyboardButton(text=i, callback_data="admin_" + i)])
    return InlineKeyboardMarkup(inline_keyboard=deisgn)


async def advert_buttons():
    design = [
        [InlineKeyboardButton(text=send_msg, callback_data=send_msg),
         InlineKeyboardButton(text=send_forward, callback_data=send_forward)],
        [InlineKeyboardButton(text=send_user, callback_data=send_user)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def user_settings_button(id_: int):
    design = [
        [InlineKeyboardButton(text=user_balance, callback_data=f"{user_balance}_{id_}")],
    ]
    buser = await Ban.get(str(id_))
    if buser:
        design.append([InlineKeyboardButton(text=unban_user, callback_data=f"{unban_user}_{id_}")])
    else:
        design.append([InlineKeyboardButton(text=ban_user, callback_data=f"{ban_user}_{id_}")])
    return InlineKeyboardMarkup(inline_keyboard=design)


async def add_money_button(id_: int):
    design = [
        [InlineKeyboardButton(text="To'lash",
                              web_app=WebAppInfo(
                                  url=f"{pay_url}?api_key={api_key}&sum={200}&client={id_}&storeid={store_id}"))]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def settings_menu_button():
    design = [
        [InlineKeyboardButton(text="💱 Valyuta kursi", callback_data='current'),
         InlineKeyboardButton(text='👤 Referal', callback_data='referal_%')],
        [InlineKeyboardButton(text="🥚 Tuxum kursi", callback_data='sub_egg'),
         InlineKeyboardButton(text="🥚 Minimal tuxum", callback_data="min_sub_egg")],
        [InlineKeyboardButton(text="♻️ Balans o'zgartirish", callback_data='exchange_%'),
         InlineKeyboardButton(text="🤖 Bot username", callback_data="bot_username")],
        [InlineKeyboardButton(text="🧑‍💻 Admin profili", callback_data="contact"),
         InlineKeyboardButton(text="📝 To'lo'vlar kanali", callback_data="payment_channel")],
        [InlineKeyboardButton(text="➗ Kredit foizi", callback_data="credit_%"),
         InlineKeyboardButton(text="🌾 Don narxi", callback_data="grain_price")],
        [InlineKeyboardButton(text="🐣 Mutatsiya narxi", callback_data="mutation_price"),
         InlineKeyboardButton(text="💊 Vitamin narxi", callback_data="vitamin_price")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def credits_button():
    design = [
        [InlineKeyboardButton(text=credit_pay, callback_data=credit_pay)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def yes_or_no_admin_button(id_: int):
    design = [
        [InlineKeyboardButton(text="✅", callback_data=f"{id_}_✅"),
         InlineKeyboardButton(text="❌", callback_data=f"{id_}_❌")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def yes_or_no_user_button(id_: int):
    design = [
        [InlineKeyboardButton(text="✅", callback_data=f"✅_{id_}"),
         InlineKeyboardButton(text="❌", callback_data=f"❌_{id_}")],
        [InlineKeyboardButton(text=ban_user, callback_data=f"{ban_user}_{id_}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)
