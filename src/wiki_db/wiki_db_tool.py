import asyncio
import sqlite3
import polars as pl

import aiohttp
from aiohttp import ClientSession
from src.utils import OISOL_HOME_PATH


class WikiTablesMirrorRunner:
    @staticmethod
    def __convert_action_to_url(action: str) -> str:
        return f'https://foxhole.wiki.gg/api.php?{action}&format=json'

    @classmethod
    async def wiki_table_update_process(cls, *target_tables):
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
        table_fields_res = await session.get(cls.__convert_action_to_url(f'action=cargofields&table={table_name}'))
        if table_fields_res.status != 200:
            return
        table_fields = list((await table_fields_res.json())['cargofields'])
        table_data_res = await session.get(
            cls.__convert_action_to_url(f'action=cargoquery&tables={table_name}&fields={','.join(table_fields)}&limit=1000')
        )
        if table_data_res.status != 200:
            return
        table_data = [row['title'] for row in (await table_data_res.json())['cargoquery']]
        df_table_data = pl.from_records(table_data)
        df_table_data.write_database(
            table_name=table_name,
            connection=f'sqlite:///{OISOL_HOME_PATH}/foxhole_wiki_mirror.db'
        )

    @classmethod
    def create_sqlite_database(cls):
        with sqlite3.connect(OISOL_HOME_PATH / 'foxhole_wiki_mirror.db') as conn:
            pass


async def run_db_wiki_update(*args) -> None:
    match args[0].lower():
        case 'update':
            await WikiTablesMirrorRunner.wiki_table_update_process(*args[1:])
        case 'init':
            WikiTablesMirrorRunner.create_sqlite_database()
