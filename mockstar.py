# -*- coding: utf-8 -*-

from functools import wraps
import unittest
import inspect

from mock import patch
from mock import MagicMock


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


def p(*args, **kw):
    """
    Acts like :func:``mock.patch``, but passes side-effects (patched
    mocks) into special dict-like ``se`` parameter.
    """
    def rv_decorator(fn):
        new_patchers = []
        for name in args:
            patcher = patch(name, **kw)
            # add names to patcher
            patcher.names = get_names(name)
            new_patchers.append(patcher)

        if hasattr(fn, 'patchers'):
            new_patchers += fn.patchers
            del fn.patchers

        @wraps(fn)
        def rv_fun(*args, **kw):
            new_kw = kw.copy()
            if hasattr(rv_fun, 'patchers'):
                d = {}
                for patcher in rv_fun.patchers:
                    m = patcher.start()
                    for name in patcher.names:
                        d[name] = m
                se = DotDict(**d)

                new_kw.update({'se': se})
            try:
                rv = fn(*args, **new_kw)
            finally:
                if hasattr(rv_fun, 'patchers'):
                    for patcher in rv_fun.patchers:
                        patcher.stop()
            return rv

        rv_fun.patchers = new_patchers
        return rv_fun
    return rv_decorator


def prefixed_p(prefix, patcher=p, **defaults):
    """
    Create "prefixed" version of p with default parameters set.

    Arguments:
    - `prefix`: prefix, which will be joined with a dot and added to your
                patch func.
    - `**defaults`: default kw-args
    """
    @wraps(patcher)
    def rv(*args, **kw):
        def_copy = defaults.copy()
        def_copy.update(kw)
        full_names = map(lambda name: prefix + '.' + name, args)
        return patcher(*full_names, **def_copy)
    return rv


class RVDescriptor(object):
    def __get__(self, instance, owner):
        if instance is None:
            return owner.return_value
        return instance.return_value

    def __set__(self, instance, value):
        instance.return_value = value

    def __delete__(self, instance):
        del instance.return_value


class M(MagicMock):
    """
    :class:`~MagicMock` with shortcuts. I just couldn't stand the
    ``.return_value.foo.return_value.bar.return_value`` thing.

    Now you can do:

    .. code-block:: python

        from mockstar import M
        m = M()
        m.rv = 10
        assert m() == 10
    """
    def __init__(self, *args, **kw):
        super(M, self).__init__(*args, **kw)

    def _get_child_mock(self, **kw):
        return M(**kw)

    #: shortcut for ``.return_value``
    rv = RVDescriptor()


def sequence_side_effect(*args):
    """
    Generates function that returns i'th arg on i'th call.

    Use like this:

    .. code-block:: python

        from mockstar import sequence_side_effect
        from mockstar import M

        m = M()
        m.side_effect = sequence_side_effect(1, 2, 3)
    """
    seq = list(args)

    def rv_fun(*args, **kw):
        return seq.pop(0)
    return rv_fun


def side_effect_ify(method):
    def new_f(self, *args, **kw):
        self._current_test_method = method
        return self.side_effects(se=DotDict())
    return new_f


class BaseTestCase(unittest.TestCase):
    def side_effects(self, se):
        return self.invoke(se=se)

    def invoke(self, se):
        try:
            rv = self._current_test_method(self, se=se)
        except TypeError, e:
            if "got an unexpected keyword argument 'se'" in e.message:
                rv = self._current_test_method(self)
            else:
                raise
        return rv

    @classmethod
    def setUpClass(cls):
        methods = filter(lambda x: inspect.ismethod(x[1]),
                         filter(lambda x: x[0].startswith('test_'),
                                inspect.getmembers(cls)))
        for method_name, method in methods:
            setattr(cls, method_name, side_effect_ify(method))
