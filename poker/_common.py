# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

import random
from functools import total_ordering
from collections import Iterable
from enum import Enum, EnumMeta


class _PokerEnumMeta(EnumMeta):
    def __init__(self, clsname, bases, classdict):
        # make sure we only have tuple values, not single values
        for member in self.__members__.values():
            values = member._value_
            if not isinstance(values, Iterable) or isinstance(values, basestring):
                raise TypeError('{} = {!r}, should be iterable, not {}!'
                    .format(member._name_, values, type(values))
                )
            for alias in values:
                if isinstance(alias, unicode):
                    alias = alias.upper()
                self._value2member_map_.setdefault(alias, member)

    def __call__(cls, value):
        """Return the appropriate instance with any of the values listed. If values contains
        text types, those will be looked up in a case insensitive manner."""
        if isinstance(value, unicode):
            value = value.upper()
        return super(_PokerEnumMeta, cls).__call__(value)

    def make_random(cls):
        return random.choice(list(cls))


@total_ordering
class OrderableMixin(object):
    # From Python manual:
    # If a class that overrides __eq__() needs to retain
    # the implementation of __hash__() from a parent class,
    # the interpreter must be told this explicitly
    def __hash__(self):
        return super(OrderableMixin, self).__hash__()

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ == other._value_
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            names = self.__class__._member_names_
            return names.index(self._name_) < names.index(other._name_)
        return NotImplemented

    def __reduce_ex__(self, proto):
        return self.__class__.__name__


class PokerEnum(OrderableMixin, Enum):
    __metaclass__ = _PokerEnumMeta

    def __str__(self):
        val = self._value_[0]
        if isinstance(val, unicode):
            return val.encode('utf-8')
        return str(val)

    def __unicode__(self):
        return unicode(self._value_[0])

    def __repr__(self):
        val = self._value_[0]
        apostrophe = "'" if isinstance(val, unicode) else ''
        return "{0}({1}{2}{1})".format(
            self.__class__.__name__, apostrophe, unicode(val)
        ).encode('utf-8')

    @property
    def val(self):
        """The first value of the Enum member."""
        return self._value_[0]


class _ReprMixin(object):
    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self).encode('utf-8')


def _make_float(string):
    return float(string.strip().replace(',', ''))


def _make_int(string):
    return int(string.strip().replace(',', ''))
