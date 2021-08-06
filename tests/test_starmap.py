import pytest
from .validator import assert_valid_schema


@pytest.mark.starmap
def test_request_systems():
    from rsi_scraper import StarmapSystems

    object = StarmapSystems('pyro')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'starmap_systems.json')


@pytest.mark.starmap
def test_request_search():
    from rsi_scraper import StarmapSearch

    object = StarmapSearch('Stanton')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'starmap_search.json')


@pytest.mark.starmap
def test_request_object():
    from rsi_scraper import StarmapCelestialObjects

    object = StarmapCelestialObjects('TOHIL.PLANETS.TOHILIII')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'starmap_object.json')


@pytest.mark.starmap
def test_request_star_system():
    from rsi_scraper import StarmapStarSystems

    object = StarmapStarSystems('STANTON')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'starmap_star_system.json')


@pytest.mark.starmap
def test_request_tunnels():
    from rsi_scraper import StarmapTunnels

    object = StarmapTunnels('1188')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'starmap_tunnels.json')


@pytest.mark.starmap
def test_request_species():
    from rsi_scraper import StarmapSpecies

    object = StarmapSpecies()
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'starmap_species.json')


@pytest.mark.starmap
@pytest.mark.parametrize('_from, to, ship_size', [
    ('STANTON.LZS.LORVILLE', 'STANTON.LZS.AREA18', "M"),
    ('STANTON.LZS.LORVILLE', 'STANTON.LZS.AREA18', "L"),
    ('STANTON.LZS.LORVILLE', 'STANTON.LZS.AREA18', "S"),
    ('SOL.PLANETS.EARTH', 'PYRO.PLANETS.PYROI', 'L'),
    ('ORION.PLANET.ORIONIIIARMITAGE', 'AYRKA.PLANET.AYRKAII', 'S'),
])
def test_request_route_search(_from, to, ship_size):
    from rsi_scraper import StarmapRouteSearch

    object = StarmapRouteSearch(_from, to, ship_size)
    data = object.execute()

    assert data is not None

    assert_valid_schema(data, 'starmap_route_search.json')
