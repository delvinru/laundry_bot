from aiogram import types
from aiogram.utils.markdown import bold, escape_md, text
from lib.settings import ADMINS, dp, bot


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(escape_md("Hello, from bot"))
