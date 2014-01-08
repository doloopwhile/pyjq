# coding=utf8
import unittest
import re
import pyjq
import _pyjq


class TestJq(unittest.TestCase):
    def test_compile_dot(self):
        s = pyjq.compile('.')
        self.assertIsInstance(s, _pyjq.Script)

    def test_syntax_error(self):
        expected_message = re.escape('''\
error: syntax error, unexpected '*', expecting $end
**
1 compile error''')

        with self.assertRaisesRegex(ValueError, expected_message):
            s = pyjq.compile('**')

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
                'key6': [None, False, True, 1, 1.5, [None, False, True], {'foo': 'bar'}],
            },
        ]

        s = pyjq.compile('.')
        for obj in objects:
            self.assertEqual([obj], s.apply(obj))

    def test_assigning_values(self):
        self.assertEqual(pyjq.one('$foo', {}, foo='bar'), 'bar')
        self.assertEqual(pyjq.one('$foo', {}, foo=['bar']), ['bar'])


    def test_apply(self):
        self.assertEqual(pyjq.apply('. + $foo', 'val', foo='bar'), ['valbar'])

    def test_first(self):
        self.assertEqual(pyjq.first('. + $foo + "1", . + $foo + "2"', 'val', foo='bar'), 'valbar1')

    def test_one(self):
        self.assertEqual(pyjq.one('. + $foo', 'val', foo='bar'), 'valbar')

        # raise IndexError if there are multiple elements
        with self.assertRaises(IndexError):
            pyjq.one('. + $foo, . + $foo', 'val', foo='bar')


if __name__ == '__main__':
    unittest.main()
