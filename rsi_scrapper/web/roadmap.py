"""Roadmap
"""
from .connector import Connector
from .interface import ICommand


class Roadmap(ICommand):
    """Roadmap
    """

    __url_roadmap_sc = "https://robertsspaceindustries.com/api/roadmap/v1/boards/1"
    __url_roadmap_s42 = "https://robertsspaceindustries.com/api/roadmap/v1/boards/2"

    def __init__(self, board: str, version: str = None):
        """
        Args:
            board (str): The roadmap board ("starcitizen" or "squadron42").
            version (str, optional): The starcitizen version. Default to None.
        """
        self.board = board
        self.version = version

    async def execute_async(self):
        return self.execute()

    def execute(self):
        req = None
        if self.board == "starcitizen":
            req = Connector().request(self.__url_roadmap_sc, method="get")
        elif self.board == "squadron42":
            req = Connector().request(self.__url_roadmap_s42, method="get")
        else:
            return None

        if req is None or req.status_code != 200:
            return None

        try:
            resp = req.json()
        except Exception as e:
            print(e, flush=True)
            return None

        # get html contents
        if resp['success'] != 1 or "data" not in resp or "releases" not in resp['data']:
            return None

        releases = resp['data']['releases']
        categories = resp['data']['categories']

        cats = {}
        for c in categories:
            cats[int(c['id'])] = c['name']

        for r in releases:
            for c in r['cards']:
                c['category_name'] = cats[int(c['category_id'])]

        if self.version is None:
            return releases

        for r in releases:
            if r['name'] == self.version:
                return [r]
        return []
