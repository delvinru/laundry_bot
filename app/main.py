import asyncio
import sys

from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

# Import handlers for bot
from lib.handlers import *
from lib.settings import bot, dp

from lib.middleware import CheckLogin


async def set_commands(bot: Bot):
    """ Setup commands for Telegram bot """
    commands = [
        BotCommand(command="/start",  description="Начать взаимодействие с ботом"),
        BotCommand(command="/check",  description="Проверить стиралки"),
        BotCommand(command="/help",   description="Помощь"),
        BotCommand(command="/dev",    description="Разработчик бота")
    ]
    await bot.set_my_commands(commands)


async def main():
    await set_commands(bot)

    # Setup middleware
    dp.middleware.setup(CheckLogin())

    logger.info('[+] Bot started...')
    # Start long polling for bot
    await dp.start_polling()

if __name__ == "__main__":
    # Set base logging
    logger.remove()
    logger.add(
        "logs/debug.log",
        format="[{time:YYYY-MM-DD HH:mm:ss}] {level} | {message}",
        level="TRACE",
        rotation="1 MB")
    logger.add(sys.__stdout__)

    asyncio.run(main())
