import pytest
from .validator import assert_valid_schema


@pytest.mark.organization_members
@pytest.mark.parametrize('sid, page', [
    ('PROTECTORA', 3),
    ('CORCOP', 1),
    ('IPIX', 3),
])
def test_request(sid, page):
    from rsi_scrapper import OrganizationMembers

    object = OrganizationMembers(sid, page=page)
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'organization_members.json')
