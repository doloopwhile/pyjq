# encoding: utf8
from __future__ import unicode_literals

import io
import os.path
import re
import shutil
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

import pytest

import _pyjq
import pyjq


def test_compile_dot():
    s = pyjq.compile(".")
    assert isinstance(s, _pyjq.Script)


def test_syntax_error():
    with pytest.raises(ValueError, match=r"error: syntax error"):
        pyjq.compile("**")


def test_non_json_data():
    with pytest.raises(
        TypeError,
        match=re.escape("<class 'datetime.datetime'> could not be converted to json"),
    ):
        pyjq.all(".", {"date": datetime.now()})


def test_conversion_between_python_object_and_jv():
    objects = [
        None,
        False,
        True,
        1,
        1.5,
        "string",
        [None, False, True, 1, 1.5, [None, False, True], {"foo": "bar"}],
        {
            "key1": None,
            "key2": False,
            "key3": True,
            "key4": 1,
            "key5": 1.5,
            "key6": [None, False, True, 1, 1.5, [None, False, True], {"foo": "bar"}],
        },
    ]

    s = pyjq.compile(".")
    for obj in objects:
        assert [obj] == s.all(obj)


def test_assigning_values():
    assert pyjq.one("$foo", {}, vars=dict(foo="bar")) == "bar"
    assert pyjq.one("$foo", {}, vars=dict(foo=["bar"])) == ["bar"]


def test_all():
    assert pyjq.all(".[] | . + $foo", ["val1", "val2"], vars=dict(foo="bar")) == [
        "val1bar",
        "val2bar",
    ]
    assert pyjq.all(". + $foo", "val", vars=dict(foo="bar")) == ["valbar"]


def test_first():
    assert (
        pyjq.first(".[] | . + $foo", ["val1", "val2"], vars=dict(foo="bar"))
        == "val1bar"
    )


def test_one():
    assert pyjq.one(". + $foo", "val", vars=dict(foo="bar")) == "valbar"

    # if got multiple elements
    with pytest.raises(IndexError):
        pyjq.one(".[]", [1, 2])

    # if got no elements
    with pytest.raises(IndexError):
        pyjq.one(".[]", [])


def test_url_argument():
    class FakeResponse:
        def getheader(self, name):
            return "application/json;charset=SHIFT_JIS"

        def read(self):
            return '["Hello", "世界", "！"]'.encode("shift-jis")

    with patch("urllib.request.urlopen", return_value=FakeResponse()):
        assert pyjq.all(".[] | . + .", url="http://example.com") == [
            "HelloHello",
            "世界世界",
            "！！",
        ]

    def opener(url):
        return [1, 2, 3]

    assert pyjq.all(".[] | . + .", url="http://example.com", opener=opener) == [2, 4, 6]


def test_library_path(tmp_path_factory):
    library_path = tmp_path_factory.mktemp("a")
    library_path2 = tmp_path_factory.mktemp("b")

    library_file = library_path / "greeting.jq"
    library_file2 = library_path2 / "increment.jq"

    with library_file.open("w", encoding="ascii") as f:
        f.write('def hello: "HELLO";')
        f.write('def world: "WORLD";')
    with library_file2.open("w", encoding="ascii") as f:
        f.write("def increment: . + 1;\n")
    values = pyjq.all(
        'include "greeting"; include "increment"; .[] | [. | increment, hello, world]',
        [1, 2, 3],
        library_paths=[
            str(library_path),
            library_path2,
        ],  # It accepts both of str and pathlib.Path
    )
    assert [
        [2, "HELLO", "WORLD"],
        [3, "HELLO", "WORLD"],
        [4, "HELLO", "WORLD"],
    ] == values


def test_script_runtime_error_exported():
    pyjq.ScriptRuntimeError  # exported
