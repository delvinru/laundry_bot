from asyncio import CancelledError
from aiogram import types
from aiogram.utils.markdown import bold, escape_md, text
from aiogram.utils.deep_linking import decode_payload
from loguru import logger

from .settings import ADMINS, dp, main_description
from .helpers import process_args
from .middleware import check_user


@dp.message_handler(commands='start')
@check_user()
async def start(message: types.Message):
    # Logger info
    logger.info(f'User {message.from_user.id} {message.from_user.username} came to start!')
    args = message.get_args() or ''

    # Check if args empty than user start new session else user start the process of washing clothes
    if args == '':
        await message.answer(escape_md(main_description))
        return

    result = await process_args(args)
    await message.answer(escape_md(result))


@dp.message_handler(commands='check')
async def check(message: types.Message):
    await message.answer(escape_md("Todo!"))


@dp.message_handler(commands='launch')
async def launch(message: types.Message):
    await message.answer(escape_md("Todo!"))
