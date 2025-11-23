from zoneinfo import ZoneInfo
import pytest
from datetime import datetime, timedelta
from pytest_mock import MockerFixture
from findmybus.utils.worker import get_buses_position
from polyfactory.factories.pydantic_factory import ModelFactory
from findmybus.utils.Models.api.models import Positions

class BusPositionFactory(ModelFactory[Positions]): ...

def bus_position_data() -> Positions: 
    return BusPositionFactory.build()

@pytest.fixture
def fixed_time():
    return datetime(2025, 11, 16, 18, 0, 0, tzinfo=ZoneInfo('America/Sao_Paulo'))

def test_get_buses_position_success(mocker: MockerFixture, fixed_time):
    # mocked = mocker.patch.object(Example, 'step')
    mock_get = mocker.patch('findmybus.utils.worker.requests.get')
    mock_dt  = mocker.patch('findmybus.utils.worker.datetime')

    dateTime = fixed_time
    last_minute = dateTime - timedelta(minutes=1)
    mock_dt.now.return_value = dateTime
    expected_payload = {
        "dataInicial": last_minute.strftime("%Y-%m-%d %H:%M:%S"),
        "dataFinal": dateTime.strftime("%Y-%m-%d %H:%M:%S")
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = bus_position_data().model_dump()
    mock_get.return_value = mock_response

    result = get_buses_position()
    assert len(result.positions) > 0
    
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert call_args[0][0] == "https://dados.mobilidade.rio/gps/sppo" 
    assert call_args[1]['payload'] == expected_payload 


def test_get_buses_position_server_error(mocker: MockerFixture, fixed_time):
    with pytest.raises(Exception) as excinfo:
        mock_get = mocker.patch('findmybus.utils.worker.requests.get')
        mock_dt  = mocker.patch('findmybus.utils.worker.datetime')

        dateTime = fixed_time
        last_minute = dateTime - timedelta(minutes=1)
        mock_dt.now.return_value = dateTime

        mock_response = mocker.Mock()
        mock_response.status_code = 500
        mock_response.text = bus_position_data().model_dump()
        mock_get.return_value = mock_response
        result = get_buses_position()
    assert str(excinfo.value)

