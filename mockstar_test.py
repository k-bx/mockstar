# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
from mock import MagicMock
from mock import patch

from mockstar import p
from mockstar import DotDict
from mockstar import prefixed_p
from mockstar import M
from mockstar import sequence_side_effect
from mockstar import BaseTestCase


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
        self.assertIsInstance(se.side_effect_one, MagicMock)
        self.assertIsInstance(se.side_effect_two, MagicMock)

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


class TestMultiPatch(TestCase):
    @p(__name__ + '.side_effect_one', __name__ + '.side_effect_two')
    def test_should_mock_to_kw(self, se):
        self.assertIsInstance(se.side_effect_one, MagicMock)
        self.assertIsInstance(se.side_effect_two, MagicMock)


class TestM(TestCase):
    def test_should_create_object(self):
        m = M()
        m.asd = 'dsa'
        self.assertEquals(m.asd, 'dsa')

    def test_should_make_couple_rv(self):
        m = M()
        m.foo.rv.bar.rv.baz.rv = 28
        self.assertEquals(m.foo().bar().baz(), 28)


ppatch = prefixed_p(__name__)
# ppatch_autospec_M = prefixed_p(__name__, autospec=True, to_m=True)
ppatch_autospec = prefixed_p(__name__, autospec=False)


class TestPrefixedP(TestCase):
    @ppatch('side_effect_five', autospec=True)
    def test_should_prefix_patch_here(self, se):
        self.assertRaises(TypeError, lambda: se.side_effect_five())

    @ppatch_autospec('side_effect_five', autospec=True)
    def test_should_rewrite_ppatch_param(self, se):
        self.assertRaises(TypeError, lambda: se.side_effect_five())

    # @ppatch_autospec_M('side_effect_five')
    # def test_should_return_m_and_raise_typeerror(self, se):
    #     self.assertRaises(TypeError, lambda: se.side_effect_five())
    #     se.side_effect_five.rv = 20
    #     res = se.side_effect_five(10)
    #     self.assertEquals(res, 20)
    #     # self.assertIsInstance(m, M)


@ppatch('side_effect_one')
@ppatch('side_effect_two')
class TestPatchClass(TestCase):
    def test_should_get_se(self, se):
        self.assertIsInstance(se.side_effect_one, MagicMock)
        self.assertIsInstance(se.side_effect_two, MagicMock)

    def test_should_also_get_se(self, se):
        self.assertIsInstance(se.side_effect_one, MagicMock)
        self.assertIsInstance(se.side_effect_two, MagicMock)


@ppatch('side_effect_one', 'side_effect_two')
class TestMultiPatchClass(TestCase):
    def test_should_get_se(self, se):
        self.assertIsInstance(se.side_effect_one, MagicMock)
        self.assertIsInstance(se.side_effect_two, MagicMock)

    def test_should_also_get_se(self, se):
        self.assertIsInstance(se.side_effect_one, MagicMock)
        self.assertIsInstance(se.side_effect_two, MagicMock)


class TestSequenceSideEffect(TestCase):
    def test_should_get_sequence(self):
        m = M(side_effect=sequence_side_effect(1, 2, 3))
        self.assertEquals(m(), 1)
        self.assertEquals(m(), 2)
        self.assertEquals(m(), 3)


def foo():
    return 2 + 3


count_score_rv = M()


def count_score():
    return count_score_rv


def count_score_caller():
    return count_score()


class TestSideEffectsMethod(BaseTestCase):
    @ppatch('count_score')
    @ppatch('foo')
    def side_effects(self, se):
        se.something = se.foo.return_value
        se.four = 4
        return self.invoke(se)

    def test_should_get_foo_mocked(self, se):
        self.assertIsInstance(se.foo(), MagicMock)

    def test_should_also_get_foo_mocksed(self, se):
        self.assertIsInstance(se.foo(), MagicMock)

    def test_should_see_something(self, se):
        self.assertIs(se.something, se.foo())

    def test_should_change_count_score(self, se):
        se.count_score.return_value = m = M()

        rv = count_score_caller()

        self.assertIs(rv, m)


if __name__ == '__main__':
    unittest.main()
