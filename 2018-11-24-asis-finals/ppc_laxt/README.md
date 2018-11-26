# LAXT (ppc, 145p, 49 solved)

In the challenge we connect to the server and after solving Proof of Work get get:

```
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
| for a give number like 2018 please construct each integer from 0 to 100, with the |
| digits of it, for example: 96 = 12 * 8 + 0, 10 = 2 + 8 + 1 * 0 and 54 = 8**2 - 10 |
| you can also see the evaluation function for ervey provided expression like above |
| Your options: 
 	 [E]valuation function for expressions
 	 [C]ontinue to solve

the number for you in this task is n = 9178
```

We can peek at the evaluation function too:

```python
def laxt(expr, num):
    ops = ' %&()*+-/<>^|~'
    nude = expr.translate(None, ops)
    try:
        if set(nude) == set(num):
            flag, val = True, eval(expr)
        else:
            flag, val = False, None
    except:
        flag, val = False, None  
    return flag, val
```

So the goal is to use only digits provided in the challenge and operations ` %&()*+-/<>^|~` to create all numbers from 0 to 100.

Judging by the flag there was some "trick" here, but we simply brute-forced the solution since we had to work with only a few digits.

The solution is quite simple:

1. Test all permutations of the digits
2. Test all possible positions of the parenthesis, but with correct order, so `(` has to be before `)`, and there has to be a number in between. There are so few digits it didn't seem necessary to consider more than 1 parenthesis.
3. Test all possible choices for the operator between numbers, including a special `$` symbol which we later removed (this way we can glue digits together).
4. Once the expression is constructed we eval is and compare to the number we're looking for.

It's a bit wasteful - we could easily store values we "accidentally" already computed while looking for a different number, but the dataset is so small there is no real need for that.

In the end the core of the solver is:

```python
def calculate(number, i):
    ops = '$%&*+-/<>^|~'
    for perm in itertools.permutations(list(number)):
        for parenthesis1 in range(len(perm) - 1):
            for parenthesis2 in range(parenthesis1, len(perm) - 1):
                for op in itertools.product(list(ops), repeat=len(perm) - 1):
                    equation = combine(perm, op, parenthesis1, parenthesis2)
                    try:
                        if eval(equation) == i:
                            return equation
                    except:
                        pass
    print("No configuration found for " + str(number) + " " + str(i))
    sys.exit(0)
```

It doesn't always provide an answer, but after few runs it usually finds the answer for all values and gives the flag:
`ASIS{~_iZ_U53fuL_un4rY_0per471On_:P!!!}`

In hindsight it was a huge overkill since the server checker didn't actually verify that each number appears only once!
We could have easily generate `1` by division of each number by itself and then combine them to get any number we want...

Full solver [here](laxt.py)
