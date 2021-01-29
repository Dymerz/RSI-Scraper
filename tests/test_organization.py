import pytest
from .validator import assert_valid_schema


@pytest.mark.organization
def test_request():
    from rsi_scrapper import Organization

    object = Organization('PROTECTORA')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'organization.json')
