from typing import Annotated
from pydantic import BaseModel, BeforeValidator, Field
from pydantic import TypeAdapter

def position_to_float(value: str):
    return float(value.replace(",", "."))

class BusPosition(BaseModel):
    order: str = Field(alias="ordem")
    latitude: Annotated[float, BeforeValidator(position_to_float)]  = Field(alias="latitude")
    longitude: Annotated[float, BeforeValidator(position_to_float)] = Field(alias="longitude")
    dateTime: int = Field(alias="datahora")
    velocity: int = Field(alias="velocidade")
    line: str = Field(alias="linha")
    sentDateTime: int = Field(alias="datahoraenvio")
    serverDateTime: int = Field(alias="datahoraservidor")

BusPositionAdapter = TypeAdapter(list[BusPosition])

