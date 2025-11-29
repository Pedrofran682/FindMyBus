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

class Geometry(BaseModel):
    type: str | None = Field(exclude=True)
    crs: str | None = Field(exclude=True)
    coordinates: list[list[float]] | list[float]
    
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


class BusStationProperties(BaseModel):
    fid: int
    wheelchair_boarding: bool | None
    zone_id: str | None
    platform_code: str
    stop_id: str| None
    stop_code: str | None
    stop_url: str | None
    stop_desc: str | None
    stop_timezone: str | None
    stop_name: str | None
    location_type: int | None
    parent_station: str

class RoutesFeatureInformation(BaseModel):
    geometry: Geometry
    id: int
    type: str
    properties : BusRoutesProperties

    model_config = ConfigDict(arbitrary_types_allowed=True)

class BusStationFeatureInformation(BaseModel):
    geometry: Geometry
    id: int
    type: str
    properties : BusStationProperties

    model_config = ConfigDict(arbitrary_types_allowed=True)

class BusesRoutesFeatures(BaseModel):
    features: list[RoutesFeatureInformation] 
    type: str = Field(exclude=True)
    properties: dict[str, Any] = Field(exclude=True)

class BusStationFeatures(BaseModel):
    features: list[BusStationFeatureInformation] 
    type: str = Field(exclude=True)
    properties: dict[str, Any] = Field(exclude=True)

