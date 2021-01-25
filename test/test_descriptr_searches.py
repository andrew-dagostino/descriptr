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
        self.two_courses = [Course({
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
            }),
            Course({
                "group": "Computing and Information Science",
                "departments": ["School of Computer Science"],
                "code": "CIS",
                "number": "2250",
                "name": "Software Design II",
                "semesters_offered": [SemesterOffered.W],
                "lecture_hours": float(3),
                "lab_hours": float(2),
                "credits": 0.5,
                "description": "This course focuses on the process of software design. Best practices for code development\n\
                and review will be the examined. The software development process and tools to support \
                this will be studied along with methods for project management. The course has an applied \
                focus and will involve software design and development experiences in teams, a literacy \
                component, and the use of software development tools.",
                "distance_education": DistanceEducation.NO,
                "year_parity_restrictions": YearParityRestrictions.NONE,
                "prerequisites": "CIS*1250, CIS*1300",
            "restrictions": ["Restricted to BCOMP:SENG majors"]
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
        d = DescSearches()
        self.assertTrue(len(d.byCourseLevel(self.single_course, "4")) == 1)

    def test_byCourseLevel_invalid(self):
        """
            Test that course level search raises exceptions for invalid numbers
        """
        d = DescSearches()

        with self.assertRaises(Exception) : d.byCourseLevel(self.single_course, "0")
        with self.assertRaises(Exception) : d.byCourseLevel(self.single_course, "11")
        with self.assertRaises(Exception) : d.byCourseLevel(self.single_course, "a")
        with self.assertRaises(Exception) : d.byCourseLevel(self.single_course, 4)

    def test_byCourseLevel_none(self):
        """
            Test that course level search returns no results if no matches are found
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseLevel(self.single_course, "1")) == 0)

    def test_byCourseNumber(self):
        """
            Test that course number search returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseNumber(self.single_course, "4080")) == 1)

    def test_byCourseNumber_invalid(self):
        """
            Test that course number search raises exceptions for invalid numbers
        """
        d = DescSearches()

        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, "abcd")
        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, 1234)
        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, "11")
        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, "40801")
        with self.assertRaises(Exception) : d.byCourseNumber(self.single_course, 4)

    def test_byCourseNumber_none(self):
        """
            Test that course level search returns no results if no matches are found
        """
        d = DescSearches()
        self.assertTrue(len(d.byCourseNumber(self.single_course, "1234")) == 0)

    def test_byKeyword(self):
        """
            Test that keyword search returns correct results
        """
        d = DescSearches()
        self.assertTrue(len(d.byKeyword(self.single_course, "htm*4080")) == 1)
        self.assertTrue(len(d.byKeyword(self.single_course, "SERVICE")) == 1)
        self.assertTrue(len(d.byKeyword(self.single_course, "hospitality and tourism")) == 1)

    def test_byKeyword_case(self):
        """
            Test that keyword search returns correct results regardless of upper/lower case
        """
        upperWord = "TOURISM"
        lowerWord = "tourism"
        mixedWord = "tOUrIsM"

        d = DescSearches()
        upperResult = d.byKeyword(self.single_course, upperWord)
        lowerResult = d.byKeyword(self.single_course, lowerWord)
        mixedResult = d.byKeyword(self.single_course, mixedWord)

        self.assertTrue(len(upperResult) == 1)
        self.assertTrue(len(lowerResult) == 1)
        self.assertTrue(len(mixedResult) == 1)

    def test_byKeyword_none(self):
        """
            Test that keyword search returns no results for keyword not in courses
        """
        d = DescSearches()
        self.assertTrue(len(d.byKeyword(self.single_course, "does not exist")) == 0)

    def test_byKeyword_invalid(self):
        """
            Test that keyword search raises exceptions for invalid keyword
        """
        d = DescSearches()

        with self.assertRaises(Exception) : d.byKeyword(self.single_course, 5)
        with self.assertRaises(Exception) : d.byKeyword(self.single_course, "")
        with self.assertRaises(Exception) : d.byKeyword(self.single_course, " ")
        with self.assertRaises(Exception) : d.byKeyword(self.single_course, "\n\t")

    def test_byKeyword_whitespace(self):
        """
            Test that keyword search ignores leading and trailing whitespace
        """
        d = DescSearches()
        self.assertTrue(len(d.byKeyword(self.single_course, " htm*4080 ")) == 1)
        self.assertTrue(len(d.byKeyword(self.single_course, "\nhtm*4080\n")) == 1)
        self.assertTrue(len(d.byKeyword(self.single_course, "\thtm*4080\t")) == 1)

    def test_bySemester(self):
        """Test that semester search returns correct results."""
        d = DescSearches()
        self.assertTrue(len(d.bySemester(self.single_course, SemesterOffered.W)) == 1)
        self.assertTrue(len(d.bySemester(self.two_courses, SemesterOffered.F)) == 1)

    def test_bySemester_invalid(self):
        """Test that semester search fails nonconforming input."""
        d = DescSearches()
        with self.assertRaises(Exception):
            d.bySemester(self.single_course, "W")
        with self.assertRaises(Exception):
            d.bySemester(self.single_course, 4)

if __name__ == '__main__':
    unittest.main()
