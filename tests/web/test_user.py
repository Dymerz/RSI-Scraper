import pytest
from .validator import assert_valid_schema

@pytest.mark.user
def test_request():
	from rsi_scrapper import User

	object = User('dymerz')
	data = object.execute()
	assert data is not None

	assert_valid_schema(data, 'user.json')
