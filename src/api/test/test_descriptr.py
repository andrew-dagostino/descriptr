import contextlib
import io
import os
import unittest
import json

from classes.descriptr import Descriptr

""" Change working directory to one level above here """
os.chdir(os.path.dirname(os.path.dirname(__file__)))


class TestDescriptr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.descriptr = Descriptr()

    def setUp(self):
        self.descriptr.carryover_data = []

    def test_export_json(self):
        """Test that carryover data is exported as JSON successfully"""
        self.descriptr.do_search_code("cis")
        self.descriptr.do_search_number("2750", carryover=True)
        json_output = self.descriptr.export_json()

        self.assertTrue(len(json_output) > 0)

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) == 1)

    def test_export_json_empty(self):
        """Test that carryover data is exported as JSON successfully even if no courses from search"""
        self.descriptr.do_search_keyword(
            "thereisnowaythatthiskeywordwillexist")
        json_output = self.descriptr.export_json()

        self.assertTrue(len(json_output) > 0)

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) == 0)

    def test_apply_filters(self):
        """Test that multiple filters returns correct results"""
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
        json_output = self.descriptr.apply_filters({
            "keyword": "thereisnowaythatthiskeywordwillexist"
        })

        self.assertTrue(len(self.descriptr.carryover_data) == 0)

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) == 0)

    def test_apply_invalid(self):
        """Test that multiple filters returns error for invalid search"""
        json_output = self.descriptr.apply_filters({
            "number": "12345"
        })

        self.assertTrue(len(self.descriptr.carryover_data) == 0)

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is not None)
        self.assertTrue(len(dictionary["courses"]) == 0)

    def test_apply_filters_group(self):
        """Test that group filter returns correct results"""
        json_output = self.descriptr.apply_filters({
            "group": "Biochemistry",
        })

        self.assertTrue(self.descriptr.carryover_data[0].group.lower() == "biochemistry")

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) == 7)

    def test_apply_filters_department(self):
        """Test that department filter returns correct results"""
        json_output = self.descriptr.apply_filters({
            "department": "Department of Plant Agriculture",
        })

        self.assertTrue(self.descriptr.carryover_data[0].code.lower() == "agr")
        self.assertTrue(self.descriptr.carryover_data[0].number == "1110")

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) > 0)
    
    def test_apply_filters_level(self):
        """Test that level filter returns correct results"""
        json_output = self.descriptr.apply_filters({
            "level": 1,
        })

        self.assertTrue(self.descriptr.carryover_data[0].code.lower() == "acct")
        self.assertTrue(self.descriptr.carryover_data[0].number == "1220")

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) > 0)
    
    def test_apply_filters_semester(self):
        """Test that semester filter returns correct results"""
        json_output = self.descriptr.apply_filters({
            "semester": "F",
        })

        self.assertTrue(self.descriptr.carryover_data[0].code.lower() == "acct")
        self.assertTrue(self.descriptr.carryover_data[0].number == "1220")

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) > 0)

    def test_apply_filters_weight(self):
        """Test that weight filter returns correct results"""
        json_output = self.descriptr.apply_filters({
            "weight": 0.75,
        })

        self.assertTrue(self.descriptr.carryover_data[0].code.lower() == "bioc")
        self.assertTrue(self.descriptr.carryover_data[0].number == "3570")

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)
        self.assertTrue(len(dictionary["courses"]) > 0)

    def test_apply_filters_capacity(self):
        """Test that capacity filter returns correct results"""
        json_output = self.descriptr.apply_filters({
            "capacity": {"capacity": 0, "comparison": "<"},
        })

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)

    def test_apply_filters_lecture(self):
        """Test that lecture hours filter returns correct results"""
        json_output = self.descriptr.apply_filters({
            "lecture": {"hours": 0, "comparison": "<"},
        })

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)

    def test_apply_filters_lab(self):
        """Test that lecture hours filter returns correct results"""
        json_output = self.descriptr.apply_filters({
            "lecture": {"hours": 0, "comparison": "<"},
        })

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)

    def test_apply_filters_offered(self):
        """Test that semester filter returns correct results"""
        json_output = self.descriptr.apply_filters({
            "offered": "Y",
        })

        dictionary = json.loads(json_output)
        self.assertTrue(dictionary["error"] is None)

if __name__ == '__main__':
    unittest.main()
