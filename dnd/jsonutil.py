import dnd.err

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Optional, Union

    Array = list
    Boolean = bool
    Number = Union[float, int]
    String = str
    Null = None
    AnyType = Union[Boolean, Number, String, Array, "Object", Null]
    Object = dict[String, AnyType]

typename_array = "array"
typename_bool = "boolean"
typename_null = "null"
typename_number = "number"
typename_object = "object"
typename_string = "string"
_typenames = {
    bool: typename_bool,
    dict: typename_object,
    list: typename_array,
    int: typename_number,
    float: typename_number,
    str: typename_string,
    type(None): typename_null,
}
_special_keys = ("comment", "_", "comments", "notes", "note")


def _unexpected_type(expected: "str", value: "Any") -> "str":
    return "expected {}, got {}".format(expected, typename(value))


def _missing_key(key: "str") -> "str":
    return "missing required key {}".format(repr(key))


def typename(value: "Any") -> "str":
    t = type(value)
    typename = _typenames.get(t, None)
    if typename is not None:
        return typename
    return "python!{}".format(t.__name__)


def check_keys(
    obj: "dict",
    allowed: "list[str]",
    special: "list[str]" = _special_keys,
    errh: "dnd.err.Handler" = dnd.err.DefaultHandler,
) -> bool:
    good = True
    for key in obj.keys():
        if key not in allowed and key not in special:
            good = False
            errh.error("unknown key {}".format(repr(key)))
    return good


def as_array(
    value: "Any", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[Array]":
    if type(value) is not list:
        errh.error(_unexpected_type(typename_array, value))
        return None
    return value


def as_bool(
    value: "Any", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[Boolean]":
    if type(value) is not bool:
        errh.error(_unexpected_type(typename_bool, value))
        return None
    return value


def as_number(
    value: "Any", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[Number]":
    t = type(value)
    if t is not int and t is not float:
        errh.error(_unexpected_type(typename_number, value))
        return None
    return value


def as_object(
    value: "Any", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[Object]":
    if type(value) is not dict:
        errh.error(_unexpected_type(typename_object, value))
        return None
    return value


def as_string(
    value: "Any", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[String]":
    if type(value) is not str:
        errh.error(_unexpected_type(typename_string, value))
        return None
    return value


def require(
    obj: "Object", key: "String", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[AnyType]":
    if key not in obj:
        errh.error(_missing_key(key))
        return None

    return obj[key]


def require_array(
    obj: "dict", key: "str", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[Array]":
    if key not in obj:
        errh.error(_missing_key(key))
        return None

    value = obj[key]
    if type(value) is not list:
        errh.error_with(_unexpected_type(typename_array, value), key)
        return None

    return value


def require_bool(
    obj: "Object", key: "str", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[Boolean]":
    if key not in obj:
        errh.error(_missing_key(key))
        return None

    value = obj[key]
    if type(value) is not bool:
        errh.error_with(_unexpected_type(typename_bool, value), key)
        return None

    return value


def require_number(
    obj: "Object", key: "str", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[Number]":
    if key not in obj:
        errh.error(_missing_key(key))
        return None

    value = obj[key]
    t = type(value)
    if t is not int and t is not float:
        errh.error_with(_unexpected_type(typename_number, value), key)
        return None

    return value


def require_object(
    obj: "Object", key: "str", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[Object]":
    if key not in obj:
        errh.error(_missing_key(key))
        return None

    value = obj[key]
    if type(value) is not dict:
        errh.error_with(_unexpected_type(typename_object, value), key)
        return None

    return value


def require_string(
    obj: "Object", key: "str", errh: "dnd.err.Handler" = dnd.err.DefaultHandler
) -> "Optional[str]":
    if key not in obj:
        errh.error(_missing_key(key))
        return None

    value = obj[key]
    if type(value) is not str:
        errh.error_with(_unexpected_type(typename_string, value), key)
        return None

    return value


def optional_array(
    obj: "Object",
    key: "str",
    default: "Optional[Array]" = None,
    errh: "dnd.err.Handler" = dnd.err.DefaultHandler,
) -> "Optional[Array]":
    if key not in obj:
        return default

    value = obj[key]
    if type(value) is not list:
        errh.error_with(_unexpected_type(typename_array, value), key)
        return default

    return value


def optional_bool(
    obj: "Object",
    key: "str",
    default: "Optional[Boolean]" = None,
    errh: "dnd.err.Handler" = dnd.err.DefaultHandler,
) -> "Optional[Boolean]":
    if key not in obj:
        return default

    value = obj[key]
    if type(value) is not bool:
        errh.error_with(_unexpected_type(typename_bool, value), key)
        return default

    return value


def optional_number(
    obj: "Object",
    key: "str",
    default: "Optional[Number]" = None,
    errh: "dnd.err.Handler" = dnd.err.DefaultHandler,
) -> "Optional[Number]":
    if key not in obj:
        return default

    value = obj[key]
    if type(value) is not float and type(value) is not int:
        errh.error_with(_unexpected_type(typename_number, value), key)
        return default

    return value


def optional_object(
    obj: "Object",
    key: "str",
    default: "Optional[Object]" = None,
    errh: "dnd.err.Handler" = dnd.err.DefaultHandler,
) -> "Optional[Object]":
    if key not in obj:
        return default

    value = obj[key]
    if type(value) is not dict:
        errh.error_with(_unexpected_type(typename_object, value), key)
        return default

    return value


def optional_string(
    obj: "Object",
    key: "str",
    default: "Optional[String]" = None,
    errh: "dnd.err.Handler" = dnd.err.DefaultHandler,
) -> "Optional[String]":
    if key not in obj:
        return default

    value = obj[key]
    if type(value) is not str:
        errh.error_with(_unexpected_type(typename_string, value), key)
        return default

    return value
