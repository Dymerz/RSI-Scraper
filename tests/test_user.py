import pytest
from .validator import assert_valid_schema


@pytest.mark.user
@pytest.mark.parametrize('handle', [
    ("dymerz"),
    ("Dewderonomy")
])
def test_request(handle):
    from rsi_scraper import User

    object = User(handle)
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'user.json')
