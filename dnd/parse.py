import dnd.roll
import dnd.token as _token

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Tuple, Union

    Token = Tuple[int, Union[None, int, float, dnd.roll.Dice]]


def isvalue(tokid: "int") -> bool:
    return tokid == _token.Int or tokid == _token.Float or tokid == _token.Dice


def _handle_op(op: "int", output: "List"):
    data = _token.Data[op]
    args = list()
    for _ in range(data[2]):
        args.append(output.pop())
    output.append(data[3](*reversed(args)))


def expression(expr: "str"):
    # Shunting-yard algorithm
    output = list()
    operators = list()

    idx, strlen = 0, len(expr)
    last = None
    # While there are tokens to be read
    while idx < strlen:
        # Read a token
        idx, tok = token(idx, expr)

        # If the token is a value
        if isvalue(tok[0]):
            # Put it into the output queue
            # N.B. the 3rd item in the data struct is the class of the node
            output.append(_token.Data[tok[0]][3](tok[1]))
            # output.append((tok[0], None))
        # If the token is a left parenthesis
        elif tok[0] == _token.OpenParen:
            # Push it into the operator stack
            operators.append(_token.OpenParen)
        # If the token is a right parenthesis
        elif tok[0] == _token.CloseParen:
            # Assert that there are other operators
            if len(operators) == 0:
                raise ValueError("mismatched parenthesis")
            # while the operator at the top of the stack is not a left parenthesis
            while operators[-1] != _token.OpenParen:
                # Pop the operator from the operator stack into the output queue
                _handle_op(operators.pop(), output)

                # output.append((operators.pop(), None))
                # Assert there are other operators
                if len(operators) == 0:
                    raise ValueError("mismatched parenthesis")
            # Pop the left paren and discard it
            operators.pop()
            # TODO: If there is a function token at the top of the operator stack, then:
            #     : pop the function from the operator stack into the output queue
        else:
            # Check if our token is '-'; if it is, we need to distinguish it
            if tok[0] == _token.Subtract:
                # If we're the first token
                if last is None:
                    # The minus is always an unary minus
                    operators.append(_token.UnaryMinus)
                # If the previous token was a operand (value) or a right parenthesis
                elif isvalue(last) or last == _token.CloseParen:
                    # The minus is always a binary minus
                    operators.append(_token.Subtract)
                # Otherwise, the last token was an operator or left parenthesis
                else:
                    # So this must be an unary minus
                    operators.append(_token.UnaryMinus)
                # Short-circuit; make sure last is updated
                last = tok[0]
                continue

            # If the token is an operator o1
            data = _token.Data[tok[0]]
            # While (
            #    there is an operator o2 other than the left parenthesis at
            #    the top of the operator stack, and (o2 has greater precedence
            #    than o1 or they have the same precedence and o1 is
            #    left-associative)
            # )
            while True:
                if len(operators) == 0:
                    break
                o2 = operators[-1]
                if o2 == _token.OpenParen:
                    break
                d2 = _token.Data[o2]
                if not (d2[0] > data[0] or (d2[0] == data[0] and data[1])):
                    break
                # Pop o2 from the operator stack into the output queue
                _handle_op(operators.pop(), output)
                # output.append((operators.pop(), None))
            # Push o1 onto the operator stack
            operators.append(tok[0])

        # Save last token ID so we can distinguish between unary and binary
        # minus
        last = tok[0]
    # While there are tokens on the operator stack
    while len(operators) > 0:
        if operators[-1] == _token.OpenParen:
            raise ValueError("mismatched parenthesis")
        # Pop the operator from the operator stack onto the output queue.
        # output.append((operators.pop(), None))
        _handle_op(operators.pop(), output)

    if len(output) > 1:
        raise ValueError("parsing error: more than one node at root")
    return output[0]


def whitespace(idx: "int", value: "str") -> "int":
    while idx < len(value) and value[idx].isspace():
        idx += 1
    return idx


def scanint(idx: "int", value: "str") -> "Tuple[int, int]":
    if idx >= len(value):
        raise ValueError("unexpected EOF")

    start = idx
    while idx < len(value) and value[idx].isdigit():
        idx += 1

    if start == idx:
        raise ValueError("unexpected character '{}'".format(value[idx]))

    return (idx, int(value[start:idx]))


