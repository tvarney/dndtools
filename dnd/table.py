import json
import os.path
import random

import dnd.err
import dnd.jsonutil
import dnd.parse

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple, Union
    from dnd.jsonutil import Number


def _pathparts(path: "str") -> "list[str]":
    parts = list()

    remainder, part = os.path.split(path)
    parts.append(part)
    while remainder != "":
        remainder, part = os.path.split(remainder)
        parts.append(part)
        if remainder == "/":
            parts.append("/")
            break
    return parts


class Row(object):
    @staticmethod
    def fromjson(
        data: "dnd.jsonutil.Any", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
    ) -> "Optional[Row]":
        datadict = dnd.jsonutil.as_object(data, errh)
        if datadict is None:
            return None

        desc = dnd.jsonutil.require_string(datadict, "desc", errh)
        weight = dnd.jsonutil.optional_number(datadict, "weight", 1.0, errh)

        return Row(weight, desc)

    def __init__(self, weight: "Number", desc: "Optional[str]") -> None:
        self._desc = desc
        self._weight = float(weight)

    @property
    def description(self) -> "str":
        return self._desc if self._desc is not None else ""

    @property
    def weight(self) -> "dnd.jsonutil.Number":
        return self._weight

    def evaluate(self, tables: "dict[str, Table]") -> "str":
        result = ""
        rest = self._desc
        while "{{" in rest:
            start = rest.index("{{")
            end = rest.index("}}", start + 2)
            statement = rest[start + 2 : end].strip()
            result += rest[0:start]
            rest = rest[end + 2 :]
            if statement in tables:
                result += Table.evaluate(statement, tables)
            else:
                try:
                    result += str(dnd.parse.expression(statement)())
                except ValueError:
                    print(
                        "no table '{}' found while evaluating table row".format(
                            statement
                        )
                    )
                    result += "<ERROR>"

        result += rest
        return result

    def __repr__(self) -> "str":
        return "Row({}, {})".format(repr(self._desc), repr(self._weight))

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
        loaded = set()
        dname, fname = os.path.split(filename)
        loaded.add(fname)
        return Table._loadjson(dname, fname, errh, loaded)

    @staticmethod
    def _loadjson(
        dname: "str", fname: "str", errh: "dnd.err.Handler", loaded: "set[str]"
    ) -> "Optional[Tuple[Optional[str], Dict[str, Table]]]":
        data = None
        with open(os.path.join(dname, fname), "r") as fp:
            data = json.load(fp)

        obj = dnd.jsonutil.as_object(data)
        if obj is None:
            return None

        default_table = dnd.jsonutil.require_string(obj, "default", errh)
        tables = dnd.jsonutil.require_object(obj, "tables", errh)
        if default_table is None or tables is None:
            return None

        tbls = dict()
        for name, tbldata in tables.items():
            tbls[name] = Table.fromjson(name, tbldata)

        references = dnd.jsonutil.optional_array(obj, "references", None, errh)
        if references is not None:
            errh.push("references")
            for i, refname in enumerate(references):
                if refname in loaded:
                    continue
                if ".." in _pathparts(refname):
                    errh.error_with("table reference may not include '..'", i)
                loaded.add(refname)
                rtables = Table._loadjson(dname, refname, errh, loaded)
                if rtables is None:
                    continue

                for name, tbl in rtables[1].items():
                    if name in tbls:
                        raise ValueError("duplicate table name {}".format(name))
                    tbls[name] = tbl
            errh.pop()

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
    def evaluate(name: "str", tables: "dict[str, Table]") -> "str":
        table = tables.get(name, None)
        if table is None:
            raise ValueError("table {} not found".format(repr(name)))

        return table.random().evaluate(tables)

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
