from sqlalchemy import BigInteger, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Positions(Base):
    __tablename__ = "positions"

    order: Mapped[str] = mapped_column(primary_key=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
    dateTime = Column(BigInteger)
    velocity: Mapped[int]
    line: Mapped[str]
    sentDateTime = Column(BigInteger)
    serverDateTime = Column(BigInteger)