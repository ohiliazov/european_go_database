import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"


class HasUser:
    """
    Mark classes that have many-to-one relationship to the "User" class.
    """

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    @declared_attr
    def user(self) -> Mapped["User"]:
        return relationship("User")


class Player(Base):
    __tablename__ = "player"

    egd_pin: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    rank: Mapped[int]
    country: Mapped[str]
    club: Mapped[str]
    image_path: Mapped[str]


class Tournament(Base, HasUser):
    __tablename__ = "tournament"

    egd_pin: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    country: Mapped[str]
    tournament_class: Mapped[str]
    date_start: Mapped[datetime.date]
    date_end: Mapped[datetime.date]
    total_rounds: Mapped[int]
    total_players: Mapped[int]
