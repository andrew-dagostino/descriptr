import contextlib
import io
import os
import unittest
import json

from classes.descriptr import Descriptr


class TestDescriptr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.f = io.StringIO()
        with contextlib.redirect_stdout(self.f):  # Hide stdout from console during unit tests
            self.descriptr = Descriptr()

    def setUp(self):
        self.f = io.StringIO()  # Clear stored stdout for each test
        self.descriptr.carryover_data = []

    def test_export_json(self):
        """Test that carryover data is exported as JSON successfully"""
        json_output = ""
        with contextlib.redirect_stdout(self.f):
            self.descriptr.do_search_code("cis")
            self.descriptr.do_search_number("2750", carryover=True)
            json_output = self.descriptr.export_json()

        self.assertTrue(len(json_output) > 0)

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) == 1)

    def test_export_json_empty(self):
        """Test that carryover data is exported as JSON successfully even if no courses from search"""
        json_output = ""
        with contextlib.redirect_stdout(self.f):
            self.descriptr.do_search_keyword("thereisnowaythatthiskeywordwillexist")
            json_output = self.descriptr.export_json()

        self.assertTrue(len(json_output) > 0)

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) == 0)

    def test_apply_filters(self):
        """Test that multiple filters returns correct results"""
        json_output = ""
        with contextlib.redirect_stdout(self.f):
            json_output = self.descriptr.apply_filters({
                "code": "cis",
                "number": "2750"
            })

        self.assertTrue(len(self.descriptr.carryover_data) == 1)
        self.assertTrue(self.descriptr.carryover_data[0].code.lower() == "cis")
        self.assertTrue(self.descriptr.carryover_data[0].number == "2750")

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) == 1)

    def test_apply_empty(self):
        """Test that multiple filters returns empty results for no match"""
        json_output = ""
        with contextlib.redirect_stdout(self.f):
            json_output = self.descriptr.apply_filters({
                "keyword": "thereisnowaythatthiskeywordwillexist"
            })

        self.assertTrue(len(self.descriptr.carryover_data) == 0)

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) == 0)

    def test_apply_invalid(self):
        """Test that multiple filters returns error for invalid search"""
        json_output = ""
        with contextlib.redirect_stdout(self.f):
            json_output = self.descriptr.apply_filters({
                "number": "12345"
            })

        self.assertTrue(len(self.descriptr.carryover_data) == 0)

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is not None)
        self.assertTrue(len(dictionary["courses"]) == 0)

if __name__ == '__main__':
    unittest.main()
