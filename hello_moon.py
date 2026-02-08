#!/usr/bin/env python3
"""
Hello Moon Script - for testing the CI/CD pipeline.
"""

from typing import Optional


def greet_moon(moon_name: Optional[str] = None) -> str:
    """Return a greeting for the moon or a named moon.

    Args:
        moon_name: Optional name to include in the greeting

    Returns:
        A greeting string
    """
    if moon_name:
        return f"Hello, {moon_name} moon!"
    return "Hello, Moon!"


def main() -> None:
    """Print greeting(s) to stdout."""
    print(greet_moon())
    print(greet_moon("Luna"))


if __name__ == '__main__':
    main()
