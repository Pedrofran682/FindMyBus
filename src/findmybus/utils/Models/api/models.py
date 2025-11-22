from pydantic import BaseModel, Field
from pydantic import TypeAdapter

class BusPosition(BaseModel):
    ordem: str = Field()
    latitude: str = Field()
    longitude: str = Field()
    datahora: int = Field()
    velocidade: int = Field()
    linha: str = Field()
    datahoraenvio: str = Field()
    datahoraservidor: str = Field()

BusPositionAdapter = TypeAdapter(list[BusPosition])

