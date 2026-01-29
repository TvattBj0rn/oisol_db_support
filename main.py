import sys

from src.wiki_db.wiki_db_tool import run_db_wiki_update

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'wiki':
        run_db_wiki_update()
