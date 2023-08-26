from aiogram.types import ReplyKeyboardMarkup

from bot.buttons.text import send_admin, back, referal, cabinet, eggs, exchange, info, credit, purchase, farm, coop, \
    grain, vitamin, mutant, back_purchase, settings, channels, statistic, user_settings, advert, admin_menu, \
    admins_txt


async def main_menu_buttons(num: int):
    design = [
        [purchase, eggs],
        [cabinet, referal, exchange],
        [credit, info],
        [send_admin]
    ]
    if num != 0:
        design[0].append(farm)
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu():
    design = [
        [back]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def farm_buttons():
    design = [
        [coop, grain],
        [vitamin, mutant],
        [back]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_farm_menu():
    design = [
        [back_purchase]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_buttons():
    design = [
        [settings, statistic],
        [user_settings],
        [admins_txt, channels],
        [advert, back]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_admin_menu():
    design = [
        [admin_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
