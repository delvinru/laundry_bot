import asyncio
from aiogram import Bot
from aiogram.types import BotCommand
from lib.settings import bot, dp

# Import handlers for bot
from lib.handlers import *


async def set_commands(bot: Bot):
    """ Setup commands for Telegram bot """

    commands = [
        BotCommand(command="/start",
                   description="Начать взаимодействие с ботом"),
        BotCommand(command="/check",  description="Проверить стиралки"),
        BotCommand(command="/launch", description="Запустить стиралку")
    ]

    await bot.set_my_commands(commands)


async def main():
    await set_commands(bot)

    # Start long polling for bot
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
