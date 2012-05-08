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
        patcher = patch(name, *args, **kw)
        # add names to patcher
        patcher.names = get_names(name)
        new_patchers = []
        if hasattr(fn, 'patchers'):
            new_patchers += fn.patchers
            del fn.patchers
        new_patchers.append(patcher)

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
    def rv(name, *args, **kw):
        new_kw = kw.copy()
        new_kw.update(defaults)
        return patcher(prefix + '.' + name, *args, **new_kw)
    return rv
