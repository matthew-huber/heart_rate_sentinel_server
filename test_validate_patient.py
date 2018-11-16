from heart_server_helpers import validate_patient
import pytest


@pytest.mark.parametrize("pat_id, expected", [
    (-1, True),
    (-2, True),
    (-3, False),
])
def test_existing_beats(pat_id, expected):
    pat_exist = validate_patient(pat_id)
    assert pat_exist == expected
