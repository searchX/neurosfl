import unittest
from unittest.mock import Mock
from unittest import TestCase
from neurosfl.main import parse_from_string

class TestParenthesis(TestCase):
    def test_parentheses(self):
        parse_from_string("where (company = 'NIKE' or category = 'Shoes') and listPrice <= 1000")

if __name__ == '__main__':
    unittest.main()