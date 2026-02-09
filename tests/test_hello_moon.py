"""
Unit tests for the hello_moon module.
"""

import unittest
from hello_moon import greet_moon, main


class TestHelloMoon(unittest.TestCase):
    def test_greet_default(self):
        self.assertEqual(greet_moon(), "Hello, Moon!")

    def test_greet_with_name(self):
        self.assertEqual(greet_moon("Selene"), "Hello, Selene moon!")

    def test_main_runs(self):
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised {type(e).__name__}: {e}")


if __name__ == '__main__':
    unittest.main()
