import unittest
from unittest.mock import Mock
from unittest import TestCase
from neurosfl.main import parse_from_string

class TestSimpleConsts(TestCase):
    def test_with_where(self):
        parse_from_string("where company = 'NIKE'")

    def test_without_where(self):
        parse_from_string("company = 'NIKE'")

if __name__ == '__main__':
    unittest.main()