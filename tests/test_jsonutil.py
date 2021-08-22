import unittest

import dnd.err
import dnd.jsonutil


class TestTypename(unittest.TestCase):
    def test_typename_int(self):
        self.assertEqual(dnd.jsonutil.typename(1), dnd.jsonutil.typename_number)

    def test_typename_float(self):
        self.assertEqual(dnd.jsonutil.typename(1.0), dnd.jsonutil.typename_number)

    def test_typename_boolean(self):
        self.assertEqual(dnd.jsonutil.typename(True), dnd.jsonutil.typename_bool)

    def test_typename_none(self):
        self.assertEqual(dnd.jsonutil.typename(None), dnd.jsonutil.typename_null)

    def test_typename_list(self):
        self.assertEqual(dnd.jsonutil.typename([]), dnd.jsonutil.typename_array)

    def test_typename_dict(self):
        self.assertEqual(dnd.jsonutil.typename({}), dnd.jsonutil.typename_object)

    def test_typename_str(self):
        self.assertEqual(dnd.jsonutil.typename(""), dnd.jsonutil.typename_string)

    def test_typename_misc(self):
        self.assertEqual(dnd.jsonutil.typename((1,)), "python!tuple")


class TestCheckKeys(unittest.TestCase):
    def test_check_keys_all_allowed(self):
        self.assertTrue(
            dnd.jsonutil.check_keys(
                {"a": 1, "b": 2},
                ["a", "b"],
            )
        )

    def test_check_keys_special_default(self):
        self.assertTrue(
            dnd.jsonutil.check_keys(
                {"a": 1, "b": 2, "comment": "special key", "_": "special key"},
                ["a", "b"],
            )
        )

    def test_check_keys_special_given(self):
        self.assertTrue(
            dnd.jsonutil.check_keys(
                {"a": 1, "b": 2, "special": 3},
                ["a", "b"],
                ["special"],
            )
        )

    def test_check_keys_special_given_not_present(self):
        with self.assertRaises(KeyError):
            h = dnd.err.Raiser(lambda _, s: KeyError(s))
            dnd.jsonutil.check_keys(
                {"a": 1, "b": 2, "_": "special key"}, ["a", "b"], ["special"], h
            )


class TestAsArray(unittest.TestCase):
    def test_as_array_array(self):
        a = [1, 2, 3]
        self.assertEqual(a, dnd.jsonutil.as_array(a))

    def test_as_array_bool(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_array(True)

    def test_as_array_float(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_array(1.0)

    def test_as_array_int(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_array(1)

    def test_as_array_object(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_array({"a": 1})

    def test_as_array_string(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_array("test")


class TestAsBool(unittest.TestCase):
    def test_as_bool_array(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_bool([1, 2, 3])

    def test_as_bool_bool(self):
        self.assertTrue(dnd.jsonutil.as_bool(True))

    def test_as_bool_float(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_bool(1.0)

    def test_as_bool_int(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_bool(1)

    def test_as_bool_object(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_bool({"a": 1})

    def test_as_bool_string(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_bool("test")


class TestAsNumber(unittest.TestCase):
    def test_as_number_array(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_number([1, 2, 3])

    def test_as_number_bool(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_number(True)

    def test_as_number_float(self):
        self.assertEqual(1.0, dnd.jsonutil.as_number(1.0))

    def test_as_number_int(self):
        self.assertEqual(1, dnd.jsonutil.as_number(1))

    def test_as_number_object(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_number({"a": 1})

    def test_as_number_string(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_number("test")


class TestAsObject(unittest.TestCase):
    def test_as_object_array(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_object([1, 2, 3])

    def test_as_object_bool(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_object(True)

    def test_as_object_float(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_object(1.0)

    def test_as_object_int(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_object(1)

    def test_as_object_object(self):
        self.assertEqual({"a": 1}, dnd.jsonutil.as_object({"a": 1}))

    def test_as_object_string(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_object("test")


class TestAsString(unittest.TestCase):
    def test_as_string_array(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_string([1, 2, 3])

    def test_as_string_bool(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_string(True)

    def test_as_string_float(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_string(1.0)

    def test_as_string_int(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_string(1)

    def test_as_string_object(self):
        with self.assertRaises(dnd.err.JsonError):
            dnd.jsonutil.as_string({"a": 1})

    def test_as_string_string(self):
        self.assertEqual("test", dnd.jsonutil.as_string("test"))
