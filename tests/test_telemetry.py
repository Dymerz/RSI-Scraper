import pytest
from .validator import assert_valid_schema


@pytest.mark.telemetry
def test_request():
    from rsi_scraper import Telemetry

    object = Telemetry('MONTH', '3.7')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'telemetry.json')
