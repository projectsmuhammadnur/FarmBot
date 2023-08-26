import json

from aiogram.utils.exceptions import ChatNotFound

from bot.dispatcher import bot

bird_types = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
bird_infos = ["10_5", "25_30", "50_65", "100_130", "250_315", "500_630", "1000_1500"]
pay_url = "https://5k.uz/api/pay"
api_key = "256dd01af7ff87b5fee3df89324b03c8"
store_id = "1669"
store_name = "Farm"


async def get_member_channel(user_id):
    with open('json_data/channels.json', 'r') as file:
        channels = json.load(file)
    test1 = ['creator', 'administrator', 'member']
    for i in channels.values():
        try:
            channel = await bot.get_chat_member(chat_id=i, user_id=user_id)
            if channel.status not in test1:
                return 0
        except ChatNotFound:
            pass
    else:
        return 1


async def get_channels():
    with open('json_data/channels.json', 'r') as file:
        channels = json.load(file)
    return channels


async def add_channels(id_: int):
    with open('json_data/channels.json', 'r') as file:
        channels = json.load(file)
    channels.update({str(id_): id_})
    with open('json_data/channels.json', 'w') as f:
        json.dump(channels, f, indent=4)


async def sub_channels(id_: int):
    with open('json_data/channels.json', 'r') as file:
        channels = json.load(file)
    channels.pop(str(id_))
    with open('json_data/channels.json', 'w') as f:
        json.dump(channels, f, indent=4)


async def get_admins():
    with open('json_data/admins.json', 'r') as file:
        channels = json.load(file)
    return channels


async def add_admin(id_: int):
    with open('json_data/admins.json', 'r') as file:
        channels = json.load(file)
    channels.update({str(id_): id_})
    with open('json_data/admins.json', 'w') as f:
        json.dump(channels, f, indent=4)


async def sub_admin(id_: int):
    with open('json_data/admins.json', 'r') as file:
        channels = json.load(file)
    channels.pop(str(id_))
    with open('json_data/admins.json', 'w') as f:
        json.dump(channels, f, indent=4)


async def admins():
    with open('json_data/admins.json', 'r') as f:
        admin = json.load(f)
    return admin.values()


async def variable(value: str):
    with open('json_data/variables.json', 'r') as f:
        data = json.load(f)
    try:
        return data[value]
    except KeyError:
        return 0


async def edit(key: str, value):
    with open('json_data/variables.json', 'r') as file:
        channels = json.load(file)
    channels[key] = value
    with open('json_data/variables.json', 'w') as f:
        json.dump(channels, f, indent=4)
