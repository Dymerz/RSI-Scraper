import pytest
from .validator import assert_valid_schema


@pytest.mark.progress_tracker
def test_request():
    from rsi_scraper import ProgressTracker

    object = ProgressTracker()
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'progress_tracker.json')


@pytest.mark.progress_tracker_info
def test_request_info():
    from rsi_scraper import ProgressTrackerInfo

    object = ProgressTrackerInfo('g42qg07ipfday')
    data = object.execute()
    assert data is not None

    assert_valid_schema(data, 'progress_tracker_info.json')
