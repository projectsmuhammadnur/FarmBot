import datetime

from sqlalchemy import String, Integer, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from db import db
from db.utils import CreatedModel

db.init()


class User(CreatedModel):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(30))
    full_name: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(35), nullable=True)
    add_user: Mapped[str] = mapped_column(String(30), nullable=True)
    member_user: Mapped[int] = mapped_column(Integer, default=0)
    added_user: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(DateTime(), default=datetime.datetime.now)


class Farm(CreatedModel):
    __tablename__ = "farm"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(30))
    coop: Mapped[str] = mapped_column(DateTime, default=datetime.datetime.now)
    grain: Mapped[Float] = mapped_column(Float, default=0)
    bird1: Mapped[int] = mapped_column(Integer, default=0)
    bird2: Mapped[int] = mapped_column(Integer, default=0)
    bird3: Mapped[int] = mapped_column(Integer, default=0)
    bird4: Mapped[int] = mapped_column(Integer, default=0)
    bird5: Mapped[int] = mapped_column(Integer, default=0)
    bird6: Mapped[int] = mapped_column(Integer, default=0)
    bird7: Mapped[int] = mapped_column(Integer, default=0)
    eggs: Mapped[int] = mapped_column(Integer, default=0)
    purchase: Mapped[float] = mapped_column(Float, default=0)
    take: Mapped[float] = mapped_column(Float, default=0)
    invest: Mapped[float] = mapped_column(Float, default=0)
    income: Mapped[float] = mapped_column(Float, default=0)


class Dayuser(CreatedModel):
    __tablename__ = 'dayusers'
    chat_id: Mapped[str] = mapped_column(String(30), primary_key=True)


class Credits(CreatedModel):
    __tablename__ = 'credits'
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(30))
    price: Mapped[float] = mapped_column(Float)
    days: Mapped[int] = mapped_column(Integer, default=-1)
    created_at: Mapped[str] = mapped_column(DateTime(), default=datetime.datetime.now)


class Eggs(CreatedModel):
    __tablename__ = "eggs"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(30))
    eggs: Mapped[float] = mapped_column(Float, default=0)


class Birds(CreatedModel):
    __tablename__ = "birds"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(30))
    type: Mapped[int] = mapped_column(Integer)
    grain: Mapped[str] = mapped_column(DateTime, default=datetime.datetime.now)
    vitamin: Mapped[str] = mapped_column(DateTime)
    mutation: Mapped[str] = mapped_column(DateTime, nullable=True)


class Ban(CreatedModel):
    __tablename__ = "ban"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[str] = mapped_column(DateTime(), default=datetime.datetime.now)
