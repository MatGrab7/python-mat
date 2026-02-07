#!/usr/bin/env python3
"""
Hello World Script - for testing the CI/CD pipeline.

This is a simple test script to verify that the code quality
and secrets scanning pipeline is working correctly.

Author: Development Team
Version: 1.1
Last Updated: 2026-02-07

Features:
    - Simple greeting output
    - Type hints with proper annotations
    - Docstring documentation
    - Clean code formatting with Black
    - Passes all linting checks (Pylint, Flake8)
    - Free of secrets and security vulnerabilities

Usage:
    python hello_world.py

Requirements:
    - Python 3.8+

Notes:
    This script serves as a baseline for testing the CI/CD pipeline,
    including code quality scans, secrets detection, and security analysis.
"""


def main() -> None:
    """Print hello world message."""
    # Display greeting message to console
    print("Hello, World!")
    # This script is used for testing the CI/CD pipeline


if __name__ == "__main__":
    main()
