import typing

if typing.TYPE_CHECKING:
    from typing import Union


class Value(object):
    def __init__(self, gp: "int" = 0, sp: "int" = 0, cp: "int" = 0) -> None:
        self._gp = gp
        self._sp = sp
        self._cp = cp
        self.normalize()

    @property
    def cp_total(self) -> "int":
        return self._cp + self._sp * 10 + self._gp * 10

    @property
    def gp(self) -> "int":
        return self._gp

    @gp.setter
    def gp(self, value: "int") -> None:
        self._gp = value
        self.normalize

    @property
    def sp(self) -> "int":
        return self._sp

    @sp.setter
    def sp(self, value: "int") -> None:
        self._sp = value
        self.normalize()

    @property
    def cp(self) -> "int":
        return self._cp

    @cp.setter
    def cp(self, value: "int") -> None:
        self._cp = value
        self.normalize()

    def normalize(self) -> None:
        v = self._cp + self._sp * 10 + self._gp * 100
        if v > 0:
            # Positive value
            if self._cp >= 10 or self._cp < 0:
                self._sp += self._cp // 10
                self._cp %= 10
            if self._sp >= 10 or self._sp < 0:
                self._gp += self._sp // 10
                self._sp %= 10
        else:
            # Negative value
            if self._cp <= -10 or self._cp > 0:
                self._sp += -(self._cp // -10)
                self._cp %= -10

            if self._sp <= -10 or self._sp > 0:
                self._gp += -(self._sp // -10)
                self._sp %= -10

    def __add__(self, rhs: "Value") -> "Value":
        if type(rhs) is not Value:
            raise TypeError(
                "cannot add dnd.item.Value and {}".format(type(rhs).__name__)
            )
        return Value(self._gp + rhs._gp, self._sp + rhs._sp, self._cp + rhs._cp)

    def __sub__(self, rhs: "Value") -> "Value":
        if type(rhs) is not Value:
            raise TypeError(
                "cannot subtract {} from dnd.item.Value".format(type(rhs).__name__)
            )
        return Value(self._gp - rhs._gp, self._sp - rhs._sp, self._cp - rhs._cp)

    def __mul__(self, rhs: "Union[int,float]") -> "Value":
        if type(rhs) is int:
            return Value(self._gp * rhs, self._sp * rhs, self._cp * rhs)
        if type(rhs) is float:
            total = int((self._gp * 100 + self._sp * 10 + self._cp) * rhs)
            return Value(0, 0, total)
        raise TypeError(
            "cannot multiply dnd.item.Value by {}".format(type(rhs).__name__)
        )

    def __div__(self, rhs: "Union[int,float]") -> "Value":
        if not (type(rhs) is int or type(rhs) is float):
            raise TypeError(
                "cannot divide dnd.item.Value by {}".format(type(rhs).__name__)
            )
        total = int((self._gp * 100 + self._sp * 10 + self._cp) / rhs)
        return Value(0, 0, total)

    def __iadd__(self, rhs: "Value") -> None:
        if type(rhs) is not Value:
            raise TypeError(
                "cannot add dnd.item.Value and {}".format(type(rhs).__name__)
            )
        self._gp += rhs._gp
        self._sp += rhs._sp
        self._cp += rhs._cp
        self.normalize()

    def __isub__(self, rhs: "Value") -> None:
        if type(rhs) is not Value:
            raise TypeError(
                "cannot subtract {} from dnd.item.Value".format(type(rhs).__name__)
            )
        self._gp -= rhs._gp
        self._sp -= rhs._sp
        self._cp -= rhs._cp
        self.normalize()

    def __imul__(self, rhs: "Union[int,float]") -> None:
        if type(rhs) is int:
            self._gp *= rhs
            self._sp *= rhs
            self._cp *= rhs
        elif type(rhs) is float:
            self._cp = int((self._cp + self._sp * 10 + self._gp * 100) * rhs)
            self._sp = 0
            self._gp = 0
        else:
            raise TypeError(
                "cannot multiply dnd.item.Value by {}".format(type(rhs).__name__)
            )
        self.normalize()

    def __idiv__(self, rhs: "Union[int,float]") -> None:
        if type(rhs) is not int and type(rhs) is not float:
            raise TypeError(
                "cannot divide dnd.item.Value by {}".format(type(rhs).__name__)
            )
        self._cp = int((self._cp + self._sp * 10 + self._gp * 100) / rhs)
        self._sp = 0
        self._gp = 0
        self.normalize()

    def __neg__(self) -> "Value":
        return Value(-self._gp, -self._sp, -self._cp)

    def __pos__(self) -> "Value":
        return Value(self._gp, self._sp, self._cp)

    def __abs__(self) -> "Value":
        if self._gp < 0 or self._sp < 0 or self._cp < 0:
            return Value(-self._gp, -self._sp, -self._cp)
        return Value(self._gp, self._sp, self._cp)

    def __eq__(self, rhs: "Value") -> "bool":
        if type(rhs) is not Value:
            return False
        return self._gp == rhs._gp and self._sp == rhs._sp and self._cp == rhs._cp

    def __ne__(self, rhs: "Value") -> "bool":
        if type(rhs) is not Value:
            return True
        return self._gp != rhs._gp or self._sp != rhs._sp or self._cp != rhs._cp

    def __lt__(self, rhs: "Value") -> "bool":
        if type(rhs) is not Value:
            return NotImplemented
        st = self._cp + self._sp * 10 + self._gp * 100
        rt = rhs._cp + rhs._sp * 10 + rhs._gp * 100
        return st < rt

    def __le__(self, rhs: "Value") -> "bool":
        if type(rhs) is not Value:
            return NotImplemented
        st = self._cp + self._sp * 10 + self._gp * 100
        rt = rhs._cp + rhs._sp * 10 + rhs._gp * 100
        return st <= rt

    def __gt__(self, rhs: "Value") -> "bool":
        if type(rhs) is not Value:
            return NotImplemented
        st = self._cp + self._sp * 10 + self._gp * 100
        rt = rhs._cp + rhs._sp * 10 + rhs._gp * 100
        return st > rt

    def __ge__(self, rhs: "Value") -> "bool":
        if type(rhs) is not Value:
            return NotImplemented
        st = self._cp + self._sp * 10 + self._gp * 100
        rt = rhs._cp + rhs._sp * 10 + rhs._gp * 100
        return st >= rt

    def __repr__(self) -> "str":
        return "dnd.item.Value({}, {}, {})".format(
            self._gp,
            self._sp,
            self._cp,
        )

    def __float__(self) -> "float":
        return self._gp + self._sp / 10 + self._cp / 100

    def __str__(self) -> "str":
        if self._cp == 0:
            if self._sp == 0:
                return "{} gp".format(self._gp)
            if self._gp == 0:
                return "{} sp".format(self._sp)
            return "{} gp {} sp".format(self._gp, self._sp)
        if self._sp == 0:
            if self._gp == 0:
                return "{} cp".format(self._cp)
            return "{} gp {} cp".format(self._gp, self._cp)
        if self._gp == 0:
            return "{} sp {} cp".format(self._sp, self._cp)
        return "{} gp {} sp {} cp".format(self._gp, self._sp, self._cp)
