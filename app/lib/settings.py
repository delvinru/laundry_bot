from os import getenv
from aiogram import Bot, Dispatcher, types

TOKEN = getenv('TOKEN') or ''
ADMINS = list(map(int, (getenv('ADMINS') or '').split(',')))
print(TOKEN)
print(ADMINS)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot)