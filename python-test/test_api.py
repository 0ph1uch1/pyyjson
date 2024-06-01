# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import datetime
import inspect
import json
import re

import pytest

import pyyjson

SIMPLE_TYPES = (1, 1.0, -1, None, "str", True, False)

LOADS_RECURSION_LIMIT = 1024


def default(obj):
    return str(obj)


class TestApi:
    def test_loads_trailing(self):
        """
        loads() handles trailing whitespace
        """
        assert pyyjson.loads("{}\n\t ") == {}

    def test_loads_trailing_invalid(self):
        """
        loads() handles trailing invalid
        """
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, "{}\n\t a")

    def test_simple_json(self):
        """
        dumps() equivalent to json on simple types
        """
        for obj in SIMPLE_TYPES:
            assert pyyjson.dumps(obj) == json.dumps(obj).encode("utf-8")

    def test_simple_round_trip(self):
        """
        dumps(), loads() round trip on simple types
        """
        for obj in SIMPLE_TYPES:
            assert pyyjson.loads(pyyjson.dumps(obj)) == obj

    def test_loads_type(self):
        """
        loads() invalid type
        """
        for val in (1, 3.14, [], {}, None):
            pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, val)

    def test_loads_recursion_partial(self):
        """
        loads() recursion limit partial
        """
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, "[" * (1024 * 1024))

    def test_loads_recursion_valid_limit_array(self):
        """
        loads() recursion limit at limit array
        """
        n = LOADS_RECURSION_LIMIT + 1
        value = b"[" * n + b"]" * n
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, value)

    def test_loads_recursion_valid_limit_object(self):
        """
        loads() recursion limit at limit object
        """
        n = LOADS_RECURSION_LIMIT
        value = b'{"key":' * n + b'{"key":true}' + b"}" * n
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, value)

    def test_loads_recursion_valid_limit_mixed(self):
        """
        loads() recursion limit at limit mixed
        """
        n = LOADS_RECURSION_LIMIT
        value = b"[" b'{"key":' * n + b'{"key":true}' + b"}" * n + b"]"
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, value)

    def test_loads_recursion_valid_excessive_array(self):
        """
        loads() recursion limit excessively high value
        """
        n = 10000000
        value = b"[" * n + b"]" * n
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, value)

    def test_loads_recursion_valid_limit_array_pretty(self):
        """
        loads() recursion limit at limit array pretty
        """
        n = LOADS_RECURSION_LIMIT + 1
        value = b"[\n  " * n + b"]" * n
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, value)

    def test_loads_recursion_valid_limit_object_pretty(self):
        """
        loads() recursion limit at limit object pretty
        """
        n = LOADS_RECURSION_LIMIT
        value = b'{\n  "key":' * n + b'{"key":true}' + b"}" * n
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, value)

    def test_loads_recursion_valid_limit_mixed_pretty(self):
        """
        loads() recursion limit at limit mixed pretty
        """
        n = LOADS_RECURSION_LIMIT
        value = b"[\n  " b'{"key":' * n + b'{"key":true}' + b"}" * n + b"]"
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, value)

    def test_loads_recursion_valid_excessive_array_pretty(self):
        """
        loads() recursion limit excessively high value pretty
        """
        n = 10000000
        value = b"[\n  " * n + b"]" * n
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, value)

    def test_version(self):
        """
        __version__
        """
        assert re.match(r"^\d+\.\d+(\.\d+)?$", pyyjson.__version__)

    def test_valueerror(self):
        """
        pyyjson.JSONDecodeError is a subclass of ValueError
        """
        pytest.raises(pyyjson.JSONDecodeError, pyyjson.loads, "{")
        pytest.raises(ValueError, pyyjson.loads, "{")

    def test_optional_none(self):
        """
        dumps() option, default None
        """
        assert pyyjson.dumps([], option=None) == b"[]"
        assert pyyjson.dumps([], default=None) == b"[]"
        assert pyyjson.dumps([], option=None, default=None) == b"[]"
        assert pyyjson.dumps([], None, None) == b"[]"

    def test_option_not_int(self):
        """
        dumps() option not int or None
        """
        with pytest.raises(pyyjson.JSONEncodeError):
            pyyjson.dumps(True, option=True)

    def test_option_invalid_int(self):
        """
        dumps() option invalid 64-bit number
        """
        with pytest.raises(pyyjson.JSONEncodeError):
            pyyjson.dumps(True, option=9223372036854775809)

    def test_option_range_low(self):
        """
        dumps() option out of range low
        """
        with pytest.raises(pyyjson.JSONEncodeError):
            pyyjson.dumps(True, option=-1)

    def test_option_range_high(self):
        """
        dumps() option out of range high
        """
        with pytest.raises(pyyjson.JSONEncodeError):
            pyyjson.dumps(True, option=1 << 12)

    def test_opts_multiple(self):
        """
        dumps() multiple option
        """
        assert (
            pyyjson.dumps(
                [1, datetime.datetime(2000, 1, 1, 2, 3, 4)],
                option=pyyjson.OPT_STRICT_INTEGER | pyyjson.OPT_NAIVE_UTC,
            )
            == b'[1,"2000-01-01T02:03:04+00:00"]'
        )

    def test_default_positional(self):
        """
        dumps() positional arg
        """
        with pytest.raises(TypeError):
            pyyjson.dumps(__obj={})  # type: ignore
        with pytest.raises(TypeError):
            pyyjson.dumps(zxc={})  # type: ignore

    def test_default_unknown_kwarg(self):
        """
        dumps() unknown kwarg
        """
        with pytest.raises(TypeError):
            pyyjson.dumps({}, zxc=default)  # type: ignore

    def test_default_empty_kwarg(self):
        """
        dumps() empty kwarg
        """
        assert pyyjson.dumps(None, **{}) == b"null"

    def test_default_twice(self):
        """
        dumps() default twice
        """
        with pytest.raises(TypeError):
            pyyjson.dumps({}, default, default=default)  # type: ignore

    def test_option_twice(self):
        """
        dumps() option twice
        """
        with pytest.raises(TypeError):
            pyyjson.dumps({}, None, pyyjson.OPT_NAIVE_UTC, option=pyyjson.OPT_NAIVE_UTC)  # type: ignore

    def test_option_mixed(self):
        """
        dumps() option one arg, one kwarg
        """

        class Custom:
            def __str__(self):
                return "zxc"

        assert (
            pyyjson.dumps(
                [Custom(), datetime.datetime(2000, 1, 1, 2, 3, 4)],
                default,
                option=pyyjson.OPT_NAIVE_UTC,
            )
            == b'["zxc","2000-01-01T02:03:04+00:00"]'
        )

    def test_dumps_signature(self):
        """
        dumps() valid __text_signature__
        """
        assert (
            str(inspect.signature(pyyjson.dumps))
            == "(obj, /, default=None, option=None)"
        )
        inspect.signature(pyyjson.dumps).bind("str")
        inspect.signature(pyyjson.dumps).bind("str", default=default, option=1)
        inspect.signature(pyyjson.dumps).bind("str", default=None, option=None)

    def test_loads_signature(self):
        """
        loads() valid __text_signature__
        """
        assert str(inspect.signature(pyyjson.loads)), "(obj == /)"
        inspect.signature(pyyjson.loads).bind("[]")

    def test_dumps_module_str(self):
        """
        pyyjson.dumps.__module__ is a str
        """
        assert pyyjson.dumps.__module__ == "pyyjson"

    def test_loads_module_str(self):
        """
        pyyjson.loads.__module__ is a str
        """
        assert pyyjson.loads.__module__ == "pyyjson"

    def test_bytes_buffer(self):
        """
        dumps() trigger buffer growing where length is greater than growth
        """
        a = "a" * 900
        b = "b" * 4096
        c = "c" * 4096 * 4096
        assert pyyjson.dumps([a, b, c]) == f'["{a}","{b}","{c}"]'.encode("utf-8")

    def test_bytes_null_terminated(self):
        """
        dumps() PyBytesObject buffer is null-terminated
        """
        # would raise ValueError: invalid literal for int() with base 10: b'1596728892'
        int(pyyjson.dumps(1596728892))
