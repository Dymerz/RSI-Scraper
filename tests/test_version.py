import pytest
from .validator import assert_valid_schema


@pytest.mark.version
def test_request():
    from rsi_scrapper import Version

    object = Version()
    data = object.execute()
    assert data is not None

    with open('log.json', 'w') as f:
        f.write(str(data))
    assert_valid_schema(data, 'version.json')
