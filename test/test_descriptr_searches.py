import unittest
import os

from classes.descriptr_searches import DescSearches
from classes.course import Course
from classes.course_enums import *

class TestDescSearches(unittest.TestCase):

    single_course = []

    @classmethod
    def setUpClass(self):
        self.single_course = [Course({
            "group": "Hospitality and Tourism Management",
            "departments": ["School of Hospitality", "Food and Tourism Management"],
            "code": "HTM",
            "number": "4080",
            "name": "Experiential Learning and Leadership in the Service Industry",
            "semesters_offered": [SemesterOffered.F, SemesterOffered.W],
            "lecture_hours": 3.5,
            "lab_hours": 0.0,
            "credits": 0.5,
            "description": "An integration of the students' academic studies with their work experiences. Emphasis\n\
            will be placed on applying and evaluating theoretical concepts in different working environments. \
            Students will investigate the concept of workplace fit applying this to their prospective career path.",
            "distance_education": DistanceEducation.ONLY,
            "year_parity_restrictions": YearParityRestrictions.EVEN_YEARS,
            "other": "Last offering - Winter 2021",
            "prerequisites": "14.00 credits and a minimum of 700 hours of verified work experience in the hospitality, sport and tourism industries.",
            "equates": "HISP*2040",
            "corequisites": "HTM*4075",
            "restrictions": ["MGMT*1000", "Not available to students in the BCOMM program."]
        })]

    def test_byCourseCode(self):
        """
            Test that course code search returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseCode(self.single_course, "HTM")) == 1)

    def test_byCourseCode_case(self):
        """
            Test that course code search returns correct results regardless of upper/lower case
        """
        upperCode = "HTM"
        lowerCode = "htm"
        mixedCode = "hTm"

        d = DescSearches()
        upperResult = d.byCourseCode(self.single_course, upperCode)
        lowerResult = d.byCourseCode(self.single_course, lowerCode)
        mixedResult = d.byCourseCode(self.single_course, mixedCode)

        self.assertTrue(len(upperResult) == 1)
        self.assertTrue(len(lowerResult) == 1)
        self.assertTrue(len(mixedResult) == 1)

    def test_byCourseCode_none(self):
        """
            Test that course code search returns no results for code not in courses
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseCode(self.single_course, "DNE")) == 0)

    def test_byCourseLevel(self):
        """
            Test that course level search returns correct results
        """
        pass #TODO

    def test_byCourseNumber(self):
        """
            Test that course number search returns correct results
        """
        pass #TODO

    def test_byCourseNumber_invalid(self):
        """
            Test that course number search raises exceptions for invalid numbers
        """
        pass #TODO

if __name__ == '__main__':
    unittest.main()