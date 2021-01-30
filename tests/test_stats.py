import pytest
from .validator import assert_valid_schema


@pytest.mark.stats
def test_request():
    from rsi_scraper import Stats

    object = Stats()
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'stats.json')
