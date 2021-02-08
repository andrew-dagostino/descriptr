import unittest
import os

from classes.descriptr_searches import DescSearches
from functions.export import export_graph
from classes.course import Course
from classes.course_enums import *

class TestDescriptrExportGraph(unittest.TestCase):
	single_course = []
	two_courses = []

	@classmethod
	def setUpClass(self):
		self.single_course = [
			Course({
				"group": "Hospitality and Tourism Management",
				"departments": ["School of Hospitality", "Food and Tourism Management"],
				"code": "CIS",
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
				"prerequisites": {
					"complex":
						[
							"14.00 credits and a minimum of 700 hours of verified work experience in the hospitality, sport and tourism industries."
						],
					"original": "14.00 credits and a minimum of 700 hours of verified work experience in the hospitality, sport and tourism industries."
				},
				"equates": "HISP*2040",
				"corequisites": "HTM*4075",
				"restrictions": ["MGMT*1000", "Not available to students in the BCOMM program."],
                "capacity_available": 10,
                "capacity_max": 20
			})
		]
		self.two_courses = self.single_course + [
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
				"prerequisites": {
					"simple":
						[
							"CIS*1250",
							"CIS*1300"
						],
					"original": "CIS*1250, CIS*1300"
				},
				"restrictions": ["Restricted to BCOMP:SENG majors"],
                "capacity_available": 0,
                "capacity_max": 5
			})
		]

	def test_blank_export(self):
		"""
            Tests that exporting of no courses works as intended.
        """
        #Set up the courses to ouput & the file name to output the export to.
		d = DescSearches()
		courses = []
		output_file_name = "blank-export-output.csv"

		#Attempt export.
		file_created = export_graph(courses, output_file_name)
		self.assertTrue(file_created is not None)

		#Read/Save export contents.
		f = open(output_file_name, "r")
		file_contents = f.read()
		f.close()

		#Delete exported file.
		os.system("rm -f "+output_file_name)

		#Check if exported file contents pass our test.
		self.assertEqual(file_contents, "Id;Label;Source;Target;group;capacity_available;capacity_max;capacity_ratio\n")

	def test_basic_export(self):
		"""
            Tests that basic exporting works as intended.
        """
        #Set up the courses to ouput & the file name to output the export to.
		d = DescSearches()
		courses = d.byCourseCode(self.two_courses, "CIS")
		output_file_name = "basic-export-output.csv"

		#Attempt export.
		file_created = export_graph(courses, output_file_name)
		self.assertTrue(file_created is not None)

		#Read/Save export contents.
		f = open(output_file_name, "r")
		file_contents = f.read()
		f.close()

		#Delete exported file.
		os.system("rm -f "+output_file_name)

		#Check if exported file contents pass our test.
		self.assertEqual(file_contents,
            "Id;Label;Source;Target;group;capacity_available;capacity_max;capacity_ratio\n"+
            "CIS*4080;CIS*4080;14.00 credits and a minimum of 700 hours of verified work experience in the hospitality, sport and tourism industries.;CIS*4080;Hospitality and Tourism Management;10;20;0.5\n"+
            "CIS*2250;CIS*2250;CIS*2250;CIS*1250;Computing and Information Science;0;5;0.0\n"+
            "CIS*2250;CIS*2250;CIS*2250;CIS*1300;Computing and Information Science;0;5;0.0\n"
        )


if __name__ == '__main__':
    unittest.main()