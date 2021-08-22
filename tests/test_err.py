import io
import typing
import unittest

import dnd.err

if typing.TYPE_CHECKING:
    from typing import Optional, Union


class TestJsonError(unittest.TestCase):
    def test_filepath_set(self):
        err = dnd.err.JsonError("something is bad", "test.json", ".a.b[1]")
        self.assertEqual(err.filepath, "test.json")

    def test_filepath_unset(self):
        err = dnd.err.JsonError("oops")
        self.assertIsNone(err.filepath)

    def test_jsonpath_set(self):
        err = dnd.err.JsonError("something is bad", "test.json", ".a.b[1]")
        self.assertEqual(err.jsonpath, ".a.b[1]")

    def test_jsonpath_unset(self):
        err = dnd.err.JsonError("oops")
        self.assertIsNone(err.jsonpath)

    def test_repr(self):
        err1 = dnd.err.JsonError("oops", "test.json", ".a.b[1]")
        self.assertEqual(
            repr(err1), "dnd.err.JsonError('oops', 'test.json', '.a.b[1]')"
        )

        err2 = dnd.err.JsonError("oops", "test.json")
        self.assertEqual(repr(err2), "dnd.err.JsonError('oops', 'test.json', None)")

        err3 = dnd.err.JsonError("oops")
        self.assertEqual(repr(err3), "dnd.err.JsonError('oops', None, None)")

    def test_str_just_message(self):
        err = dnd.err.JsonError("oops")
        self.assertEqual(str(err), "oops")

    def test_str_msg_and_filename(self):
        err = dnd.err.JsonError("oops", "test.json")
        self.assertEqual(str(err), "test.json: oops")

    def test_str_msg_and_path(self):
        err = dnd.err.JsonError("oops", None, ".a.b[1].c")
        self.assertEqual(str(err), ".a.b[1].c: oops")

    def test_str_all_fields(self):
        err = dnd.err.JsonError("oops", "test.json", ".a.b[1].c")
        self.assertEqual(str(err), "test.json .a.b[1].c: oops")


class TestHandler(unittest.TestCase):
    def test_filename_empty(self):
        h = dnd.err.Handler()
        self.assertEqual(h.filename, "")

    def test_filename_set(self):
        h = dnd.err.Handler()
        h.filename = "test.json"
        self.assertEqual(h.filename, "test.json")

    def test_path_empty(self):
        h = dnd.err.Handler()
        self.assertEqual(h.path, ".")

    def test_path_key(self):
        h = dnd.err.Handler()
        h.push("key")
        self.assertEqual(h.path, ".key")

    def test_path_index(self):
        h = dnd.err.Handler()
        h.push(1)
        self.assertEqual(h.path, ".[1]")

    def test_pop(self):
        h = dnd.err.Handler()
        h.extend("a", "b", 1, "c")
        self.assertEqual(h.path, ".a.b[1].c")
        h.pop()
        self.assertEqual(h.path, ".a.b[1]")
        h.pop(2)
        self.assertEqual(h.path, ".a")
        h.pop(50)
        self.assertEqual(h.path, ".")
        h.pop()
        self.assertEqual(h.path, ".")


class TestWriter(unittest.TestCase):
    def _test(
        self, errmsg: "Union[str,BaseException]",
        filename: "Optional[str]" = None,
        path: "Optional[list[dnd.err.JsonPathElement]]" = None
    ) -> "str":
        stream = io.StringIO()
        w = dnd.err.Writer(stream)
        if filename is not None:
            w.filename = filename
        if path is not None:
            w.extend(*path)
        w.error(errmsg)
        stream.seek(0)
        return stream.read()

    def test_error_no_fields(self):
        result = self._test("error")
        self.assertEqual(result, ".: error\n")

    def test_error_filename(self):
        result = self._test("error", "test.json")
        self.assertEqual(result, "test.json .: error\n")

    def test_error_path(self):
        result = self._test("error", None, ["a", "b", 1])
        self.assertEqual(result, ".a.b[1]: error\n")
    
    def test_error_filename_and_path(self):
        result = self._test("error", "test.json", ["a", 3, "c"])
        self.assertEqual(result, "test.json .a[3].c: error\n")
    
    def test_error_with_exception(self):
        result = self._test(KeyError("key"), "test.json", ["a", 3, "c"])
        self.assertEqual(result, "test.json .a[3].c: KeyError: 'key'\n")


class TestRaiser(unittest.TestCase):
    def test_error_default_type(self):
        r = dnd.err.Raiser()
        with self.assertRaises(dnd.err.JsonError):
            r.error("error")

    def test_error_value_error(self):
        r = dnd.err.Raiser(lambda _, s: ValueError(s))
        with self.assertRaises(ValueError):
            r.error("error")

    def test_error_default_type_with_exception(self):
        r = dnd.err.Raiser()
        with self.assertRaises(KeyError):
            r.error(KeyError("key"))
