from pydantic import BaseModel, Field
from pydantic import TypeAdapter

class BusPosition(BaseModel):
    order: str = Field(alias="ordem")
    latitude: str = Field(alias="latitude")
    longitude: str = Field(alias="longitude")
    dateTime: str = Field(alias="datahora")
    velocity: str = Field(alias="velocidade")
    line: str = Field(alias="linha")
    sentDateTime: str = Field(alias="datahoraenvio")
    serverDateTime: str = Field(alias="datahoraservidor")

BusPositionAdapter = TypeAdapter(list[BusPosition])

