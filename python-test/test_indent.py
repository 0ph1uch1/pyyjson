# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import datetime
import json

import pyyjson

from util import read_fixture_obj


class TestIndentedOutput:
    def test_equivalent(self):
        """
        OPT_INDENT_2 is equivalent to indent=2
        """
        obj = {"a": "b", "c": {"d": True}, "e": [1, 2]}
        assert pyyjson.dumps(obj, option=pyyjson.OPT_INDENT_2) == json.dumps(
            obj, indent=2
        ).encode("utf-8")

    def test_sort(self):
        obj = {"b": 1, "a": 2}
        assert (
            pyyjson.dumps(obj, option=pyyjson.OPT_INDENT_2 | pyyjson.OPT_SORT_KEYS)
            == b'{\n  "a": 2,\n  "b": 1\n}'
        )

    def test_non_str(self):
        obj = {1: 1, "a": 2}
        assert (
            pyyjson.dumps(obj, option=pyyjson.OPT_INDENT_2 | pyyjson.OPT_NON_STR_KEYS)
            == b'{\n  "1": 1,\n  "a": 2\n}'
        )

    def test_options(self):
        obj = {
            1: 1,
            "b": True,
            "a": datetime.datetime(1970, 1, 1),
        }
        assert (
            pyyjson.dumps(
                obj,
                option=pyyjson.OPT_INDENT_2
                | pyyjson.OPT_SORT_KEYS
                | pyyjson.OPT_NON_STR_KEYS
                | pyyjson.OPT_NAIVE_UTC,
            )
            == b'{\n  "1": 1,\n  "a": "1970-01-01T00:00:00+00:00",\n  "b": true\n}'
        )

    def test_empty(self):
        obj = [{}, [[[]]], {"key": []}]
        ref = b'[\n  {},\n  [\n    [\n      []\n    ]\n  ],\n  {\n    "key": []\n  }\n]'
        assert pyyjson.dumps(obj, option=pyyjson.OPT_INDENT_2) == ref

    def test_twitter_pretty(self):
        """
        twitter.json pretty
        """
        obj = read_fixture_obj("twitter.json.xz")
        assert pyyjson.dumps(obj, option=pyyjson.OPT_INDENT_2) == json.dumps(
            obj, indent=2, ensure_ascii=False
        ).encode("utf-8")

    def test_github_pretty(self):
        """
        github.json pretty
        """
        obj = read_fixture_obj("github.json.xz")
        assert pyyjson.dumps(obj, option=pyyjson.OPT_INDENT_2) == json.dumps(
            obj, indent=2, ensure_ascii=False
        ).encode("utf-8")

    def test_canada_pretty(self):
        """
        canada.json pretty
        """
        obj = read_fixture_obj("canada.json.xz")
        assert pyyjson.dumps(obj, option=pyyjson.OPT_INDENT_2) == json.dumps(
            obj, indent=2, ensure_ascii=False
        ).encode("utf-8")

    def test_citm_catalog_pretty(self):
        """
        citm_catalog.json pretty
        """
        obj = read_fixture_obj("citm_catalog.json.xz")
        assert pyyjson.dumps(obj, option=pyyjson.OPT_INDENT_2) == json.dumps(
            obj, indent=2, ensure_ascii=False
        ).encode("utf-8")
