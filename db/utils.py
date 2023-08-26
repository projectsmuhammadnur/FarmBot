import datetime

from sqlalchemy import delete as sqlalchemy_delete, desc, or_
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from db import Base, db

db.init()


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def create(cls, **kwargs):
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.chat_id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def update_bird(cls, id_: str, type_: int, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.chat_id == id_, cls.type == type_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get(cls, id_):
        query = select(cls).where(cls.chat_id == id_)
        objects = await db.execute(query)
        object_ = objects.first()
        return object_

    @classmethod
    async def delete(cls, id_):
        query = (
            sqlalchemy_delete(cls)
            .where(cls.chat_id == id_)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get_all(cls):
        query = select(cls)
        objects = await db.execute(query)
        return objects.all()

    @classmethod
    async def get_top(cls, name: str):
        query = select(cls).order_by(desc(name)).limit(10)
        objects = await db.execute(query)
        return objects.all()

    @classmethod
    async def get_birds(cls, id_):
        query = select(cls).where(
            cls.chat_id == id_,
            or_(
                cls.mutation >= datetime.datetime.now(),
                cls.vitamin >= datetime.datetime.now()
            )
        )
        objects = await db.execute(query)
        object_ = objects.all()
        return object_


class CreatedModel(Base, AbstractClass):
    __abstract__ = True
