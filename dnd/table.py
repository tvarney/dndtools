import json


class Row(object):
    def __init__(self, description: "str", weight: "int") -> None:
        self._desc = description
        self._weight = weight

    @property
    def description(self) -> "str":
        return self._desc

    @property
    def weight(self) -> "int":
        return self._weight


class Table(object):
    def __init__(self, id_: "str") -> None:
        self._id = id_

    @property
    def id(self) -> "str":
        return self._id
