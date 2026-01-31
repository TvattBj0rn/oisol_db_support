import asyncio
import sqlite3
from time import sleep

import aiohttp
import polars as pl
from aiohttp import ClientSession

from src.utils import OISOL_HOME_PATH


class WikiTablesMirrorRunner:
    @staticmethod
    def __convert_action_to_url(action: str) -> str:
        return f'https://foxhole.wiki.gg/api.php?{action}&format=json'

    @classmethod
    async def wiki_table_update_process(cls, *target_tables) -> None:
        async with aiohttp.ClientSession() as session:
            # If no table is provided by the user, all wiki tables will be mirrored
            target_tables = await cls.__get_tables_list(session) if not target_tables else list(target_tables)

            tasks = (cls.mirror_wiki_table(session, target_table) for target_table in target_tables)
            await asyncio.gather(*tasks)

    @classmethod
    async def __get_tables_list(cls, session: ClientSession) -> list[str] | None:
        res = await session.get(cls.__convert_action_to_url('action=cargotables'))
        if res.status == 200:
            return (await res.json())['cargotables']
        return None

    @classmethod
    async def mirror_wiki_table(cls, session: ClientSession, table_name: str) -> None:
        # Retrieve table fields, no special field for "all"
        table_fields_res = await session.get(cls.__convert_action_to_url(f'action=cargofields&table={table_name}'))
        if table_fields_res.status != 200:
            return
        tables_fields = (await table_fields_res.json())['cargofields']
        sleep(20)

        # run cargoquery with all fields with a limit at 1000 (heaviest db has ~500 rows) to ensure all rows are retrieved
        # it seems the max value of limit of 500 is optional, as setting a higher limit works
        table_fields_query = list(tables_fields)
        table_data_res = await session.get(
            cls.__convert_action_to_url(f'action=cargoquery&tables={table_name}&fields={','.join(table_fields_query)}&limit=1000'),
        )
        if table_data_res.status != 200:
            return
        sleep(20)

        # Todo: separate the query & df into two methods: get from wiki /post to db
        # Convert retrieved data to polars df for typing and writing
        df_table_data = pl.from_records([row['title'] for row in (await table_data_res.json())['cargoquery']])

        # Todo: make a proper data converter before writing
        df_table_data.write_database(
            table_name=table_name,
            connection=f'sqlite:///{OISOL_HOME_PATH}/foxhole_wiki_mirror.db',
            if_table_exists='replace',
        )

    @classmethod
    def create_sqlite_database(cls) -> None:
        with sqlite3.connect(OISOL_HOME_PATH / 'foxhole_wiki_mirror.db') as _conn:
            pass

    @classmethod
    async def view_db_tables(cls) -> None:
        # Retrieve existing tables in db
        with sqlite3.connect(OISOL_HOME_PATH / 'foxhole_wiki_mirror.db') as conn:
            raw_tables = conn.cursor().execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        tables_in_db = {table_tup[0] for table_tup in raw_tables}

        # Retrieve available tables on the wiki
        async with aiohttp.ClientSession() as session:
            wiki_tables = set(await cls.__get_tables_list(session))

        print(f'Current tables on the db: {tables_in_db}')
        print(f'Available tables on the wiki: {wiki_tables}')
        print(f'Tables on the wiki not in the db (missing): {wiki_tables - tables_in_db}')
        print(f'Tables on the db not on the wiki (deprecated): {tables_in_db - wiki_tables}')

async def run_db_wiki_update(*args) -> None:
    match args[0].lower():
        case 'update':
            await WikiTablesMirrorRunner.wiki_table_update_process(*args[1:])
        case 'init':
            WikiTablesMirrorRunner.create_sqlite_database()
        case 'tables':
            await WikiTablesMirrorRunner.view_db_tables()

