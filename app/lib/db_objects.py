from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Laundry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    machine: str
    end: Optional[datetime] = Field(default=None)
    check: bool = False


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tgid: int
    nickname: Optional[str]
    laundry_1: int = 0
    laundry_2: int = 0
    dryer: int = 0
