"""
Unit tests for the hello_world module.
"""

import unittest
from hello_world import main, greet


class TestGreetFunction(unittest.TestCase):
    """Test cases for greet function."""

    def test_greet_default(self):
        """Test greet with default parameter."""
        result = greet()
        self.assertEqual(result, "Hello, World!")

    def test_greet_with_name(self):
        """Test greet with custom name."""
        result = greet("Alice")
        self.assertEqual(result, "Hello, Alice!")

    def test_greet_with_empty_string(self):
        """Test greet with empty string."""
        result = greet("")
        self.assertEqual(result, "Hello, !")

    def test_greet_return_type(self):
        """Test that greet returns a string."""
        result = greet("Test")
        self.assertIsInstance(result, str)


class TestHelloWorld(unittest.TestCase):
    """Test cases for hello_world module."""

    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        self.assertTrue(callable(main))

    def test_main_function_runs(self):
        """Test that main function runs without error."""
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised {type(e).__name__}: {e}")


if __name__ == '__main__':
    unittest.main()
