#!/usr/bin/env python3
"""Simple terminal calculator: calculator 1
Usage:
  - Enter arithmetic expressions, e.g. 2+3*4, (1+2)/3, 2**8
  - Use math functions: sqrt(x), sin(x), cos(x), tan(x), log(x), exp(x)
  - Commands: help, history, clear, exit
"""
import ast
import math


def _eval(node):
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        ops = {
            ast.Add: lambda a, b: a + b,
            ast.Sub: lambda a, b: a - b,
            ast.Mult: lambda a, b: a * b,
            ast.Div: lambda a, b: a / b,
            ast.Pow: lambda a, b: a ** b,
            ast.Mod: lambda a, b: a % b,
            ast.FloorDiv: lambda a, b: a // b,
        }
        fn = ops.get(type(node.op))
        if fn is None:
            raise TypeError('Unsupported operator')
        return fn(left, right)
    if isinstance(node, ast.UnaryOp):
        val = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +val
        if isinstance(node.op, ast.USub):
            return -val
        raise TypeError('Unsupported unary operator')
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise TypeError('Unsupported constant')
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            name = node.func.id
            allowed = {'sqrt', 'sin', 'cos', 'tan', 'log', 'log10', 'exp', 'fabs'}
            if name in allowed:
                fn = getattr(math, name)
                args = [_eval(a) for a in node.args]
                return fn(*args)
        raise TypeError('Unsupported function call')
    raise TypeError('Unsupported expression')


def eval_expr(expr):
    tree = ast.parse(expr, mode='eval')
    return _eval(tree.body)


def print_help():
    print('Commands: help, history, clear, exit')
    print('Examples: 2+2, (3+4)*5, 2**10, sqrt(16), sin(0.5)')


def main():
    history = []
    print('calculator 1 — type "help" for commands, "exit" to quit')
    while True:
        try:
            s = input('calculator 1> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not s:
            continue
        cmd = s.lower()
        if cmd in ('exit', 'quit', 'q'):
            break
        if cmd == 'help':
            print_help()
            continue
        if cmd == 'history':
            if not history:
                print('No history')
            else:
                for i, (expr, res) in enumerate(history, 1):
                    print(f'{i}: {expr} = {res}')
            continue
        if cmd == 'clear':
            history.clear()
            print('History cleared')
            continue
        try:
            result = eval_expr(s)
            print(result)
            history.append((s, result))
        except Exception as e:
            print('Error:', e)


if __name__ == '__main__':
    main()
