from pydantic import TypeAdapter, ValidationError
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
import schedule
from findmybus.utils.Connector import Connector
from findmybus.utils.Models.api.models import BusPosition, BusPositionAdapter


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
            response = requests.get("https://dados.mobilidade.rio/gps/sppo",
                                    params=payload)
            if response.ok:
                return BusPositionAdapter.validate_json(response.text)
            raise Exception(f"Status code: {response.status_code}")
        except ValidationError as e:
            raise e
        except Exception as e:
            raise Exception(f"An error happened. Message: {e}")

    def remove_duplicate_dict(self, list_dict: list[dict[str, str]]) -> list[dict[str, str]]:
        data = pd.DataFrame(list_dict)
        return data.drop_duplicates(subset=['order']).to_dict(orient="records")


# import logging
# from logging.config import fileConfig

# import os
# CONFIG_FILE = 'logging.ini'
# LOG_DIR = 'log'
# os.makedirs(LOG_DIR, exist_ok=True)
# log_filename = f"{LOG_DIR}/execution_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"

# fileConfig(CONFIG_FILE, 
#            defaults={'log_file_path': log_filename})
# logger = logging.getLogger(__name__)

if __name__ == "__main__":
    worker = Worker()
    responseAdapter = worker.get_buses_position()
    responseDict = worker.remove_duplicate_dict([obj.model_dump() for obj in responseAdapter])
    worker.dbConnector.upinsert(responseDict)
    print("Should run just once")
