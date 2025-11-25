from pydantic import TypeAdapter, ValidationError
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
import schedule
from findmybus.Models.orm import Positions
from findmybus.database.Connector import Connector
from findmybus.Models.schemas import BusPosition, BusPositionAdapter, BusesRoutesFeatures
from findmybus.database import dbActions

class Worker:
    def __init__(self):
        self.dbConnector = Connector()

    def get_buses_position(self) -> TypeAdapter[list[BusPosition]]:
        now = datetime.now(ZoneInfo('America/Sao_Paulo'))
        last_minute = now - timedelta(minutes=1)
        try:
            payload = {
                "dataInicial": last_minute.strftime("%Y-%m-%d %H:%M:%S"),
                "dataFinal": now.strftime("%Y-%m-%d %H:%M:%S")
                }
            response = self.get_request("https://dados.mobilidade.rio/gps/sppo",
                                        payload)
            return BusPositionAdapter.validate_json(response)
        except ValidationError as e:
            raise e
        except Exception as e:
            raise Exception(f"An error happened. Message: {e}")


    def get_buses_routes(self) -> TypeAdapter[list[BusPosition]]:
        try:
            response = self.get_request("https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Hosted/Itiner%C3%A1rios_da_rede_de_transporte_p%C3%BAblico_por_%C3%B4nibus_(SPPO)/FeatureServer/1/query?outFields=*&where=1%3D1&f=geojson")
            return BusesRoutesFeatures.model_validate_json(response)
        except ValidationError as e:
            raise e
        except Exception as e:
            raise Exception(f"An error happened. Message: {e}")


    def remove_duplicate_dict(self, list_dict: list[dict[str, str]]) -> list[dict[str, str]]:
        data = pd.DataFrame(list_dict)
        return data.drop_duplicates(subset=['order']).to_dict(orient="records")


    def get_request(self, url: str, payload = None):
        try:
            response = requests.get(url=url,
                                    params=payload)
            if response.ok:
                return response.text
            raise Exception(f"Status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"An error happened. Message: {e}")


if __name__ == "__main__":
    worker = Worker()
    # responseAdapter = worker.get_buses_position()
    # responseDict = worker.remove_duplicate_dict([obj.model_dump() for obj in responseAdapter])
    # dbActions.upinsert(worker.dbConnector.get_db_engine(),
    #                    Positions,
    #                    responseDict,
    #                    {"order"}, "order" )
    # positions = dbActions.get_buses_position(worker.dbConnector.get_db_engine(), "457")

    responseAdapter = worker.get_buses_routes()

    print("Should run just once")
