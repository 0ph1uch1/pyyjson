# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import pyyjson


@pytest.mark.parametrize(
    "input",
    [
        b'"\xc8\x93',
        b'"\xc8',
    ],
)
def test_invalid(input):
    with pytest.raises(pyyjson.JSONDecodeError):
        pyyjson.loads(input)
