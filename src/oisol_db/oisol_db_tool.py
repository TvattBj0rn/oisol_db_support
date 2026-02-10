import sqlite3

from src.utils import OISOL_HOME_PATH
import polars as pl

class OisolDBRunner:
    __db_name = 'oisol.db'
    @classmethod
    def view_oisol_db(cls, table_name: str) -> None:
        with sqlite3.connect(OISOL_HOME_PATH / cls.__db_name) as conn:
            df = pl.read_database(
                query=f'SELECT * FROM {table_name}',
                connection=conn,
            )
        df.show(limit=None)

    @classmethod
    def add_column_to_table(cls, /, table_name: str, column_name: str, column_type: str):
        with sqlite3.connect(OISOL_HOME_PATH / cls.__db_name) as conn:
            conn.cursor().execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}')
            conn.commit()


def oisol_db_runner(*args) -> None:
    match args[0].lower():
        case 'view':
            OisolDBRunner.view_oisol_db(args[1])
        case 'add_column':
            OisolDBRunner.add_column_to_table(*args[1:])