def token(idx: "int", expr: "str") -> "Tuple[int, Token]":
    idx = whitespace(idx, expr)
    if idx >= len(expr):
        return ("EOF", None)

    c = expr[idx]
    if c.isdigit():
        return value(idx, expr)
    if c == "+":
        return (idx + 1, (_token.Add, None))
    if c == "-":
        return (idx + 1, (_token.Subtract, None))
    if c == "*":
        if idx + 1 >= len(expr) or expr[idx + 1] != "*":
            return (idx + 1, (_token.Multiply, None))
        return (idx + 2, (_token.Power, None))
    if c == "/":
        if idx + 1 >= len(expr) or expr[idx + 1] != "/":
            return (idx + 1, (_token.Divide, None))
        return (idx + 2, (_token.FloorDiv, None))
    if c == "%":
        return (idx + 1, (_token.Modulo, None))
    if c == "(":
        return (idx + 1, (_token.OpenParen, None))
    if c == ")":
        return (idx + 1, (_token.CloseParen, None))

    raise ValueError("unexpected character '{}'".format(c))


def tokenize(value: "str") -> "List[Token]":
    tokens = list()
    strlen = len(value)
    idx = 0
    while idx < strlen:
        idx, tok = token(idx, value)
        tokens.append(tok)
    return tokens


def value(idx: "int", value: "str") -> "Tuple[int, Token]":
    start = idx
    strlen = len(value)
    while idx < strlen:
        if not value[idx].isdigit():
            break
        idx += 1

    if start == idx:
        # If we broke from the loop without moving, we don't have a valid
        # value.
        raise ValueError("unexpected character '{}'".format(value[idx]))

    # At this point, idx should point to the character _after_ the integral
    # part of a value. Check if it is a period, 'e', 'E', or 'd' and handle appropriately
    if idx >= strlen:
        return (idx, (_token.Int, int(value[start:idx])))

    c = value[idx]
    if c == ".":
        return _finishDecimal(start, idx + 1, value)
    if c == "e" or c == "E":
        return _finishExponent(start, idx + 1, value)
    if c == "d":
        count = int(value[start:idx])
        return _finishDice(count, idx + 1, value)

    # Otherwise, assume that this is an integer
    return (idx, (_token.Int, int(value[start:idx])))


def _finishDecimal(start: "int", idx: "int", value: "str") -> "Tuple[int, Token]":
    strlen = len(value)
    dstart = idx
    while idx < strlen:
        if not value[idx].isdigit():
            break
        idx += 1

    if dstart == idx:
        # If we broke from the loop without moving, we don't have a valid
        # value.
        raise ValueError("unexpected character '{}'".format(value[idx]))

    # At this point, idx should point to the character _after_ the decimal
    # part of a value. Check if it is a 'e' or 'E' and handle appropriately
    if idx >= strlen:
        return (idx, (_token.Float, float(value[start:idx])))

    c = value[idx]
    if c == "e" or c == "E":
        return _finishExponent(start, idx + 1, value)
    return (idx, (_token.Float, float(value[start:idx])))


def _finishExponent(start: "int", idx: "int", value: "str") -> "Tuple[int, Token]":
    strlen = len(value)
    if idx >= strlen:
        raise ValueError("unexpected EOF")
    if value[idx] == "+" or value[idx] == "-":
        idx += 1

    estart = idx
    while idx < strlen:
        if not value[idx].isdigit():
            break
        idx += 1

    if estart == idx:
        # If we broke from the loop without moving, we don't have a valid
        # value.
        raise ValueError("unexpected character '{}'".format(value[idx]))

    return (idx, (_token.Float, float(value[start:idx])))


def _finishDice(count: "int", idx: "int", value: "str") -> "Tuple[int, Token]":
    # We should be one past the 'd'
    strlen = len(value)
    if idx >= strlen:
        raise ValueError("unexpected EOF")

    idx, sides = scanint(idx, value)
    if idx >= strlen:
        return (idx, (_token.Dice, dnd.roll.Dice(count, sides)))

    if value[idx] == "H":
        idx, drophigh = scanint(idx, value)

        if idx < strlen and value[idx] == "L":
            idx, droplow = scanint(idx, value)
            return (idx, (_token.Dice, dnd.roll.Dice(count, sides, droplow, drophigh)))

        return (idx, (_token.Dice, dnd.roll.Dice(count, sides, 0, drophigh)))
    elif value[idx] == "L":
        idx, droplow = scanint(idx, value)

        if idx < strlen and value[idx] == "H":
            idx, drophigh = scanint(idx, value)
            return (idx, (_token.Dice, dnd.roll.Dice(count, sides, droplow, drophigh)))

        return (idx, (_token.Dice, dnd.roll.Dice(count, sides, droplow)))
    return (idx, (_token.Dice, dnd.roll.Dice(count, sides)))
