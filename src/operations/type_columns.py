import logging
from enum import Enum

import sqlite3
import polars as pl


class SqliteTypes(Enum):
    INTEGER = pl.Int64
    TEXT = pl.String


class TypeColumns:
    def __init__(self, db_path: str):
        self.__db_path = db_path
        self.__table_name = input('> 1/3 Enter the target table: ')
        self.__columns = input('> 2/3 Enter the columns to cast (e.g. col1 col2 ...): ').split()

        try:
            self.__new_cols_type = SqliteTypes[
                input('> 3/3 What type should the columns be converted to? (INTEGER, TEXT): ').upper()]
        except KeyError:
            logging.warning('> The provided type is invalid, must be either INTEGER or TEXT')
            exit()
        with sqlite3.connect(self.__db_path) as conn:
            self.__validate_inputs(conn)
            self.__edit_columns_typing(conn)
        logging.info('Typing was properly done !')

    def __validate_inputs(self, conn: sqlite3.Connection):
        cursor = conn.cursor()
        # Validate table
        try:
            cursor.execute(
                f'SELECT 1 FROM {self.__table_name} LIMIT 1',
            )
        except sqlite3.OperationalError:
            logging.warning('> The selected table is invalid')
            exit()

        # Validate columns
        try:
            cursor.execute(
                f'SELECT {','.join(col_name for col_name in self.__columns)} from {self.__table_name}'
            )
        except sqlite3.OperationalError:
            logging.warning('> At least one of the provided columns is incorrect')
            exit()

    def __edit_columns_typing(self, conn: sqlite3.Connection):
        # Retrieve the whole table
        df = pl.read_database(
            query=f'SELECT * FROM {self.__table_name}',
            connection=conn,
        )

        # Apply type conversion
        df = df.with_columns(
            (pl.col(column_name).cast(self.__new_cols_type.value).alias(column_name) for column_name in self.__columns)
        )

        # Overwrite existing table with new typed table
        df.write_database(
            table_name=self.__table_name,
            if_table_exists='replace',
            connection=f'sqlite:///{self.__db_path}',
        )
