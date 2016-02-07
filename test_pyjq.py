# encoding: utf8
from __future__ import unicode_literals
import unittest
import re

from mock import patch

import pyjq
import _pyjq


class TestCaseBackwardCompatMixin:
    def assertRaisesRegex(self, *a, **kw):
        return self.assertRaisesRegexp(*a, **kw)


class TestJq(unittest.TestCase, TestCaseBackwardCompatMixin):
    def test_compile_dot(self):
        s = pyjq.compile('.')
        self.assertIsInstance(s, _pyjq.Script)

    def test_syntax_error(self):
        expected_message = re.escape(r"error: syntax error")
        with self.assertRaisesRegexp(ValueError, expected_message):
            pyjq.compile('**')

    def test_conversion_between_python_object_and_jv(self):
        objects = [
            None,
            False,
            True,
            1,
            1.5,
            "string",
            [None, False, True, 1, 1.5, [None, False, True], {'foo': 'bar'}],
            {
                'key1': None,
                'key2': False,
                'key3': True,
                'key4': 1,
                'key5': 1.5,
                'key6': [None, False, True, 1, 1.5,
                         [None, False, True], {'foo': 'bar'}],
            },
        ]

        s = pyjq.compile('.')
        for obj in objects:
            self.assertEqual([obj], s.all(obj))

    def test_assigning_values(self):
        self.assertEqual(pyjq.one('$foo', {}, vars=dict(foo='bar')), 'bar')
        self.assertEqual(pyjq.one('$foo', {}, vars=dict(foo=['bar'])), ['bar'])

    def test_all(self):
        self.assertEqual(
            pyjq.all('.[] | . + $foo', ['val1', 'val2'], vars=dict(foo='bar')),
            ['val1bar', 'val2bar']
        )

        self.assertEqual(
            pyjq.all('. + $foo', 'val', vars=dict(foo='bar')),
            ['valbar']
        )

    def test_first(self):
        self.assertEqual(
            pyjq.first('.[] | . + $foo', ['val1', 'val2'], vars=dict(foo='bar')),
            'val1bar'
        )

    def test_one(self):
        self.assertEqual(
            pyjq.one('. + $foo', 'val', vars=dict(foo='bar')),
            'valbar'
        )

        # raise IndexError if got multiple elements
        with self.assertRaises(IndexError):
            pyjq.one('.[]', [1, 2])

        # raise IndexError if got no elements
        with self.assertRaises(IndexError):
            pyjq.one('.[]', [])

    def test_url_argument(self):
        class FakeResponse:
            def getheader(self, name):
                return 'application/json;charset=SHIFT_JIS'

            def read(self):
                return '["Hello", "世界", "！"]'.encode('shift-jis')

        try:
            import urllib.request
            del urllib
        except ImportError:
            to_patch = 'urllib2.urlopen'
        else:
            to_patch = 'urllib.request.urlopen'
        to_patch = 'six.moves.urllib.request.urlopen'

        with patch(to_patch, return_value=FakeResponse()):
            self.assertEqual(
                pyjq.all('.[] | . + .', url='http://example.com'),
                ["HelloHello", "世界世界", "！！"]
            )

        def opener(url):
            return [1, 2, 3]

        self.assertEqual(
            pyjq.all('.[] | . + .', url='http://example.com', opener=opener),
            [2, 4, 6]
        )


if __name__ == '__main__':
    unittest.main()
