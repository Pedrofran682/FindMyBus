from pydantic import BaseModel, Field

class BusPosition(BaseModel):
    ordem: str = Field(alias="ordem")
    latitude: str = Field(alias="latitude")
    longitude: str = Field(alias="longitude")
    datahora: int = Field(alias="datahora")
    velocidade: int = Field(alias="velocidade")
    linha: str = Field(alias="linha")
    datahoraenvio: int = Field(alias="datahoraenvio")
    datahoraservidor: int = Field(alias="datahoraservidor")

class Positions(BaseModel):
    positions: list[BusPosition]

