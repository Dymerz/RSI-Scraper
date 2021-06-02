import pytest
from .validator import assert_valid_schema


@pytest.mark.organization
@pytest.mark.parametrize('sid', [
    ('SIBYLLA'),
    ('PROTECTORA'),
    ('ODINT'),
    ('HWFC'),
    ('STARD'),
])
@pytest.mark.organization
def test_request(sid):
    from rsi_scraper import Organization

    object = Organization(sid)
    data = object.execute()

    # with open("./test.json", 'w') as f:
    #     f.write(str(data))

    assert data is not None

    assert_valid_schema(data, 'organization.json')
