"""
Unit tests for the hello_world module.
"""

import unittest
from hello_world import main


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
