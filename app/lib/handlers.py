from aiogram import types
from aiogram.utils.markdown import escape_md
from aiogram.utils.deep_linking import decode_payload
from loguru import logger

from .settings import ADMINS, dp, main_description
from .helpers import process_args, check_laundry
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

    try:
        result = await process_args(args=decode_payload(args), uid=message.from_user.id)
    except Exception as e:
        logger.warning(f'Got exception in process args: {e}')
        result = escape_md('Возникла ошибочка 🤷')

    await message.answer(result)


@dp.message_handler(commands='check')
async def check(message: types.Message):
    logger.info(f'User {message.from_user.id} {message.from_user.username} request check function!')
    await message.answer(check_laundry())

@dp.message_handler(commands='help')
async def help(message: types.Message):
    logger.info(f'User {message.from_user.id} {message.from_user.username} request help function!')
    await message.answer(escape_md(main_description))

@dp.message_handler(commands='dev')
async def dev(message: types.Message):
    logger.info(f'User {message.from_user.id} {message.from_user.username} request dev function!')
    await message.answer(escape_md("Разработчик данного бота @delvinru"))

@dp.message_handler(regexp='.*')
async def mumble(message: types.Message):
    logger.info(f'User {message.from_user.id} {message.from_user.username} mumbled!')
    await message.answer(escape_md("А как ...? Я такого не знаю и не умею"))