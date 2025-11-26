from typing import Any
from sqlalchemy import Engine, Sequence, select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from findmybus.Models.orm import Base, Positions, Routes


def upinsert(engine: Engine,
             orm_table: Base,
             list_of_dict_insert: list[dict[str, Any]],
             exclude_cols: dict[str] = {},
             index_elements = None) -> None:
    with Session(engine) as session:
        insert_stmt = insert(orm_table).values(list_of_dict_insert)
        exclude_cols = exclude_cols 

        on_conflict_set = {
            column.name: getattr(insert_stmt.excluded, column.name)
            for column in orm_table.__table__.columns
            if column.name not in exclude_cols
        }
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=[index_elements],
            set_=on_conflict_set)

        session.execute(do_update_stmt)
        session.commit()


def get_buses_position(engine: Engine,
                     line: str) -> Sequence[Positions]:
    with Session(engine) as session:
        return session.scalars(
            select(Positions).where(Positions.line == line)).all()
    

def get_bus_route(engine: Engine,
                  line: str) -> Sequence[Routes]:
    with Session(engine) as session:
        return session.scalars(
            select(Routes).where(Routes.line == line)).all()