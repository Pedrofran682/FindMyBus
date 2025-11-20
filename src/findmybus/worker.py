from pydantic import ValidationError
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from findmybus.utils.models import Positions


def get_buses_position() -> Positions:
    now = datetime.now(ZoneInfo('America/Sao_Paulo'))
    last_minute = now - timedelta(minutes=1)
    try:
        payload = {
            "dataInicial": last_minute.strftime("%Y-%m-%d %H:%M:%S"),
            "dataFinal": now.strftime("%Y-%m-%d %H:%M:%S")
            }
        response = requests.get("https://dados.mobilidade.rio/gps/sppo",
                                payload=payload)
        if response.status_code < 400:
            return Positions.model_validate(response.text)
        raise Exception(f"Status code: {response.status_code}")
    except ValidationError as e:
        raise e
    except Exception as e:
        raise Exception(f"An error happened. Message: {e}")