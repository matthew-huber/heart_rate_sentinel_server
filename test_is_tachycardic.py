from heart_server_helpers import is_tachycardic
import pytest


@pytest.mark.parametrize("pat_id, expected", [
    (-1, False),
    (-4, True),
])
def test_existing_beats(pat_id, expected):
    tachycardia = is_tachycardic(pat_id)
    assert tachycardia == expected
