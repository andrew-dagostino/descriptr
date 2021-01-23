import unittest
import os

from classes.descriptr_searches import DescSearches

class TestDescSearches(unittest.TestCase):

    def test_byCourseCode(self):
        """
            Test that course code search returns correct results
        """
        pass #TODO

    def test_byCourseCode_case(self):
        """
            Test that course code search returns correct results regardless of upper/lower case
        """
        pass #TODO

    def test_byCourseCode_none(self):
        """
            Test that course code search returns no results for code not in courses
        """
        pass #TODO

if __name__ == '__main__':
    unittest.main()