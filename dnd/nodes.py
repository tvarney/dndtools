from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union
    import dnd.roll


PrecedenceValue = 100
PrecedencePower = 30
PrecedenceMulDiv = 20
PrecedenceAddSub = 10


def nodestr(node, parent_precedence: "int") -> "str":
    if node.precedence() < parent_precedence:
        return "({})".format(str(node))
    return str(node)


class Value(object):
    __slots__ = ("value",)

    def __init__(self, value: "Union[float, int]") -> None:
        self.value = value

    def precedence(self) -> int:
        return PrecedenceValue

    def __call__(self) -> "Union[float, int]":
        return self.value

    def __repr__(self) -> "str":
        return "Value({})".format(self.value)

    def __str__(self) -> "str":
        return str(self.value)


class Dice(object):
    __slots__ = ("dice",)

    def __init__(self, value: "dnd.roll.Dice") -> None:
        self.dice = value

    def precedence(self) -> int:
        return PrecedenceValue

    def __call__(self) -> "int":
        return self.dice.roll().result

    def __repr__(self) -> "str":
        return repr(self.dice)

    def __str__(self) -> "str":
        return str(self.dice)


class Add(object):
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def precedence(self) -> int:
        return PrecedenceAddSub

    def __call__(self) -> "Union[float, int]":
        return self.lhs() + self.rhs()

    def __repr__(self) -> "str":
        return "Add({}, {})".format(repr(self.lhs), repr(self.rhs))

    def __str__(self) -> "str":
        return "{} + {}".format(
            nodestr(self.lhs, PrecedenceAddSub), nodestr(self.rhs, PrecedenceAddSub)
        )


class Subtract(object):
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def __call__(self) -> "Union[float, int]":
        return self.lhs() - self.rhs()

    def __repr__(self) -> "str":
        return "Subtract({}, {})".format(repr(self.lhs), repr(self.rhs))

    def __str__(self) -> "str":
        return "{} - {}".format(
            nodestr(self.lhs, PrecedenceAddSub), nodestr(self.rhs, PrecedenceAddSub)
        )


class Negative(object):
    __slots__ = ("value",)

    def __init__(self, value) -> None:
        self.value = value

    def precedence(self) -> int:
        return PrecedenceValue

    def __call__(self) -> "Union[float, int]":
        return -(self.value())

    def __repr__(self) -> "str":
        return "Negative({})".format(repr(self.value))

    def __str__(self) -> "str":
        if self.value.precedence == PrecedenceValue:
            if type(self.value) is Dice:
                return "-({})".format(self.value)
            return "-{}".format(self.value)
        return "-({})".format(self.value)


class Multiply(object):
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def precedence(self) -> "int":
        return PrecedenceMulDiv

    def __call__(self) -> "Union[float, int]":
        return self.lhs() * self.rhs()

    def __repr__(self) -> "str":
        return "Multiply({}, {})".format(repr(self.lhs), repr(self.rhs))

    def __str__(self) -> "str":
        return "{} * {}".format(
            nodestr(self.lhs, PrecedenceMulDiv), nodestr(self.rhs, PrecedenceMulDiv)
        )


class Divide(object):
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def precedence(self) -> "int":
        return PrecedenceMulDiv

    def __call__(self) -> "Union[float, int]":
        return self.lhs() / self.rhs()

    def __repr__(self) -> "str":
        return "Divide({}, {})".format(repr(self.lhs), repr(self.rhs))

    def __str__(self) -> "str":
        return "{} / {}".format(
            nodestr(self.lhs, PrecedenceMulDiv), nodestr(self.rhs, PrecedenceMulDiv)
        )


class FloorDiv(object):
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def precedence(self) -> "int":
        return PrecedenceMulDiv

    def __call__(self) -> "int":
        return self.lhs() // self.rhs()

    def __repr__(self) -> "str":
        return "FloorDiv({}, {})".format(repr(self.lhs), repr(self.rhs))

    def __str__(self) -> "str":
        return "{} // {}".format(
            nodestr(self.lhs, PrecedenceMulDiv), nodestr(self.rhs, PrecedenceMulDiv)
        )


class Power(object):
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def precedence(self) -> "int":
        return PrecedencePower

    def __call__(self) -> "Union[int, float]":
        return self.lhs() ** self.rhs()

    def __repr__(self) -> "str":
        return "Power({}, {})".format(repr(self.lhs), repr(self.rhs))

    def __str__(self) -> "str":
        return "{}**{}".format(
            nodestr(self.lhs, PrecedencePower), nodestr(self.rhs, PrecedencePower)
        )


class Modulo(object):
    __slots__ = ("lhs", "rhs")

    def __init__(self, lhs, rhs) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def precedence(self) -> "int":
        return PrecedenceMulDiv

    def __call__(self) -> "Union[int, float]":
        return self.lhs() % self.rhs()

    def __repr__(self) -> "str":
        return "Modulo({}, {})".format(repr(self.lhs), repr(self.rhs))
