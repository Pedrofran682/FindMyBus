from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Positions(Base):
    __tablename__ = "positions"

    order: Mapped[str] = mapped_column(primary_key=True)
    latitude: Mapped[str]
    longitude: Mapped[float]
    dateTime: Mapped[str]
    velocity: Mapped[str]
    line: Mapped[str]
    sentDateTime: Mapped[str]
    serverDateTime: Mapped[str]