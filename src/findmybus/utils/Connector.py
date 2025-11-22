from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import URL
from findmybus.utils.Models.database.models import Base, Positions
from sqlalchemy.dialects.postgresql import insert


class Connector:
    def __init__(self):
        load_dotenv()
        self.engine = create_engine(self._get_url_connection(),
                                    pool_pre_ping=True)
        Base.metadata.create_all(self.engine)
        

    def _get_url_connection(self):
        return URL.create(
            "postgresql+pg8000",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
            )
    
    def upinsert(self, list_of_dict: list[dict[str, Any]]) -> None:
        insert_stmt = insert(Positions).values(list_of_dict)
        exclude_cols = {'order'} 

        on_conflict_set = {
            c.name: getattr(insert_stmt.excluded, c.name)
            for c in Positions.__table__.columns
            if c.name not in exclude_cols
        }
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['order'],
            set_=on_conflict_set)

        with Session(self.engine) as session:
            session.execute(do_update_stmt)
            session.commit()