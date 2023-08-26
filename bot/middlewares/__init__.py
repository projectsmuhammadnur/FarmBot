from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .checksub import BigBrother
from ..dispatcher import dp

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(BigBrother())

