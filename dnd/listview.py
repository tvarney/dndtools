from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List


class ListView(object):
    """ListView is an immutable view into a list of ints"""

    def __init__(self, values: "List[int]", start: "int", end: "int") -> None:
        self._values = values
        self._start = start
        self._end = end

    def __len__(self) -> "int":
        return len(self._values) - (self._start + self._end)

    def __getitem__(self, idx: "int") -> "int":
        return self._values[self._start + idx]

    def __contains__(self, value: "int") -> "int":
        return value in self._values[self._start : self._end]

    def __iter__(self):
        return (i for i in self._values[self._start : self._end])

    def __repr__(self) -> "str":
        return "ListView({}, {}, {})".format(
            repr(self._values), repr(self._start), repr(self._end)
        )

    def __str__(self) -> "str":
        return repr(self._values[self._start : self._end])
