# Immutable lists.
#
# Compared to a regular list, an immutable list can be used as a key
# in dictionaries and sets.
#
# An `IList[T]` behaves basically like homogeneous tuples `tuple[T, ...]`,
# i.e. tuples of arbitrary length, where all elements have the same
# type, but has much better type inference properties.
#
# You can write `IList([1, 2, 3])` to construct an immutable list from
# a list, and `ilist(1, 2, 3)` for list literals, if you want to avoid
# writing extra brackets.
#
# In contrast to the regular list, the `IList` type is also covariant
# in its type parameter, which means that if `U` is a subtype of `T`,
# then `IList[U]` is also a subtype of `IList[T]`.
# This is very useful when working with union types, as you can use
# for example an `IList[int]` also at places where an
# `IList[int | bool]` is expected.

from collections.abc import Sequence
from functools import total_ordering
from typing import TypeVar, overload, Optional

T = TypeVar("T", covariant=True)
U = TypeVar("U", covariant=True)


@total_ordering
class IList(Sequence[T]):
    __slots__ = ("_frozen", "_items")

    def __init__(self, items: Optional[Sequence[T]] = None):
        if items is not None:
            items = list(items)
        else:
            items = []
        self._items = items

    @overload
    def __getitem__(self, i: int) -> T: ...

    @overload
    def __getitem__(self, i: slice) -> "IList[T]": ...

    def __getitem__(self, i: slice | int) -> "IList[T]" | T:
        match i:
            case int(i):
                return self._items[i]
            case slice():
                return IList(self._items[i])

    def __len__(self) -> int:
        return self._items.__len__()

    def __eq__(self, other: object) -> bool:
        if type(other) is type(self):
            return self._items == other._items  # type: ignore
        raise Exception(f"cannot compare IList with {type(other)}")

    def __le__(self, other: "IList[T]") -> bool:
        return self._items <= other._items

    def __repr__(self) -> str:
        s = "ilist("
        for i, x in enumerate(self):
            if i != 0:
                s += ", "
            s += repr(x)
        s += ")"
        return s

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __add__(self, other: "IList[U]") -> "IList[T | U]":
        return IList(self._items + other._items)  # type: ignore


def ilist[T](*args: T) -> IList[T]:
    return IList(args)
