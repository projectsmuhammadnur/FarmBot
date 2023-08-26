from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.buttons.inline_buttons import member_buttons
from bot.dispatcher import bot
from bot.handlers.variables import get_channels


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update):
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else:
            return
        test1 = ['creator', 'administrator', 'member']
        s = 1
        for i in await get_channels():
            channel = await bot.get_chat_member(chat_id=i, user_id=user)
            if channel.status not in test1:
                s = 0

        if s == 0:
            await update.message.answer(text=f"<b>Bizning kanallarga obuna bo'lmagansiz❌</b>", parse_mode="HTML",
                                        reply_markup=await member_buttons())
            raise CancelHandler()
