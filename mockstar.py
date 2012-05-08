# -*- coding: utf-8 -*-

from mock import patch
from functools import wraps


class DotDict(dict):
    """Dict with dot-syntax enabled.
    """

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, val):
        return self.__setitem__(key, val)


def get_names(name):
    """
    Gets list of names to store in side_effects dict.

    Arguments:
    - `name`:
    """
    pos = name.rfind('.')
    if pos != -1:
        return [name[pos + 1:]]
    return [name]


def p(name, *args, **kw):
    """
    Acts like :func:``mock.patch``, but passes side-effects (patched mocks)
    into special dict-like ``se`` parameter.
    """
    def rv_decorator(fn):
        if not hasattr(fn, 'side_effects'):
            fn.side_effects = DotDict()

        # we will store mock obj here
        rv_decorator.patch_mock = None

        def collector(mocked):
            rv_decorator.patch_mock = mocked

        patch(name, *args, **kw)(collector)()

        names = get_names(name)
        for store_name in names:
            fn.side_effects[store_name] = rv_decorator.patch_mock

        @wraps(fn)
        def rv_fun(*args, **kw):
            new_kw = kw.copy()
            new_kw.update({'se': fn.side_effects})
            return fn(*args, **new_kw)
        return rv_fun
    return rv_decorator










# def complex_function(silly_obj):
#     rv1 = side_effect_1(1)
#     side_effect_2(rv1)
#     transmit(silly_obj)
#     additional()
#     obj = Object.get(10)
#     return obj.double_pk()


# def side_effect_1(num):
#     return num


# def side_effect_2(num):
#     pass


# def transmit():
#     pass


# def additional():
#     pass


# class Object(object):
#     def __init__(self, pk):
#         self.pk = pk
#         super(Object, self).__init__()

#     @staticmethod
#     def get(self, pk):
#         return Object(pk)

#     def double_pk(self):
#         return self.pk * 2


# class BaseTestCase(TestCase):
#     pass


# def patch(*args, **kw):
#     pass


# def p(*args, **kw):
#     pass


# def build_silly_obj():
#     return object()


# class TestComplexFunction(BaseTestCase):
#     def side_effects(self):
#         return [
#             p('side_effect_1', autospec=True),
#             p('side_effect_2', autospec=False),
#             p('Object.get', autospec=False),
#             p('transmit', autospec=True)]

#     @patch('additional')
#     def test_should_call_side_effect_2(self, additional_mock, se=None):
#         """``se`` is for side-effects. ``m`` is for by-hand mocks
#         """
#         silly_obj = build_silly_obj()

#         # do
#         result = complex_function(silly_obj)


# class TestCallback(BaseTestCase):
#     def setUp(self):
#         super(TestCallback, self).setUp()

#     def tearDown(self):
#         super(TestCallback, self).tearDown()

#     side_effects = [
#         p('build_engine', rv_name='engine'),
#         p('_callback_success_profile', side_effect='success'),
#         p('_callback_failure_profile', side_effect='failure')]

#     def test_should_go_success(self, se=None):
#         request = build_request()
#         backend = 'twitter'
#         # engine = se.build_engine.return_value
#         se.engine.profile = M()  # not None

#         # do
#         result = views.callback(request, backend)

#         se.success.assert_called_with(
#             request, engine, 'web')
#         self.assertEquals(
#             result,
#             se.success.return_value)
