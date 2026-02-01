import asyncio
import sys

from src.wiki_db.wiki_db_tool import run_db_wiki_update


async def parser() -> None:
    # sys.argv -> 0 is the binary
    if len(sys.argv) == 1:
        return

    if sys.argv[1].lower() == '--wiki':
        await run_db_wiki_update(*sys.argv[2:])
    if sys.argv[1].lower() == 'test':
        print(f'This seems to be working: {sys.argv}')


if __name__ == '__main__':
    asyncio.run(parser())
