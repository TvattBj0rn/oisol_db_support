import asyncio
import sys

from src.wiki_db.wiki_db_tool import run_db_wiki_update


async def parser() -> None:
    # sys.argv -> 0 is the binary
    if len(sys.argv) == 1:
        return

    match sys.argv[1].lower():
        case '--wiki':
            await run_db_wiki_update(*sys.argv[2:])
        case '--oisol':
            pass
        case 'test':
            print(f'This seems to be working: {sys.argv}')
        case _:
            print('Unknown command')


if __name__ == '__main__':
    asyncio.run(parser())
