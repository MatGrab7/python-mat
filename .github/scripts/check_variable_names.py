#!/usr/bin/env python3
"""
Variable naming convention checker.

Detects poorly named variables that don't follow Python naming conventions.
Flags single-letter variables (except common loop counters),
generic names like 'data', 'temp', 'foo', 'test', etc.
"""

import ast
import sys
from pathlib import Path
from typing import List, Set, Tuple


# Common acceptable single-letter variables
ACCEPTABLE_SINGLE_LETTERS = {'i', 'j', 'k', 'x', 'y', 'z', '_', 'n', 'e'}

# Generic/meaningless names that should be flagged
GENERIC_NAMES = {
    'data', 'temp', 'tmp', 'test', 'foo', 'bar', 'baz',
    'val', 'var', 'item', 'obj', 'thing', 'value', 'result',
    'a', 'b', 'c', 'd', 'f', 'g', 'h', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'xxx', 'yyy', 'zzz', 'xx', 'yy', 'zz',
    'buf', 'cnt', 'num', 'idx', 'ptr'
}

# Common acceptable names in specific contexts
CONTEXT_ACCEPTABLE = {'self', 'cls', 'args', 'kwargs'}


class VariableNameChecker(ast.NodeVisitor):
    """AST visitor to check for poorly named variables."""

    def __init__(self, filename: str):
        self.filename = filename
        self.issues: List[Tuple[int, str, str]] = []
        self.in_loop = False

    def visit_Name(self, node: ast.Name) -> None:
        """Check variable names."""
        self._check_name(node.id, node.lineno)
        self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> None:
        """Check function argument names."""
        self._check_name(node.arg, node.lineno)
        self.generic_visit(node)

    def _check_name(self, name: str, lineno: int) -> None:
        """Check if a variable name is acceptable."""
        # Skip private/magic variables
        if name.startswith('__') or name.startswith('_'):
            return

        # Skip context-specific names
        if name in CONTEXT_ACCEPTABLE:
            return

        # Check for generic names
        if name.lower() in GENERIC_NAMES:
            self.issues.append(
                (lineno, name, f"Generic/meaningless name: '{name}'")
            )
            return

        # Check for single-letter variables (except acceptable ones)
        if len(name) == 1 and name not in ACCEPTABLE_SINGLE_LETTERS:
            self.issues.append(
                (lineno, name, f"Single-letter variable: '{name}' (only use i, j, k, x, y, z)")
            )


def check_file(filepath: Path) -> List[Tuple[str, int, str, str]]:
    """Check a Python file for variable naming issues."""
    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)
        checker = VariableNameChecker(str(filepath))
        checker.visit(tree)

        for lineno, name, message in checker.issues:
            issues.append((str(filepath), lineno, name, message))

    except (SyntaxError, ValueError) as e:
        print(f"Warning: Could not parse {filepath}: {e}")

    return issues


def main() -> int:
    """Check all Python files in the repository."""
    issues = []

    # Get all Python files
    python_files = list(Path('.').rglob('*.py'))

    # Skip venv, .git, __pycache__, etc.
    skip_dirs = {'.git', 'venv', '.venv', '__pycache__', '.pytest_cache', 'build', 'dist'}
    python_files = [
        f for f in python_files
        if not any(skip in f.parts for skip in skip_dirs)
    ]

    # Check each file
    for filepath in sorted(python_files):
        file_issues = check_file(filepath)
        issues.extend(file_issues)

    # Report issues
    if issues:
        print("❌ Variable naming issues found:")
        print("-" * 70)
        for filepath, lineno, name, message in issues:
            print(f"{filepath}:{lineno}: {message}")
        print("-" * 70)
        print(f"\nTotal issues: {len(issues)}")
        return 1
    else:
        print("✅ Variable naming check passed - no issues found!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
