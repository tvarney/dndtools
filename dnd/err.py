from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Union

    JsonPathElement = Union[int, float]
    JsonPath = list[JsonPathElement]


class JsonError(ValueError):
    """An error which indicates an error occured at a given json context"""

    def __init__(
        self, message: "str", filepath: "Optional[str]", jsonpath: "Optional[str]"
    ) -> None:
        ValueError.__init__(self, message, filepath, jsonpath)

    @property
    def filepath(self) -> "Optional[str]":
        return self.args[1]

    @property
    def jsonpath(self) -> "Optional[str]":
        return self.args[2]

    def __str__(self) -> "str":
        if self.args[1] is None:
            if self.args[2] is None:
                return self.args[0]
            return "{}: {}".format(self.args[2], self.args[0])
        if self.args[2] is None:
            return "{}: {}".format(self.args[1], self.args[0])
        return "{} {}: {}".format(self.args[1], self.args[2], self.args[0])

    def __repr__(self) -> "str":
        return "dnd.err.JsonError({}, {}, {})".format(
            self.args[0], self.args[1], self.args[2]
        )


class Handler(object):
    def __init__(self) -> None:
        self._path = list()  # type: JsonPath
        self._pathrepr = None  # type: Optional[str]
        self._filename = None  # type: Optional[str]

    @property
    def filename(self) -> str:
        if self._filename is None:
            return ""
        return self._filename

    @filename.setter
    def filename(self, newval: "str") -> None:
        self._filename = newval

    @property
    def path(self) -> "str":
        if self._pathrepr is None:
            self._pathrepr = "".join(
                ("[{}]" if type(item) is int else ".{}").format(item)
                for item in self._path
            )
        return self._pathrepr

    def error_with(self, err: "str", key: "JsonPathElement") -> None:
        self.push(key)
        self.error(err)
        self.pop()

    def error(self, err: "str") -> None:
        raise NotImplementedError()

    def push(self, key: "JsonPathElement") -> None:
        self._path.append(key)
        self._pathrepr = None

    def pop(self, n: "int" = 0) -> None:
        remove = min(n, len(self._path))
        for _ in range(remove):
            self._path.pop()
        self._pathrepr = None


class Writer(Handler):
    def __init__(self, stream) -> None:
        Handler.__init__(self)
        self._stream = stream

    def error(self, err: "str") -> None:
        if self.filename != "":
            print("{} {}: {}".format(self.filename, self.path, err, file=self._stream))
        print("{}: {}".format(self.path, err), file=self._stream)


class Raiser(Handler):
    def __init__(self, errtype: "type") -> None:
        Handler.__init__(self)
        self._errtype = errtype

    def error(self, err: "str") -> None:
        raise self._errtype(err)


DefaultHandler = Raiser(ValueError)
