import dnd.parse

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Any
    import dnd.table

_EMPTY_DICT = dict()


class Template(object):
    def __init__(self, text: "str") -> None:
        self._text = text
        self._parts = list()
        self._values = None  # type: Optional[dict[str, Any]]
        self._tables = None  # type: Optional[dict[str, dnd.table.Table]]

        self._error_behavior = 0

        rest = text
        while "{{" in rest:
            start = rest.index("{{")
            end = rest.index("}}", start + 2)
            statement = rest[start + 2 : end].strip()
            strpart = rest[0:start]
            if len(strpart) > 0:
                self._parts.append((0, strpart))
            rest = rest[end + 2 :]
            try:
                self._parts.append((1, dnd.parse.expression(statement)))
            except ValueError:
                self._parts.append((2, statement))
        if len(rest) > 0:
            self._parts.append((0, rest))

    @property
    def text(self) -> "str":
        return self._text

    @property
    def values(self) -> "Optional[dict[str, Any]]":
        return self._values

    @values.setter
    def values(self, values: "Optional[dict[str, Any]]") -> None:
        self._values = values

    @property
    def tables(self) -> "Optional[dict[str, Any]]":
        return self._tables

    @tables.setter
    def tables(self, tables: "Optional[dict[str, dnd.table.Table]]") -> None:
        self._tables = tables

    def raise_on_error(self) -> None:
        self._error_behavior = 0

    def print_on_error(self) -> None:
        self._error_behavior = 1

    def ignore_on_error(self) -> None:
        self._error_behavior = 2

    def evaluate(
        self,
        values: "Optional[dict[str,Any]]" = None,
        tables: "Optional[dict[str, dnd.table.Table]]" = None,
    ) -> "str":
        if values is None:
            values = self._values if self._values is not None else _EMPTY_DICT
        if tables is None:
            tables = self._tables if self._tables is not None else _EMPTY_DICT

        result = ""
        for t, v in self._parts:
            if t == 0:
                # String
                result += v
            elif t == 1:
                # Dice Expression
                result += str(v())
            elif t == 2:
                # Value/Table lookup
                if v in values:
                    try:
                        # E.g. a Dice object or Expression Node
                        result += str(values[v]())
                    except Exception:
                        result += str(values[v])
                elif v in tables:
                    result += tables[v].random().template.evaluate(values, tables)
                else:
                    # This may raise an error, or continue
                    self._error("statement {} not in values or tables".format(repr(v)))
                    result += "<ERROR>"
        return result

    def _error(self, message: "str"):
        if self._error_behavior == 0:
            raise ValueError(message)
        elif self._error_behavior == 1:
            print(message)

    def __repr__(self) -> "str":
        return "Template({})".format(repr(self._text))

    def __str__(self) -> "str":
        if self._values is not None or self._tables is not None:
            return self.evaluate()
        return self._text
