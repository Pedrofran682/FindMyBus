from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import URL
from findmybus.utils.Models.database.models import Positions, Base



class Connector:
    def __init__(self):
        load_dotenv()
        self.engine = create_engine(self._get_url_connection(),
                                    pool_pre_ping=True)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine,checkfirst=False)
        

    def _get_url_connection(self):
        return URL.create(
            "postgresql+pg8000",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
            )
    