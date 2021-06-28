"""Stats
"""
import re

from .connector import Connector
from .interface import ICommand


class Stats(ICommand):
    __url_crow_stat = "https://robertsspaceindustries.com/api/stats/getCrowdfundStats"
    __url_roadmap = "https://robertsspaceindustries.com/api/roadmap/v1/init"
    __regex_api_live = r'(live\s*version\s*:\s*(?P<live_api>(\d+(\.\d+)*))?)'
    __regex_api_ptu = r'(ptu\s*version\s*:\s*(?P<ptu_version>(\d+(\.\d+)*))?)'
    __regex_api_etf = r'(ptu\s*version\s*:\s*(?P<etf_version>(\d+(\.\d+)*)(.*?)((ETF)|(Evocati))))'

    async def execute_async(self):
        return self.execute()

    def execute(self):
        """ Get general info
        """

        # Get stats info
        stats = self.__get_crow_stats()
        if stats is None:
            return None

        fleet = stats['fleet']
        if fleet is not None:
            fleet = int(fleet)

        req = Connector().request(self.__url_roadmap, method="get")
        if req is None or req.status_code != 200:
            return None

        text = req.text
        live_pu = self.__get_live_pu(text)
        live_ptu = self.__get_live_ptu(text)
        live_etf = self.__get_live_etf(text)

        return {
            "fans": int(stats['fans']),
            "funds": float(stats['funds']) / 100,
            "fleet": fleet,
            'current_live': live_pu,
            'current_ptu': live_ptu,
            'current_etf': live_etf,
        }

    def __get_live_pu(self, text):
        m = re.search(self.__regex_api_live, text, re.IGNORECASE)
        if m:
            return m.group(3)
        return None

    def __get_live_ptu(self, text):
        m = re.search(self.__regex_api_ptu, text, re.IGNORECASE)
        if m:
            return m.group(3)
        return None

    def __get_live_etf(self, text):
        m = re.search(self.__regex_api_etf, text, re.IGNORECASE)
        if m:
            return m.group(3)
        return None

    def __get_crow_stats(self, chart="day"):
        """ Get all Crow stats

            Returns:
                dict: assoc array of stats.
        """
        data = {
            "alpha_slots": True,
            "chart": chart,
            "fans": True,
            "fleet": True,
            "funds": True,
        }

        req = Connector().request(self.__url_crow_stat, method="post", json_data=data)

        if req is None or req.status_code != 200:
            return None

        resp = req.json()

        # check response
        if resp['success'] != 1 or "data" not in resp:
            return None

        return resp['data']
