from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger
from sqlmodel import Session, select

from .db_objects import Users
from .settings import engine


def check_user():
    def decorator(func):
        return func
    return decorator


class CheckLogin(BaseMiddleware):
    def __init__(self):
        super(CheckLogin, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        with Session(engine) as s:
            statement = select(Users).where(Users.tgid == message.from_user.id)
            result = s.exec(statement).all()
            # If got empty result than have new user
            if len(result) == 0:
                s.add(Users(
                    tgid = message.from_user.id,
                    nickname = message.from_user.username,
                ))
                s.commit()
                logger.info(f'User {message.from_user} {message.from_user.username} registered!')