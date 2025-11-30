from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import URL
from findmybus.Models.orm import Base
from sqlalchemy import Engine


class Connector:
    def __init__(self, scope: str):
        load_dotenv()
        self._validate_tables()
        self._get_user_credentials(scope)
        self.engine = create_engine(self._get_url_connection(),
                                    pool_pre_ping=True)


    def _get_url_connection(self) -> URL:
        return URL.create(
            "postgresql+pg8000",
            username=os.getenv(self.username),
            password=os.getenv(self.password),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("POSTGRES_DB")
            )

    def get_db_engine(self) -> Engine:
        return self.engine
    

    def _get_user_credentials(self, scope: str):
        if scope == "db":
            self.username = "POSTGRES_WORKER_USER"
            self.password = "POSTGRES_WORKER_PASSWORD"
        if scope == "ui":
            self.username = "POSTGRES_UI_USER"
            self.password = "POSTGRES_UI_PASSWORD"


    def _validate_tables(self):
        self.username = "POSTGRES_USER"
        self.password = "POSTGRES_PASSWORD"
        engine = create_engine(self._get_url_connection(),
                               pool_pre_ping=True)
        Base.metadata.create_all(engine)