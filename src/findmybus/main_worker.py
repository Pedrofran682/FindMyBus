import time
from findmybus.Models.orm import Base, BusesStations, Positions, Routes
from findmybus.database import dbActions
from findmybus.worker.Worker import Worker
from findmybus.config.Constants import DELTA_REFRESH
import logging
from logging.config import fileConfig

CONFIG_FILE = 'logging.ini'
LOG_DIR = 'log'
fileConfig(CONFIG_FILE) 
log = logging.getLogger(__name__)

def update_db(worker: Worker):
    log.info("Updating database")
    dbActions.erase_table_entries(worker.dbConnector.get_db_engine(),
                        Positions)
    responseAdapter = worker.get_buses_position()
    responseDict = worker.remove_duplicate_dict([obj.model_dump() for obj in responseAdapter])
    dbActions.upinsert(worker.dbConnector.get_db_engine(),
                       Positions,
                       responseDict,
                       {"order"}, "order" )

    responseAdapter = worker.get_buses_routes()
    responseDict = worker.clean_bus_route_response(responseAdapter)
    dbActions.upinsert(worker.dbConnector.get_db_engine(),
                       Routes,
                       responseDict,
                       {"id"}, "id" )
    
    responseAdapter = worker.get_buses_stations()
    responseDict = worker.clean_bus_station_response(responseAdapter)
    dbActions.upinsert(worker.dbConnector.get_db_engine(),
                       BusesStations,
                       responseDict,
                       {"id"}, "id" )

if __name__ == "__main__":
    worker = Worker()
    while True:
        update_db(worker)
        time.sleep(DELTA_REFRESH)