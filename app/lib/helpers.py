import asyncio
from datetime import datetime, timedelta
from threading import Thread

from aiogram import Bot
from aiogram.utils.markdown import bold, escape_md, text
from loguru import logger
from sqlalchemy import exc
from sqlmodel import Session, select

from .db_objects import Laundry, Users
from .settings import TOKEN, engine


async def notify_user(machine: str, uid: int):
    """ Notify user when laundry end work """

    # Create new session
    bot = Bot(token=TOKEN)

    if machine == "dryer":
        data = "Забрать вещи можно через 10 минут ❗️"
        await bot.send_message(chat_id=uid, text=data)
        logger.info(f'10 minute warning for user {uid} with machine {machine}')

        await asyncio.sleep(10 * 60)
        data = "Сушка завершена, забери вещи ✅"
        await bot.send_message(chat_id=uid, text=data)
        await bot.close()
    else:
        await asyncio.sleep(50 * 60)
        data = "Забрать вещи можно через 10 минут ❗️"
        await bot.send_message(chat_id=uid, text=data)
        logger.info(f'10 minute warning for user {uid} with machine {machine}')

        await asyncio.sleep(7 * 60)
        data = "Забрать вещи можно через 3 минуты ❗️"
        logger.info(f'3 minute warning for user {uid} with machine {machine}')
        await bot.send_message(chat_id=uid, text=data)

        await asyncio.sleep(3 * 60)
        data = "Стирка завершена, забери вещи ✅"
        await bot.send_message(chat_id=uid, text=data)
        await bot.close()

    logger.info(f'Clear state for machine: {machine}')
    with Session(engine) as s:
        statement = select(Laundry).where(Laundry.machine == machine)
        laundry = s.exec(statement).one()
        laundry.check = False
        s.add(laundry)
        s.commit()


def between_notify(machine: str, uid: int):
    """ Start async thread """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(notify_user(machine, uid))
    loop.close()


def update_state(machine: str, name: str, tgid: int) -> str:
    with Session(engine) as s:
        statement = select(Laundry).where(Laundry.machine == machine).where(Laundry.check == False)
        try:
            laundry = s.exec(statement).one()
        except exc.NoResultFound:
            return text('Извини, но машинка уже занята😌')

    # Change end value
    laundry.check = True

    if machine == 'dryer':
        laundry.end = datetime.now() + timedelta(minutes=10)
    else:
        laundry.end = datetime.now() + timedelta(hours=1)
    # Craft response text
    data = bold(name) + f' закончит в {laundry.end.hour}:'
    if laundry.end.minute < 10:
        data += f'0{laundry.end.minute}'
    else:
        data += f'{laundry.end.minute}'

    # Save changed data
    s.add(laundry)
    s.commit()

    # Start notify thread
    thread = Thread(target=between_notify, args=(machine, tgid))
    thread.daemon = True
    thread.start()

    # Info log
    logger.info(f'User {tgid} took {machine}')

    # Add stats to database
    with Session(engine) as s:
        statement = select(Users).where(Users.tgid == tgid)
        user = s.exec(statement).one()
        if machine == 'laundry_1':
            user.laundry_1 += 1
        elif machine == 'laundry_2':
            user.laundry_2 += 1
        elif machine == 'dryer':
            user.dryer += 1
        s.add(user)
        s.commit()

    return data


async def process_args(args: str, uid: int) -> str:
    """ Helper function to processing arguments from QR-code """

    # To prevent SQLInjection, the following check is used, instead of update_state(args)
    if args == 'laundry_1':
        res = update_state(machine='laundry_1', name='Первая машинка', tgid=uid)
    elif args == 'laundry_2':
        res = update_state(machine='laundry_2', name='Вторая машинка', tgid=uid)
    elif args == 'dryer':
        res = update_state(machine='dryer', name='Сушилка', tgid=uid)
    else:
        res = escape_md('Хмм, а ты уверен, что пользуешься ботом по назначению?🤔')

    return res


def check_laundry() -> str:
    """ Helper function to check laundry state """

    with Session(engine) as s:
        statement = select(Laundry)
        result = s.exec(statement).all()
        text = ''
        for laundry in result:
            if laundry.machine == 'laundry_1':
                text += bold('Первая машинка: ')
            elif laundry.machine == 'laundry_2':
                text += bold('Вторая машинка: ')
            elif laundry.machine == 'dryer':
                text += bold('Сушилка: ')

            if laundry.check == False:
                text += '✅\n'        
            else:
                text += f'❌ до '
                if laundry.end.hour < 10:
                    text += f'0{laundry.end.hour}:'
                else:
                    text += f'{laundry.end.hour}:'

                if laundry.end.minute < 10:
                    text += f'0{laundry.end.minute}\n'
                else:
                    text += f'{laundry.end.minute}\n'

    return text
