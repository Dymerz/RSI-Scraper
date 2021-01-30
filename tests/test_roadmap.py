import pytest
from .validator import assert_valid_schema


@pytest.mark.roadmap
@pytest.mark.roadmap_starcitizen
def test_request_starcitizen():
    from rsi_scraper import Roadmap

    object = Roadmap('starcitizen', '3.12')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'roadmap_starcitizen.json')


@pytest.mark.roadmap
@pytest.mark.roadmap_squadron42
def test_request_squadron():
    from rsi_scraper import Roadmap

    object = Roadmap('squadron42')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'roadmap_squadron42.json')
