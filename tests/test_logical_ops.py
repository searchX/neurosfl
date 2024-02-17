import unittest
from unittest.mock import Mock
from unittest import TestCase
from neurosfl.main import parse_from_string

class TestLogicalOps(TestCase):
    def test_and(self):
        parse_from_string("where company = 'NIKE' and category = 'Shoes'")

    def test_or(self):
        parse_from_string("where company = 'NIKE' or category = 'Shoes'")

    def test_and_or(self):
        parse_from_string("where company = 'NIKE' and category = 'Shoes' or listPrice <= 1000")

    def test_or_and(self):
        parse_from_string("where company = 'NIKE' or category = 'Shoes' and listPrice <= 1000")

    def test_and_or_and(self):
        parse_from_string("where company = 'NIKE' and category = 'Shoes' or (listPrice <= 1000 AND price >= 500)")

if __name__ == '__main__':
    unittest.main()