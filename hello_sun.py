#!/usr/bin/env python3
"""
Hello Sun Script - for testing the CI/CD pipeline.

This is a simple test script to verify that the code quality
and secrets scanning pipeline is working correctly.

Author: Development Team
Version: 1.0
Last Updated: 2026-02-09

Features:
    - Simple greeting output for the sun
    - Type hints with proper annotations
    - Docstring documentation
    - Clean code formatting with Black
    - Passes all linting checks (Pylint, Flake8)
    - Free of secrets and security vulnerabilities

Usage:
    python hello_sun.py

Requirements:
    - Python 3.8+

Notes:
    This script serves as a test for the CI/CD pipeline,
    including code quality scans, secrets detection, and security analysis.
"""

from typing import Optional


def greet_sun(sun_name: Optional[str] = None) -> str:
    """
    Generate a greeting message for the sun.

    Args:
        sun_name: Optional name to include in the greeting

    Returns:
        The formatted greeting message
    """
    if sun_name:
        return f"Hello, {sun_name} sun!"
    return "Hello, Sun!"


def main() -> None:
    """Print hello sun message(s)."""
    # Display greeting messages to console
    print(greet_sun())
    print(greet_sun("Sol"))


if __name__ == '__main__':
    main()
