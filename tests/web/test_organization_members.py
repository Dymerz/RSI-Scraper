import pytest
from .validator import assert_valid_schema

@pytest.mark.organization_members
def test_request():
	from rsi_scrapper import OrganizationMembers

	object = OrganizationMembers('PROTECTORA', page=2)
	data = object.execute()
	assert data is not None

	assert_valid_schema(data, 'organization_members.json')
