import json
import random

import dnd.err
import dnd.jsonutil

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple, Union


class Row(object):
    @staticmethod
    def fromjson(
        data: "dnd.jsonutil.Any", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
    ) -> "Optional[Row]":
        datadict = dnd.jsonutil.as_object(data, errh)
        if datadict is None:
            return None

        desc = dnd.jsonutil.optional_string(datadict, "desc")
        subtable = dnd.jsonutil.optional_string(datadict, "subtable")
        weight = dnd.jsonutil.require_number(datadict, "weight")
        if weight is None:
            return None

        if desc is None and subtable is None:
            errh.error("one of 'desc' or 'subtable' must be defined")
            return None

        return Row(weight, desc, subtable)

    def __init__(
        self,
        weight: "dnd.jsonutil.Number",
        desc: "Optional[str]",
        subtable: "Optional[str]",
    ) -> None:
        self._desc = desc
        self._subtable = subtable
        self._weight = float(weight)

    @property
    def description(self) -> "str":
        return self._desc if self._desc is not None else ""

    @property
    def weight(self) -> "dnd.jsonutil.Number":
        return self._weight

    @property
    def subtable(self) -> "Optional[str]":
        return self._subtable

    def __repr__(self) -> "str":
        return "Row({}, {}, {})".format(
            repr(self._desc), repr(self._weight), repr(self._subtable)
        )

    def __str__(self) -> "str":
        return self._desc


class Table(object):
    @staticmethod
    def load(
        filename: "str", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
    ) -> "Optional[Tuple[Optional[str], Dict[str, Table]]]":
        # TODO: Support other formats? E.g. a binary format
        return Table.load_json(filename, errh)

    @staticmethod
    def load_json(
        filename: "str", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
    ) -> "Optional[Tuple[Optional[str], Dict[str, Table]]]":
        data = None
        with open(filename, "r") as fp:
            data = json.load(fp)

        obj = dnd.jsonutil.as_object(data)
        if obj is None:
            return None

        default_table = dnd.jsonutil.require_string(obj, "default")
        tables = dnd.jsonutil.require_object(obj, "tables")
        if default_table is None or tables is None:
            return None

        tbls = dict()
        for name, tbldata in tables.items():
            tbls[name] = Table.fromjson(name, tbldata)
        return default_table, tbls

    @staticmethod
    def fromjson(name: "str", tabledata: "Any") -> "Optional[Table]":
        """Given a name and a JSON data structure, create a Table"""
        rows = dnd.jsonutil.as_array(tabledata)
        if rows is None:
            return None

        tbl = Table(name)
        for row in rows:
            tbl.append(Row.fromjson(row))
        return tbl

    @staticmethod
    def evaluate(name: "str", tables: "dict[str, Table]") -> "list[str]":
        results = list()
        table = tables.get(name, None)
        if table is None:
            raise ValueError("table {} not found".format(repr(name)))
        row = table.random()
        if row.description != "":
            results.append(row.description)

        while row.subtable is not None:
            table = tables.get(row.subtable, None)
            if table is None:
                raise ValueError("table {} not found".format(repr(name)))

            row = table.random()
            if row.description != "":
                results.append(row.description)

        return results

    def __init__(self, id_: "str", rows: "Optional[List[Row]]" = None) -> None:
        self._id = id_
        self._rows = list() if rows is None else rows
        self._weight = sum(r.weight for r in self._rows)

    @property
    def id(self) -> "str":
        return self._id

    @property
    def weight(self) -> "float":
        return self._weight

    def append(self, row: "Row") -> None:
        self._rows.append(row)
        self._weight += row.weight

    def extend(self, rows: "List[Row]") -> None:
        self._rows.extend(rows)
        self._weight += sum(r.weight for r in rows)

    def random(self) -> "Row":
        value = random.uniform(0, self._weight)
        for row in self._rows:
            if row.weight >= value:
                return row
            value -= row.weight
        # Shouldn't happen, but just return the last row
        return self._rows[-1]

    def __len__(self) -> "int":
        return len(self._rows)

    def __getitem__(self, idx: "int") -> "Row":
        return self._rows[idx]

    def __contains__(self, value: "Union[Row, str]") -> bool:
        if type(value) is Row:
            return value in self._rows
        for r in self._rows:
            if r.description == value:
                return True
        return False

    def __iter__(self):
        return (r for r in self._rows)

    def __repr__(self) -> "str":
        return "Table({}, {})".format(repr(self._id), repr(self._rows))

    def __str__(self) -> "str":
        rows = list()
        wlen, dlen = 6, 11
        for r in self._rows:
            wstr = "{} ({:.2f}%)".format(r.weight, r.weight / self.weight * 100.0)
            wlen = max(len(wstr), wlen)
            desc = ""
            if r.description != "":
                desc += r.description + " "
            if r.subtable is not None:
                desc += "-> " + r.subtable
            desc = desc.strip()
            dlen = max(len(desc), dlen)
            rows.append((wstr, desc))
        return "weight {}| description\n-------{}|-----------{}\n".format(
            (wlen - 6) * " ", (wlen - 6) * "-", (dlen - 11) * "-"
        ) + "\n".join(
            "{} {}| {}".format(r[0], " " * (wlen - len(r[0])), r[1]) for r in rows
        )
