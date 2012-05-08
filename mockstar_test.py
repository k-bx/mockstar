# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
from mock import Mock
from mock import patch

from mockstar import p
from mockstar import DotDict
from mockstar import prefixed_p


def side_effect_one():
    pass


def side_effect_two():
    pass


def side_effect_three():
    val = side_effect_four()
    return val * 2


def side_effect_four():
    return 4


def side_effect_five(n):
    return n


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

    @p(__name__ + '.side_effect_five', autospec=True)
    @patch('mockstar.patch')
    def test_should_pass_mock_parameters(self, mockstar_patch_mock, se):
        se.side_effect_five(10)
        self.assertRaises(TypeError, lambda: se.side_effect_five())


ppatch = prefixed_p(__name__)


class TestPrefixedP(TestCase):
    @ppatch('side_effect_five', autospec=True)
    def test_should_prefix_patch_here(self, se):
        self.assertRaises(TypeError, lambda: se.side_effect_five())


if __name__ == '__main__':
    unittest.main()
