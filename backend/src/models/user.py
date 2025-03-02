from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    total_attempts: Mapped[int] = mapped_column(Integer, default=0)

    @property
    def score(self) -> float:
        if self.total_attempts == 0:
            return 0.0
        return round((self.correct_answers / self.total_attempts) * 100, 2)
