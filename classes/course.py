"""
Class for representing a course.
Includes both requried properties and optional properties.
Validates all fields upon attempted initialization.
"""

from classes.course_enums import *
from functions.course_helpers import multi_line_repr

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
		if type(group) != str:
			raise Exception("Course group name must be a string.")
		if len(group) == 0:
			raise Exception("Course group name can't be an empty string.")
		self._group = group

	@property
	def departments(self):
		return self._departments

	@departments.setter
	def departments(self, departments):
		if type(departments) != list:
			raise Exception("Course departments must be a list.")
		if len(departments) == 0:
			raise Exception("Course must be part of at least one department.")

		for department in departments:
			if isinstance(department, str) == False or len(department) == 0:
				raise Exception("All course departments must be non-empty strings.")

		self._departments = departments

	@property
	def code(self):
		return self._code

	@code.setter
	def code(self, code):
		if type(code) != str:
			raise Exception("Course code must be a string.")
		if len(code) == 0:
			raise Exception("Course code can't be an empty string.")
		self._code = code

	@property
	def number(self):
		return self._number

	@number.setter
	def number(self, number):
		if type(number) != str:
			raise Exception("Course number must be a string.")
		if len(number) == 0 or len(number) > 4:
			raise Exception("Course number has invalid range.")
		self._number = number

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
		if type(name) != str:
			raise Exception("Course name must be a string.")
		if len(name) == 0:
			raise Exception("Course name can't be an empty string.")
		self._name = name

	@property
	def semesters_offered(self):
		return self._semesters_offered

	@semesters_offered.setter
	def semesters_offered(self, semesters_offered):
		if type(semesters_offered) != list:
			raise Exception("Course semesters_offered must be a list.")

		if len(semesters_offered) == 0:
			raise Exception("Course semester offerings must be specified implicitly")

		for semester_offered in semesters_offered:
			if isinstance(semester_offered, SemesterOffered) == False:
				raise Exception("All course semesters offered must be a SemesterOffered enum")

		self._semesters_offered = semesters_offered

	@property
	def lecture_hours(self):
		return self._lecture_hours

	@lecture_hours.setter
	def lecture_hours(self, lecture_hours):
		if type(lecture_hours) != float:
			raise Exception("Course lecture_hours must be a float.")
		if lecture_hours < 0 and lecture_hours > (24*7):
			raise Exception("Course lecture_hours has invalid range.")
		self._lecture_hours = lecture_hours

	@property
	def lab_hours(self):
		return self._lab_hours

	@lab_hours.setter
	def lab_hours(self, lab_hours):
		if type(lab_hours) != float:
			raise Exception("Course lab_hours must be a float.")
		if lab_hours < 0 or lab_hours > (24*7):
			raise Exception("Course lab_hours has invalid range.")
		self._lab_hours = lab_hours

	@property
	def credits(self):
		return self._credits

	@credits.setter
	def credits(self, credits):
		if type(credits) != float:
			raise Exception("Course credit must be a float.")
		if credits < 0:
			raise Exception("Course credit not within allowable range.")
		self._credits = credits

	@property
	def description(self):
		return self._description

	@description.setter
	def description(self, description):
		if type(description) != str:
			raise Exception("If the course has a description, it must be a string.")
		self._description = description

	@property
	def distance_education(self):
		return self._distance_education

	@distance_education.setter
	def distance_education(self, distance_education):
		if isinstance(distance_education, DistanceEducation) == False:
			raise Exception("All courses must store a distance_education property with an enum type of DistanceEducation.")

		self._distance_education = distance_education

	@property
	def year_parity_restrictions(self):
		return self._year_parity_restrictions

	@year_parity_restrictions.setter
	def year_parity_restrictions(self, year_parity_restrictions):
		if isinstance(year_parity_restrictions, YearParityRestrictions) == False:
			raise Exception("All courses must store a year_parity_restrictions property with an enum type of YearParityRestrictions.")

		self._year_parity_restrictions = year_parity_restrictions

	@property
	def other(self):
		return self._other

	@other.setter
	def other(self, other):
		if type(other) != str:
			raise Exception("Course offering under the other category must be a string.")
		if len(other) == 0:
			raise Exception("If the course has an offering under the other category, it must have a length.")
		self._other = other

	@property
	def prerequisites(self):
		return self._prerequisites

	@prerequisites.setter
	def prerequisites(self, prerequisites):
		if type(prerequisites) != str:
			raise Exception("Course prerequisites must be a non-empty string.")
		if len(prerequisites) == 0:
			raise Exception("If the course has a prerequisites property, the prerequisites can't be an empty string.")
		self._prerequisites = prerequisites

	@property
	def equates(self):
		return self._equates

	@equates.setter
	def equates(self, equates):
		if type(equates) != str:
			raise Exception("Course equates must be a non-empty string.")
		if len(equates) == 0:
			raise Exception("If the course has a equates property, the equates can't be an empty string.")
		self._equates = equates

	@property
	def corequisites(self):
		return self._corequisites

	@corequisites.setter
	def corequisites(self, corequisites):
		if type(corequisites) != str:
			raise Exception("Course corequisites must be a non-empty string.")
		if len(corequisites) == 0:
			raise Exception("If the course has a corequisites property, the corequisites can't be an empty string.")
		self._corequisites = corequisites

	@property
	def restrictions(self):
		return self._restrictions

	@restrictions.setter
	def restrictions(self, restrictions):
		if type(restrictions) != list:
			raise Exception("Course restrictions must be a list of non-empty string.")
		if len(restrictions) == 0:
			raise Exception("If the course has a restrictions property, there must be at least one restriction.")

		for restriction in restrictions:
			if isinstance(restriction, str) == False or len(restriction) == 0:
				raise Exception("All course restrictions must be non-empty strings.")

		self._restrictions = restrictions

	"""
	Print a visual representation of the course:
	"""
	def __str__(self):
		max_line_length = 150

		lines = multi_line_repr(self.group, max_line_length)

		semesters_offered_str = ",".join(semester_offered.name for semester_offered in self.semesters_offered)

		lecture_hours = self.lecture_hours
		if float(self.lecture_hours).is_integer() == True:
			lecture_hours = int(self.lecture_hours)

		lab_hours = self.lab_hours
		if float(self.lab_hours).is_integer() == True:
			lab_hours = int(self.lab_hours)

		course_header = self.code+"*"+self.number+" "+self.name+" "+semesters_offered_str+\
			" ("+str(lecture_hours)+"-"+str(lab_hours)+") ["+str("%.2f" % self.credits)+"]"
		lines += multi_line_repr(course_header, max_line_length)

		after_header_pos = len(lines)

		offerings = "Offering(s): "+str(self.distance_education.value or "") + " " + str(self.year_parity_restrictions.value or "")
		if hasattr(self, "other"):
			offerings += " "+self.other

		lines += multi_line_repr(offerings, max_line_length)

		if hasattr(self, "prerequisites"):
			prerequisites = "Prerequisite(s): "+self.prerequisites
			lines += multi_line_repr(prerequisites, max_line_length)

		if hasattr(self, "equates"):
			equates = "Equate(s): "+self.equates
			lines += multi_line_repr(equates, max_line_length)

		if hasattr(self, "corequisites"):
			corequisites = "Co-requisite(s): "+self.corequisites
			lines += multi_line_repr(corequisites, max_line_length)

		if hasattr(self, "restrictions"):
			for restriction in self.restrictions:
				restriction = ("Restriction(s): "+restriction)
				lines += multi_line_repr(restriction, max_line_length)

		departments = "Department(s): "+(", ".join(department for department in self.departments))
		lines += [departments]

		#Code to print the above lines. Everything is auto-scaled into a nice display box:
		lines_len = len(lines)
		longest_line_len = len(max(lines, key=len))

		course_description_lines = []
		if hasattr(self, "description"):
			course_description_lines = [""]+multi_line_repr(self.description, longest_line_len)+[""]

		lines = lines[0:after_header_pos] + course_description_lines + lines[after_header_pos:lines_len]

		result = "+"+("-"*(longest_line_len+2))+"+\n"
		for line in lines:
			curr_line_len = len(line)
			result += ("| "+line + (" "*(longest_line_len-curr_line_len))+" |\n")
		result += "+"+("-"*(longest_line_len+2))+"+"

		return result
