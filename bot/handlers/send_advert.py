from time import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.utils.exceptions import ChatNotFound

from bot.dispatcher import dp
from bot.handlers import admins
from db.model import User


@dp.message_handler(commands='advert')
async def advert_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in admins:
        await state.set_state('advert')
        await msg.answer("<b>Habarni yuboring!</b>", parse_mode="HTML")


@dp.message_handler(state='advert', content_types=ContentType.ANY)
async def get_user_id_for_send_to_user(msg: types.Message, state: FSMContext):
    await state.finish()
    users = await User.get_all()
    suc = 0
    text = "*Session Started:*"
    session = await msg.bot.send_message(msg.from_user.id, text, 'MarkdownV2')
    for user in users:
        try:
            await msg.copy_to(chat_id=int(user[0].chat_id), caption=msg.caption,
                              caption_entities=msg.caption_entities,
                              reply_markup=msg.reply_markup)
            suc += 1
            await sleep(0.05)
        except ChatNotFound:
            pass
        except Exception:
            pass
    else:
        await session.delete()
        await msg.answer(
            text=f"<b>Habar userlarga tarqatildi✅\n\n{suc}-ta userga yetib bordi✅\n</b>",
            parse_mode="HTML")
