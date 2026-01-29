import requests


class WikiTablesMirrorRunner:
    __entrypoint = 'https://foxhole.wiki.gg/api.php?'
    __json_format = '&format=json'

    def __init__(self):
        wiki_tables = self.__get_tables_list()

    def __get_tables_list(self) -> list[str] | None:
        res = requests.get(f'{self.__entrypoint}action=cargotables{self.__json_format}')
        if res.status_code == 200:
            return res.json()['cargotables']
        return None


def run_db_wiki_update() -> None:
    WikiTablesMirrorRunner()
