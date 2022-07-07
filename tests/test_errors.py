import pytest

from relic.core.errors import MismatchError

SAMPLES = [
    (MismatchError("Int", 0, 1),),
    (MismatchError("Str", "A", "B"),),
    (MismatchError("Float", 0.0, 0.1),),
]


class TestMismatchError:
    @pytest.mark.parametrize("err", SAMPLES)
    def test_str(self, err: MismatchError):
        str(err)
