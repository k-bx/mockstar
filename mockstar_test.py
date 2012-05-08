# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
from mock import Mock

from mockstar import p
from mockstar import DotDict


def side_effect_one():
    pass


def side_effect_two():
    pass


def side_effect_three():
    val = side_effect_four()
    return val * 2


def side_effect_four():
    return 4


class TestDotDict(TestCase):
    def test_should_setattr_getattr(self):
        d = DotDict()
        d['foo'] = 'something'

        # do
        result = d.foo

        self.assertEquals(result, 'something')


class TestPatch(TestCase):
    @p(__name__ + '.side_effect_one')
    @p(__name__ + '.side_effect_two')
    def test_should_mock_to_kw(self, se):
        self.assertIsInstance(se.side_effect_one, Mock)
        self.assertIsInstance(se.side_effect_two, Mock)

    @p(__name__ + '.side_effect_four')
    def test_should_mock_inner_call(self, se):
        se.side_effect_four.return_value = 1

        # do
        result = side_effect_three()

        self.assertEquals(result, 2)


if __name__ == '__main__':
    unittest.main()
