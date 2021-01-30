import pytest
from .validator import assert_valid_schema


@pytest.mark.ship
def test_request():
    from rsi_scraper import Ship

    object = Ship(name='Cutlass Black')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'ship.json')
