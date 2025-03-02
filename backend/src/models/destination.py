from typing import List
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(primary_key=True)
    alias: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    country: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    clues: Mapped[List[str]] = mapped_column(JSON)
    fun_facts: Mapped[List[str]] = mapped_column(JSON)
