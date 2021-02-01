"""
Class for representing a course.
Includes both requried properties and optional properties.
Validates all fields upon attempted initialization.
"""

from classes.course_validation import *
from functions.course_helpers import get_course_representation

class Course:
	def __init__(self, course_info):
		required_course_info = [
			"group", "departments", "code", "number", "name", "semesters_offered",
			"lecture_hours", "lab_hours", "credits", "distance_education", "year_parity_restrictions"
		]
		optional_course_info = [
			"description", "other", "prerequisites", "equates", "corequisites", "restrictions"
		]

		for key in required_course_info:
			if key in course_info:
				setattr(self, key, course_info[key])
			else:
				raise Exception("course_info missing required key: \""+key+"\"")

		for key in optional_course_info:
			if key in course_info:
				setattr(self, key, course_info[key])

	#Getters and Setter Validation:

	@property
	def group(self):
		return self._group

	@group.setter
	def group(self, group):
		CourseVal.group(group)
		self._group = group

	@property
	def departments(self):
		return self._departments

	@departments.setter
	def departments(self, departments):
		CourseVal.departments(departments)
		self._departments = departments

	@property
	def code(self):
		return self._code

	@code.setter
	def code(self, code):
		CourseVal.code(code)
		self._code = code

	@property
	def number(self):
		return self._number

	@number.setter
	def number(self, number):
		CourseVal.number(number)
		self._number = number

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
		CourseVal.name(name)
		self._name = name

	@property
	def semesters_offered(self):
		return self._semesters_offered

	@semesters_offered.setter
	def semesters_offered(self, semesters_offered):
		CourseVal.semesters_offered(semesters_offered)
		self._semesters_offered = semesters_offered

	@property
	def lecture_hours(self):
		return self._lecture_hours

	@lecture_hours.setter
	def lecture_hours(self, lecture_hours):
		CourseVal.lecture_hours(lecture_hours)
		self._lecture_hours = lecture_hours

	@property
	def lab_hours(self):
		return self._lab_hours

	@lab_hours.setter
	def lab_hours(self, lab_hours):
		CourseVal.lab_hours(lab_hours)
		self._lab_hours = lab_hours

	@property
	def credits(self):
		return self._credits

	@credits.setter
	def credits(self, credits):
		CourseVal.credits(credits)
		self._credits = credits

	@property
	def description(self):
		return self._description

	@description.setter
	def description(self, description):
		CourseVal.description(description)
		self._description = description

	@property
	def distance_education(self):
		return self._distance_education

	@distance_education.setter
	def distance_education(self, distance_education):
		CourseVal.distance_education(distance_education)
		self._distance_education = distance_education

	@property
	def year_parity_restrictions(self):
		return self._year_parity_restrictions

	@year_parity_restrictions.setter
	def year_parity_restrictions(self, year_parity_restrictions):
		CourseVal.year_parity_restrictions(year_parity_restrictions)
		self._year_parity_restrictions = year_parity_restrictions

	@property
	def other(self):
		return self._other

	@other.setter
	def other(self, other):
		CourseVal.other(other)
		self._other = other

	@property
	def prerequisites(self):
		return self._prerequisites

	@prerequisites.setter
	def prerequisites(self, prerequisites):
		CourseVal.prerequisites(prerequisites)

		self._prerequisites = prerequisites

	@property
	def equates(self):
		return self._equates

	@equates.setter
	def equates(self, equates):
		CourseVal.equates(equates)
		self._equates = equates

	@property
	def corequisites(self):
		return self._corequisites

	@corequisites.setter
	def corequisites(self, corequisites):
		CourseVal.corequisites(corequisites)
		self._corequisites = corequisites

	@property
	def restrictions(self):
		return self._restrictions

	@restrictions.setter
	def restrictions(self, restrictions):
		CourseVal.restrictions(restrictions)
		self._restrictions = restrictions

	"""
	Print a visual representation of the course:
	"""
	def __str__(self):
		max_line_length = 150
		result = get_course_representation(self, max_line_length)

		return result
