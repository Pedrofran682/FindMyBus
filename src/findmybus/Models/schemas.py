from typing import Annotated, Any
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
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

class BusesRoutesGeometry(BaseModel):
    type: str | None = Field(exclude=True)
    crs: str | None = Field(exclude=True)
    coordinates: list[list[float]]
    
class BusRoutesProperties(BaseModel):
    fid: int
    extensao: int
    data_inicio: str | None
    consorcio: str
    descricao_desvio: str| None
    data_fim: str | None
    tipo_rota: str | None
    shape_id: str | None
    direcao: int 
    destino: str | None
    servico: str | None
    SHAPE__Length: float

class BusesRoutesInformation(BaseModel):
    geometry: BusesRoutesGeometry
    id: int
    type: str
    properties : BusRoutesProperties
    model_config = ConfigDict(arbitrary_types_allowed=True)


class BusesRoutesFeatures(BaseModel):
    features: list[BusesRoutesInformation] 
    type: str = Field(exclude=True)
    properties: dict[str, Any] = Field(exclude=True)
