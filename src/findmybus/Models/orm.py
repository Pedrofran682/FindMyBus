from sqlalchemy import BigInteger, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import JSONB

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

class Routes(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    consortium: Mapped[str]
    type_route: Mapped[str]
    direction:  Mapped[int]
    destination: Mapped[str]
    line: Mapped[str]
    geometry = Column(JSONB)