from heart_server_helpers import existing_beats
import pytest


@pytest.mark.parametrize("pat_id, expected", [
    (-1, True),
    (-2, False),
])
def test_existing_beats(pat_id, expected):
    pat_exist = existing_beats(pat_id)
    assert pat_exist == expected
