import sys
import ast


blacklist = [ast.Call, ast.Attribute]

def check(node):
    if isinstance(node, list):
        return all([check(n) for n in node])
    else:
        """
	expr = BoolOp(boolop op, expr* values)
	     | BinOp(expr left, operator op, expr right)
	     | UnaryOp(unaryop op, expr operand)
	     | Lambda(arguments args, expr body)
	     | IfExp(expr test, expr body, expr orelse)
	     | Dict(expr* keys, expr* values)
	     | Set(expr* elts)
	     | ListComp(expr elt, comprehension* generators)
	     | SetComp(expr elt, comprehension* generators)
	     | DictComp(expr key, expr value, comprehension* generators)
	     | GeneratorExp(expr elt, comprehension* generators)
	     -- the grammar constrains where yield expressions can occur
	     | Yield(expr? value)
	     -- need sequences for compare to distinguish between
	     -- x < 4 < 3 and (x < 4) < 3
	     | Compare(expr left, cmpop* ops, expr* comparators)
	     | Call(expr func, expr* args, keyword* keywords,
			 expr? starargs, expr? kwargs)
	     | Repr(expr value)
	     | Num(object n) -- a number as a PyObject.
	     | Str(string s) -- need to specify raw, unicode, etc?
	     -- other literals? bools?

	     -- the following expression can appear in assignment context
	     | Attribute(expr value, identifier attr, expr_context ctx)
	     | Subscript(expr value, slice slice, expr_context ctx)
	     | Name(identifier id, expr_context ctx)
	     | List(expr* elts, expr_context ctx) 
	     | Tuple(expr* elts, expr_context ctx)

	      -- col_offset is the byte offset in the utf8 string the parser uses
	      attributes (int lineno, int col_offset)

        """

        attributes = {
            'BoolOp': ['values'],
            'BinOp': ['left', 'right'],
            'UnaryOp': ['operand'],
            'Lambda': ['body'],
            'IfExp': ['test', 'body', 'orelse'],
            'Dict': ['keys', 'values'],
            'Set': ['elts'],
            'ListComp': ['elt'],
            'SetComp': ['elt'],
            'DictComp': ['key', 'value'],
            'GeneratorExp': ['elt'],
            'Yield': ['value'],
            'Compare': ['left', 'comparators'],
            'Call': False, # call is not permitted
            'Repr': ['value'],
            'Num': True,
            'Str': True,
            'Attribute': False, # attribute is also not permitted
            'Subscript': ['value'],
            'Name': True,
            'List': ['elts'],
            'Tuple': ['elts'],
            'Expr': ['value'], # root node 
        }

        for k, v in attributes.items():
            if hasattr(ast, k) and isinstance(node, getattr(ast, k)):
                if isinstance(v, bool):
                    return v
                return all([check(getattr(node, attr)) for attr in v])


if __name__ == '__main__':
    expr = sys.stdin.read()
    body = ast.parse(expr).body
    if check(body):
        sys.stdout.write(repr(eval(expr)))
    else:
        sys.stdout.write("Invalid input")
    sys.stdout.flush()
