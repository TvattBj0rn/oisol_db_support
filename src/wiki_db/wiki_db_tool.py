import aiohttp
from aiohttp import ClientSession


class WikiTablesMirrorRunner:
    __entrypoint = 'https://foxhole.wiki.gg/api.php?'
    __json_format = '&format=json'

    @classmethod
    async def wiki_table_update_process(cls, *target_tables):
        async with aiohttp.ClientSession() as session:
            # If no table is provided by the user, all wiki tables will be mirrored
            target_tables = await cls.__get_tables_list(session) if not target_tables else list(target_tables)
            print(target_tables)

    @classmethod
    async def __get_tables_list(cls, session: ClientSession) -> list[str] | None:
        res = await session.get(f'{cls.__entrypoint}action=cargotables{cls.__json_format}')
        if res.status == 200:
            return (await res.json())['cargotables']
        return None


async def run_db_wiki_update(*args) -> None:
    if args[0].lower() == 'update':
        await WikiTablesMirrorRunner.wiki_table_update_process(*args[1:])
