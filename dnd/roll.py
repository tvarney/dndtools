import random

import dnd.listview

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List


class Roll(object):
    """Roll represents the results of rolling a Dice object"""

    def __init__(self, values: "List[int]", droplow: "int", drophigh: "int") -> None:
        """Initialize the roll object with the given data

        Invariants:
            values must be a non-empty list of values.
            droplow must be a non-negative integer >= 0
            drophigh must be a non-negative integer >= 0
            len(values) must be >= droplow + drophigh

        :param values: The list of die values
        :param droplow: The number of low dice to drop
        :param drophigh: The number of high dice to drop
        """
        self._values = values
        self._droplow = droplow
        self._drophigh = drophigh

        endidx = len(values) - drophigh
        self._vHigh = dnd.listview.ListView(values, endidx, len(values))
        self._vLow = dnd.listview.ListView(values, 0, droplow)
        self._vGood = dnd.listview.ListView(values, droplow, endidx)
        self._result = sum(self._vGood)

    @property
    def result(self) -> "int":
        return self._result

    @property
    def values(self) -> "dnd.listview.ListView":
        return self._vGood

    @property
    def dropped_low(self) -> "dnd.listview.ListView":
        return self._vLow

    @property
    def dropped_high(self) -> "dnd.listview.ListView":
        return self._vHigh

    def __repr__(self) -> "str":
        return "Roll({}, {}, {})".format(self._values, self._droplow, self._drophigh)

    def __str__(self) -> "str":
        return "{} = [{}, {}, {}]".format(
            self._result, self._vLow, self._vGood, self._vHigh
        )


class Dice(object):
    def __init__(
        self, count: "int", sides: "int", droplow: "int" = 0, drophigh: "int" = 0
    ) -> None:
        """Create a Dice instance with the given values.

        All values must be >= 0; any values which are less than zero will be
        set to 0.

        :param count: The number of dice to roll
        :param sides: The number of sides the dice should have
        :param droplow: How many low values to drop from the result
        :param drophigh: How many high values to drop from the result
        """
        self._count = max(count, 0)
        self._sides = max(sides, 1)
        self._droplow = max(droplow, 0)
        self._drophigh = max(drophigh, 0)

    @property
    def count(self) -> "int":
        return self._count

    @property
    def sides(self) -> "int":
        return self._sides

    @property
    def droplow(self) -> "int":
        return self._droplow

    @property
    def drophigh(self) -> "int":
        return self._drophigh

    def roll(self) -> "Roll":
        """Simulate rolling this set of dice and return a Roll object

        :returns: A Roll containing the results of the roll
        """
        r = [random.randint(1, self._sides) for _ in range(self._count)]
        r.sort()
        return Roll(r, self._droplow, self._drophigh)

    def __call__(self) -> "Roll":
        return self.roll()

    def __repr__(self) -> "str":
        return "Dice({}, {}, {}, {})".format(
            self._count, self._sides, self._droplow, self._drophigh
        )

    def __str__(self) -> "str":
        if self._droplow > 0:
            if self._drophigh > 0:
                return "{}d{}L{}H{}".format(
                    self._count, self._sides, self._droplow, self._drophigh
                )
            return "{}d{}L{}".format(self._count, self._sides, self._droplow)
        if self._drophigh > 0:
            return "{}d{}H{}".format(self._count, self._sides, self._drophigh)
        return "{}d{}".format(self._count, self._sides)
