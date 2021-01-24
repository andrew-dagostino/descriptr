'''
    file: course_parser.py
    author(s): Joshua Sarabdial

    Parses the course calander text for each of its courses
'''

import re
from classes.course import *

class CourseParser:
    def open_file(self, file_name):
        '''
            Opens contents of given file path and calls parsing function on them
            @param {String} file_name   The path to the .txt file
            @return {Course[]}  An array of Course objects
        '''
        courses = None

        try:
            f = open(file_name, "r")
        except Exception as e:
            print(e)
            return
        with f:
            courses=  self._parse_contents(f)

        return courses

    def _parse_contents(self, file):
        '''
            Iterates through file and parses contents into a course object array
            @param {File} file  The file object of .txt file opened
            @return {Course[]}  An array of Course objects
        '''
        courses = []
        course = None
        course_data = None

        line = file.readline()
        subject = line[:-1]
        description_check = False

        while line:
            if not description_check:
                ''' Checks if start of course description box '''
                txt = self._course_label_check(file, line)
                if txt:
                    course_data = self._course_label_parse(txt)
                    description_check = True
                elif re.search("XII\.", line):
                    x = file.tell()
                    line = file.readline()
                    if not re.search("]$", line):
                        subject = line[:-1]
                    else:
                        file.seek(x)
            elif description_check:
                ''' Checks if still inside of description box'''
                txt = self._course_label_check(file, line)
                if txt:
                    course_data.subject = subject
                    course_data.description = course_data.description[:-1]
                    course = self._create_course(course_data)
                    courses.append(course)
                    course_data = self._course_label_parse(txt)
                elif re.search("2020-2021", line):
                    course_data.subject = subject
                    course_data.description = course_data.description[:-1]
                    course = self._create_course(course_data)
                    courses.append(course)
                    description_check = False
                else:
                    course_data.description = course_data.description + line

            line = file.readline()

        return courses

    def _course_label_check(self, file, line):
        '''
            Checks if lines are the start of course description box
            @param {File} file  The file object of .txt file opened
            @param {String} line  The current line being iterated in file
            @return {String} The entire course label
        '''
        txt = None
        if re.search("^...\*", line) or re.search("^....\*", line):
            if  re.search("]$", line) and (not re.search("\D]$", line)):
                txt = line.rstrip("]\n")
            else:
                ''' Peeks at next line if we suspect the course label is overflowing '''
                x = file.tell()
                txt = file.readline()
                line = line.rstrip("\n")
                txt = line + txt
                if re.search("]$", txt) and (not re.search("\D]$", txt)) and re.search("\(", txt):
                    txt = txt.rstrip("]\n")
                else:
                    txt = None
                    file.seek(x)
        return txt

    def _course_label_parse(self, txt):
        '''
            Parses the course label
            @param {File} file  The file object of .txt file opened
            @param {String} line  The current line being iterated in file
            @return {CourseData} Filled out course data object except its description
        '''

        course = CourseData()
        pos = 0
        i = 1
        end = len(txt)

        ''' Extracts section '''
        while i < end and txt[i] != '*':
            i += 1
        if i >= end:
            raise Exception("Failed to parse '*' in line: ", txt)
        course.section = txt[pos:i].strip()

        ''' Extracts number and uses section to make course code '''
        i += 1
        pos = i
        while i < end and ((not txt[i].isalpha()) and (not txt[i-1].isspace()) ):
            i += 1
        if i >= end:
            raise Exception("Failed to parse alphabet character in line: ", txt)
        course.number = txt[pos:i].strip()
        course.code = course.section + "*" + course.number

        ''' Extracts course name and semester offerings '''
        pos = i
        j = end - 1
        while j > pos and txt[j] != '(':
            j -= 1
        if j <= pos:
            raise Exception("Failed to parse '(' in line: ", txt)
        i = j
        j = i - 2
        while j > pos and txt[j] != ' ':
            j -= 1
        if j < pos:
            raise Exception("Failed to parse ' ' in line: ", txt)
        course.name = txt[pos:j].strip()
        course.semesters = txt[j:i].strip()

        ''' Extracts time estimates of course '''
        i += 1
        pos = i
        while i < end and txt[i] != ')':
            i += 1
        if i >= end:
            raise Exception("Failed to parse ')' in line: ", txt)
        times = txt[pos:i]
        times = times.split("-", 1)
        course.lecture_time = times[0]
        course.lab_time = times[1]

        ''' Extracts credit weighting '''
        i += 1
        pos = i
        while i < end and txt[i] != '[':
            i += 1
        if i >= end:
            raise Exception("Failed to parse '[' in line: ", txt)
        i += 1
        course.credits = txt[i:end]

        return course

    def _create_course(self, course_data):
        '''
            Calls function to parse the description and put everything in Course
            @param {CourseData} course_data    a temp data structure for storing course information
            @return {Course} A filled out Course object
        '''

        semester_data = course_data.semesters.split(",")
        lecture_time = None
        lab_time = None
        desc_parts = None

        ''' Change semester info to enums '''
        semesters_offered = []
        if len(semester_data) == 0:
            semesters_offered.append(SemesterOffered.U)
        else:
            for semester in semester_data:
                if (semester == "S"):
                    semesters_offered.append(SemesterOffered.S)
                elif (semester == "F"):
                    semesters_offered.append(SemesterOffered.F)
                elif (semester == "W"):
                    semesters_offered.append(SemesterOffered.W)
                else:
                    semesters_offered.append(SemesterOffered.U)

        ''' Converts lecture and lab times to floats '''
        if course_data.lecture_time == "V":
            lecture_time = 0.0
        else:
            lecture_time = float(course_data.lecture_time)

        if course_data.lab_time == "V":
            lab_time = 0.0
        else:
            lab_time = float(course_data.lab_time)


        desc_parts = self._parse_description(course_data.description)

        course = Course({
            "group": course_data.subject,
            "departments": desc_parts[8],
            "code": course_data.section,
            "number": course_data.number,
            "name": course_data.name,
            "semesters_offered": semesters_offered,
            "lecture_hours": lecture_time,
            "lab_hours": lab_time,
            "credits": float(course_data.credits),
            "distance_education": desc_parts[1],
            "year_parity_restrictions": desc_parts[2],
        })

        ''' Add optional course info '''
        if desc_parts[0]:
            setattr(course, "description", desc_parts[0])
        if desc_parts[3]:
            setattr(course, "other", desc_parts[3])
        if desc_parts[4]:
            setattr(course, "prerequisites", desc_parts[4])
        if desc_parts[5]:
            setattr(course, "equates", desc_parts[5])
        if desc_parts[6]:
            setattr(course, "corequisites", desc_parts[6])
        if desc_parts[7]:
            setattr(course, "restrictions", desc_parts[7])

        return course

    def _parse_description(self, description):
        '''
            Parses the description box of a course into its details
            @param {String} description  The entire raw data of the description box unparsed
            @return {List} A list object containing all the seperate parts of the description
        '''
        lines = description.split("\n")
        i = 0
        n = len(lines)
        data = None
        description = ""
        distance_education = DistanceEducation.NO
        year_parity_restrictions = YearParityRestrictions.NONE
        other = None
        prerequisites = None
        equates = None
        corequisites = None
        restrictions = []
        departments = []

        if n > 0:
            while i < n and not re.search("\(s\):", lines[i]):
                description = description + lines[i] + " "
                i += 1
            while i < n:
                data = ""

                if re.search("Offerings\(s\):", lines[i]):
                    ''' Extracts distance education, year parity, and other from Offering(s) '''
                    data =  lines[i].split(" ", 1)
                    if len(data) > 0:
                        data = data[1] + " "
                    while i < (n - 1) and not re.search("\(s\):", lines[i+1]):
                        data = data + lines[i+1] + " "
                        i += 1
                    data.split(".")
                    for part in data:
                        if re.search("Distance", part):
                            if re.search("Also", part):
                                distance_education = DistanceEducation.SUPPLEMENTARY
                            else:
                                distance_education = DistanceEducation.ONLY
                        elif re.search("even-numbered", part):
                            year_parity_restrictions = YearParityRestrictions.EVEN_YEARS
                        elif re.search("odd-numbered", part):
                            year_parity_restrictions = YearParityRestrictions.ODD_YEARS
                        else:
                            if other == none:
                                other = part.split() + "."
                            else:
                                other = other + part + "."

                elif re.search("Prerequisite\(s\):", lines[i]):
                    ''' Extracts prerequisites '''
                    data =  lines[i].split(" ", 1)
                    if len(data) > 0:
                        data = data[1] + " "
                    while i < (n - 1) and not re.search("\(s\):", lines[i+1]):
                        data = data + lines[i+1] + " "
                        i += 1
                    prerequisites = data

                elif re.search("Equate\(s\):", lines[i]):
                    ''' Extracts equates '''
                    data =  lines[i].split(" ", 1)
                    if len(data) > 0:
                        data = data[1] + " "
                    while i < (n - 1) and not re.search("\(s\):", lines[i+1]):
                        data = data + lines[i+1] + " "
                        i += 1
                    equates = data

                elif re.search("Co-requisite\(s\):", lines[i]):
                    ''' Extracts corequisites '''
                    data =  lines[i].split(" ", 1)
                    if len(data) > 0:
                        data = data[1] + " "
                    while i < (n - 1) and not re.search("\(s\):", lines[i+1]):
                        data = data + lines[i+1] + " "
                        i += 1
                    corequisites = data

                elif re.search("Restriction\(s\):", lines[i]):
                    ''' Extracts restrictions '''
                    data =  lines[i].split(" ", 1)
                    if len(data) > 0:
                        data = data[1] + " "
                    while i < (n - 1) and not re.search("\(s\):", lines[i+1]):
                        data = data + lines[i+1] + " "
                        i += 1
                    restrictions.append(data)

                elif re.search("Department\(s\):", lines[i]):
                    ''' Extracts departments '''
                    data =  lines[i].split(" ", 1)
                    if len(data) > 0:
                        data = data[1] + " "
                    while i < (n - 1) and not re.search("\(s\):", lines[i+1]):
                        data = data + lines[i+1] + " "
                        i += 1
                    departments.append(data)

                i += 1

        return [description, distance_education, year_parity_restrictions, other, prerequisites, equates, corequisites, restrictions, departments]

class CourseData:
    def __init__(self):
        self.subject = None
        self.code = None
        self.section = None
        self.number = None
        self.name = None
        self.semesters = None
        self.lecture_time = None
        self.lab_time = None
        self.credits = None
        self.description = ""
