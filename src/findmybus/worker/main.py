import time
from findmybus.Models.orm import BusesStations, Positions, Routes
from findmybus.database import dbActions
from findmybus.worker.Worker import Worker
from findmybus.config.Constants import DELTA_REFRESH
import logging
from logging.config import fileConfig
import schedule

CONFIG_FILE = 'logging.ini'
LOG_DIR = 'log'
fileConfig(CONFIG_FILE) 
log = logging.getLogger(__name__)

def upinsert_bus_position(worker: Worker):
    try:
        log.info("Updating positions database")
        dbActions.erase_table_entries(worker.dbConnector.get_db_engine(),
                            Positions)
        responseAdapter = worker.get_buses_position()
        responseDict = worker.remove_duplicate_dict([obj.model_dump() for obj in responseAdapter])
        dbActions.upinsert(worker.dbConnector.get_db_engine(),
                        Positions,
                        responseDict,
                        {"order"}, "order" )
    except Exception as e:
        log.error(f"Error getting positions. Error: {e}")

def upinsert_bus_route(worker: Worker):
    try:
        log.info("Updating routes database")
        dbActions.erase_table_entries(worker.dbConnector.get_db_engine(),
                    Routes)
        responseAdapter = worker.get_buses_routes()
        responseDict = worker.clean_bus_route_response(responseAdapter)
        dbActions.upinsert(worker.dbConnector.get_db_engine(),
                        Routes,
                        responseDict,
                        {"id"}, "id" )
    except Exception as e:
        log.error(f"Error getting routes. Error: {e}")


def upinsert_bus_staion(worker: Worker):
    try:
        log.info("Updating bus_station database")
        dbActions.erase_table_entries(worker.dbConnector.get_db_engine(),
                    BusesStations)
        responseAdapter = worker.get_buses_stations()
        responseDict = worker.clean_bus_station_response(responseAdapter)
        dbActions.upinsert(worker.dbConnector.get_db_engine(),
                        BusesStations,
                        responseDict,
                        {"id"}, "id" )
    except Exception as e:
        log.error(f"Error getting bus station. Error: {e}")


if __name__ == "__main__":
    worker = Worker()
    schedule.every(1).minutes.do(lambda: upinsert_bus_position(worker))
    schedule.every(1).day.do(lambda: upinsert_bus_route(worker))
    schedule.every(1).day.do(lambda: upinsert_bus_staion(worker))
    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(DELTA_REFRESH)