"""Starmap
"""
from .connector import Connector
from .interface import ICommand


class StarmapSystems(ICommand):
    """StarmapSystems
    """

    def __init__(self, name: str = None):
        """
        Args:
            name (str, optional): The name of the System. Default to None.
        """
        self.name = name

    async def execute_async(self):
        return self.execute()

    # Get Systems info
    def execute(self):
        systems = get_data("systems")
        if systems is None:
            return None

        if self.name is None:
            res = systems
        else:
            res = list(filter(lambda s: (str(s['name']).lower() == str(self.name).lower()), systems))

        if len(res) == 0:
            return None
        return res


class StarmapTunnels(ICommand):
    """StarmapTunnels
    """

    def __init__(self, tid: str = None):
        """

        Args:
            tid (str, optional): The tunnel identifier (tid). Default to None.
        """
        self.tid = tid

    async def execute_async(self):
        return self.execute()

    # Get Tunnels info
    def execute(self):
        tunnels = get_data("tunnels")
        if tunnels is None:
            return None

        if self.tid is None:
            res = tunnels
        else:
            res = list(filter(lambda s: str(s['id']).lower() == str(self.tid).lower(), tunnels))

        if len(res) == 0:
            return None
        return res


class StarmapSpecies(ICommand):
    """StarmapSpecies
    """

    def __init__(self, name: str = None):
        """
        Args:
            name (str, optional): The name of the specie. Default to None.
        """
        self.name = name

    async def execute_async(self):
        return self.execute()

    # Get Species info
    def execute(self):
        species = get_data("species")
        if species is None:
            return None

        if self.name is None:
            res = species
        else:
            res = list(filter(
                lambda s: str(s['name']).lower() == str(self.name).lower() or str(s['code']).lower() == str(
                    self.name).lower(), species))

        if len(res) == 0:
            return None
        return res


class StarmapAffiliations(ICommand):
    """StarmapAffiliations
    """

    def __init__(self, name: str = None):
        """
        Args:
            name (str, optional): The name of the affiliation. Default to None.
        """
        self.name = name

    async def execute_async(self):
        return self.execute()

    # Get Affiliations info
    def execute(self):
        affiliations = get_data("affiliations")
        if affiliations is None:
            return None

        if self.name is None:
            res = affiliations
        else:
            res = list(filter(lambda s: s['name'] == self.name or s['code'] == self.name, affiliations))

        if len(res) == 0:
            return None
        return res


class StarmapStarSystems(ICommand):
    """StarmapStarSystems
    """

    __url_star_system = "https://robertsspaceindustries.com/api/starmap/star-systems/{0}"

    def __init__(self, code: str):
        """
        Args:
            code (str): The code of the star system.
        """
        self.code = code

    async def execute_async(self):
        return self.execute()

    # Get Celetial Objects info
    def execute(self):
        req = Connector().request(self.__url_star_system.format(self.code))
        if req is None or req.status_code != 200:
            return None

        resp = req.json()

        # check response
        if resp['success'] != 1 or "data" not in resp:
            return None

        return resp['data']['resultset']


class StarmapCelestialObjects(ICommand):
    """StarmapCelestialObjects
    """

    __url_celestial = "https://robertsspaceindustries.com/api/starmap/celestial-objects/{0}"

    def __init__(self, code: str):
        """
        Args:
            code (str): The code field of the object.
        """
        self.code = code

    async def execute_async(self):
        return self.execute()

    # Get Celetial Objects info
    def execute(self):
        req = Connector().request(self.__url_celestial.format(self.code))
        if req is None or req.status_code != 200:
            return None

        resp = req.json()

        # check response
        if resp['success'] != 1 or "data" not in resp:
            return None

        return resp['data']['resultset']


class StarmapSearch(ICommand):
    """StarmapSearch
    """

    __url_find = "https://robertsspaceindustries.com/api/starmap/find"

    def __init__(self, search: str):
        """
        Args:
            search (str): The search.
        """
        self.search = search

    async def execute_async(self):
        return self.execute()

    def execute(self):
        data = {
            "query": self.search
        }
        req = Connector().request(self.__url_find, data)
        if req is None or req.status_code != 200:
            return None

        resp = req.json()

        # check response
        if resp['success'] != 1 or "data" not in resp:
            return None

        res = {
            "systems": resp['data']['systems']['resultset'],
            "objects": resp['data']['objects']['resultset']
        }
        return res


class StarmapRouteSearch(ICommand):
    """StarmapRouteSearch
    """

    __url_find = "https://robertsspaceindustries.com/api/starmap/routes/find"

    def __init__(self, _from: str, to: str, ship_size: str):
        """
        Args:
            _from (str): The object code for the departing system
            to (str): The object code for the destination system
            ship_size (str): The size of the ship traveling. Valid values are S, M, L
        """
        self._from = _from
        self._to = to
        self._size = ship_size

    async def execute_async(self):
        return self.execute()

    def execute(self):
        data = {
            "departure": self._from,
            "destination": self._to,
            "ship_size": self._size
        }
        req = Connector().request(self.__url_find, data)
        if req is None or req.status_code != 200:
            return None

        resp = req.json()

        # check response
        if resp['success'] != 1 or "data" not in resp:
            return None

        res = {
            "shortest": resp['data']['shortest'],
            "leastjumps": resp['data']['leastjumps']
        }
        return res


__url_systems = "https://robertsspaceindustries.com/api/starmap/bootup"


def get_data(field: str):
    """Retrieved data from the website

    Args:
        field (str): The field to return

    Returns:
        dict: The selected data
    """
    req = Connector().request(__url_systems)
    if req is None or req.status_code != 200:
        return None

    resp = req.json()

    # check response
    if resp['success'] != 1 or "data" not in resp:
        return None

    return resp['data'][field]['resultset']
