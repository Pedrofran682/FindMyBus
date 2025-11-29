from typing import Any
from pydantic import TypeAdapter, ValidationError
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
from findmybus.Models.orm import Routes, BusesStations
from findmybus.database.Connector import Connector
from findmybus.Models.schemas import BusPosition, BusPositionAdapter, BusesRoutesFeatures, BusStationFeatures

import logging
log = logging.getLogger()

class Worker:
    def __init__(self):
        self.dbConnector = Connector()
        self.urlBusPosition = "https://dados.mobilidade.rio/gps/sppo"
        self.urlBusRoute = "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Hosted/Itiner%C3%A1rios_da_rede_de_transporte_p%C3%BAblico_por_%C3%B4nibus_(SPPO)/FeatureServer/1/query?outFields=*&where=1%3D1&f=geojson"
        self.urlBusStation = "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Hosted/Pontos_de_Parada_da_rede_de_transporte_p%C3%BAblico_por_%C3%B4nibus_(SPPO)/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
    
    
    def get_buses_position(self) -> TypeAdapter[list[BusPosition]]:
        now = datetime.now(ZoneInfo('America/Sao_Paulo'))
        last_minute = now - timedelta(minutes=1)
        try:
            payload = {
                "dataInicial": last_minute.strftime("%Y-%m-%d %H:%M:%S"),
                "dataFinal": now.strftime("%Y-%m-%d %H:%M:%S")
                }
            response = self.get_request(self.urlBusPosition,
                                        payload)
            return BusPositionAdapter.validate_json(response)
        except ValidationError as e:
            raise e
        except Exception as e:
            raise Exception(f"An error happened. Message: {e}")


    def get_buses_routes(self) -> TypeAdapter[list[BusPosition]]:
        try:
            response = self.get_request(self.urlBusRoute)
            return BusesRoutesFeatures.model_validate_json(response)
        except ValidationError as e:
            raise e
        except Exception as e:
            raise Exception(f"An error happened. Message: {e}")


    def get_buses_stations(self) -> TypeAdapter[list[BusPosition]]:
        try:
            response = self.get_request(self.urlBusStation)
            return BusStationFeatures.model_validate_json(response)
        except ValidationError as e:
            raise e
        except Exception as e:
            raise Exception(f"An error happened. Message: {e}")


    def remove_duplicate_dict(self, list_dict: list[dict[str, str]]) -> list[dict[str, str]]:
        data = pd.DataFrame(list_dict)
        return data.drop_duplicates(subset=['order']).to_dict(orient="records")


    def get_request(self, url: str, payload = None):
        try:
            log.info(f"Exectuing GET request for {url[:20]}...")
            response = requests.get(url=url,
                                    params=payload)
            if response.ok:
                log.info(f"GET request status code: {response.status_code}")
                return response.text
            log.warning(f"GET request status code: {response.status_code}")
            raise Exception(f"Status code: {response.status_code}")
        except Exception as e:
            log.error(f"GET request status code: {response.status_code}. An error happened. Message: {e}")
            raise Exception(f"An error happened. Message: {e}")


    def clean_bus_route_response(self, response: BusesRoutesFeatures) -> list[dict[str,Any]]:
        log.info(f"Cleaning up bus route response")
        dict_routes = []
        for feature in response.features:
            nRoute = Routes(id=feature.id,
                            consortium=feature.properties.consorcio,
                            type_route=feature.properties.tipo_rota,
                            direction=feature.properties.direcao,
                            destination=feature.properties.destino,
                            line=feature.properties.servico,
                            geometry=feature.geometry.model_dump())
            dict_routes.append({col.name: getattr(nRoute, col.name)
                                for col in nRoute.__table__.columns})
        return dict_routes

    
    def clean_bus_station_response(self, response: BusStationFeatures) -> list[dict[str,Any]]:
        log.info(f"Cleaning up buses station response")
        dict_stations = []
        for feature in response.features:
            nBusStation = BusesStations(id=feature.id,
                            stop_id=feature.properties.stop_id,
                            stop_name=feature.properties.stop_name,
                            geometry=feature.geometry.model_dump())
            dict_stations.append({col.name: getattr(nBusStation, col.name)
                                for col in nBusStation.__table__.columns})
        return dict_stations