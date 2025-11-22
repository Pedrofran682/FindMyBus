from pydantic import ValidationError
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import schedule
from findmybus.utils.Connector import Connector
from findmybus.utils.Models.api.models import BusPositionAdapter


class Worker:
    def __init__(self):
        self.dbConnector = Connector()

    def get_buses_position(self):
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

    

    def run(self):
        return self.get_buses_position()


if __name__ == "__main__":
    worker = Worker()
    response = worker.run()
    # schedule.every(2).minutes.do(worker.run())
    print("Should run just once")
