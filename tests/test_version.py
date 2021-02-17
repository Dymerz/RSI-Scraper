import pytest
from .validator import assert_valid_schema


@pytest.mark.version
def test_request():
    from rsi_scraper import Version

    object = Version()
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'version.json')
