# from findmybus.database.Connector import Connector
# from datetime import datetime
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

# if __name__ == "__main__":
#     Connector()