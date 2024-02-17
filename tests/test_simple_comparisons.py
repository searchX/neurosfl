import unittest
from unittest.mock import Mock
from unittest import TestCase
from neurosfl.main import parse_from_string

class TestSimpleComparisons(TestCase):
    def test_simple_equals(self):
        parse_from_string("where company = 'NIKE'")

    def test_simple_not_equals(self):
        parse_from_string("where company != 'NIKE'")

    def test_simple_greater_than(self):
        parse_from_string("where listPrice > 1000")
    
    def test_simple_less_than(self):
        parse_from_string("where listPrice < 1000")

    def test_simple_greater_than_or_equals(self):
        parse_from_string("where listPrice >= 1000")

    def test_simple_less_than_or_equals(self):
        parse_from_string("where listPrice <= 1000")

if __name__ == '__main__':
    unittest.main()