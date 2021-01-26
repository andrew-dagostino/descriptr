import unittest
from classes.pdf_converter import PDFConverter
from classes.course_parser import *

class TestCourseParser(unittest.TestCase):

    def test_open_file_simple(self):
        '''
            Tests that a Course object can be created from a text file. Also parses the text file.
        '''

        f = open("./test/test-text/typical-course.txt")
        self.assertTrue(f is not None)
        f.close()

        cp = CourseParser()
        courses = cp.open_file("./test/test-text/typical-course.txt")

        self.assertTrue(courses is not None)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].group, "Accounting")
        self.assertEqual(courses[0].departments, ["Department of Management"])
        self.assertEqual(courses[0].code, "ACCT")
        self.assertEqual(courses[0].number, "1220")
        self.assertEqual(courses[0].name, "Introductory Financial Accounting")
        self.assertEqual(courses[0].semesters_offered, [SemesterOffered.F, SemesterOffered.W])
        self.assertEqual(courses[0].lecture_hours, 3.0)
        self.assertEqual(courses[0].lab_hours, 0.0)
        self.assertEqual(courses[0].credits, 0.50)
        self.assertEqual(courses[0].description,    "This introductory course is designed to develop a foundational understanding of current"
                                                    + " accounting principles and their implication for published financial reports of business"
                                                    + " enterprises. It builds the base of knowledge and understanding required to succeed in"
                                                    + " more advanced study of accounting. The course approaches the subject from the point"
                                                    + " of view of the user of accounting information rather than that of a person who supplies"
                                                    + " the information.")
        self.assertEqual(courses[0].distance_education, DistanceEducation.SUPPLEMENTARY)
        self.assertEqual(courses[0].restrictions,   ["ACCT*2220 , This is a Priority Access Course. Enrolment may be"
                                                    + " restricted to particular programs or specializations. See department for"
                                                    + " more information."])

    def test_open_file_complex(self):
        '''
            Tests that a more complex course can be parsed and put into a Course structure
        '''

        f = open("./test/test-text/complex-course.txt")
        self.assertTrue(f is not None)
        f.close()

        cp = CourseParser()
        courses = cp.open_file("./test/test-text/complex-course.txt")

        self.assertTrue(courses is not None)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].group, "Subject")
        self.assertEqual(courses[0].departments, ["Department of Management", "Department of Science"])
        self.assertEqual(courses[0].code, "ASDF")
        self.assertEqual(courses[0].number, "1234")
        self.assertEqual(courses[0].name, "A complex Example")
        self.assertEqual(courses[0].semesters_offered, [SemesterOffered.U])
        self.assertEqual(courses[0].lecture_hours, 0.0)
        self.assertEqual(courses[0].lab_hours, 0.0)
        self.assertEqual(courses[0].credits, 0.75)
        self.assertEqual(courses[0].description, "Short descript with one line to test for next line peek test")
        self.assertEqual(courses[0].distance_education, DistanceEducation.ONLY)
        self.assertEqual(courses[0].year_parity_restrictions, YearParityRestrictions.EVEN_YEARS)
        self.assertEqual(courses[0].prerequisites, "ACCT*4220")
        self.assertEqual(courses[0].corequisites, "MUSC*2180")
        self.assertEqual(courses[0].equates, "CLAS*2150")
        self.assertEqual(courses[0].restrictions,   ["AAAA*1111 , This is a Priority Access Course.",
                                                    "Enrolment may be restricted to particular programs or specializations."
                                                    + " See department for more information."])
