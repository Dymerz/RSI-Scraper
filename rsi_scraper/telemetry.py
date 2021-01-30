"""Telemetry
"""

from .connector import Connector
from .interface import ICommand


class Telemetry(ICommand):
    """Telemetry
    """

    __url_telemetry = "https://robertsspaceindustries.com/api/telemetry/v2/community/"

    def __init__(self, timetable: str, version: str):
        """
        Args:
            timetable (str): "DAY", "WEEK", "MONTH".
            version (str): The Star Citizen game version.
        """
        self.timetable = timetable
        self.version = version

    async def execute_async(self):
        return self.execute()

    def execute(self):
        query = f"?&timetable={self.timetable}&branch=sc-alpha-{self.version}"

        req = Connector().request(self.__url_telemetry + query, method="get")

        if req is None or req.status_code != 200:
            return None

        resp = req.json()

        # check response
        if resp['success'] != 1 or "data" not in resp:
            return None

        return resp['data']
