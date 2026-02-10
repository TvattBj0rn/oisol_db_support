import asyncio
import sys

from src.oisol_db import oisol_db_runner
from src.wiki_db import run_db_wiki_update


async def parser() -> None:
    # sys.argv -> 0 is the binary
    if len(sys.argv) == 1:
        return

    argv_copy = sys.argv.copy()

    match argv_copy[1].lower():
        case '--wiki':
            await run_db_wiki_update(*argv_copy[2:])
        case '--oisol':
            oisol_db_runner(*argv_copy[2:])
        case 'test':
            print(f'This seems to be working: {argv_copy}')
        case _:
            print('Unknown command')


if __name__ == '__main__':
    asyncio.run(parser())
