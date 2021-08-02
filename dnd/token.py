import dnd.nodes as _node

Int = 0
Float = 1
Dice = 2
Add = 3
Subtract = 4
Multiply = 5
Divide = 6
FloorDiv = 7
Modulo = 8
Power = 9
OpenParen = 10
CloseParen = 11
UnaryMinus = 12


Names = [
    "int",
    "float",
    "dice",
    "add",
    "subtract",
    "multiply",
    "divide",
    "floor-div",
    "modulo",
    "power",
    "open-paren",
    "close-paren",
    "unary-minus",
]

Values = ["", "", "", "+", "-", "*", "/", "//", "%", "**", "(", ")", "-"]

Data = [
    (0, False, 1, _node.Value),
    (0, False, 1, _node.Value),
    (0, False, 1, _node.Dice),
    (2, True, 2, _node.Add),
    (2, True, 2, _node.Subtract),
    (3, True, 2, _node.Multiply),
    (3, True, 2, _node.Divide),
    (3, True, 2, _node.FloorDiv),
    (3, True, 2, _node.Modulo),
    (4, False, 2, _node.Power),
    (0, False, 0, None),
    (0, False, 0, None),
    (5, False, 1, _node.Negative),
]
