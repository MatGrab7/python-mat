"""
Unit tests for the hello_sun module.
"""

import unittest
from hello_sun import greet_sun, main


class TestGreetSunFunction(unittest.TestCase):
    """Test cases for greet_sun function."""

    def test_greet_sun_default(self):
        """Test greet_sun with default parameter."""
        result = greet_sun()
        self.assertEqual(result, "Hello, Sun!")

    def test_greet_sun_with_name(self):
        """Test greet_sun with custom name."""
        result = greet_sun("Sol")
        self.assertEqual(result, "Hello, Sol sun!")

    def test_greet_sun_with_another_name(self):
        """Test greet_sun with another custom name."""
        result = greet_sun("Helios")
        self.assertEqual(result, "Hello, Helios sun!")

    def test_greet_sun_with_empty_string(self):
        """Test greet_sun with empty string returns default (empty string is falsy)."""
        result = greet_sun("")
        self.assertEqual(result, "Hello, Sun!")

    def test_greet_sun_return_type(self):
        """Test that greet_sun returns a string."""
        result = greet_sun("Test")
        self.assertIsInstance(result, str)

    def test_greet_sun_with_none(self):
        """Test greet_sun explicitly with None."""
        result = greet_sun(None)
        self.assertEqual(result, "Hello, Sun!")


class TestHelloSun(unittest.TestCase):
    """Test cases for hello_sun module."""

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
