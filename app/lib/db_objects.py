from sqlmodel import Field, SQLModel
from typing import Optional


class Laundry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    machine: str
    end: int = 0
    check: bool = False


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tgid: int
    nickname: Optional[str]
    laundry_1: int = 0
    laundry_2: int = 0
    dryer: int = 0
