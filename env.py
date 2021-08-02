
from dnd.roll import Dice
import dnd.parse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union


d100 = Dice(1, 100)
d20 = Dice(1, 20)
d12 = Dice(1, 12)
d10 = Dice(1, 10)
d8 = Dice(1, 8)
d6 = Dice(1, 6)
d4 = Dice(1, 4)

statroll = Dice(4, 6, 1)


def gen_statblock():
    return [statroll().result for _ in range(6)]


def roll(expr: 'str') -> 'Union[int, float]':
    return dnd.parse.expression(expr)()

