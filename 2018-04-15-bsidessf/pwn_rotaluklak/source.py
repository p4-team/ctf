#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import sys


class Calculator(object):
    """
+-------------------------------------------------------------------------+
| This is a calculator that takes expressions in reverse polish notation. |
|                                                                         |
| In reverse polish notation the operands precede the operators. Unlike   |
| conventional infix notation every statement is unambiguous so no        |
| parenthesis are required.                                               |
|                                                                         |
| Here are some examples of how to use it:                                |
| 1 1 add             -> (1 + 1)                                          |
| 1 1 add 5 multiply  -> (1 + 1) * 5                                      |
|                                                                         |
| Here are the operators available to you.                                |
| add      - addition                                                     |
| subtract - subtraction                                                  |
| multiply - multiplication                                               |
| divide   - standard division                                            |
| idivide  - integer division                                             |
| power    - exponentiation                                               |
| xor      - standard exclusive-or function                               |
| wumbo    - standard wumbo function                                      |
|                                                                         |
| the quick brown fox jumps over the lazy dog                             |
| THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG                             |
| 1234567890~!@#$%^&*()_+-=[]{}\|:;"'?/>.<,     ¯\_(ツ)_/¯                |
+_________________________________________________________________________+
"""

    multiply = operator.mul
    divide = operator.div
    idivide = operator.truediv
    add = operator.add
    subtract = operator.sub
    xor = operator.xor
    power = operator.pow
    wumbo = lambda _, x, y: int((str(x) + str(y)) * x)

    def evaluate(self, expr, debug=False):
        expr = expr.split()
        stack = []
        for token in expr:
            try:
                # If the token is a number, push it onto the stack.
                stack.append(int(token))
            except ValueError:
                # This is an operator call the appropriate function
                y = stack.pop()
                x = stack.pop()
                stack.append(operator.attrgetter(token)(self)(x, y))
        return stack[0]


if __name__ == '__main__':
    c = Calculator()
    sys.stdout.write(c.__doc__ + '\nEnter your expression: \n')
    sys.stdout.flush()
    line = raw_input()

    sys.stdout.write("You entered: {}".format(line.strip()) + '\n')
    sys.stdout.write("Answer: {}".format(c.evaluate(line)) + '\n')
    sys.stdout.flush()