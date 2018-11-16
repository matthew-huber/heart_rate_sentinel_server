from heart_server_helpers import hr_avg_since
import pytest


@pytest.mark.parametrize("pat_id, start_time, expected", [
    (-1, "2017-01-01 12:00:00.000000", 90),
    (-1, "2018-11-16 11:19:00.000000", 100),
    (-1, "2018-11-16 12:30:00.000000", 100),
    (-1, "2018-11-17 12:10:00.000000", 0),
])
def test_existing_beats(pat_id, start_time, expected):
    hr_avg = hr_avg_since(pat_id, start_time)
    assert hr_avg == expected
