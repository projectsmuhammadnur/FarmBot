import asyncio
import datetime
import logging

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils import executor
from bot.handlers import *
from sqlalchemy import text

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.dispatcher import dp
from bot.middlewares import ThrottlingMiddleware
from db import db


async def create_all():
    await db.create_all()


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
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
        channels_ = await get_channels()
        for i in channels_.values():
            try:
                channel = await bot.get_chat_member(chat_id=i, user_id=user)
                if channel.status not in test1:
                    s = 0
            except ChatNotFound:
                pass
        buser = await Ban.get(str(user))
        if buser:
            try:
                await update.message.answer(text=f"<b>Siz bloklangansiz❌</b>", parse_mode="HTML",
                                            reply_markup=ReplyKeyboardRemove())
            except AttributeError:
                pass
            raise CancelHandler()
        if s == 0:
            try:
                await update.message.answer(text=f"<b>Bizning kanallarga obuna bo'lmagansiz❌</b>", parse_mode="HTML",
                                            reply_markup=await member_buttons())
            except AttributeError:
                pass
            raise CancelHandler()


scheduler = AsyncIOScheduler()


@scheduler.scheduled_job("interval", hours=1)
async def auto():
    mutation_delete = text("""
DELETE FROM birds
WHERE birds.mutation < :current_time;
    """)
    birds_coop_delete = text("""
DELETE FROM birds
USING farm
WHERE birds.chat_id = farm.chat_id AND farm.coop < :d2_time;

        """)
    birds_delete = text("""
DELETE FROM birds 
WHERE grain < :time
        """)
    vitamin_1 = text("""
UPDATE eggs
SET eggs = eggs + 10
FROM birds
WHERE birds.type = 1
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin >= :current_time;
""")
    vitamin_2 = text("""
UPDATE eggs
SET eggs = eggs + 60
FROM birds
WHERE birds.type = 2
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin >= :current_time;
""")
    vitamin_3 = text("""
UPDATE eggs
SET eggs = eggs + 130
FROM birds
WHERE birds.type = 3
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin >= :current_time;
""")
    vitamin_4 = text("""
UPDATE eggs
SET eggs = eggs + 260
FROM birds
WHERE birds.type = 4
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin >= :current_time;
""")
    vitamin_5 = text("""
UPDATE eggs
SET eggs = eggs + 630
FROM birds
WHERE birds.type = 5
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin >= :current_time;
""")
    vitamin_6 = text("""
UPDATE eggs
SET eggs = eggs + 1260
FROM birds
WHERE birds.type = 6
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin >= :current_time;
""")
    vitamin_7 = text("""
UPDATE eggs
SET eggs = eggs + 3000
FROM birds
WHERE birds.type = 7
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin >= :current_time;
""")
    mutant_1 = text("""
UPDATE eggs
SET eggs = eggs + 10
FROM birds
WHERE birds.type = 1
AND eggs.chat_id = birds.chat_id 
AND birds.mutation >= :current_time;
""")
    mutant_2 = text("""
UPDATE eggs
SET eggs = eggs + 60
FROM birds
WHERE birds.type = 2
AND eggs.chat_id = birds.chat_id 
AND birds.mutation >= :current_time;
""")
    mutant_3 = text("""
UPDATE eggs
SET eggs = eggs + 130
FROM birds
WHERE birds.type = 3
AND eggs.chat_id = birds.chat_id 
AND birds.mutation >= :current_time;
""")
    mutant_4 = text("""
UPDATE eggs
SET eggs = eggs + 260
FROM birds
WHERE birds.type = 4
AND eggs.chat_id = birds.chat_id 
AND birds.mutation >= :current_time;
""")
    mutant_5 = text("""
UPDATE eggs
SET eggs = eggs + 630
FROM birds
WHERE birds.type = 5
AND eggs.chat_id = birds.chat_id 
AND birds.mutation >= :current_time;
""")
    mutant_6 = text("""
UPDATE eggs
SET eggs = eggs + 1260
FROM birds
WHERE birds.type = 6
AND eggs.chat_id = birds.chat_id 
AND birds.mutation >= :current_time;
""")
    mutant_7 = text("""
UPDATE eggs
SET eggs = eggs + 3000
FROM birds
WHERE birds.type = 7
AND eggs.chat_id = birds.chat_id 
AND birds.mutation >= :current_time;
""")
    bird_1 = text("""
UPDATE eggs
SET eggs = eggs + 5
FROM birds
WHERE birds.type = 1
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin < :current_time;
    """)
    bird_2 = text("""
UPDATE eggs
SET eggs = eggs + 30
FROM birds
WHERE birds.type = 2
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin < :current_time;
    """)
    bird_3 = text("""
UPDATE eggs
SET eggs = eggs + 65
FROM birds
WHERE birds.type = 3
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin < :current_time;
    """)
    bird_4 = text("""
UPDATE eggs
SET eggs = eggs + 130
FROM birds
WHERE birds.type = 4
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin < :current_time;
    """)
    bird_5 = text("""
UPDATE eggs
SET eggs = eggs + 315
FROM birds
WHERE birds.type = 5
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin < :current_time;
    """)
    bird_6 = text("""
UPDATE eggs
SET eggs = eggs + 630
FROM birds
WHERE birds.type = 6
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin < :current_time;
    """)
    bird_7 = text("""
UPDATE eggs
SET eggs = eggs + 1500
FROM birds
WHERE birds.type = 7
AND eggs.chat_id = birds.chat_id 
AND birds.vitamin < :current_time;
    """)
    grain_1 = text("""
UPDATE birds
SET grain = :current_time
FROM farm
WHERE birds.type = 1
AND farm.chat_id = birds.chat_id
AND birds.grain > :grain_time
AND farm.grain >= 1
AND farm.grain = farm.grain - 0.01;

""")
    grain_2 = text("""
UPDATE birds
SET grain = :current_time
FROM farm
WHERE birds.type = 2
AND farm.chat_id = birds.chat_id
AND birds.grain > :grain_time
AND farm.grain >= 1
AND farm.grain = farm.grain - 0.025;
    """)
    grain_3 = text("""
UPDATE birds
SET grain = :current_time
FROM farm
WHERE birds.type = 3
AND farm.chat_id = birds.chat_id
AND birds.grain > :grain_time
AND farm.grain >= 1
AND farm.grain = farm.grain - 0.05;
    """)
    grain_4 = text("""
UPDATE birds
SET grain = :current_time
FROM farm
WHERE birds.type = 4
AND farm.chat_id = birds.chat_id
AND birds.grain > :grain_time
AND farm.grain >= 1
AND farm.grain = farm.grain - 0.1;
    """)
    grain_5 = text("""
UPDATE birds
SET grain = :current_time
FROM farm
WHERE birds.type = 5
AND farm.chat_id = birds.chat_id
AND birds.grain > :grain_time
AND farm.grain >= 1
AND farm.grain = farm.grain - 0.25;
    """)
    grain_6 = text("""
UPDATE birds
SET grain = :current_time
FROM farm
WHERE birds.type = 6
AND farm.chat_id = birds.chat_id
AND birds.grain > :grain_time
AND farm.grain >= 1
AND farm.grain = farm.grain - 0.5;
    """)
    grain_7 = text("""
UPDATE birds
SET grain = :current_time
FROM farm
WHERE birds.type = 7
AND farm.chat_id = birds.chat_id
AND birds.grain > :grain_time
AND farm.grain >= 1
AND farm.grain = farm.grain - 1;
    """)
    day_user = text("""
    DELETE FROM dayusers
    WHERE created_at < :date
    """)
    vitamin_param = {
        "current_time": datetime.datetime.now(),
        "d2_time": datetime.datetime.now() + datetime.timedelta(hours=60),
        "grain_time": datetime.datetime.now() + datetime.timedelta(hours=1),
        "time": datetime.datetime.now() + datetime.timedelta(days=2),
        "date": datetime.datetime.now() + datetime.timedelta(days=1)
    }
    await db.execute(mutation_delete, vitamin_param)
    await db.commit()
    await db.execute(birds_coop_delete, vitamin_param)
    await db.commit()
    await db.execute(birds_delete, vitamin_param)
    await db.commit()
    await db.execute(day_user, vitamin_param)
    await db.commit()
    await db.execute(vitamin_1, vitamin_param)
    await db.commit()
    await db.execute(vitamin_2, vitamin_param)
    await db.commit()
    await db.execute(vitamin_3, vitamin_param)
    await db.commit()
    await db.execute(vitamin_4, vitamin_param)
    await db.commit()
    await db.execute(vitamin_5, vitamin_param)
    await db.commit()
    await db.execute(vitamin_6, vitamin_param)
    await db.commit()
    await db.execute(vitamin_7, vitamin_param)
    await db.commit()
    await db.execute(mutant_1, vitamin_param)
    await db.commit()
    await db.execute(mutant_2, vitamin_param)
    await db.commit()
    await db.execute(mutant_3, vitamin_param)
    await db.commit()
    await db.execute(mutant_4, vitamin_param)
    await db.commit()
    await db.execute(mutant_5, vitamin_param)
    await db.commit()
    await db.execute(mutant_6, vitamin_param)
    await db.commit()
    await db.execute(mutant_7, vitamin_param)
    await db.commit()
    await db.execute(bird_1, vitamin_param)
    await db.commit()
    await db.execute(bird_2, vitamin_param)
    await db.commit()
    await db.execute(bird_3, vitamin_param)
    await db.commit()
    await db.execute(bird_4, vitamin_param)
    await db.commit()
    await db.execute(bird_5, vitamin_param)
    await db.commit()
    await db.execute(bird_6, vitamin_param)
    await db.commit()
    await db.execute(bird_7, vitamin_param)
    await db.commit()
    await db.execute(grain_1, vitamin_param)
    await db.commit()
    await db.execute(grain_2, vitamin_param)
    await db.commit()
    await db.execute(grain_3, vitamin_param)
    await db.commit()
    await db.execute(grain_4, vitamin_param)
    await db.commit()
    await db.execute(grain_5, vitamin_param)
    await db.commit()
    await db.execute(grain_6, vitamin_param)
    await db.commit()
    await db.execute(grain_7, vitamin_param)
    await db.commit()


if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(BigBrother())
    logging.basicConfig(level=logging.ERROR)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_all())
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
