from aiogram import types
from sqlmodel import Session

from .db_objects import Laundry, Users
from .settings import engine


async def process_args(args: str) -> str:
	return 'hello'
